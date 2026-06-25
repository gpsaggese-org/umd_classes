---
name: gridworld_4x3
description: Interactive Jupyter notebook outline for teaching MDPs and reinforcement learning through the canonical 4x3 grid world, built from scratch without gymnasium
metadata:
  type: notebook_outline
  lesson: MSML610 Lesson 12 Probabilistic Reinforcement Learning
  libraries: numpy, pandas, seaborn, matplotlib, ipywidgets
  domain: reinforcement_learning
---

# The 4x3 Grid World: From MDPs to Reinforcement Learning

- This notebook teaches sequential decision making through the canonical AIMA
  4x3 grid world, built entirely from scratch with `numpy` (no `gymnasium`)
- The grid world is the unifying example throughout the lecture:
  - It appears in MDP definition, utility of states, Bellman equations, value
    iteration, policy iteration, and Q-learning
- The pedagogical arc is:
  - Build the environment (states, stochastic transitions, rewards) ->
    solve it with full knowledge (value iteration, policy iteration) ->
    learn it without knowing the model (Q-learning)
- The design choice to build from scratch is pedagogical:
  - Students see the full transition model $\Pr(s' \mid s, a)$ as an explicit
    table, which `gymnasium` hides inside `env.step()`
- Focus is on hands-on discovery: students change rewards, discount factors, and
  exploration rates and watch utilities, policies, and learning curves respond

# Part 1: Building the Grid World Environment

## Cell 1.1: The 4x3 Grid and Its States

- **Purpose**: Anchor students in the concrete environment that every later
  algorithm will reason about, so each step refers to a visible layout
- **Display**:
  - A 4x3 grid (4 columns, 3 rows) drawn as a `seaborn` heatmap or annotated
    matplotlib grid
  - Cell `(1, 1)` is `START`, cell `(4, 3)` is the `+1` terminal (green), cell
    `(4, 2)` is the `-1` terminal (red), cell `(2, 2)` is a wall (grey block)
  - Each cell labeled with its `(col, row)` coordinate
- **Interactive widget**: None (reference cell that sets up the running example)
- **Key insights**:
  - The environment has 11 reachable states (12 cells minus 1 wall)
  - Two states are terminal: reaching either ends the episode
  - The agent always knows its exact cell (fully observable)
- **Comment box**: "This is the world the agent lives in. It is fully observable
  (the agent knows its cell) but stochastic (actions do not always succeed)."
- **Implementation**: `numpy` array for the grid layout, `seaborn.heatmap` or
  `matplotlib` patches for rendering, helper in utils to map coordinates to
  state indices

## Cell 1.2: Stochastic Action Model

- **Purpose**: Show why this is an MDP and not a deterministic puzzle, since the
  unreliable actions are the entire source of difficulty
- **Display**:
  - A diagram centered on one cell showing the intended action (e.g., `Up`) and
    the three possible outcomes
  - Intended direction with probability $0.8$, each perpendicular direction with
    probability $0.1$ each, drawn with arrows whose thickness encodes
    probability
  - If an outcome would hit a wall or boundary, the agent stays in place (shown
    as a self-loop)
- **Interactive widget**:
  - Dropdown for `action`: select `Up`, `Down`, `Left`, `Right`
  - Slider for `p_intended`: probability of the intended action (0.5-1.0)
  - Description: "Pick an action and the reliability. Watch how probability
    spreads to the perpendicular directions and how walls cause the agent to
    stay put"
- **Key insights**:
  - With $\Pr(\text{intended}) = 0.8$, the agent goes sideways $20\%$ of the time
  - Walls and boundaries do not stop a transition: they bounce the agent back to
    its current cell
  - As `p_intended` approaches $1.0$, the world becomes deterministic and the
    problem becomes a simple shortest path
- **Comment box**: "The wheels slip. Intended action happens 80% of the time;
  the agent veers perpendicular 10% each way. This randomness is why a single
  plan is not enough: we need a policy."
- **Implementation**: `matplotlib` arrows with width proportional to
  probability, `ipywidgets.Dropdown` and slider, transition logic in utils

## Cell 1.3: Transition Model as an Explicit Table

- **Purpose**: Make the abstract $\Pr(s' \mid s, a)$ concrete by displaying the
  actual probability table, which is exactly what `gymnasium` would hide
- **Display**:
  - For a selected state and action, a `pandas` DataFrame listing each reachable
    next state $s'$ and its probability $\Pr(s' \mid s, a)$
  - The grid is shown alongside, with reachable next states shaded by
    probability
- **Interactive widget**:
  - Dropdown for `state`: select the current cell
  - Dropdown for `action`: select `Up`, `Down`, `Left`, `Right`
  - Description: "Select a state and action to see the full row of the
    transition model. These probabilities sum to 1"
- **Key insights**:
  - The transition model is a lookup table of shape
    $|S| \times |A| \times |S|$, but most entries are zero (sparse)
  - Each $(s, a)$ row sums to $1.0$: it is a probability distribution
  - This table is the model: value iteration and policy iteration need it,
    Q-learning does not
- **Comment box**: "This table is the MDP model $\Pr(s' \mid s, a)$. We build it
  by hand here. In Part 4, Q-learning will solve the same world without ever
  seeing this table."
- **Implementation**: `pandas` DataFrame for the probability row, `seaborn`
  heatmap overlay, transition model precomputed in utils

## Cell 1.4: Rewards and Episode Returns

- **Purpose**: Define the reward structure and show how a single trajectory
  accumulates discounted return, connecting per-step rewards to the quantity we
  optimize
- **Display**:
  - The grid annotated with the reward for entering each cell: $-0.04$ for
    non-terminal cells, $+1$ and $-1$ for the terminals
  - A sample trajectory drawn as a path from `START`, with the running
    discounted return $\sum_t \gamma^t R_t$ displayed step by step
- **Interactive widget**:
  - Slider for `r_step`: the per-step reward (-1.0 to 0.0)
  - Slider for `gamma`: discount factor (0.0-1.0)
  - Description: "Change the living reward and discount. Watch how the
    accumulated return of the same path changes"
- **Key insights**:
  - The small negative living reward $-0.04$ pushes the agent to reach a
    terminal quickly rather than wander
  - The discount factor $\gamma$ weights near-term rewards more than distant ones
  - Total return depends on the whole sequence of states, not just the final
    cell
- **Comment box**: "Reward is the feedback signal. The living reward of $-0.04$
  is a gentle penalty for taking too long. Return is the discounted sum the
  agent actually tries to maximize."
- **Implementation**: `matplotlib` grid annotation, `ipywidgets` sliders, return
  computation in utils

# Part 2: Solving the MDP with Value Iteration

## Cell 2.1: The Bellman Equation for One State

- **Purpose**: Build intuition for the Bellman update on a single state before
  iterating it over the whole grid, since the full algorithm is this update
  applied everywhere
- **Display**:
  - One highlighted state with its four candidate actions
  - For each action, the expected one-step value
    $\sum_{s'} \Pr(s' \mid s, a)[R(s, a, s') + \gamma U(s')]$ shown as a small bar
  - The chosen action (the $\max$) highlighted
- **Interactive widget**:
  - Dropdown for `state`: select which cell to inspect
  - Slider for `gamma`: discount factor (0.0-1.0)
  - Description: "Pick a state and see the value of each action under the current
    utility estimates. The Bellman update keeps the best one"
- **Key insights**:
  - The utility of a state is the value of its best action, not an average
  - Each action's value blends immediate reward with the discounted utility of
    likely next states
  - The $\max$ operator makes the system nonlinear, which is why we iterate
    instead of solving directly
- **Comment box**: "Bellman: utility of a state = best immediate action + future
  potential. We compute one value per action and keep the maximum."
- **Implementation**: `matplotlib` bar chart for action values, Bellman update
  in utils

## Cell 2.2: Value Iteration Converging Over Sweeps

- **Purpose**: Show the core algorithm in action, watching state utilities
  converge to a fixed point as the Bellman update is applied repeatedly
- **Display**:
  - The grid as a utility heatmap, with each cell annotated with its current
    $U(s)$ value
  - A side panel line plot of the max utility change $\lVert U_{i+1} - U_i
    \rVert$ per sweep, showing convergence toward $0$
- **Interactive widget**:
  - Slider for `iteration`: step through sweeps $0, 1, 2, \ldots$ to watch
    utilities update
  - Slider for `gamma`: discount factor (0.0-1.0)
  - Slider for `r_step`: living reward (-1.0 to 0.0)
  - Description: "Step through the sweeps and watch utilities spread out from the
    terminals. Change gamma and the living reward to see the converged values
    shift"
- **Key insights**:
  - Utility information propagates backward from the terminal states, one ring
    of cells per sweep
  - Cells near the $+1$ terminal end with high utility; cells near the $-1$
    terminal are lower
  - The change per sweep shrinks geometrically: convergence is guaranteed for
    $\gamma < 1$
- **Comment box**: "Value iteration sweeps the Bellman update until utilities
  stop changing. Watch value flow backward from the goal, like tracing a route
  from finish to start."
- **Implementation**: `seaborn.heatmap` with annotations, `matplotlib` line plot
  for convergence, value iteration loop in utils returning per-sweep snapshots

## Cell 2.3: Extracting the Optimal Policy

- **Purpose**: Show the second half of value iteration, turning converged
  utilities into an actionable policy by taking the greedy action everywhere
- **Display**:
  - The grid with an arrow in each non-terminal cell pointing to the greedy
    action $\pi^*(s) = \argmax_a \sum_{s'} \Pr(s' \mid s, a)[R + \gamma U(s')]$
  - The utility heatmap shown underneath the arrows for context
- **Interactive widget**:
  - Slider for `r_step`: living reward (-2.0 to 0.0)
  - Description: "Change the living reward and watch the optimal policy change.
    A large penalty makes the agent rush; a tiny one makes it cautious"
- **Key insights**:
  - The policy is derived from utilities, not learned separately
  - With a large negative living reward, the agent takes the short risky path
    near the $-1$ terminal
  - With a near-zero living reward, the agent takes the long safe path that
    avoids the $-1$ terminal entirely
- **Comment box**: "The policy is greedy with respect to the converged
  utilities. The living reward silently controls how much risk the agent
  accepts to save time."
- **Implementation**: `matplotlib` quiver or arrow annotations over the heatmap,
  greedy policy extraction in utils

# Part 3: Solving the MDP with Policy Iteration

## Cell 3.1: Policy Evaluation for a Fixed Policy

- **Purpose**: Introduce the evaluation half of policy iteration, computing the
  utility of a fixed (possibly bad) policy, which is a simpler linear problem
  than the full Bellman equation
- **Display**:
  - The grid showing a fixed policy as arrows, with the evaluated utilities
    $U^\pi(s)$ as a heatmap underneath
  - Start with a random or deliberately poor policy so students see low
    utilities
- **Interactive widget**:
  - Dropdown for `policy`: select a preset policy (random, always-up,
    always-right, hand-tuned)
  - Slider for `gamma`: discount factor (0.0-1.0)
  - Description: "Pick a fixed policy and see how good it is. Evaluation answers:
    if I always follow this policy, what is each state worth?"
- **Key insights**:
  - Policy evaluation drops the $\max$: with a fixed action per state the
    equations are linear and can be solved directly
  - A bad policy yields low utilities, especially for states it steers into the
    $-1$ terminal
  - Evaluation answers "how good is this policy" but not "what should I do
    instead"
- **Comment box**: "Policy evaluation fixes the action in each state, removing
  the max. The Bellman equations become linear and solvable in one shot."
- **Implementation**: `numpy.linalg.solve` for the linear system, `seaborn`
  heatmap with arrow overlay, evaluation in utils

## Cell 3.2: Policy Improvement and Iteration to Optimality

- **Purpose**: Complete the algorithm by alternating evaluation and improvement,
  showing convergence to the optimal policy in few iterations
- **Display**:
  - Side-by-side before/after grids for each iteration: the current policy
    arrows and the improved policy arrows
  - A counter showing how many states changed action this iteration, dropping to
    $0$ at convergence
- **Interactive widget**:
  - Slider for `iteration`: step through evaluate-improve rounds
  - Description: "Step through policy iteration. Each round evaluates the current
    policy, then greedily improves it. Watch arrows flip until none change"
- **Key insights**:
  - Policy iteration alternates: evaluate the policy, then make it greedy with
    respect to the new utilities
  - It converges in very few iterations, often fewer than value iteration needs
    sweeps
  - It terminates exactly when no state changes its action: the policy is stable
    and optimal
- **Comment box**: "Policy iteration: evaluate, improve, repeat. It typically
  reaches the optimal policy in a handful of iterations because each step makes
  a big, decisive change."
- **Implementation**: `matplotlib` dual-panel arrow grids, policy iteration loop
  in utils returning per-iteration snapshots

## Cell 3.3: Value Iteration vs Policy Iteration

- **Purpose**: Contrast the two exact methods so students understand the
  tradeoff between many cheap sweeps and few expensive iterations
- **Display**:
  - A line plot comparing convergence: value iteration's utility change per
    sweep against policy iteration's changed-action count per iteration
  - A small table summarizing iterations to converge and per-iteration cost
- **Interactive widget**:
  - Slider for `gamma`: discount factor (0.5-0.99)
  - Description: "Change gamma and compare how fast each method converges. Notice
    that high gamma slows value iteration much more than policy iteration"
- **Key insights**:
  - Value iteration does many cheap sweeps; policy iteration does few expensive
    evaluations
  - As $\gamma \to 1$, value iteration needs many more sweeps while policy
    iteration is relatively unaffected
  - Both converge to the same optimal policy: they are different routes to the
    same answer
- **Comment box**: "Same optimal policy, different paths. Value iteration:
  simple, many sweeps. Policy iteration: more work per step, fewer steps,
  robust to large gamma."
- **Implementation**: `seaborn` line plot, `pandas` summary table, both solvers
  reused from utils

# Part 4: Learning Without a Model (Q-Learning)

## Cell 4.1: Why Reinforcement Learning is Harder Than Planning

- **Purpose**: Motivate the shift from planning to learning by removing the
  transition model, so students see what changes when the agent is ignorant of
  the rules
- **Display**:
  - The same grid, but the transition table from Cell 1.3 is shown greyed out or
    hidden behind a "unknown to the agent" overlay
  - A contrast panel: planning (knows $\Pr$ and $R$) versus learning (must
    experience transitions)
- **Interactive widget**: None (conceptual framing cell)
- **Key insights**:
  - In RL the agent does not know $\Pr(s' \mid s, a)$ or $R(s, a, s')$: it must
    act to discover them
  - The agent only sees experience tuples $(s, a, r, s')$ as it moves
  - The goal is unchanged (maximize expected return) but the agent must learn and
    act at the same time
- **Comment box**: "Same world, blindfolded. The agent no longer has the
  transition table. It must learn the value of actions purely from the rewards
  it stumbles into."
- **Implementation**: `matplotlib` grid with masked transition table, static
  comparison rendered in utils

## Cell 4.2: The Q-Learning Update Rule

- **Purpose**: Introduce the single update that powers Q-learning, showing how
  one experience tuple nudges a Q-value toward a better estimate
- **Display**:
  - A focused diagram of one transition $s \xrightarrow{a} s'$ with reward $r$
  - The update $Q(s, a) \leftarrow Q(s, a) + \alpha[r + \gamma \max_{a'} Q(s',
    a') - Q(s, a)]$ broken into parts: old estimate, TD target, TD error
  - The numeric before/after value of $Q(s, a)$ for the chosen tuple
- **Interactive widget**:
  - Slider for `alpha`: learning rate (0.0-1.0)
  - Slider for `gamma`: discount factor (0.0-1.0)
  - Description: "Adjust the learning rate and discount. Watch the TD error and
    how much a single experience moves the Q-value"
- **Key insights**:
  - The TD error $r + \gamma \max_{a'} Q(s', a') - Q(s, a)$ measures surprise:
    the gap between expectation and observed return
  - The learning rate $\alpha$ controls how aggressively each experience
    overwrites the old estimate
  - The update bootstraps: it uses the current (imperfect) estimate of the next
    state's value
- **Comment box**: "One tuple, one nudge. Q-learning moves each estimate a
  fraction alpha of the way toward the TD target. No model needed: just $(s, a,
  r, s')$."
- **Implementation**: `matplotlib` annotated transition diagram, single-step
  update in utils

## Cell 4.3: Exploration vs Exploitation with Epsilon-Greedy

- **Purpose**: Show why the agent must sometimes act randomly, since a purely
  greedy agent can lock onto a suboptimal path and never discover better ones
- **Display**:
  - The grid with a heatmap of visit counts per state, showing where the agent
    has and has not explored
  - Two runs side by side: low epsilon (narrow, exploitative) versus high epsilon
    (broad, exploratory) coverage
- **Interactive widget**:
  - Slider for `epsilon`: exploration probability (0.0-1.0)
  - Slider for `n_episodes`: number of training episodes (log scale)
  - Description: "Adjust exploration. Low epsilon exploits a known path; high
    epsilon explores widely but acts randomly too often"
- **Key insights**:
  - A greedy agent ($\epsilon = 0$) may never visit states off its first decent
    path, missing the optimal route
  - Too much exploration ($\epsilon$ near $1$) wastes episodes acting randomly
    instead of refining good actions
  - Effective learning needs a balance, often decaying $\epsilon$ over time
- **Comment box**: "Explore to learn, exploit to earn. Epsilon-greedy takes the
  best-known action most of the time but occasionally tries something new to
  avoid getting stuck."
- **Implementation**: `seaborn` heatmap of visit counts, `ipywidgets` sliders,
  epsilon-greedy action selection in utils

## Cell 4.4: Watching Q-Learning Learn the Optimal Policy

- **Purpose**: Tie the whole notebook together by running full Q-learning and
  showing the learned policy converge to the one value iteration found with full
  knowledge
- **Display**:
  - The grid with the Q-derived greedy policy arrows, updating as training
    episodes accumulate
  - A learning curve: total return per episode rising and stabilizing
  - A comparison panel overlaying the Q-learning policy against the value
    iteration optimal policy from Cell 2.3
- **Interactive widget**:
  - Slider for `n_episodes`: training episodes (log scale)
  - Slider for `alpha`: learning rate (0.0-1.0)
  - Slider for `epsilon`: exploration probability (0.0-1.0)
  - Description: "Train the agent and watch its policy emerge. Compare it to the
    optimal policy we computed with full knowledge of the model"
- **Key insights**:
  - With enough episodes, Q-learning recovers the same optimal policy as value
    iteration without ever knowing the transition model
  - The learning curve is noisy early (exploration) and stabilizes as Q-values
    converge
  - Model-free learning trades sample efficiency for not needing a model: it
    takes many episodes but no prior knowledge
- **Comment box**: "Same answer, no model. Q-learning rediscovers the optimal
  policy purely from experience. This is the payoff of reinforcement learning:
  learning to act well in an unknown world."
- **Implementation**: `matplotlib` arrow grid plus `seaborn` learning curve,
  full Q-learning training loop in utils returning per-episode snapshots and the
  final policy

# Summary: The Mental Model

- An MDP is defined by states, stochastic actions $\Pr(s' \mid s, a)$, rewards
  $R(s, a, s')$, and a discount $\gamma$; the 4x3 grid makes all four concrete
- When the model is known, value iteration and policy iteration compute the
  optimal policy exactly by solving the Bellman equations
- When the model is unknown, Q-learning learns the optimal policy from raw
  experience tuples $(s, a, r, s')$, balancing exploration and exploitation
- All three methods converge to the same optimal policy on the same world: the
  difference is whether you plan with a model or learn without one
