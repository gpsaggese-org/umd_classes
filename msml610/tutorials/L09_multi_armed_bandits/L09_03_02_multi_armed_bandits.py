# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Multi Armed Bandits

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
    hintros.print_obj_info(cls)

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
# # Cell 3: Greedy Algorithm Failure
#
# **Goal**:
# - See the greedy algorithm get permanently stuck on a suboptimal arm
# - Understand why pure exploitation is not enough
#
# _Pull timeline_: shows which machine was pulled at each round and the reward
# it returned, color-coded by machine
# _Empirical mean estimates_: empirical mean of each machine over time, with
# the (usually hidden) true means shown as dotted lines
# _Comments_: current seed, pull counts, and whether greedy got stuck

# %%
utils.cell3_greedy_algorithm_failure()

# %% [markdown]
# **Key observations**:
# - Greedy pulls each machine once, then always exploits the best one so far
# - If the first pull of a suboptimal machine returns a lucky high reward,
#   greedy locks onto it and never revisits the truly best machine again
# - This is why greedy alone has linear regret: it never corrects an early
#   mistake
# - Try different seeds to see how often greedy gets stuck vs finds the best
#   machine by luck

# %% [markdown]
# # Cell 5: Epsilon-Greedy Algorithm
#
# **Goal**:
# - See how a small exploration probability $\epsilon$ prevents the
#   "stuck forever" failure of pure greedy
#
# _Pull timeline_: pulls color-coded by decision type (gray=init,
# blue=explore, green=exploit)
# _Pull counts_: number of times each machine was pulled
# _Cumulative reward_: total reward earned over time
# _Comments_: current seed, epsilon, decision counts, pull counts

# %%
utils.cell5_epsilon_greedy()

# %% [markdown]
# **Key observations**:
# - With $\epsilon=0.1$, about 10% of rounds explore (random machine) and 90%
#   exploit (best known machine)
# - Occasional exploration lets epsilon-greedy discover and recover from an
#   early unlucky estimate, unlike pure greedy
# - Try $\epsilon=0$ to recover the greedy algorithm from Cell 3
# - Try increasing $\epsilon$ and see the machine pulled uniformly more often,
#   at the cost of exploiting less

# %% [markdown]
# # Cell 6: Confidence Intervals for Each Arm
#
# **Goal**:
# - Introduce confidence bounds and uncertainty quantification for the
#   empirical mean of each arm
#
# _Empirical mean with CI_: bar chart of empirical mean per machine with a
# Hoeffding confidence-interval error bar; true means shown as dotted lines
# when toggled
# _CI half-width vs N_: theoretical curve of how the half-width shrinks as
# the number of pulls grows, with a marker at the current N
# _Comments_: current seed, N, confidence level, and numeric CI bounds

# %%
utils.cell6_confidence_intervals()

# %% [markdown]
# **Key observations**:
# - More pulls shrink the confidence interval: uncertainty about $\mu_i$
#   decreases as $1/\sqrt{N}$
# - A higher confidence level (e.g. 99% vs 90%) widens the interval, since it
#   must hold with higher probability
# - Toggle "Show True Means" to see whether the true mean actually falls
#   inside the interval
# - This shrinking uncertainty radius is exactly the "exploration bonus" used
#   by UCB in the next cells

# %% [markdown]
# # Cell 7: Upper Confidence Bound (UCB) Intuition
#
# **Goal**:
# - See the UCB index as empirical mean plus an exploration bonus
# - Build intuition for why UCB can prefer a machine with a lower empirical
#   mean if it has been pulled fewer times
#
# _UCB index_: stacked bar chart with empirical mean (blue) stacked with the
# exploration bonus (orange); the machine with the highest total (marked `*`)
# would be pulled next
# _Comments_: current $t$, and each machine's $N_i$, mean, bonus, and UCB
# index

# %%
utils.cell7_ucb_intuition()

# %% [markdown]
# **Key observations**:
# - UCB = empirical mean + exploration bonus; the policy always pulls the arm
#   with the highest UCB index
# - Machine 3 has the lowest empirical mean here, but its small $N_i$ gives it
#   a large bonus, which can make its UCB the highest
# - Increasing $t$ (the slider) grows every machine's bonus a little, since
#   $\log t$ grows for all arms regardless of which one is pulled
# - This is "optimism in the face of uncertainty": under-explored arms get
#   the benefit of the doubt

# %% [markdown]
# # Cell 8: UCB Algorithm Simulation
#
# **Goal**:
# - Watch UCB1 run end-to-end on 4 arms and converge to the best one
#
# _Pull timeline_: which machine was pulled at each round
# _Pull counts over time_: $N_i(t)$ for each machine as the run progresses
# _Cumulative regret_: $L_t$ over time
# _Comments_: pull counts, optimal arm, and final regret

# %%
utils.cell8_ucb_simulation()

# %% [markdown]
# **Key observations**:
# - UCB1 quickly identifies Machine 3 (the true best arm, $\mu=0.7$) and
#   pulls it most often, while occasionally revisiting the others
# - The cumulative regret curve flattens over time: its slope decreases as
#   $\log t$ grows more slowly than $t$
# - Try increasing the time horizon $T$ to see the pull counts on the
#   suboptimal arms grow much more slowly than the optimal arm's

# %% [markdown]
# # Cell 9: UCB Exploration Bonus Decay
#
# **Goal**:
# - Isolate how the UCB exploration bonus $\sqrt{2 \log(t) / N_i}$ depends on
#   $N_i$ alone
#
# _Bonus vs $N_i$_: curve of the exploration bonus as a function of the
# number of pulls, at a fixed round $t$, with a marker at the current $N_i$
# _Comments_: current $t$, $N_i$, and the resulting bonus value

# %%
utils.cell9_ucb_bonus_decay()

# %% [markdown]
# **Key observations**:
# - The bonus decays as $1/\sqrt{N_i}$: doubling the number of pulls does not
#   halve the bonus, it shrinks it by a factor of $\sqrt{2}$
# - Increasing $t$ shifts the whole curve up slightly (via $\sqrt{\log t}$),
#   but $N_i$ dominates the shape of the decay
# - More pulls of an arm mean less exploration bonus for that arm, and
#   therefore less incentive to keep exploring it

# %% [markdown]
# # Cell 10: Regret Accumulation
#
# **Goal**:
# - Visualize how per-step and cumulative regret accumulate for a chosen
#   algorithm
#
# _Per-step regret_: bar chart of instantaneous regret $\ell_t = \mu^* -
# \mu_{A_t}$ at every round, colored green when the optimal arm was chosen
# _Cumulative regret_: line plot of $L_t = \sum_{\tau \le t} \ell_\tau$
# _Comments_: algorithm, optimal-arm pull count, and final regret

# %%
utils.cell10_regret_accumulation()

# %% [markdown]
# **Key observations**:
# - Random and Greedy accumulate regret steadily at every round (bars rarely
#   turn green)
# - Epsilon-Greedy and UCB show mostly green bars once they lock onto the
#   best arm, with occasional red bars from exploration
# - Switch the algorithm dropdown to compare how differently each one's
#   cumulative regret curve bends

# %% [markdown]
# # Cell 11: Comparing Algorithms: Regret Curves
#
# **Goal**:
# - Compare the regret growth rate of Random, Greedy, Epsilon-Greedy, UCB,
#   and Thompson Sampling on the same log-t axis
#
# _Regret curves_: mean cumulative regret (averaged over a few trials) for
# each selected algorithm, log scale on the round axis
# _Comments_: final regret for each selected algorithm, with its theoretical
# growth rate

# %%
utils.cell11_regret_comparison()

# %% [markdown]
# **Key observations**:
# - Random and Greedy grow linearly in $T$ ($\Theta(T)$): their curves keep
#   climbing even on a log-t axis
# - Epsilon-Greedy (fixed $\epsilon$) also grows roughly linearly, since it
#   never stops exploring
# - UCB and Thompson Sampling flatten out on the log-t axis, consistent with
#   $O(\log T)$ regret
# - Try increasing $K$ (number of arms): all algorithms get worse, but UCB
#   and Thompson Sampling degrade much more gracefully

# %% [markdown]
# # Cell 12: Bayesian Bandits: Prior and Posterior
#
# **Goal**:
# - Introduce Bayesian inference for bandits: start from a prior belief and
#   update it with observed data
#
# _Prior vs posterior_: prior $\text{Beta}(\alpha, \beta)$ (dotted) and
# posterior $\text{Beta}(\alpha+s, \beta+f)$ (solid, shaded) probability
# density over the unknown success probability $\mu$
# _Comments_: successes $s$, failures $f$, and posterior mean/variance

# %%
utils.cell12_bayesian_prior_posterior()

# %% [markdown]
# **Key observations**:
# - Starting from a flat prior $\text{Beta}(1,1)$, each pull narrows the
#   posterior around the true (hidden) success probability
# - The posterior mean moves toward the observed success rate, while its
#   variance shrinks as more data arrives
# - Try a more concentrated prior (large $\alpha, \beta$) to see it takes
#   more pulls to move the posterior away from the prior belief

# %% [markdown]
# # Cell 13: Thompson Sampling Algorithm
#
# **Goal**:
# - See Thompson Sampling sample one $\theta_i$ from each arm's posterior and
#   pull the arm with the highest sample
#
# _Posterior curves_: one Beta posterior density per arm at the chosen round,
# with a dot at each arm's sampled $\theta_i$ (a star marks the arm that was
# actually pulled)
# _Comments_: each arm's posterior parameters, sampled value, and the round's
# selection

# %%
utils.cell13_thompson_sampling()

# %% [markdown]
# **Key observations**:
# - The selected arm is always the one whose sampled $\theta_i$ happens to be
#   highest that round, not necessarily the one with the highest posterior
#   mean
# - Early on, wide posteriors mean any arm's sample can win, so exploration is
#   automatic
# - Scrub the round slider forward to see the posteriors narrow and the
#   sampled dots cluster increasingly around the true best arm

# %% [markdown]
# # Cell 14: Thompson Sampling: Probability Matching
#
# **Goal**:
# - Verify that Thompson Sampling selects each arm with probability exactly
#   equal to the probability that arm is optimal given the data
#
# _Theoretical Pr(optimal)_: bar chart of $\Pr(i = i^* \mid \mathcal{D})$ for
# each arm, estimated with a large number of posterior draws
# _Empirical frequency_: bar chart of how often each arm wins when sampling
# 1000 more times from the same fixed posterior
# _Comments_: posterior parameters and the theoretical vs empirical numbers

# %%
utils.cell14_probability_matching()

# %% [markdown]
# **Key observations**:
# - The two bar charts closely match: this is "probability matching", the
#   defining property of Thompson Sampling
# - An arm that is rarely optimal is rarely selected, but never with exactly
#   zero probability, so it can still be revisited if new data supports it
# - Increasing the number of pulls per arm (more data) sharpens the posterior
#   toward the truly best arm, so both bar charts concentrate on one machine

# %% [markdown]
# # Cell 15: UCB vs Thompson Sampling Comparison
#
# **Goal**:
# - Compare the two order-optimal algorithms empirically on the same bandit
#   environment
#
# _Regret curves_: cumulative regret of UCB and Thompson Sampling overlaid
# _Pull counts_: grouped bar chart of pull counts per arm for each algorithm
# _Comments_: setup ($K$, $\Delta$, $T$) and each algorithm's final regret

# %%
utils.cell15_ucb_vs_thompson()

# %% [markdown]
# **Key observations**:
# - Both algorithms achieve $O(\log T)$ regret, so their cumulative regret
#   curves both flatten out over time
# - Thompson Sampling often has better constants in practice: try several
#   seeds to see it frequently (not always) end with lower final regret
# - Shrinking the gap $\Delta$ makes the arms harder to distinguish: both
#   algorithms need more pulls of the suboptimal arms before locking onto the
#   best one
