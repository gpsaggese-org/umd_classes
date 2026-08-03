"""
Milestone 1 evaluation harness.

Runs the sanity checks from the spec:
  1. Symmetric-skill check: identical players + symmetric policies
     -> ~50% win rate (validates the engine, per the spec's edge case)
  2. Head-to-head matrix: random vs aim-opposite vs backward-induction
  3. Skill-gap check: advanced player should beat beginner at equal policy

Usage:  python evaluate.py [n_episodes]
"""

from __future__ import annotations

import sys

import numpy as np

from rally_env import RallyEngine, make_skill
from baselines import AimOppositePolicy, BackwardInductionSolver, RandomPolicy


def play_match(engine: RallyEngine, policy0, policy1, n_points: int = 2000,
               seed: int = 0) -> float:
    """Returns player 0's win rate over n_points."""
    engine.rng = np.random.default_rng(seed)
    wins0 = 0
    policies = (policy0, policy1)
    for k in range(n_points):
        engine.reset(serving=k % 2)  # alternate serve to remove serve bias
        while True:
            s = engine.state
            me, opp = s.turn, 1 - s.turn
            obs = np.array([
                s.t / engine.max_rally_length,
                s.x_ball / engine.L,
                s.x_players[me] / engine.L,
                s.x_players[opp] / engine.L,
                1.0,
            ], dtype=np.float32)
            _, outcome, winner, _ = engine.step(policies[me](obs))
            if winner is not None:
                wins0 += int(winner == 0)
                break
    return wins0 / n_points


def main(n_points: int = 2000):
    print(f"== Milestone 1 sanity checks ({n_points} points per match) ==\n")

    # ---- 1. Symmetric-skill sanity check (spec edge case) ------------------
    eng = RallyEngine(players=(make_skill("intermediate"), make_skill("intermediate")))
    wr = play_match(eng, RandomPolicy(np.random.default_rng(1)),
                    RandomPolicy(np.random.default_rng(2)), n_points)
    print(f"[1] symmetric skill, random vs random    : P0 win rate = {wr:.3f}  (expect ~0.50)")
    assert 0.45 < wr < 0.55, "symmetric check FAILED — engine is biased"

    wr = play_match(eng, AimOppositePolicy(), AimOppositePolicy(), n_points)
    print(f"    symmetric skill, heuristic vs same   : P0 win rate = {wr:.3f}  (expect ~0.50)")
    assert 0.45 < wr < 0.55, "symmetric heuristic check FAILED"

    # ---- 2. Head-to-head baseline matrix -----------------------------------
    print("\n[2] head-to-head (intermediate vs intermediate):")
    solver = BackwardInductionSolver(eng)
    lineup = {
        "random   ": RandomPolicy(np.random.default_rng(3)),
        "heuristic": AimOppositePolicy(),
        "dp-solver": solver,
    }
    names = list(lineup)
    for a in names:
        for b in names:
            if a >= b:
                continue
            wr = play_match(eng, lineup[a], lineup[b], n_points)
            print(f"    {a} vs {b}: {a.strip()} wins {wr:.3f}")

    # ---- 3. Skill-gap check -------------------------------------------------
    eng_gap = RallyEngine(players=(make_skill("advanced"), make_skill("beginner")))
    wr = play_match(eng_gap, RandomPolicy(np.random.default_rng(4)),
                    RandomPolicy(np.random.default_rng(5)), n_points)
    print(f"\n[3] advanced vs beginner (both random)   : advanced wins {wr:.3f}  (expect >0.60)")
    assert wr > 0.60, "skill-gap check FAILED — skill params have no effect"

    print("\nAll sanity checks passed.")


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    main(n)
