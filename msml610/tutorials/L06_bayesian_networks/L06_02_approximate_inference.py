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
# # Approximate Inference in Bayesian Networks
#
# - This notebook teaches how to estimate posteriors $P(X \mid \mathbf{e})$ by
#   sampling, when exact inference is too expensive or impossible
# - Concepts are built on the Garden Wold examples with variables
#   to run the query $P(Rain \mid Sprinkler{=}T)$
# - The flow is:
#   - Turn uniform randomness into samples (inverse transform)
#   - Sample a whole network (prior sampling)
#   - Watch estimates converge ($1/\sqrt{N}$)
#   - Condition on evidence by rejection
#   - Rescue rare evidence with importance weights
#   - Walk the state space with MCMC (mixing, Gibbs, Metropolis-Hastings)
# - The exact posteriors from `pgmpy` are reused throughout as the ground-truth
#   reference that every estimate is compared against

# %% [markdown]
# # Approximate Inference

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

# %%
# Use this for most notebooks.
import helpers.htutorial as htutori

import L06_02_approximate_inference_utils as utils

htutori.config_notebook()

# Initialize logger.
_LOG = logging.getLogger(__name__)
utils.init_loggers(_LOG)

# Convert `display` into `print()` when running outside IPython.
try:
    from IPython.display import display
except ImportError:
    display = print  # type: ignore

# %% [markdown]
# # Part 1: From Randomness to Samples

# %% [markdown]
# ## Cell 1.1: Turning Uniform Randomness into Any Distribution
#
# **Goal**:
# - Show that a single stream of uniform numbers $r \in [0,1]$ becomes samples
#   from any distribution via the inverse CDF
#
# **Plots**:
# - _Target distribution_: a discrete biased die or a continuous exponential
# - _CDF and inverse map_: the CDF $F(x)$ with a sampled $r$ mapped to its
#   $x = F^{-1}(r)$
# - _Sample histogram_: $N$ generated samples (solid) vs the target (dotted)
# - _Comments_: the construction and the achieved accuracy
#
# **Parameters**:
# - `Target`: biased die (discrete) vs exponential (continuous)
# - `lambda` ($\lambda$): rate of the exponential
# - `N` ($N$): number of samples drawn
# - `seed`: random seed
#
# **Key observations**:
# - Every sampler ultimately consumes uniform numbers; the CDF is the adapter
# - For discrete targets find the smallest $x$ with $F(x) > r$; for the
#   exponential invert in closed form, $x = -\frac{1}{\lambda}\ln(1-r)$
# - Larger $N$ fills the histogram in toward the target

# %%
# TODO(ai_gp): Split this into two cells one for discrete die and the other for the exponentials. Also update the markdown above.
# Reuse the code as much as possible.

# Map a uniform r through the CDF into a sample from the chosen target.
utils.cell1_1_inverse_transform_widget()

# %% [markdown]
# - One trick underlies everything: stretch a flat $[0,1]$ number through the
#   CDF and it comes out distributed like the target
# - Sampling a network is just doing this many times in the right order
# - When $F^{-1}$ has no closed form the same idea works with numerical inversion

# %% [markdown]
# ## Cell 1.2: Prior Sampling from the Sprinkler Network
#
# **Goal**:
# - Scale the single-variable trick up to a whole Bayesian network
# - Sample variables in topological order to generate full events with no
#   evidence
# - Compare estimated frequencies with the exact joint
#
# **Plots**:
# - _DAG_: the sprinkler network, colored by topological depth
# - _Marginal_: estimated $P(\cdot)$ of a tracked variable vs its exact value
# - _Joint frequencies_: estimated joint over all 16 configurations vs exact
# - _Comments_: the sampling order and the achieved errors
#
# **Parameters**:
# - `N` ($N$): number of full events to generate
# - `Track marginal`: variable whose marginal estimate is tracked
# - `seed`: random seed
#
# **Key observations**:
# - Topological order guarantees every parent has a value before its child
# - Prior sampling realizes the factorization
#   $\prod_i \Pr(x_i \mid parents(X_i))$
# - The relative frequency of an event approximates its joint probability

# %%
# Generate N complete worlds in topological order and compare with the exact joint.
utils.cell1_2_prior_sampling_widget()

# %% [markdown]
# - Prior sampling is inverse-transform sampling, once per node, parents first
# - The fraction of samples equal to an event estimates that event's joint
#   probability
# - With more samples both the marginal and the joint estimates sharpen

# %% [markdown]
# ## Cell 1.3: Consistency and the 1/sqrt(N) Convergence Rate
#
# **Goal**:
# - Make convergence tangible and show estimates are consistent
# - Show that error shrinks like $1/\sqrt{N}$, setting expectations for every
#   later sampler
#
# **Plots**:
# - _One estimate_: a single running estimate converging to the exact value
# - _Independent chains_: a fan of chains (different seeds) narrowing with $N$
# - _Error vs N_: absolute error on log-log axes with a $-1/2$ reference slope
# - _Comments_: the exact value and the final error
#
# **Parameters**:
# - `max N` ($N$): largest sample count shown
# - `reps`: number of independent chains in the fan
# - `Estimate`: which marginal event is being estimated
# - `seed`: random seed
#
# **Key observations**:
# - Estimates are consistent: $N_{PS}(x)/N \to \Pr(x)$
# - A slope of $-1/2$ on log-log axes is the signature of Monte Carlo
# - Accuracy is expensive, which motivates smarter samplers

# %%
# Show one estimate, many estimates, and the 1/sqrt(N) error rate.
utils.cell1_3_convergence_widget()

# %% [markdown]
# - Sampling is consistent but slow to sharpen
# - The $1/\sqrt{N}$ law is unavoidable for plain Monte Carlo
# - This is why the rest of the notebook focuses on using each sample better

# %% [markdown]
# # Part 2: Conditioning on Evidence

# %% [markdown]
# ## Cell 2.1: Rejection Sampling
#
# **Goal**:
# - Introduce the simplest way to condition on evidence
# - Generate prior samples and throw away those that disagree with the evidence
# - Expose the central weakness when evidence is rare
#
# **Plots**:
# - _Sample stream_: dots colored by kept (matches evidence) vs rejected
# - _Retained fraction_: counts of generated, rejected, and kept samples
# - _Posterior estimate_: $P(X \mid \mathbf{e})$ vs the exact reference
# - _Comments_: the retained fraction and the estimate
#
# **Parameters**:
# - `N` ($N$): total prior samples generated
# - `Query X`: the query variable
# - `observe <node>`: evidence selection and value
# - `seed`: random seed
#
# **Key observations**:
# - Rejection sampling is consistent: kept samples are distributed as
#   $P(X \mid \mathbf{e})$
# - The retained fraction equals $\Pr(\mathbf{e})$
# - The effective sample size, not $N$, controls accuracy

# %%
# Keep only the prior samples that agree with the evidence.
utils.cell2_1_rejection_sampling_widget()

# %% [markdown]
# - Correct but wasteful: only samples that already agree with the evidence are
#   kept
# - The rarer the evidence, the more samples are burned to learn anything
# - This motivates keeping every sample and correcting with weights

# %% [markdown]
# ## Cell 2.2: Importance Sampling and Likelihood Weighting
#
# **Goal**:
# - Fix rejection's waste by keeping every sample and correcting with weights
# - Show likelihood weighting as the Bayesian-network instance of the idea
# - Watch for weight collapse via the effective sample size
#
# **Plots**:
# - _Weighted samples_: dots sized by importance weight $w = \Pr(X)/Q(X)$
# - _Weight distribution_: histogram of weights, flagging collapse
# - _Posterior estimate_: weighted estimate vs exact and vs rejection
# - _Comments_: the effective sample size and the estimates
#
# **Parameters**:
# - `N` ($N$): number of weighted samples
# - `Query X`: the query variable
# - `observe <node>`: evidence selection and value
# - `seed`: random seed
#
# **Key observations**:
# - Drawing from an easier $Q$ and weighting by $w=\Pr(X)/Q(X)$ stays unbiased
# - Every sample is kept, so no work is discarded
# - Very uneven weights shrink the effective sample size despite a large $N$

# %%
# Keep every sample and correct the bias with importance weights.
utils.cell2_2_likelihood_weighting_widget()

# %% [markdown]
# - Reweight instead of reject: importance sampling spends every sample
# - It focuses effort where the evidence lives
# - It only helps if the weights stay reasonably balanced

# %% [markdown]
# # Part 3: Markov Chain Monte Carlo

# %% [markdown]
# ## Cell 3.1: Markov Chains and the Stationary Distribution
#
# **Goal**:
# - Introduce the core MCMC idea, a designed random walk over states
# - Show its long-run distribution settles to a fixed stationary shape
# - Show the limit is independent of where the walk starts
#
# **Plots**:
# - _Transition diagram_: states as nodes with the current state highlighted
# - _State distribution_: $\pi_t$ (solid) settling onto the stationary (dotted)
# - _Convergence_: total-variation distance to stationary decaying with $t$
# - _Comments_: the stationary distribution and current distance
#
# **Parameters**:
# - `t`: number of steps taken
# - `Initial state`: where the walk starts
# - `seed`: random seed
#
# **Key observations**:
# - A Markov chain is memoryless: the next state depends only on the current one
# - Under ergodicity and aperiodicity $\pi_t$ converges to a unique stationary
#   distribution
# - MCMC builds a chain whose stationary distribution is the posterior

# %%
# Step the chain and watch the state distribution converge to a fixed shape.
utils.cell3_1_markov_chain_widget()

# %% [markdown]
# - The magic link: design the walk so the posterior is its equilibrium
# - Then just walk and count where the chain lands
# - Convergence happens regardless of the starting state

# %% [markdown]
# ## Cell 3.2: Mixing and Burn-in
#
# **Goal**:
# - Show that a correct stationary distribution is not enough
# - Show that mixing speed determines whether finite-sample estimates are
#   trustworthy
# - Introduce burn-in as discarding the chain's wandering start
#
# **Plots**:
# - _Trace_: the sampled value over iterations with the burn-in region shaded
# - _Collected samples_: histogram vs the true bimodal posterior
# - _Autocorrelation_: autocorrelation vs lag, high for poor mixing
# - _Comments_: the mixing diagnostics
#
# **Parameters**:
# - `step`: proposal step size controlling mixing quality
# - `burnin`: number of initial samples discarded
# - `N` ($N$): total iterations
# - `seed`: random seed
#
# **Key observations**:
# - Good mixing moves between modes often with low correlation
# - Early samples reflect the arbitrary start and are discarded as burn-in
# - Poor mixing gives biased, high-variance estimates even with a correct target

# %%
# Tune the step size between poor and good mixing and set the burn-in.
utils.cell3_2_mixing_burnin_widget()

# %% [markdown]
# - Right target, wrong speed: a chain can be correct in the limit yet useless
# - Watch the trace and the autocorrelation, not just the final histogram
# - Small steps stay stuck in one mode; large steps explore both

# %% [markdown]
# ## Cell 3.3: Gibbs Sampling and the Markov Blanket
#
# **Goal**:
# - Specialize MCMC to Bayesian networks with Gibbs sampling
# - Resample one variable at a time from its Markov blanket
# - Hold evidence clamped so every sample is consistent with it
#
# **Plots**:
# - _DAG_: evidence frozen, the resampled variable and its blanket highlighted
# - _Full conditional_: $P(X_i \mid \text{MB}(X_i))$ being sampled from
# - _Running estimate_: $P(Rain \mid \mathbf{e})$ vs the exact reference
# - _Comments_: the hidden variables and the estimate
#
# **Parameters**:
# - `sweeps`: number of Gibbs sweeps
# - `burnin`: burn-in sweeps discarded
# - `Query X` and `observe <node>`: query and evidence
# - `seed`: random seed
#
# **Key observations**:
# - Gibbs only needs the local conditional $P(X_i \mid \text{MB}(X_i))$
# - Evidence variables stay clamped, so no rejection is needed
# - It is simple and local but mixes slowly under strong correlations

# %%
# Resample each hidden variable from its Markov blanket with evidence clamped.
utils.cell3_3_gibbs_sampling_widget()

# %% [markdown]
# - Gibbs sampling is MCMC made local: resample one variable from its blanket
# - Easy to code and scales to large graphs via local updates
# - Watch out for slow mixing under strong correlations

# %% [markdown]
# ## Cell 3.4: Metropolis-Hastings and Accept/Reject Moves
#
# **Goal**:
# - Generalize beyond Gibbs to Metropolis-Hastings
# - Correct an arbitrary proposal with an acceptance probability
# - Unify proposing, accepting, and exploring
#
# **Plots**:
# - _Last proposed move_: current vs proposed state with acceptance probability
# - _Trace_: accepted states over iterations with the acceptance rate
# - _Running estimate_: $P(Rain \mid Sprinkler{=}T)$ vs the exact reference
# - _Comments_: the proposal mix, acceptance rate, and estimate
#
# **Parameters**:
# - `p_local`: probability of a local single-variable move vs a broad jump
# - `iters`: number of iterations
# - `burnin`: burn-in iterations discarded
# - `seed`: random seed
#
# **Key observations**:
# - Metropolis-Hastings sometimes accepts downhill moves, escaping local modes
# - The acceptance ratio guarantees the posterior is the stationary distribution
# - Gibbs sampling is the special case where every proposal is accepted

# %%
# Propose a move, then accept or reject it by the Hastings ratio.
utils.cell3_4_metropolis_hastings_widget()

# %% [markdown]
# - Propose anything, then correct with the Hastings ratio
# - Flexibility is the prize and the cost: any proposal is valid, but a bad one
#   mixes slowly
# - Gibbs is just the case where you always accept
