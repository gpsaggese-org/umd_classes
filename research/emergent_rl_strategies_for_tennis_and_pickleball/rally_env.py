"""
1D Rally Environment — Milestone 1 (Approximation 1)

Implements the spec:
  - 1D court x in [0, L]
  - Turn-based: attacker aims -> ball travels at constant speed -> defender
    tries to reach it in time
  - Option A (aggregate skill) player model: v_move, sigma_precision,
    p_ufoe, t_react
  - Rally ends on: unreachable ball (winner), unforced error, or ball out
  - 5 discrete actions -> targets {0.2L, 0.4L, 0.5L, 0.6L, 0.8L}
  - Execution noise: x_hit = x_target + N(0, sigma_precision^2)
  - Reward: 0 per step, +1 win / -1 loss terminal, optional step cost
  - Gymnasium-compatible wrapper (RallyGymEnv)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

import numpy as np

try:
    import gymnasium as gym
    from gymnasium import spaces
except ImportError:  # pragma: no cover
    gym = None
    spaces = None


# ---------------------------------------------------------------------------
# Player model (Option A: aggregate skill)
# ---------------------------------------------------------------------------

@dataclass
class PlayerParams:
    """Aggregate-skill player model."""
    v_move: float          # movement speed (units / time)
    sigma_precision: float # std-dev of execution noise on target position
    p_ufoe: float          # per-shot unforced error probability
    t_react: float         # reaction delay subtracted from movement budget

    @property
    def name(self) -> str:
        return getattr(self, "_name", "custom")


def make_skill(level: str) -> PlayerParams:
    """3 discrete skill levels per the spec (beginner/intermediate/advanced)."""
    table = {
        "beginner":     PlayerParams(v_move=1.2, sigma_precision=2.5, p_ufoe=0.12, t_react=0.35),
        "intermediate": PlayerParams(v_move=1.6, sigma_precision=1.5, p_ufoe=0.06, t_react=0.25),
        "advanced":     PlayerParams(v_move=2.0, sigma_precision=0.8, p_ufoe=0.02, t_react=0.15),
    }
    if level not in table:
        raise ValueError(f"unknown skill level: {level!r}; choose from {list(table)}")
    p = table[level]
    p._name = level
    return p


# ---------------------------------------------------------------------------
# Core turn-based engine
# ---------------------------------------------------------------------------

class Outcome(Enum):
    ONGOING = "ongoing"
    OUT = "out"                # hitter's ball landed out -> hitter loses point
    UNFORCED_ERROR = "ufoe"    # hitter flubbed the shot -> hitter loses point
    WINNER = "winner"          # defender couldn't reach -> hitter wins point
    MAX_LENGTH = "max_length"  # rally cap reached -> draw, resolved as coin flip


N_ACTIONS = 5
ACTION_FRACTIONS = np.array([0.2, 0.4, 0.5, 0.6, 0.8])


@dataclass
class RallyState:
    t: int                 # step within rally
    x_ball: float          # current ball position (where it was last struck from)
    x_players: np.ndarray  # shape (2,) positions of player 0 and player 1
    turn: int              # whose turn to hit (0 or 1)


class RallyEngine:
    """Turn-based 1D rally game engine.

    One call to ``step(action)`` = the current hitter chooses a target,
    the ball travels, and the defender either reaches it (rally continues,
    turn flips) or the point ends.
    """

    def __init__(
        self,
        L: float = 20.0,
        v_ball: float = 4.0,
        t_flight_base: float = 2.0,    # constant cross-court flight time (net crossing)
        max_rally_length: int = 50,
        players: Optional[tuple[PlayerParams, PlayerParams]] = None,
        step_cost_coef: float = 0.0,   # 0.001 in the spec's optional ablation
        rng: Optional[np.random.Generator] = None,
    ):
        self.L = L
        self.v_ball = v_ball
        self.t_flight_base = t_flight_base
        self.max_rally_length = max_rally_length
        self.players = players or (make_skill("intermediate"), make_skill("intermediate"))
        self.step_cost_coef = step_cost_coef
        self.rng = rng or np.random.default_rng()
        self.state: Optional[RallyState] = None

    # -- public API ---------------------------------------------------------

    def reset(self, serving: Optional[int] = None) -> RallyState:
        serving = self.rng.integers(2) if serving is None else serving
        self.state = RallyState(
            t=0,
            x_ball=self.L / 2.0,               # serve from center
            x_players=np.array([self.L / 2.0, self.L / 2.0]),
            turn=int(serving),
        )
        return self.state

    def action_to_target(self, action: int) -> float:
        return float(ACTION_FRACTIONS[action] * self.L)

    def step(self, action: int) -> tuple[RallyState, Outcome, int | None, float]:
        """Current hitter plays ``action``.

        Returns (state, outcome, winner, step_cost) where winner is the
        player index that won the point (None while ongoing), and step_cost
        is the movement penalty charged to the hitter this step (>= 0).
        """
        assert self.state is not None, "call reset() first"
        s = self.state
        hitter, defender = s.turn, 1 - s.turn
        hp, dp = self.players[hitter], self.players[defender]

        target = self.action_to_target(action)
        step_cost = self.step_cost_coef * abs(target - s.x_players[hitter])

        # 1. Unforced error check (hitter flubs the shot)
        if self.rng.random() < hp.p_ufoe:
            return self._finish(Outcome.UNFORCED_ERROR, winner=defender, step_cost=step_cost)

        # 2. Execution noise on the intended target
        x_hit = target + self.rng.normal(0.0, hp.sigma_precision)

        # 3. Out-of-bounds check
        if x_hit < 0.0 or x_hit > self.L:
            return self._finish(Outcome.OUT, winner=defender, step_cost=step_cost)

        # 4. Ball transit: constant cross-court flight time + lateral component.
        #    The defender has that long (minus reaction time) to cover the
        #    lateral gap between themselves and the landing spot.
        if not self.reachable(x_hit, s.x_ball, s.x_players[defender], dp):
            # Defender cannot reach in time -> winner for the hitter
            return self._finish(Outcome.WINNER, winner=hitter, step_cost=step_cost)

        # 5. Rally continues: defender arrives at the ball, hitter stays put
        s.x_players[defender] = x_hit
        s.x_ball = x_hit
        s.t += 1
        s.turn = defender

        if s.t >= self.max_rally_length:
            # Cap reached: resolve as a neutral coin flip so values stay bounded
            return self._finish(Outcome.MAX_LENGTH, winner=int(self.rng.integers(2)),
                                step_cost=step_cost)

        return s, Outcome.ONGOING, None, step_cost

    # -- helpers ------------------------------------------------------------

    def reachable(self, x_hit, x_ball, x_def, dp: PlayerParams):
        """Can a defender at x_def reach a ball struck from x_ball toward x_hit?

        Transit time = t_flight_base (cross-court) + lateral travel / v_ball.
        Works on scalars or numpy arrays (used by the DP solver too).
        """
        t_transit = self.t_flight_base + np.abs(x_hit - x_ball) / self.v_ball
        budget = np.maximum(t_transit - dp.t_react, 0.0)
        return dp.v_move * budget >= np.abs(x_hit - x_def)

    def _finish(self, outcome: Outcome, winner: int, step_cost: float):
        return self.state, outcome, winner, step_cost


# ---------------------------------------------------------------------------
# Gymnasium wrapper (single-agent view: agent = player 0, opponent = policy)
# ---------------------------------------------------------------------------

class RallyGymEnv(gym.Env if gym else object):
    """Gym-compatible single-agent wrapper.

    The learning agent is player 0. The opponent (player 1) is any callable
    ``opponent_policy(obs: np.ndarray) -> int``. Between the agent's turns the
    env automatically plays out the opponent's shots.

    Observation (5,): [t / max_len, x_ball / L, x_self / L, x_opp / L, turn]
    Action: Discrete(5) -> aim {0.2, 0.4, 0.5, 0.6, 0.8} * L
    Reward: +1 win, -1 loss, minus optional step cost while ongoing.
    """

    metadata = {"render_modes": []}

    def __init__(self, engine: Optional[RallyEngine] = None,
                 opponent_policy=None, agent_id: int = 0):
        if gym is None:
            raise ImportError("gymnasium is required for RallyGymEnv")
        super().__init__()
        self.engine = engine or RallyEngine()
        self.agent_id = agent_id
        self.opponent_policy = opponent_policy or (
            lambda obs: int(np.random.default_rng().integers(N_ACTIONS)))
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(5,), dtype=np.float32)
        self.action_space = spaces.Discrete(N_ACTIONS)

    # -- gym API ------------------------------------------------------------

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        if seed is not None:
            self.engine.rng = np.random.default_rng(seed)
        self.engine.reset()
        # If it's the opponent's serve, play opponent shots until agent's turn
        term, reward = self._advance_opponent()
        if term:  # point ended before the agent ever hit; re-serve for simplicity
            return self.reset(seed=None, options=options)
        return self._obs(), {}

    def step(self, action: int):
        s, outcome, winner, cost = self.engine.step(int(action))
        reward = -cost
        if outcome is not Outcome.ONGOING:
            reward += 1.0 if winner == self.agent_id else -1.0
            return self._obs(), reward, True, False, {"outcome": outcome.value}
        term, opp_reward = self._advance_opponent()
        reward += opp_reward
        return self._obs(), reward, term, False, {}

    # -- internals ----------------------------------------------------------

    def _advance_opponent(self) -> tuple[bool, float]:
        """Play opponent turns until it's the agent's turn or the point ends.

        Returns (terminated, reward_from_opponent_phase).
        """
        while self.engine.state.turn != self.agent_id:
            opp_action = self.opponent_policy(self._obs(perspective=1 - self.agent_id))
            _, outcome, winner, _ = self.engine.step(int(opp_action))
            if outcome is not Outcome.ONGOING:
                return True, (1.0 if winner == self.agent_id else -1.0)
        return False, 0.0

    def _obs(self, perspective: Optional[int] = None) -> np.ndarray:
        s = self.engine.state
        me = self.agent_id if perspective is None else perspective
        opp = 1 - me
        return np.array([
            s.t / self.engine.max_rally_length,
            s.x_ball / self.engine.L,
            s.x_players[me] / self.engine.L,
            s.x_players[opp] / self.engine.L,
            float(s.turn == me),
        ], dtype=np.float32)
