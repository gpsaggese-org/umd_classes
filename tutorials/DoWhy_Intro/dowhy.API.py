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
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # DoWhy API Overview
#
# This notebook walks through the core building blocks of DoWhy, the Python
# library for causal inference from the PyWhy ecosystem. DoWhy implements a
# four-step workflow:
#
# 1. **Model**: encode causal assumptions as a directed acyclic graph (DAG)
# 2. **Identify**: determine whether the causal effect is estimable from data
# 3. **Estimate**: compute the treatment effect using statistical methods
# 4. **Refute**: test the robustness of the estimate
#
# We use a synthetic dataset with a known true effect so every result can be
# verified against ground truth. For the theoretical background see Chapters
# 4 (Structural Causal Models), 6 (Causal Identification), 7 (Estimating
# Causal Effects), and 8 (Sensitivity Analysis) of the companion book.

# %%
# %load_ext autoreload
# %autoreload 2

import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)

# %%
import dowhy_utils as ut

ut.init_logger(_LOG)

# %% [markdown]
# ## 1. Generate Synthetic Data
#
# We create a dataset where the true average treatment effect (ATE) is exactly
# 10.0. Three confounders affect both treatment assignment and outcome. This
# lets us verify whether our causal estimates recover the true value.

# %%
# Generate a linear dataset with known causal effect.
data = ut.load_linear_dataset(
    n_samples=1000, beta=10.0, num_common_causes=3, seed=42,
)
df = data["df"]

print(f"Shape: {df.shape}")
print(f"True ATE: {data['ate']}")
display(df.head())
# The dataset has 1000 observations, a binary treatment (v0), continuous
# outcome (y), and three confounders (W0, W1, W2).

# %%
# Compare naive treated vs control means.
naive_ate = df[df["v0"] == 1]["y"].mean() - df[df["v0"] == 0]["y"].mean()

print(f"Naive ATE (biased): {naive_ate:.4f}")
print(f"True ATE: {data['ate']:.4f}")
# The naive estimate is biased because it ignores confounders.

# %% [markdown]
# ## 2. Define the Causal Graph
#
# A causal graph encodes domain knowledge about which variables cause which.
# DoWhy uses this graph to determine what statistical adjustments are needed.

# %%
# Build the causal model with the graph from the data generator.
model = ut.build_causal_model(
    df,
    treatment="v0",
    outcome="y",
    graph=data["dot_graph"],
)

print(model)
# The model contains the data, the treatment/outcome specification, and the DAG.

# %%
# Display the DAG.
ut.plot_causal_graph(model)
# Nodes represent variables. Edges represent direct causal relationships.
# Common causes (confounders) point to both treatment and outcome.

# %% [markdown]
# ## 3. Identify the Causal Effect
#
# Identification answers: can we estimate the causal effect from observational
# data given our graph? DoWhy checks whether the backdoor criterion is
# satisfied and returns an estimand -- the statistical quantity to compute.
# When the backdoor path is not identifiable, DoWhy can also attempt the
# frontdoor criterion or instrumental variable identification.

# %%
# Identify the causal effect using the backdoor criterion.
estimand = ut.identify_effect(model)

print(estimand)
# The estimand specifies which variables to condition on.

# %% [markdown]
# ## 4. Beyond Backdoor: Frontdoor and Instrumental Variables
#
# The backdoor criterion fails when an important confounder is unobserved. Two
# alternatives recover the effect under different assumptions:
#
# - **Frontdoor**: works when a fully observed mediator carries the entire
#   effect of treatment on outcome
# - **Instrumental variable**: works when a variable affects treatment but
#   reaches the outcome only through treatment
#
# DoWhy detects which criteria apply from the graph alone.

# %%
# Instrumental variable identification.
iv_data = ut.load_iv_dataset(n_samples=1000, beta=10.0, seed=42)
iv_model = ut.build_causal_model(
    iv_data["df"],
    treatment="v0",
    outcome="y",
    graph=iv_data["dot_graph"],
)
iv_estimand = ut.identify_effect(iv_model)

print(iv_estimand)
# DoWhy reports an IV estimand because the graph contains an instrument.

# %%
# Estimate the effect using the instrumental variable.
iv_estimate = ut.estimate_effect(
    iv_model,
    iv_estimand,
    method_name="iv.instrumental_variable",
)

print(f"IV estimate: {iv_estimate.value:.4f} (true ATE: {iv_data['ate']:.4f})")
# The IV estimator recovers the true effect without conditioning on confounders.

# %%
# Frontdoor identification.
fd_data = ut.load_frontdoor_dataset(n_samples=1000, beta=10.0, seed=42)
fd_model = ut.build_causal_model(
    fd_data["df"],
    treatment="v0",
    outcome="y",
    graph=fd_data["dot_graph"],
)
fd_estimand = ut.identify_effect(fd_model)

print(fd_estimand)
# DoWhy reports a frontdoor estimand when a mediator covers the full path.

# %% [markdown]
# ## 5. Estimate the Effect
#
# With an identified estimand, we apply different statistical methods to
# estimate the causal effect. Comparing methods with different assumptions
# is a useful sanity check.

# %%
# Estimate using propensity score matching.
estimate_psm = ut.estimate_effect(
    model,
    estimand,
    method_name="backdoor.propensity_score_matching",
)

print(f"Propensity score matching: {estimate_psm.value:.4f}")
# Matches treated and control units with similar propensity scores.

# %%
# Estimate using linear regression.
estimate_lr = ut.estimate_effect(
    model,
    estimand,
    method_name="backdoor.linear_regression",
)

print(f"Linear regression: {estimate_lr.value:.4f}")
# Controls for confounders by including them as covariates.

# %%
# Estimate using inverse propensity weighting.
estimate_ipw = ut.estimate_effect(
    model,
    estimand,
    method_name="backdoor.propensity_score_weighting",
)

print(f"Inverse propensity weighting: {estimate_ipw.value:.4f}")
# Reweights observations to create a pseudo-population where treatment
# is independent of confounders.

# %%
# Compare all estimators side by side.
results = ut.compare_estimators(model, estimand)

display(results)
# All estimates should be close to the true ATE of 10.0.

# %%
# Visualize the comparison.
ut.plot_estimate_comparison(results)
# Agreement across methods strengthens confidence in the result.

# %% [markdown]
# ## 6. Refute the Estimate
#
# Refutation tests check robustness. Each test perturbs the data or model
# in a specific way. If the estimate changes drastically, the original result
# may not be reliable.

# %%
# Refutation 1: Add a random common cause.
# Adds a random variable as an extra confounder. If the estimate changes
# significantly, the model may be sensitive to unobserved confounders.
ref_random = ut.run_refutation(
    model, estimand, estimate_lr, method_name="random_common_cause",
)

print(ref_random)
# The estimate should remain close to the original value.

# %%
# Refutation 2: Placebo treatment.
# Replaces the real treatment with random noise. The estimated effect should
# drop to approximately zero if the original estimate was genuine.
ref_placebo = ut.run_refutation(
    model, estimand, estimate_lr, method_name="placebo_treatment_refuter",
)

print(ref_placebo)
# An effect near zero confirms the original treatment was driving the result.

# %%
# Refutation 3: Data subset.
# Re-estimates on a random subset of the data. A stable estimate across
# subsets indicates robustness.
ref_subset = ut.run_refutation(
    model, estimand, estimate_lr, method_name="data_subset_refuter",
)

print(ref_subset)
# Stability across subsets confirms the result is not driven by outliers.

# %% [markdown]
# ## Summary
#
# This notebook covered the four-step DoWhy workflow on synthetic data:
#
# 1. **Model**: defined a causal graph encoding confounder relationships
# 2. **Identify**: applied the backdoor criterion to obtain an estimand, then
#    showed that DoWhy also detects frontdoor and instrumental variable
#    estimands when the graph supports them
# 3. **Estimate**: compared propensity score matching, linear regression, and
#    IPW, all recovering estimates close to the true ATE of 10.0
# 4. **Refute**: ran three refutation tests confirming robustness
#
# The next notebook (`dowhy.example.ipynb`) applies this workflow to the
# Lalonde job training dataset, a real-world causal inference benchmark.
