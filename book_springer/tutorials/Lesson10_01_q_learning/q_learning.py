# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Q-Learning: From Brute-Force Policy Search to Learned Control
#
# - This notebook teaches Q-learning through `FrozenLake`, the canonical
#   off-policy control benchmark: an agent crosses a slippery frozen lake to a
#   goal tile without falling into a hole
# - The pedagogical arc is:
#   - See the environment and why it is hard (stochastic, sparse reward) ->
#     watch brute-force policy enumeration fail combinatorially -> learn the
#     single TD update that replaces it -> balance exploration and
#     exploitation -> train a full Q-table and watch it converge -> compare the
#     learned policy against the brute-force baseline
# - Unlike a from-scratch grid-world notebook, this one uses `gymnasium`
#   directly: the transition model is never built by hand, mirroring how
#   Q-learning is used in practice when the environment is a black box

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

import q_learning_utils as utils

hnotebook.config_notebook()
_LOG = logging.getLogger(__name__)
utils.init_loggers(_LOG)

# %% [markdown]
# # Part 1: The FrozenLake Problem and Why Brute Force Fails

# %% [markdown]
# ## Cell 1.1: The FrozenLake Environment: States, Actions, Rewards
#
# **Goal**:
# - Ground students in the concrete environment every later cell reasons
#   about, so the algorithm is never discussed in the abstract
# - Establish the three MDP ingredients (states, actions, rewards) and the
#   fact that the agent is not told the transition model
#
# _Grid layout_: 4x4 `FrozenLake` grid with tiles colored by type: start
# (blue), frozen (white), hole (grey), goal (green)
# _Comments_: number of states, number of actions, reward structure

# %%
# Draw the grid and print the environment's states, actions, and rewards.
utils.cell1_1_show_environment()

# %% [markdown]
# **Key observations**:
# - The reward is sparse: every step gives $0$ except the single step that
#   reaches the goal, so most actions carry no immediate feedback
# - With `is_slippery` on, the intended action succeeds only part of the time
#   and the agent can slide sideways, matching the slides' stochastic control
#   setting
# - Falling into a hole ends the episode with no reward, so a careless policy
#   can wander forever without ever learning what went wrong

# %% [markdown]
# ## Cell 1.2: Why Enumerating Every Policy Is Infeasible
#
# **Goal**:
# - Show concretely why the "obvious" brute-force solution, scoring every
#   deterministic policy by Monte Carlo rollouts, does not scale
# - Motivate the need for an algorithm that improves a single running estimate
#   instead of evaluating whole policies from scratch
#
# _Policy count_: bar chart comparing the number of deterministic policies
# against the number brute force can actually afford to score in one cell
# _Noisy ranking_: estimated success rate for a few sample policies as
# rollouts accumulate, showing how rankings still wobble
# _Comments_: current rollouts-per-policy value, resulting policy counts

# %%
# Show the policy-count blow-up and how noisy Monte Carlo scoring stays.
utils.cell1_2_bruteforce_infeasibility()

# %% [markdown]
# **Key observations**:
# - The number of deterministic policies grows as $|\mathcal{A}|^{|\mathcal{S}|}$:
#   with 14 non-terminal states and 4 actions this is already in the billions
# - Because the reward is sparse and stochastic, ranking policies reliably
#   needs many rollouts per policy, multiplying an already infeasible count
# - Q-learning sidesteps both problems: it never enumerates policies and it
#   refines one shared table from every single step, not whole episodes

# %% [markdown]
# # Part 2: Learning the Optimal Policy with Q-Learning

# %% [markdown]
# ## Cell 2.1: The Q-Learning TD Update Rule
#
# **Goal**:
# - Introduce the single update that powers Q-learning by applying it to one
#   experience tuple, before running any full training loop
# - Build on Cell 1.2: this update is the mechanism that replaces
#   whole-policy scoring with incremental, per-step improvement
#
# _Transition diagram_: one step $s \xrightarrow{a} s'$ with reward $r$ drawn
# on the grid
# _Q-value bar_: before/after value for $Q(s,a)$ showing the old estimate, the
# TD target, and the updated value
# _Comments_: current $\alpha$, $\gamma$, the TD error, and the numeric
# before/after $Q(s,a)$

# %%
# Show how a single experience tuple nudges one Q-value.
utils.cell2_1_q_update_rule()

# %% [markdown]
# **Key observations**:
# - The TD error $r + \gamma \max_{a'} Q(s',a') - Q(s,a)$ measures surprise:
#   the gap between the current estimate and the observed outcome
# - The learning rate $\alpha$ controls how much of that surprise gets folded
#   into $Q(s,a)$ on this single step
# - The update bootstraps: it uses the current, possibly wrong, estimate of
#   the next state's best action value rather than waiting for the episode to
#   end

# %% [markdown]
# ## Cell 2.2: Exploration vs Exploitation with Epsilon-Greedy
#
# **Goal**:
# - Show why the agent must sometimes act randomly instead of always taking
#   its current best-known action
# - Extend Cell 2.1: repeated application of the TD update only teaches the
#   agent about states it actually visits, so visitation itself becomes a
#   variable to control
#
# _Visit heatmap_: grid heatmap of how many times each tile was visited during
# training at the chosen epsilon
# _Coverage comparison_: a second heatmap at a fixed high epsilon for contrast
# _Comments_: current $\epsilon$, number of episodes, unvisited state counts

# %%
# Compare state coverage under low vs high epsilon.
utils.cell2_2_exploration_exploitation()

# %% [markdown]
# **Key observations**:
# - A near-greedy agent ($\epsilon$ close to $0$) can lock onto the first path
#   that reaches the goal and never visit tiles that might lead to a safer or
#   shorter route
# - A highly exploratory agent ($\epsilon$ close to $1$) covers the grid more
#   evenly but wastes many episodes acting randomly instead of exploiting what
#   it already knows
# - Coverage is not the goal by itself: it is a means to make sure the Q-table
#   gets accurate estimates everywhere that matters

# %% [markdown]
# ## Cell 2.3: Training the Q-Table and Watching Convergence
#
# **Goal**:
# - Run the full Q-learning training loop, combining the TD update
#   (Cell 2.1) and epsilon-greedy action selection (Cell 2.2) over many
#   episodes
# - Show the learning curve rising from near-random performance to a
#   consistently successful policy
#
# _Learning curve_: rolling-average success rate per training episode
# _Q-table heatmap_: grid heatmap of $\max_a Q(s,a)$ per state
# _Comments_: current episode count, current rolling success rate, current
# final $\epsilon$ after decay

# %%
# Train Q-learning and watch the learning curve and Q-table converge.
utils.cell2_3_training_convergence()

# %% [markdown]
# **Key observations**:
# - The learning curve is noisy early, dominated by exploration and slipping
#   on the ice, then rises and stabilizes as the Q-table becomes accurate
# - States near the goal develop high $\max_a Q(s,a)$ first; this high-value
#   region spreads backward toward the start tile over training, the same
#   backward propagation seen in value-based planning
# - Decaying $\epsilon$ lets the agent shift from exploring broadly early to
#   exploiting its learned table later, without hand-tuning a fixed rate

# %% [markdown]
# ## Cell 2.4: The Learned Policy vs the Brute-Force Baseline
#
# **Goal**:
# - Tie the notebook together by extracting the greedy policy
#   $\arg\max_a Q(s,a)$ from the trained table and evaluating it head to head
#   against the brute-force approach from Cell 1.2
# - Show what Q-learning bought: a policy at least as good, found without ever
#   enumerating policies or knowing the transition model
#
# _Policy grid_: greedy action drawn as an arrow in every non-terminal tile,
# overlaid on the final Q-table heatmap
# _Success-rate comparison_: success rate over evaluation episodes for three
# policies: random, best of a small brute-force sample, and Q-learning
# _Comments_: success rate for each of the three policies shown

# %%
# Compare the trained Q-learning policy against the brute-force baseline.
utils.cell2_4_policy_vs_bruteforce()

# %% [markdown]
# **Key observations**:
# - The Q-learning policy reaches or exceeds the success rate of the best
#   policy brute force found, despite brute force scoring only a tiny sample
#   of all possible policies
# - Q-learning needed one shared table updated per step, not a separate
#   Monte Carlo score per candidate policy: the same training episodes that
#   produced the learning curve in Cell 2.3 already double as the evaluation
#   budget
# - The comparison makes the payoff concrete: the same guarantee (a good
#   policy) at a fraction of the sampling cost, and without ever seeing the
#   transition probabilities

# %% [markdown]
# # Summary: The Mental Model
#
# - `FrozenLake` is a sparse-reward, stochastic MDP where brute-force policy
#   search is combinatorially infeasible: billions of deterministic policies,
#   each needing many rollouts to score reliably
# - Q-learning replaces whole-policy scoring with a single incremental update,
#   $Q(s,a) \leftarrow Q(s,a) + \alpha[r + \gamma \max_{a'} Q(s',a') - Q(s,a)]$,
#   applied to every experienced transition
# - Epsilon-greedy action selection, decayed over training, balances visiting
#   new states against exploiting what the table already knows
# - After enough episodes, the greedy policy extracted from the learned
#   Q-table matches or beats the best brute-force policy, learned purely from
#   experience and without ever knowing the transition model
