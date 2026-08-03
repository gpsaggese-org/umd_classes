"""
Milestone 1 baselines:

  1. RandomPolicy            — uniform over the 5 aim actions
  2. AimOppositePolicy       — heuristic: aim at whichever target is farthest
                               from the opponent's current position
  3. BackwardInductionSolver — finite-horizon dynamic programming on a
                               discretized state grid; the "ground truth"
                               optimal policy for the 1D game

The DP solver is the RL-theory piece of Milestone 1: it computes
V_t(state) = max_a E[outcome | a] by working backward from the rally cap,
integrating the Gaussian execution noise exactly over grid cells.
"""

from __future__ import annotations

from typing import Optional

import numpy as np
from scipy.stats import norm

from rally_env import ACTION_FRACTIONS, N_ACTIONS, PlayerParams, RallyEngine


# ---------------------------------------------------------------------------
# Simple baselines
# ---------------------------------------------------------------------------

class RandomPolicy:
    def __init__(self, rng: Optional[np.random.Generator] = None):
        self.rng = rng or np.random.default_rng()

    def __call__(self, obs: np.ndarray) -> int:
        return int(self.rng.integers(N_ACTIONS))


class AimOppositePolicy:
    """Aim at the target position farthest from the opponent."""

    def __call__(self, obs: np.ndarray) -> int:
        # obs = [t_norm, x_ball, x_self, x_opp, my_turn], all normalized to [0,1]
        x_opp = obs[3]
        return int(np.argmax(np.abs(ACTION_FRACTIONS - x_opp)))


# ---------------------------------------------------------------------------
# Backward-induction optimal solver (finite-horizon DP on a grid)
# ---------------------------------------------------------------------------

class BackwardInductionSolver:
    """Exact-ish optimal policy via finite-horizon dynamic programming.

    State (from the current hitter's perspective):
        (t, i_hitter, i_defender)  — positions discretized onto a grid.
    (The ball is always at the hitter's position when they strike, so it
    is not a separate state variable.)

    Value V_t(i_h, i_d) = probability-weighted expected terminal reward
    (+1 hitter eventually wins the point, -1 loses) under optimal play by
    BOTH sides — i.e. after a successful return the roles swap and the
    continuation value is -V_{t+1}(defender's state).

    Transition math per action a with target x_a:
        p_ufoe                      -> hitter loses            (-1)
        P(x_hit outside [0, L])     -> hitter loses            (-1)
        P(x_hit in cell j, unreachable) -> hitter wins         (+1)
        P(x_hit in cell j, reachable)   -> continue: -V_{t+1}(j, i_h)

    The Gaussian execution noise is integrated exactly over grid cells via
    the normal CDF, so the only approximation is the position grid itself.
    """

    def __init__(
        self,
        engine: RallyEngine,
        n_grid: int = 41,
        hitter_params: Optional[PlayerParams] = None,
        defender_params: Optional[PlayerParams] = None,
    ):
        self.engine = engine
        self.L = engine.L
        self.n = n_grid
        self.grid = np.linspace(0.0, self.L, n_grid)
        self.hp = hitter_params or engine.players[0]
        self.dp = defender_params or engine.players[1]
        self.T = engine.max_rally_length
        self._solve()

    # -- DP -----------------------------------------------------------------

    def _cell_probs(self, target: float, sigma: float) -> tuple[np.ndarray, float]:
        """P(x_hit lands in each grid cell), and P(out of bounds)."""
        edges = np.concatenate(([0.0], (self.grid[:-1] + self.grid[1:]) / 2, [self.L]))
        cdf = norm.cdf(edges, loc=target, scale=sigma)
        p_cells = np.diff(cdf)
        p_out = 1.0 - (cdf[-1] - cdf[0])
        return p_cells, p_out

    def _reachable(self, x_hit: np.ndarray, x_ball: float, x_def: np.ndarray,
                   dp: PlayerParams) -> np.ndarray:
        # Delegates to the engine so simulator and solver can never diverge.
        return self.engine.reachable(x_hit, x_ball, x_def, dp)

    def _solve(self):
        n, T = self.n, self.T
        # V[t, i_h, i_d]: value to the CURRENT hitter at step t.
        # Both players share params in the symmetric case; for asymmetric
        # params the hitter role alternates, handled via two value arrays.
        V_a = np.zeros((n, n))  # value when player A (self.hp) is hitting
        V_b = np.zeros((n, n))  # value when player B (self.dp) is hitting
        # Terminal step: rally cap -> coin flip -> value 0. Already zeros.

        self.policy_a = np.zeros((T, n, n), dtype=np.int64)
        self.policy_b = np.zeros((T, n, n), dtype=np.int64)
        targets = ACTION_FRACTIONS * self.L

        for t in range(T - 1, -1, -1):
            V_a_new = np.empty_like(V_a)
            V_b_new = np.empty_like(V_b)
            for hitter_is_a in (True, False):
                hp = self.hp if hitter_is_a else self.dp
                dp = self.dp if hitter_is_a else self.hp
                V_next_other = V_b if hitter_is_a else V_a  # after return, other hits
                Q = np.empty((N_ACTIONS, n, n))
                for a, x_t in enumerate(targets):
                    p_cells, p_out = self._cell_probs(x_t, hp.sigma_precision)
                    # For each hitter cell i_h (ball position = grid[i_h]):
                    for i_h in range(n):
                        x_ball = self.grid[i_h]
                        # reachability of each landing cell for each defender pos
                        # shape (n_cells, n_def)
                        reach = self._reachable(
                            self.grid[:, None], x_ball, self.grid[None, :], dp)
                        # Continuation: new hitter = defender at landing cell j,
                        # new defender = old hitter at i_h -> value -V_next[j, i_h]
                        cont = -V_next_other[:, i_h]           # shape (n_cells,)
                        per_cell = np.where(reach, cont[:, None], 1.0)  # (cells, def)
                        ev = p_cells @ per_cell                 # (n_def,)
                        Q[a, i_h, :] = (
                            hp.p_ufoe * (-1.0)
                            + (1 - hp.p_ufoe) * (p_out * (-1.0) + ev)
                        )
                best = Q.argmax(axis=0)
                V_best = Q.max(axis=0)
                if hitter_is_a:
                    V_a_new = V_best
                    self.policy_a[t] = best
                else:
                    V_b_new = V_best
                    self.policy_b[t] = best
            V_a, V_b = V_a_new, V_b_new

        self.V_a, self.V_b = V_a, V_b  # values at t=0

    # -- policy interface ----------------------------------------------------

    def _nearest(self, x: float) -> int:
        return int(np.abs(self.grid - x).argmin())

    def __call__(self, obs: np.ndarray) -> int:
        """obs = [t_norm, x_ball, x_self, x_opp, my_turn] (normalized)."""
        t = min(int(round(obs[0] * self.T)), self.T - 1)
        i_h = self._nearest(obs[2] * self.L)
        i_d = self._nearest(obs[3] * self.L)
        return int(self.policy_a[t, i_h, i_d])
