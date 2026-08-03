# Emergent RL Strategies for Tennis and Pickleball

## Summary

This project explores reinforcement learning strategies for racket sports using
a simplified 1D rally simulation. Milestone 1 implements a turn-based rally
engine with discrete aiming, Gaussian execution noise, and three baseline
policies (random, heuristic, dynamic programming).

## Milestone 1: 1D Simulation Assumptions

The current environment is a heavily simplified approximation of real
tennis/pickleball. The following assumptions and simplifications apply:

### Court Model

- The court is a **1D line** from `0` to `L` (default `L = 20`)
- No court width, no net height, no service boxes
- No distinction between tennis and pickleball court dimensions

### Player Model

- Players are represented by **4 aggregate skill parameters** only:
  - `v_move`: movement speed (units/time)
  - `sigma_precision`: standard deviation of shot accuracy (Gaussian noise)
  - `p_ufoe`: per-shot unforced error probability
  - `t_react`: reaction delay before the player can start moving
- **No racket or paddle size** — the defender either reaches the ball in time or
  does not, based purely on movement speed vs distance
- **No stamina, fatigue, or injury**
- **No handedness** — no forehand/backhand distinction

### Ball and Shot Model

- **No physics** — no spin, no bounce, no gravity, no ball trajectory arc
- Ball travels at a **constant speed** (`v_ball`) in 1D
- **5 discrete aim targets** at `{0.2, 0.4, 0.5, 0.6, 0.8} * L` — not
  continuous aiming
- Shot landing position is `x_target + N(0, sigma^2)` — Gaussian execution
  noise around the intended target
- **No stroke types** — no lob, drop shot, slice, topspin, serve, or volley
- **No net interactions** — balls never hit the net

### Gameplay Model

- **Turn-based** — players alternate hitting; no simultaneous movement
- The defender is stationary until the ball is struck, then moves to intercept
- A shot is "reachable" if `v_move * (transit_time - t_react) >= distance`
- Rally ends on: unreachable ball (winner), unforced error, ball out of bounds,
  or rally cap (50 shots, resolved by coin flip)
- **No scoring system** — each rally is an independent `+1/-1` outcome
- **No serve mechanics** — serve is just the first shot from center court

### What Is NOT Modeled

- Racket/paddle size and sweet spot
- 2D or 3D court geometry
- Ball spin, bounce height, and trajectory
- Shot selection (forehand, backhand, overhead, volley)
- Player positioning strategy and court coverage patterns
- Doubles play
- Fatigue and momentum effects
- Wind and surface type
- Scoring, sets, games, and match structure

## Quick Start

- From the root of the repository, change directory to the project folder:
  ```bash
  > cd research/emergent_rl_strategies_for_tennis_and_pickleball
  ```

- Build the Docker image:
  ```bash
  > ./docker_build.sh
  ```

- Run the Milestone 1 sanity checks to verify the environment works:
  ```bash
  > ./docker_cmd.sh "cd /git_root/research/emergent_rl_strategies_for_tennis_and_pickleball && python3 evaluate.py"
  ```

- Launch Jupyter Lab to work with notebooks:
  ```bash
  > ./docker_jupyter.sh
  ```

- Launch an interactive bash shell inside the container:
  ```bash
  > ./docker_bash.sh
  ```

- For more information on the Docker build system refer to
  [Project template readme](/class_project/project_template/README.md)

## Project Files

- `rally_env.py`: 1D rally engine (`RallyEngine`) and Gymnasium wrapper
  (`RallyGymEnv`)
- `baselines.py`: `RandomPolicy`, `AimOppositePolicy`, and
  `BackwardInductionSolver` (finite-horizon DP)
- `evaluate.py`: Milestone 1 sanity checks — symmetric win rate, head-to-head
  matrix, skill-gap verification
