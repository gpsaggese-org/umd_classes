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
# ## Imports

# %%
# %load_ext autoreload
# %autoreload 2

import logging

import matplotlib.pyplot as plt
import seaborn as sns

# Set plotting style.
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# %%
import helpers.hintrospection as hintros
import helpers.htutorial as ut
import L09_03_multi_armed_bandits_sim as sim
import L09_03_multi_armed_bandits_utils as utils

ut.config_notebook()

# Initialize logger.
logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)

# %%
# #!apt-get update && apt-get install -y git

# %% [markdown]
# # Cell 1: Introduction - Casino Slot Machines
#
# Interactive casino slot machine visualization.
# - There are 3 slot machines
# - You have 10 coins
# - Each gives you a payout in [-1, 1] with an unknown mean $\mu_i$
# - Choose which machine to play
# - Track total winnings and coin budget
# - How do you maximize your winnings?

# %%
# TODO(ai_gp): For each machine show an histogram with the sequence of values and empirical mean.
# After 10 coins stop.
utils.cell1_casino_slot_machines()

# %% [markdown]
# ## Core classes
#
# The interactive cells above and below are built on top of a few core classes:
#
# | Object | Description | Comments |
# |--------|-------------|----------|
# | `MultiArmedBandit` | Environment with $K$ machines, each with a fixed but unknown true mean $\mu_i$ | Tracks pulls and rewards per machine |
# | `Strategy` | Abstract base class for a machine-selection policy | Subclasses: `ExplorationStrategy`, `ExploitationStrategy`, `EpsilonGreedyStrategy` |
# | `BanditExperiment` | Runs one `MultiArmedBandit` with one `Strategy` for $N$ coins | Returns rewards and cumulative rewards |
# | `BanditSimulation` | Runs many `BanditExperiment` trials with different seeds | Aggregates mean/std statistics across trials |

# %%
# Show the public API and GitHub source link of the core classes.
for cls in [
    sim.MultiArmedBandit,
    sim.Strategy,
    sim.BanditExperiment,
    sim.BanditSimulation,
]:
    print(f"=== {cls.__name__} ===")
    hintros.get_link_to_code(cls)
    hintros.print_public_methods(cls)

# %% [markdown]
# # Cell 2: Exploration vs Exploitation Dilemma
#
# Demonstrate the fundamental tradeoff between exploration and exploitation in the three slot machine set up.
#
# **Setup**:
# - Same 3 slot machines as before, each with a fixed but unknown true mean $\mu_i$
# - Instead of playing one coin at a time, play $N$ coins automatically (set with the coins slider)
# - Compare the total reward earned by each strategy over the $N$ coins
#
# **Strategies**:
# - **Pure exploration**: pick a machine uniformly at random on every coin
#   - Learns the true means accurately but wastes coins on bad machines
# - **Pure exploitation**: pull each machine once, then always pick the machine with the highest observed mean
#   - Can get stuck on a suboptimal machine if an early random reward looks good
# - **Balanced (epsilon-greedy)**: explore with probability $\epsilon$, otherwise exploit the best known machine
#   - Balances the two extremes: $\epsilon$ controls how much exploration is kept
#
# // Add a strategy with optimal choice (oracle)

# %%
utils.cell2_exploration_vs_exploitation()
# Pure exploration learns but earns little
# Pure exploitation gets stuck on suboptimal choices
# Balance is key.

# %% [markdown]
# <!-- # Cell A: Strategy Comparison with Epsilon Sweep
#
# Interactive comparison of strategies with epsilon sweep analysis.
# - Run multiple trials with different epsilon values
# - Compare exploration, exploitation, and balanced strategies
# - Visualize mean performance with error bars
# - Find optimal epsilon value -->

# %%
# utils.cell3_strategy_comparison()

# %% [markdown]
# <!-- # Cell 4: Ensemble Comparison Across Random Mu Configurations
#
# Compare strategies averaged over multiple random mu configurations.
# - Test strategy robustness across different machine configurations
# - Average results over many random mu values
# - Compare mean performance with confidence intervals
# - Understand which strategy is most reliable -->

# %%
# utils.cell4_ensemble_comparison()

# %%
