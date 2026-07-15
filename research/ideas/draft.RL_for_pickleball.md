# RL for Pickleball / Tennis Strategy

## Objective
Learn optimal rally strategy via RL: shot selection, court positioning, and
adaptive tactics.

Validate learned behavior resembles real coaching principles (exploit weak side,
let inferior player play)

**Scope**: Model 1D baseline rallies (Approximation 1) as tractable testbed.
Extend to 2D court later.

## Approximation 1: 1D Simplified Baseline Rally

**Game Physics**
- 1D court: positions $x \in [0, L]$ (L = baseline length, e.g., 20 units)
- Turn-based: player hits -> ball travels -> opponent receives
  - Ball motion: fixed travel time $t_{transit}$ based on distance (speed constant)
  - No intermediate trajectory simulation
- Rally ends when opponent cannot reach the ball in time, commits error, or
  ball is out (stochastic)

**Turn Sequence**
1. Attacking player chooses action: `(target_x)` where `target_x \in [0,L]`
2. Traveling player has $t_{transit}(|x_{ball} - x_{player}|) = |x_{ball} - x_{player}| / v_{ball}$
   time to move to ball
3. If travel time sufficient (i.e., $t_{transit} \geq 0$):
   - Player moves toward ball: reaches $x_{ball} + \text{noise}$ per precision
   - If reaches in time: hit ball to opponent; otherwise miss (winner shot)
4. If travel time insufficient: opponent wins (forced error / winner)

## State Space

**Observation** (fully observable per player):
- `t`: step within rally (0 to max_rally_length)
- `x_ball`: ball position, $x \in [0, L]$
- `x_player`: own position
- `x_opponent`: opponent position
- `whose_turn`: whose turn to hit (boolean or player ID)

**Derived**:
- `time_to_reach = |x_ball - x_player| / v_ball`
- `ball_reachable = (time_to_reach <= t_move(distance, speed))`

## Action Space

**Discrete (preferred for simplicity)**:
- 5 actions: `[aim_left, aim_mid_left, aim_center, aim_mid_right, aim_right]`
  - Maps to target positions: $x_{target} \in \{0.2L, 0.4L, 0.5L, 0.6L, 0.8L\}$
- **Shot-type variant** (Option B): 10 actions = 5 positions × 2 shot types
  (forehand vs backhand, depends on player position relative to ball)

**Continuous (for future)**:
- $a = (x_{target}, v_{spin}) \in [0,L] \times [0, v_{max}]$
  - Adds depth (net clearance, pace)

**Execution with Noise**:
- Intended $x_{target}$ -> realized $x_{hit} = x_{target} + \mathcal{N}(0, \sigma_{precision}^2)$
  - $\sigma_{precision}$ player-specific; high skill = low noise
- Ball out if $|x_{hit}| > L$ (chance ∝ distance from target, skill)

---

## Player Models

### Option A: Aggregate Skill (Simpler)
**Parameters**:
- Movement speed: $v_{move}$ (units/time-step)
- Shot precision: $\sigma_{precision}$ (std of aim noise)
- Unforced error rate: $p_{ufoe}$ (independent error each turn; skill $\uparrow$ -> $p_{ufoe} \downarrow$)
- Reaction time: $t_{react}$ (delay before moving)

**Skill Levels**: Define 3–5 discrete levels (e.g., beginner, intermediate, advanced)
with parameter sets.

### Option B: Shot-Type Breakdown (Advanced)
**Parameters** (separate per shot):
- Forehand: $\sigma_{FH}$, $p_{FH,ufoe}$
- Backhand: $\sigma_{BH}$, $p_{BH,ufoe}$
- Weak-side penalty: backhand inherently worse ($\sigma_{BH} > \sigma_{FH}$,
  $p_{BH,ufoe} > p_{FH,ufoe}$)

**Strategy Implication**: Agent learns to force opponent to weak side
(backhand in this model).

---

## Reward Function

**Per-Step**:
- Rally ongoing: $r_t = 0$ (no reward until termination)

**Terminal Reward** (end of rally):
- Own win: $r = +1$
- Own loss: $r = -1$

**Optional: Step Cost**
- Add $-0.001 \cdot |x_{target} - x_{current}|$ to penalize large position
  changes (pushes toward lazy, economic strategy)
  - Ablation: test with/without

**Alternative: Win-Rate Tracking**
- Use raw win rate vs baseline as metric (not necessarily reward signal)

---

## Training & Evaluation

### Training Setup
- **Algorithm**: DQN or PPO (continuous action space -> PPO preferred)
  - State: 5D vector $[t, x_{ball}, x_{player}, x_{opponent}, whose\_turn]$
  - Action: discrete (5) or continuous (2D)
- **Self-play**: Train agent against copy of itself; periodically snapshot
- **Episodes**: 10k–100k episodes (rally = 1 episode, reset on point end)
- **Convergence**: Check win rate vs random baseline (should reach >90%)

### Baselines
1. **Random**: Pick random action each turn
2. **Heuristic**: Always aim opposite to opponent position (force movement)
3. **Optimal (if solvable)**: Minimax / backward induction on small state space

### Validation Metrics
- **Win rate** vs random, heuristic, self-play opponent
- **Learned strategy inspection**: What positions does agent target? Frequency?
- **Realism**: Does learned policy match coaching heuristics?
  - E.g., does agent exploit backhand? Avoid center when opponent near center?
  - Does it set up aggressive shots after soft setup (dinking in 2D)?

---

## Key Assumptions & Relaxations

### Current (Approximation 1)
1. **Perfect information**: Both players observe full state (relax: partial
   observability, reaction delay)
2. **Fixed ball speed**: No pace variation (relax: add continuous spin/speed action)
3. **1D only**: No net, no court depth (relax: 2D court in Approximation 2)
4. **Single-opponent skill fixed**: No opponent learning during play (relax:
   adaptive opponent or multi-agent training)

### Roadmap to Realism
- **Approximation 2**: 2D court with net (rally success depends on net clearance)
- **Approximation 3**: Dinking phase + attack phase (multi-phase rally model)
- **Approximation 4**: Variable ball speed / spin (continuous actions for pace)

---

## Experiments

### Exp 1: Baseline Learning Curves
**Hypothesis**: Agent learns >80% win rate vs random within 10k episodes.
- Plot win rate, loss rate, episode length over time
- Compare Option A (aggregate skill) vs Option B (shot type)

### Exp 2: Skill-Level Ablation
**Hypothesis**: Agent learns different strategies vs weak vs strong opponents.
- Train separate agents against beginner, intermediate, advanced baselines
- Compare learned policies (position heatmaps, shot distribution)

### Exp 3: Exploit Asymmetry (Option B)
**Hypothesis**: When opponent has weak backhand, agent learns to target it.
- Measure % of shots to backhand side vs forehand side
- Expected: high skill agent -> high backhand targeting; random agent -> 50/50

### Exp 4: Strategy Transfer
**Hypothesis**: Policy trained on Approximation 1 transfers qualitatively to
Approximation 2 (2D court).
- Benchmark 1D-trained policy on 2D environment (expect drop in win rate)
- Fine-tune on 2D; measure if convergence is faster than from-scratch

---

## Implementation Checklist

- [ ] Game engine (simulator, turn logic, error/out detection)
- [ ] RL environment (Gym-compatible state/action/reward)
- [ ] Player skill parameterization (fixed for initial runs)
- [ ] PPO / DQN agent
- [ ] Self-play loop
- [ ] Logging: win rate, rally length, action distribution
- [ ] Visualization: position heatmaps, learned policy inspection
- [ ] Baseline implementations (random, heuristic, optimal)
