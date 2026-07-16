---
name: q_learning
description: Interactive Jupyter notebook outline teaching Q-learning through the FrozenLake grid navigation problem, contrasting brute-force policy search with the TD-based Q-learning algorithm from gymnasium
metadata:
  type: notebook_outline
  lesson: Book.Springer Lesson 10.01 Decision-Making Algorithms (Algorithm 1: Q-Learning)
  libraries: gymnasium, numpy, pandas, seaborn, matplotlib, ipywidgets
  domain: reinforcement_learning
---

# Q-Learning: From Brute-Force Policy Search to Learned Control

- This notebook teaches Q-learning through `FrozenLake`, the canonical
  off-policy control benchmark: an agent crosses a slippery frozen lake to a
  goal tile without falling into a hole
- The pedagogical arc is:
  - See the environment and why it is hard (stochastic, sparse reward) ->
    watch brute-force policy enumeration fail combinatorially -> learn the
    single TD update that replaces it -> balance exploration and
    exploitation -> train a full Q-table and watch it converge -> compare the
    learned policy against the brute-force baseline
- Focus is on hands-on discovery: students change the learning rate, discount,
  exploration rate, and training length and watch the Q-table, learning
  curve, and policy respond live
- Unlike a from-scratch grid-world notebook, this one uses `gymnasium`
  directly: the transition model is never built by hand, mirroring how
  Q-learning is used in practice when the environment is a black box

# Part 1: The FrozenLake Problem and Why Brute Force Fails

## Cell 1.1: The FrozenLake Environment: States, Actions, Rewards

**Goal**:
- Ground students in the concrete environment every later cell reasons
  about, so the algorithm is never discussed in the abstract
- Establish the three MDP ingredients (states, actions, rewards) and the
  fact that the agent is not told the transition model

**Plots and their descriptions**:
- _Grid layout_: 4x4 `FrozenLake` grid drawn as a `seaborn` heatmap, with
  tiles colored by type: start (blue), frozen (light blue), hole (black),
  goal (green)
- _Agent position_: a marker on the current tile, with the 4 possible moves
  (left, down, right, up) drawn as arrows from that tile
- _Comments_: number of states (16), number of actions (4), reward structure
  ($+1$ only on reaching the goal, $0$ otherwise)

**Widgets**:
- `is_slippery`: toggle for deterministic vs stochastic ice (default: on)
- `seed`: random seed for reproducibility

**Key observations**:
- The reward is sparse: every step gives $0$ except the single step that
  reaches the goal, so most actions carry no immediate feedback
- With `is_slippery` on, the intended action succeeds only part of the time
  and the agent can slide sideways, matching the slides' stochastic control
  setting
- Falling into a hole ends the episode with no reward, so a careless policy
  can wander forever without ever learning what went wrong

**Implementation**: `gymnasium.make("FrozenLake-v1")` for the environment,
`seaborn.heatmap` for the grid, `matplotlib` arrows for the action set

## Cell 1.2: Why Enumerating Every Policy Is Infeasible

**Goal**:
- Show concretely why the "obvious" brute-force solution, scoring every
  deterministic policy by Monte Carlo rollouts, does not scale
- Motivate the need for an algorithm that improves a single running estimate
  instead of evaluating whole policies from scratch

**Plots and their descriptions**:
- _Policy count_: bar chart comparing the number of deterministic policies
  ($4^{16} \approx 4.3$ billion) against the number brute force can actually
  afford to score in a reasonable budget
- _Noisy ranking_: line plot of the estimated score of a few sample policies
  as the number of rollouts per policy grows, showing how rankings still
  wobble even after many rollouts
- _Comments_: current rollouts-per-policy value, resulting score variance for
  the displayed policies

**Widgets**:
- `n_rollouts`: slider for rollouts per policy (1-500, log scale), controls
  how noisy each policy's estimated score is
- `seed`: random seed for reproducibility

**Key observations**:
- The number of deterministic policies grows as $|\mathcal{A}|^{|\mathcal{S}|}$:
  with 16 states and 4 actions this is already in the billions
- Because the reward is sparse and stochastic, ranking policies reliably
  needs many rollouts per policy, multiplying an already infeasible count
- Q-learning sidesteps both problems: it never enumerates policies and it
  refines one shared table from every single step, not whole episodes

**Implementation**: `numpy` for sampling and scoring a small subset of
policies (not all $4^{16}$), `gymnasium` for rollouts, `matplotlib` bar and
line plots

# Part 2: Learning the Optimal Policy with Q-Learning

## Cell 2.1: The Q-Learning TD Update Rule

**Goal**:
- Introduce the single update that powers Q-learning by applying it to one
  experience tuple, before running any full training loop
- Build on Cell 1.2: this update is the mechanism that replaces
  whole-policy scoring with incremental, per-step improvement

**Plots and their descriptions**:
- _Transition diagram_: one step $s \xrightarrow{a} s'$ with reward $r$ drawn
  on the grid, from a chosen tile to its resulting tile
- _Q-value bar_: before/after bar for $Q(s,a)$ showing the old estimate, the
  TD target $r + \gamma \max_{a'} Q(s',a')$, and the updated value
- _Comments_: current $\alpha$, $\gamma$, the TD error for this tuple, and
  the numeric before/after $Q(s,a)$

**Widgets**:
- `alpha`: slider for the learning rate (0.0-1.0)
- `gamma`: slider for the discount factor (0.0-1.0)
- `seed`: random seed for reproducibility (selects which transition is shown)

**Key observations**:
- The TD error $r + \gamma \max_{a'} Q(s',a') - Q(s,a)$ measures surprise:
  the gap between the current estimate and the observed outcome
- The learning rate $\alpha$ controls how much of that surprise gets folded
  into $Q(s,a)$ on this single step
- The update bootstraps: it uses the current, possibly wrong, estimate of
  the next state's best action value rather than waiting for the episode to
  end

**Implementation**: `matplotlib` annotated transition diagram over the grid,
`numpy` for the single-step Q-update, bar chart for before/after values

## Cell 2.2: Exploration vs Exploitation with Epsilon-Greedy

**Goal**:
- Show why the agent must sometimes act randomly instead of always taking
  its current best-known action
- Extend Cell 2.1: repeated application of the TD update only teaches the
  agent about states it actually visits, so visitation itself becomes a
  variable to control

**Plots and their descriptions**:
- _Visit heatmap_: grid heatmap of how many times each tile was visited
  during a fixed number of training episodes
- _Coverage comparison_: two small heatmaps side by side, low $\epsilon$
  versus high $\epsilon$, for the same episode budget
- _Comments_: current $\epsilon$, number of episodes, fraction of tiles
  never visited

**Widgets**:
- `epsilon`: slider for exploration probability (0.0-1.0)
- `n_episodes`: log-scale slider for training episodes (16-1024)
- `seed`: random seed for reproducibility

**Key observations**:
- A near-greedy agent ($\epsilon$ close to $0$) can lock onto the first path
  that reaches the goal and never visit tiles that might lead to a safer or
  shorter route
- A highly exploratory agent ($\epsilon$ close to $1$) covers the grid more
  evenly but wastes many episodes acting randomly instead of exploiting what
  it already knows
- Coverage is not the goal by itself: it is a means to make sure the Q-table
  gets accurate estimates everywhere that matters

**Implementation**: `seaborn.heatmap` for visit counts, `gymnasium` rollouts
under an epsilon-greedy policy, counting logic in utils

## Cell 2.3: Training the Q-Table and Watching Convergence

**Goal**:
- Run the full Q-learning training loop, combining the TD update
  (Cell 2.1) and epsilon-greedy action selection (Cell 2.2) over many
  episodes
- Show the learning curve rising from near-random performance to a
  consistently successful policy

**Plots and their descriptions**:
- _Learning curve_: rolling-average success rate (episode reaches the goal)
  per training episode
- _Q-table heatmap_: grid heatmap of $\max_a Q(s,a)$ per state, updating as
  training progresses
- _Comments_: current episode count, current rolling success rate, current
  $\epsilon$ (after decay)

**Widgets**:
- `n_episodes`: log-scale slider for total training episodes (100-20000)
- `alpha`: slider for the learning rate (0.0-1.0)
- `epsilon_decay`: slider controlling how fast $\epsilon$ decays toward 0
  over training
- `seed`: random seed for reproducibility

**Key observations**:
- The learning curve is noisy early, dominated by exploration and slipping
  on the ice, then rises and stabilizes as the Q-table becomes accurate
- States near the goal develop high $\max_a Q(s,a)$ first; this high-value
  region spreads backward toward the start tile over training, the same
  backward propagation seen in value-based planning
- Decaying $\epsilon$ lets the agent shift from exploring broadly early to
  exploiting its learned table later, without hand-tuning a fixed rate

**Implementation**: full Q-learning training loop in utils returning
per-episode success and Q-table snapshots, `seaborn.heatmap` for the Q-table,
`matplotlib`/`seaborn` line plot for the learning curve

## Cell 2.4: The Learned Policy vs the Brute-Force Baseline

**Goal**:
- Tie the notebook together by extracting the greedy policy
  $\arg\max_a Q(s,a)$ from the trained table and evaluating it head to head
  against the brute-force approach from Cell 1.2
- Show what Q-learning bought: a policy at least as good, found without ever
  enumerating policies or knowing the transition model

**Plots and their descriptions**:
- _Policy grid_: the greedy action drawn as an arrow in every non-terminal
  tile, overlaid on the final Q-table heatmap
- _Success-rate comparison_: bar chart of success rate over many evaluation
  episodes for three policies: random, a brute-force-scored policy (best of
  the small sample from Cell 1.2), and the trained Q-learning policy
- _Comments_: success rate and number of rollouts needed for each of the
  three policies shown

**Widgets**:
- `n_eval_episodes`: slider for evaluation episodes used to estimate each
  success rate (100-5000)
- `seed`: random seed for reproducibility

**Key observations**:
- The Q-learning policy reaches or exceeds the success rate of the best
  policy brute force found, despite brute force scoring only a tiny sample
  of the $4^{16}$ possible policies
- Q-learning needed one shared table updated per step, not a separate
  Monte Carlo score per candidate policy: the same training episodes that
  produced the learning curve in Cell 2.3 already double as the evaluation
  budget
- The comparison makes the payoff concrete: the same guarantee (a good
  policy) at a fraction of the sampling cost, and without ever seeing the
  transition probabilities

**Implementation**: greedy policy extraction from the final Q-table,
`gymnasium` rollouts for evaluation, `matplotlib` arrow overlay on the grid,
`seaborn`/`matplotlib` bar chart for the comparison

# Summary: The Mental Model

- `FrozenLake` is a sparse-reward, stochastic MDP where brute-force policy
  search is combinatorially infeasible: $4^{16}$ deterministic policies, each
  needing many rollouts to score reliably
- Q-learning replaces whole-policy scoring with a single incremental update,
  $Q(s,a) \leftarrow Q(s,a) + \alpha[r + \gamma \max_{a'} Q(s',a') - Q(s,a)]$,
  applied to every experienced transition
- Epsilon-greedy action selection, decayed over training, balances visiting
  new states against exploiting what the table already knows
- After enough episodes, the greedy policy extracted from the learned
  Q-table matches or beats the best brute-force policy, learned purely from
  experience and without ever knowing the transition model
