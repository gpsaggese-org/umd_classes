# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.3
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # The 4x3 Grid World: From MDPs to Reinforcement Learning
#
# - This notebook teaches sequential decision making through the canonical AIMA
#   4x3 grid world, built entirely from scratch with `numpy` (no `gymnasium`)
# - The grid world is the unifying example throughout:
#   - It appears in the MDP definition, utility of states, Bellman equations,
#     value iteration, policy iteration, and Q-learning
# - The pedagogical arc is:
#   - Build the environment (states, stochastic transitions, rewards)
#   - Solve it with full knowledge (value iteration, policy iteration)
#   - Learn it without knowing the model (Q-learning)
# - Building from scratch is a deliberate choice: students see the full
#   transition model $\Pr(s' \mid s, a)$ as an explicit table, which `gymnasium`
#   hides inside `env.step()`

# %% [markdown]
# ## Imports

# %%
# %load_ext autoreload
# %autoreload 2

# System libraries.
import logging

# Third-party libraries.
import matplotlib.pyplot as plt
import seaborn as sns

# Set plotting style.
# TODO(ai_gp): Use usual style.
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (14, 5)

# %%
import helpers.hnotebook as hnotebook

import L12_01_gridworld_4x3_utils as utils

# Initialize notebook configuration and logging.
hnotebook.config_notebook()
_LOG = logging.getLogger(__name__)
utils.init_loggers(_LOG)

# %% [markdown]
# # Part 1: Building the Grid World Environment

# %% [markdown]
# ## Cell 1.1: The 4x3 Grid and Its States
#
# - This is the world the agent lives in
# - It is fully observable (the agent always knows its cell) but stochastic
#   (actions do not always succeed)
# - Cell `(1, 1)` is `START`, cell `(4, 3)` is the `+1` terminal (green), cell
#   `(4, 2)` is the `-1` terminal (red), cell `(2, 2)` is a wall (grey)

# %%
# Draw the grid layout that every later algorithm will reason about.
utils.cell1_1_show_grid()

# %% [markdown]
# - The environment has 11 reachable states (12 cells minus 1 wall)
# - Two states are terminal: reaching either ends the episode

# %% [markdown]
# ## Cell 1.2: Stochastic Action Model
#
# **Goal**:
# - Show why this is an MDP and not a deterministic puzzle
# - The unreliable actions are the entire source of difficulty
#
# **Plots**:
# - _Action spread_: the intended action and the three possible outcomes, with
#   arrow thickness encoding probability
# - _Comments_: current parameters and the outcome distribution
#
# **Parameters**:
# - `action`: the intended action (`Up`, `Down`, `Left`, `Right`)
# - `p_intended`: probability the intended action succeeds (0.5 to 1.0)
#
# **Key observations**:
# - With $\Pr(\text{intended}) = 0.8$, the agent goes sideways $20\%$ of the time
# - Walls and boundaries bounce the agent back to its current cell
# - As `p_intended` approaches $1.0$, the world becomes deterministic

# %%
# The wheels slip: the intended action happens 80% of the time; the agent
# veers perpendicular 10% each way. This randomness is why a single plan is not
# enough: we need a policy.
# TODO(ai_gp): Allow to select the cell Select a state and action to see the model row:
# state: (1, 1) action, like for cell1_3_transition_table
# Add a button retry
utils.cell1_2_stochastic_action()

# %% [markdown]
# - The intended direction carries probability `p_intended`
# - The two perpendicular directions split the remaining mass equally
# - A blocked move (wall or boundary) returns the agent to its current cell

# %% [markdown]
# ## Cell 1.3: Transition Model as an Explicit Table
#
# **Goal**:
# - Make the abstract $\Pr(s' \mid s, a)$ concrete as an actual probability table
#
# **Plots**:
# - _Probability grid_: reachable next states shaded by probability
# - _DataFrame_: each reachable next state $s'$ and its probability
#
# **Parameters**:
# - `state`: the current cell
# - `action`: the intended action
#
# **Key observations**:
# - The transition model has shape $|S| \times |A| \times |S|$, but is sparse
# - Each $(s, a)$ row sums to $1.0$: it is a probability distribution

# %%
# TODO(ai_gp): Represent the transition model as a table

# %%
# This table is the MDP model Pr(s' | s, a). We build it by hand here. In Part
# 4, Q-learning will solve the same world without ever seeing this table.
# TODO(ai_gp): Make the wall cell look like in cell1_2_stochastic_action
# TODO(ai_gp): Make the cells with probability 0, white
# TODO(ai_gp): print the probability table in a comments fig on the right
utils.cell1_3_transition_table()

# %% [markdown]
# - Most next states have zero probability: the model is sparse
# - The non-zero entries always sum to one
# - This explicit model is exactly what model-free learning will do without

# %% [markdown]
# ## Cell 1.4: Rewards and Episode Returns
#
# **Goal**:
# - Define the reward structure and connect per-step rewards to discounted return
# - Show how a single trajectory accumulates $\sum_t \gamma^t R_t$
#
# **Plots**:
# - _Rewards and trajectory_: per-cell rewards with a sample path from START
# - _Comments_: the running discounted return step by step
#
# **Parameters**:
# - `r_step`: the per-step living reward (-1.0 to 0.0)
# - `gamma`: discount factor (0.0 to 1.0)
# - `seed`: trajectory seed
#
# **Key observations**:
# - The small negative living reward $-0.04$ pushes the agent to finish quickly
# - The discount factor $\gamma$ weights near-term rewards more than distant ones
# - Total return depends on the whole sequence of states, not just the final cell

# %%
# Reward is the feedback signal. The living reward of -0.04 is a gentle penalty
# for taking too long. Return is the discounted sum the agent tries to maximize.
utils.cell1_4_rewards_and_returns()

# %% [markdown]
# - Each non-terminal step costs a little, so wandering is penalized
# - Lowering gamma shrinks the contribution of later rewards
# - The same path yields different returns as the reward and discount change

# %% [markdown]
# # Part 2: Solving the MDP with Value Iteration

# %% [markdown]
# ## Cell 2.1: The Bellman Equation for One State
#
# **Goal**:
# - Build intuition for the Bellman update on a single state
# - The full algorithm is just this update applied everywhere
#
# **Plots**:
# - _Inspected state_: the highlighted cell on the grid
# - _Action values_: a bar per action, the best (max) highlighted
# - _Comments_: the action values and the resulting utility
#
# **Parameters**:
# - `state`: which cell to inspect
# - `gamma`: discount factor (0.0 to 1.0)
#
# **Key observations**:
# - The utility of a state is the value of its best action, not an average
# - Each action blends immediate reward with the discounted utility of next states
# - The $\max$ operator makes the system nonlinear, so we iterate

# %%
# Bellman: utility of a state = best immediate action + future potential. We
# compute one value per action and keep the maximum.
utils.cell2_1_bellman_one_state()

# %% [markdown]
# - Different actions can have very different values at the same state
# - The greedy action is the one whose expected next-state utility is highest
# - Repeating this max update everywhere is exactly value iteration

# %% [markdown]
# ## Cell 2.2: Value Iteration Converging Over Sweeps
#
# **Goal**:
# - Watch state utilities converge to a fixed point as we sweep the grid
# - See value information propagate backward from the terminals
#
# **Plots**:
# - _Utility heatmap_: each cell annotated with its current $U(s)$
# - _Convergence_: max utility change $\lVert U_{i+1} - U_i \rVert$ per sweep
# - _Comments_: current sweep, parameters, and sweeps to converge
#
# **Parameters**:
# - `iteration`: step through sweeps $0, 1, 2, \ldots$
# - `gamma`: discount factor (0.5 to 1.0)
# - `r_step`: living reward (-1.0 to 0.0)
#
# **Key observations**:
# - Utility spreads backward from the terminals, one ring of cells per sweep
# - Cells near the $+1$ terminal end high; cells near the $-1$ terminal end low
# - The change per sweep shrinks geometrically: convergence is guaranteed

# %%
# Value iteration sweeps the Bellman update until utilities stop changing. Watch
# value flow backward from the goal, like tracing a route from finish to start.
utils.cell2_2_value_iteration()

# %% [markdown]
# - Early sweeps only affect cells adjacent to the terminals
# - Later sweeps refine the interior until nothing changes
# - Higher gamma propagates value further but converges more slowly

# %% [markdown]
# ## Cell 2.3: Extracting the Optimal Policy
#
# **Goal**:
# - Turn converged utilities into an actionable policy
# - Take the greedy action in every cell
#
# **Plots**:
# - _Policy over utilities_: an arrow per cell over the utility heatmap
# - _Comments_: parameters and the utility of START
#
# **Parameters**:
# - `r_step`: living reward (-2.0 to 0.0)
#
# **Key observations**:
# - The policy is derived from utilities, not learned separately
# - A large negative living reward makes the agent take the short risky path
# - A near-zero living reward makes the agent take the long safe path

# %%
# The policy is greedy with respect to the converged utilities. The living
# reward silently controls how much risk the agent accepts to save time.
utils.cell2_3_extract_policy()

# %% [markdown]
# - The arrows point toward the action that maximizes expected return
# - Near the $-1$ terminal the policy steers cautiously when steps are cheap
# - Making each step expensive flips the policy toward the shorter risky route

# %% [markdown]
# # Part 3: Solving the MDP with Policy Iteration

# %% [markdown]
# ## Cell 3.1: Policy Evaluation for a Fixed Policy
#
# **Goal**:
# - Compute the utility of a fixed (possibly bad) policy
# - This is a simpler linear problem than the full Bellman equation
#
# **Plots**:
# - _Policy utilities_: the fixed policy as arrows over its evaluated utilities
# - _Comments_: parameters and the utility of START
#
# **Parameters**:
# - `policy`: a preset policy (random, always-up, always-right, hand-tuned)
# - `gamma`: discount factor (0.0 to 1.0)
#
# **Key observations**:
# - With a fixed action per state the $\max$ disappears: the equations are linear
# - A bad policy yields low utilities, especially where it steers into $-1$
# - Evaluation answers "how good is this policy", not "what should I do instead"

# %%
# Policy evaluation fixes the action in each state, removing the max. The
# Bellman equations become linear and solvable in one shot.
utils.cell3_1_policy_evaluation()

# %% [markdown]
# - The linear system $(I - \gamma P) U = b$ is solved directly with `numpy`
# - A poor policy produces visibly low utilities near the $-1$ terminal
# - Evaluation is the first half of policy iteration

# %% [markdown]
# ## Cell 3.2: Policy Improvement and Iteration to Optimality
#
# **Goal**:
# - Alternate evaluation and improvement until the policy stops changing
# - Watch convergence to the optimal policy in a few iterations
#
# **Plots**:
# - _Before / after_: the current policy arrows and the improved policy arrows
# - _Comments_: states that changed action and rounds to converge
#
# **Parameters**:
# - `iteration`: step through evaluate/improve rounds
#
# **Key observations**:
# - Each round evaluates the policy, then makes it greedy with respect to it
# - It converges in very few iterations, often fewer than value iteration sweeps
# - It terminates exactly when no state changes its action

# %%
# Policy iteration: evaluate, improve, repeat. It typically reaches the optimal
# policy in a handful of iterations because each step is a big, decisive change.
utils.cell3_2_policy_iteration()

# %% [markdown]
# - Early rounds flip many arrows at once
# - The count of changed states drops to zero at convergence
# - A stable policy is provably optimal

# %% [markdown]
# ## Cell 3.3: Value Iteration vs Policy Iteration
#
# **Goal**:
# - Contrast the two exact methods and their convergence behavior
# - Understand the tradeoff between many cheap sweeps and few expensive rounds
#
# **Plots**:
# - _Value iteration_: utility change per sweep
# - _Policy iteration_: changed-action count per round
# - _Comments_: sweeps vs rounds at the current gamma
#
# **Parameters**:
# - `gamma`: discount factor (0.5 to 0.99)
#
# **Key observations**:
# - Value iteration does many cheap sweeps; policy iteration does few expensive ones
# - As $\gamma \to 1$, value iteration needs many more sweeps
# - Both converge to the same optimal policy

# %%
# Same optimal policy, different paths. Value iteration: simple, many sweeps.
# Policy iteration: more work per step, fewer steps, robust to large gamma.
utils.cell3_3_compare_solvers()

# %% [markdown]
# - Raising gamma stretches the value iteration curve to the right
# - Policy iteration stays at a handful of rounds across gamma
# - They are different routes to the same answer

# %% [markdown]
# # Part 4: Learning Without a Model (Q-Learning)

# %% [markdown]
# ## Cell 4.1: Why Reinforcement Learning is Harder Than Planning
#
# - Same world, blindfolded: the agent no longer has the transition table
# - It must learn the value of actions purely from the rewards it stumbles into
# - In RL the agent does not know $\Pr(s' \mid s, a)$ or $R(s, a, s')$
# - The agent only sees experience tuples $(s, a, r, s')$ as it moves
# - The goal is unchanged (maximize expected return), but it must learn and act
#   at the same time

# %%
# Contrast planning (knows Pr and R) with learning (must experience transitions).
utils.cell4_1_planning_vs_learning()

# %% [markdown]
# - Planning reads the model; learning must discover it through action
# - Every later algorithm in this part sees only $(s, a, r, s')$ tuples
# - The same optimal policy is the target, reached by a harder route

# %% [markdown]
# ## Cell 4.2: The Q-Learning Update Rule
#
# **Goal**:
# - Introduce the single update that powers Q-learning
# - Show how one experience tuple nudges a Q-value toward a better estimate
#
# **Plots**:
# - _Transition diagram_: one transition $s \xrightarrow{a} s'$ with reward $r$
# - _Comments_: the update broken into old estimate, TD target, and TD error
#
# **Parameters**:
# - `alpha`: learning rate (0.0 to 1.0)
# - `gamma`: discount factor (0.0 to 1.0)
#
# **Key observations**:
# - The TD error $r + \gamma \max_{a'} Q(s', a') - Q(s, a)$ measures surprise
# - The learning rate $\alpha$ controls how aggressively we overwrite the estimate
# - The update bootstraps from the current estimate of the next state's value

# %%
# One tuple, one nudge. Q-learning moves each estimate a fraction alpha of the
# way toward the TD target. No model needed: just (s, a, r, s').
utils.cell4_2_q_update_rule()

# %% [markdown]
# - A larger alpha makes each experience move the estimate further
# - The TD target combines the observed reward with the discounted next value
# - With alpha near zero the estimate barely moves; near one it jumps to the target

# %% [markdown]
# ## Cell 4.3: Exploration vs Exploitation with Epsilon-Greedy
#
# **Goal**:
# - Show why the agent must sometimes act randomly
# - A purely greedy agent can lock onto a suboptimal path
#
# **Plots**:
# - _Low-epsilon visits_: visit counts under the chosen exploration rate
# - _High-epsilon visits_: visit counts under broad exploration
# - _Comments_: parameters and the exploration tradeoff
#
# **Parameters**:
# - `epsilon`: exploration probability (0.0 to 1.0)
# - `n_episodes`: number of training episodes (log scale)
# - `seed`: random seed
#
# **Key observations**:
# - A greedy agent may never visit states off its first decent path
# - Too much exploration wastes episodes acting randomly
# - Effective learning needs a balance, often decaying $\epsilon$ over time

# %%
# Explore to learn, exploit to earn. Epsilon-greedy takes the best-known action
# most of the time but occasionally tries something new to avoid getting stuck.
utils.cell4_3_exploration()

# %% [markdown]
# - Low epsilon concentrates visits on a narrow corridor of states
# - High epsilon spreads visits broadly but refines actions slowly
# - The visit heatmap shows exactly which states the agent has explored

# %% [markdown]
# ## Cell 4.4: Watching Q-Learning Learn the Optimal Policy
#
# **Goal**:
# - Run full Q-learning and watch the learned policy emerge
# - Compare it to the policy value iteration found with full knowledge
#
# **Plots**:
# - _Q-learning policy_: the greedy policy derived from the learned Q-table
# - _Learning curve_: smoothed total return per episode
# - _Comments_: parameters and how many states match the planning optimum
#
# **Parameters**:
# - `n_episodes`: training episodes (log scale)
# - `alpha`: learning rate (0.0 to 1.0)
# - `epsilon`: exploration probability (0.0 to 1.0)
# - `seed`: random seed
#
# **Key observations**:
# - With enough episodes, Q-learning recovers the same optimal policy
# - The learning curve is noisy early (exploration) and stabilizes as Q converges
# - Model-free learning trades sample efficiency for not needing a model

# %%
# Same answer, no model. Q-learning rediscovers the optimal policy purely from
# experience. This is the payoff of reinforcement learning.
utils.cell4_4_q_learning_converges()

# %% [markdown]
# - The learned arrows converge to the value iteration policy as episodes grow
# - Returns rise and flatten as the Q-table stops changing
# - The same optimal behavior is reached without ever reading the model

# %% [markdown]
# # Summary: The Mental Model
#
# - An MDP is defined by states, stochastic actions $\Pr(s' \mid s, a)$, rewards
#   $R(s, a, s')$, and a discount $\gamma$; the 4x3 grid makes all four concrete
# - When the model is known, value iteration and policy iteration compute the
#   optimal policy exactly by solving the Bellman equations
# - When the model is unknown, Q-learning learns the optimal policy from raw
#   experience tuples $(s, a, r, s')$, balancing exploration and exploitation
# - All three methods converge to the same optimal policy on the same world: the
#   difference is whether you plan with a model or learn without one
