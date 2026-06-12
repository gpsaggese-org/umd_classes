# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # The 4x3 Grid World with Gymnasium
#
# - This notebook mirrors the `L12_01_gridworld_4x3` notebook cell-by-cell
# - Uses a `gymnasium.Env` subclass for the same 4x3 grid world
# - The environment exposes `P[s][a]` (FrozenLake convention) for planning, and
#   `step()` for model-free learning
# - The pedagogical arc is identical:
#   - Build the env -> solve it with full knowledge -> learn without a model
# - The only difference from the from-scratch version is the API:
#   - States are integer IDs (0-10) instead of `(col, row)` tuples
#   - Actions are integer IDs (0-3) instead of strings
#   - `gymnasium` calls `reset()` and `step()` instead of direct model access

# %% [markdown]
# ## Imports

# %%
# %load_ext autoreload
# %autoreload 2

import logging

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (14, 5)

# %%
import helpers.hnotebook as hnotebook

import L12_02_gridworld_4x3_gymnasium_utils as utils

hnotebook.config_notebook()
_LOG = logging.getLogger(__name__)
utils.init_loggers(_LOG)

# %% [markdown]
# # Part 1: Building the Grid World Environment (Gymnasium)

# %% [markdown]
# ## Cell 1.1: The 4x3 Grid and Its States
#
# - Same layout as the from-scratch version: 4x3 grid with START, +1, -1, WALL
# - This time, states are `gym.spaces.Discrete(11)` and actions are
#   `gym.spaces.Discrete(4)`
# - The grid world is fully observable (the agent sees its state ID) but
#   stochastic (actions do not always succeed)

# %%
# Draw the grid and print the gymnasium observation / action spaces.
utils.cell1_1_show_grid()

# %% [markdown]
# - The environment has 11 reachable states (12 cells minus 1 wall)
# - Two states are terminal: reaching either ends the episode
# - State IDs 0-10 map to the same `(col, row)` cells

# %% [markdown]
# ## Cell 1.2: Stochastic Action Model
#
# - The gymnasium env uses the same slip model under the hood
# - Transition probabilities live in `env.P[s][a]` as a list of
#   `(prob, s', reward, terminated)` tuples
# - The intended action succeeds with probability `p_intended`; the agent
#   slips perpendicular with probability `(1-p_intended)/2` each

# %%
# The wheels slip. The transition data comes from env.P[s][a].
utils.cell1_2_stochastic_action()

# %% [markdown]
# - The intended direction carries probability `p_intended`
# - The two perpendicular directions split the remaining mass equally
# - Blocked moves bounce back. All this is handled by `_compute_transitions()`

# %% [markdown]
# ## Cell 1.3: Transition Model from env.P
#
# - `env.P[s][a]` exposes `[(prob, s', reward, terminated)]` -- the same row
#   of the transition model that the from-scratch version built explicitly
# - This is exactly what `gymnasium` would hide inside `step()` for planning
# - Value iteration and policy iteration read this dict; Q-learning uses
#   `step()` instead and never touches `env.P`

# %%
# This table is env.P[s][a]. Planning algorithms read it; Q-learning does not.
utils.cell1_3_transition_table()

# %% [markdown]
# - Each row sums to 1.0
# - The reward and terminal flag are part of each transition tuple
# - Planning solvers read this table directly

# %% [markdown]
# ## Cell 1.4: Rewards and Episode Returns
#
# - The reward structure is identical: $-0.04$ living reward, $+1$ and $-1$
#   for the two terminal cells
# - A fixed policy is rolled out via `env.step()` for a sample trajectory

# %%
# Rewards and the discounted return of a sample trajectory.
utils.cell1_4_rewards_and_returns()

# %% [markdown]
# - Each step returns a reward, and the total return is the discounted sum
# - Changing `r_step` and `gamma` shifts the return of the same path

# %% [markdown]
# # Part 2: Solving the MDP with Value Iteration

# %% [markdown]
# ## Cell 2.1: The Bellman Equation for One State
#
# - The Bellman update reads the action values from `env.P[s][a]`
# - The gymnasium version computes `Q(s,a)` the same way, but uses integer
#   state IDs and action IDs

# %%
# Bellman one state: utilities come from value_iteration() using env.P.
utils.cell2_1_bellman_one_state()

# %% [markdown]
# - The utility of a state is the value of its best action
# - The max is what makes the system nonlinear, requiring iteration

# %% [markdown]
# ## Cell 2.2: Value Iteration Converging Over Sweeps
#
# - Same `value_iteration()` algorithm, but operating on `env.P[s][a]`
# - Sweeps converge to the same fixed point as the from-scratch version

# %%
# Watch value iteration converge on the gymnasium env.P model.
utils.cell2_2_value_iteration()

# %% [markdown]
# - Value propagates backward from the terminals, one ring per sweep
# - The change per sweep shrinks geometrically

# %% [markdown]
# ## Cell 2.3: Extracting the Optimal Policy
#
# - The greedy policy derived from converged utilities
# - Identical to the from-scratch result -- same MDP, same answer

# %%
# Extract the optimal policy from converged utilities.
utils.cell2_3_extract_policy()

# %% [markdown]
# - The living reward controls risk: expensive steps push the agent toward
#   the short risky path; cheap steps let it take the long safe route

# %% [markdown]
# # Part 3: Solving the MDP with Policy Iteration

# %% [markdown]
# ## Cell 3.1: Policy Evaluation for a Fixed Policy
#
# - Solves $(I - \gamma P) U = b$ using `numpy.linalg.solve`
# - Reads the transition probabilities from `env.P[s][a]`

# %%
# Evaluate a fixed policy by solving linear Bellman equations.
utils.cell3_1_policy_evaluation()

# %% [markdown]
# - A bad policy yields low utilities, especially near the $-1$ terminal
# - Evaluation answers "how good is this policy"

# %% [markdown]
# ## Cell 3.2: Policy Improvement and Iteration to Optimality
#
# - Alternates evaluation and improvement, converging in a handful of rounds
# - Starts from a deliberately poor policy so the improvement is visible

# %%
# Step through policy iteration. Each round improves the policy.
utils.cell3_2_policy_iteration()

# %% [markdown]
# - Policy iteration typically converges in fewer rounds than value iteration
# - Each round is more expensive (solving a linear system), but the total
#   wall-clock can still be lower

# %% [markdown]
# ## Cell 3.3: Value Iteration vs Policy Iteration
#
# - Both methods use the same `env.P[s][a]` model
# - Both converge to the same optimal policy
# - The tradeoff is many cheap sweeps vs few expensive evaluations

# %%
# Compare the convergence behaviour of both solvers.
utils.cell3_3_compare_solvers()

# %% [markdown]
# - As $\gamma \to 1$, value iteration needs many more sweeps
# - Policy iteration is relatively unaffected by gamma

# %% [markdown]
# # Part 4: Learning Without a Model (Q-Learning)

# %% [markdown]
# ## Cell 4.1: Why Reinforcement Learning is Harder Than Planning
#
# - Same world, but the agent now calls `env.step()` and never reads
#   `env.P[s][a]`
# - It must learn the value of actions purely from the experience tuples
#   it gets back from each step

# %%
# Planning reads env.P; learning calls env.step().
utils.cell4_1_planning_vs_learning()

# %% [markdown]
# - The transition model is hidden behind the gymnasium API
# - The agent discovers the world by interacting with it

# %% [markdown]
# ## Cell 4.2: The Q-Learning Update Rule
#
# - One call to `env.step()` produces the tuple used in the TD update
# - The Q-value is nudged toward the TD target $\alpha$ at a time

# %%
# One step, one nudge. The update uses only the (s, a, r, s') tuple.
utils.cell4_2_q_update_rule()

# %% [markdown]
# - The TD error measures surprise: the gap between old expectation and
#   observed outcome
# - No transition probabilities are needed

# %% [markdown]
# ## Cell 4.3: Exploration vs Exploitation with Epsilon-Greedy
#
# - The same epsilon-greedy policy is used within `q_learning()`
# - Low epsilon concentrates visits on a narrow path; high epsilon spreads
#   visits broadly

# %%
# Compare state coverage at low and high exploration.
utils.cell4_3_exploration()

# %% [markdown]
# - The visit heatmap reveals exactly which states the agent has explored
# - A balance between exploration and exploitation is essential

# %% [markdown]
# ## Cell 4.4: Watching Q-Learning Learn the Optimal Policy
#
# - With enough episodes, Q-learning recovers the same optimal policy found
#   by value iteration -- without ever reading `env.P[s][a]`
# - The only interface it uses is `env.step()`

# %%
# Train Q-learning and compare to the planning optimum.
utils.cell4_4_q_learning_converges()

# %% [markdown]
# - The learned arrows converge to the value iteration arrows as episodes grow
# - Returns rise and flatten as the Q-table stabilises
# - This is the payoff: the same optimal behaviour emerges from pure
#   experience, no model required

# %% [markdown]
# # Summary: The Mental Model
#
# - A `gymnasium.Env` subclass is an MDP: its `P[s][a]` encodes the transition
#   model and its `step()` lets the agent interact without reading the model
# - When the model is known (planning), `value_iteration()` and
#   `policy_iteration()` read `env.P` and compute the optimal policy exactly
# - When the model is unknown (learning), `q_learning()` calls `env.step()`
#   and discovers the optimal policy from experience tuples
# - All three methods converge to the same optimal policy on the same
#   environment -- the difference is whether you plan with the model or learn
#   without it
# - The gymnasium `GridWorldEnv` produces exactly the same optimal utilities
#   and policies as the from-scratch `GridWorld` class