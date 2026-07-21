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
# # DoWhy: Causal Analysis of the Lalonde Job Training Program
#
# The Lalonde dataset is a canonical benchmark in causal inference. It comes
# from a 1986 study evaluating the National Supported Work (NSW) program, a
# job training intervention for disadvantaged workers. The key question:
# did the training program increase participants' earnings?
#
# A naive comparison of earnings between treated and control groups is biased
# because program participants differ systematically from non-participants in
# age, education, race, and prior earnings. This notebook applies DoWhy's
# four-step workflow to estimate the causal effect while controlling for these
# confounders.

# %%
# %load_ext autoreload
# %autoreload 2

import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)

# %%
import dowhy_utils as ut

ut.init_logger(_LOG)

# %% [markdown]
# ## Part 1: Load and Explore the Data

# %%
# Load the Lalonde dataset.
df = ut.load_lalonde_dataset()

print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
display(df.head())
# Each row is one individual with demographic covariates, treatment indicator,
# and post-program earnings (re78).

# %%
# Check treatment group sizes.
treatment_col = "treat"
outcome_col = "re78"

print(df[treatment_col].value_counts())
# Fewer treated than control units, typical of observational studies.

# %%
# Compare outcome distributions between groups.
treated = df[df[treatment_col] == 1][outcome_col]
control = df[df[treatment_col] == 0][outcome_col]

print(f"Treated mean earnings: ${treated.mean():,.2f}")
print(f"Control mean earnings: ${control.mean():,.2f}")
print(f"Naive difference: ${treated.mean() - control.mean():,.2f}")
# This naive difference is biased by confounders.

# %%
# Visualize the selection bias.
_, axes = plt.subplots(1, 2, figsize=(12, 4))
# Outcome distribution by treatment group.
for label, group in df.groupby(treatment_col):
    axes[0].hist(group[outcome_col], bins=30, alpha=0.5, label=f"T={label}")
axes[0].set_xlabel("Earnings (re78)")
axes[0].set_ylabel("Count")
axes[0].set_title("Outcome Distribution by Treatment")
axes[0].legend()
# Age distribution by treatment group.
for label, group in df.groupby(treatment_col):
    axes[1].hist(group["age"], bins=20, alpha=0.5, label=f"T={label}")
axes[1].set_xlabel("Age")
axes[1].set_ylabel("Count")
axes[1].set_title("Age Distribution by Treatment (Selection Bias)")
axes[1].legend()
plt.tight_layout()
plt.show()
# Covariate distributions differ between groups, confirming selection bias.

# %% [markdown]
# ## Part 2: Define the Causal Model
#
# We encode domain knowledge as a DAG. The confounders (age, education, race,
# marital status, prior earnings) affect both the likelihood of receiving
# training and the post-program earnings.

# %%
# Identify confounder columns.
confounders = [c for c in df.columns if c not in [treatment_col, outcome_col]]

print(f"Confounders: {confounders}")
# These are the variables we need to condition on.

# %%
# Build the causal model.
model = ut.build_causal_model(
    df,
    treatment=treatment_col,
    outcome=outcome_col,
    common_causes=confounders,
)

print(model)
# The model encodes our causal assumptions.

# %%
# Display the causal graph.
ut.plot_causal_graph(model)
# All confounders point to both treatment and outcome.

# %% [markdown]
# ## Part 3: Identify the Causal Effect
#
# DoWhy checks whether the causal effect is identifiable given the graph. The
# backdoor criterion requires conditioning on all common causes of treatment
# and outcome.

# %%
# Identify the estimand.
estimand = ut.identify_effect(model)

print(estimand)
# The estimand specifies which variables to condition on.

# %% [markdown]
# ## Part 4: Estimate and Compare
#
# We run three estimators and compare results. Agreement across methods with
# different assumptions increases confidence in the result.

# %%
# Compare three estimation methods.
results = ut.compare_estimators(model, estimand)

display(results)
# Each row shows a method and its estimated treatment effect.

# %%
# Visualize the comparison.
ut.plot_estimate_comparison(results)
# Agreement across estimators strengthens confidence.

# %%
# Use linear regression as our primary estimate for refutation.
estimate = ut.estimate_effect(
    model,
    estimand,
    method_name="backdoor.linear_regression",
)

print(f"Primary estimate (linear regression): {estimate.value:.2f}")
# This is the estimate we will subject to refutation tests.

# %% [markdown]
# ## Part 5: Refutation Suite
#
# We run all three standard refutation tests. A reliable estimate should
# survive all of them.

# %%
# Run all refutation tests.
refutations = ut.run_all_refutations(model, estimand, estimate)

for name, ref in refutations.items():
    print(f"\n{'=' * 60}")
    print(f"Refutation: {name}")
    print(f"{'=' * 60}")
    print(ref)
# Random common cause: estimate should not change with a random confounder.
# Placebo treatment: replacing treatment with noise should give effect near 0.
# Data subset: re-estimating on a subset should give a similar result.

# %% [markdown]
# ## Part 6: Sensitivity Analysis
#
# Even when refutation tests pass, the estimate could still be biased by
# unmeasured confounders. Sensitivity analysis asks: how strong would an
# unobserved confounder need to be to change our conclusion?

# %%
# Test robustness to unobserved confounding.
ref_sensitivity = ut.run_refutation(
    model,
    estimand,
    estimate,
    method_name="add_unobserved_common_cause",
    confounders_effect_on_treatment="binary_flip",
    confounders_effect_on_outcome="linear",
    effect_strength_on_treatment=0.01,
    effect_strength_on_outcome=0.02,
)

print(ref_sensitivity)
# A small effect strength that changes the estimate substantially indicates
# fragility. A large effect strength needed to nullify the result indicates
# robustness.

# %% [markdown]
# ## Part 7: Counterfactual Outcomes
#
# Counterfactual queries ask: what would have happened to a specific individual
# under a different treatment? This moves from population-level effects (ATE)
# to individual-level reasoning. Two approaches follow: a simple linear
# approximation that applies the estimated ATE uniformly, and Part 7b's fully
# fitted structural causal model that conditions on each individual's
# covariates.

# %%
# Select a few individuals for counterfactual analysis.
sample = df.head(5).copy()

print("Observed data:")
display(sample[[treatment_col, outcome_col] + confounders[:3]])
# These are the actual observations we will reason about.

# %%
# Compute approximate counterfactual outcomes using the estimated ATE.
cf_results = ut.compute_counterfactual(
    sample,
    treatment_col,
    outcome_col,
    estimate,
    treatment_value=1.0,
    control_value=0.0,
)

print("Counterfactual outcomes:")
display(cf_results)
# Each row shows the observed outcome and the approximate counterfactual
# obtained by applying the ATE.

# %% [markdown]
# ### Part 7b: Counterfactuals From a Fitted Structural Causal Model
#
# The ATE-based approximation above assumes the treatment effect is the same
# for every individual. In reality, effects vary with covariates. DoWhy's `gcm`
# module fits a structural causal model and computes per-observation
# counterfactuals that depend on each individual's confounders. The trade-off
# is fitting cost: gcm trains a regression for every node in the graph.

# %%
# Compute SCM counterfactuals on a small subset to keep fitting time short.
scm_cf = ut.compute_scm_counterfactual(
    df,
    treatment_col,
    outcome_col,
    confounders,
    n_samples=200,
)

print("SCM counterfactual outcomes:")
display(scm_cf.head())
# Counterfactuals differ across individuals because the fitted mechanisms
# condition on each row's confounders.

# %%
# Compare the two counterfactual approaches on the same five individuals.
comparison = sample[[treatment_col, outcome_col]].copy()
comparison["ate_counterfactual"] = cf_results["counterfactual_outcome"].values
comparison["scm_counterfactual"] = scm_cf.head(5)["counterfactual_outcome"].values

display(comparison)
# The ATE column applies a constant shift; the SCM column varies with each
# individual's covariates.

# %% [markdown]
# ## Part 8: Connections to the Book
#
# The "Causal AI and Decision Making" book assigns DoWhy as the headline
# tutorial for the following chapters; each section above is the practical
# expression of that material:
#
# - **Chapter 1 (The Limits of Prediction)**: the Lalonde analysis is an
#   end-to-end example of causal reasoning from observational data, the kind
#   of question prediction models cannot answer
# - **Chapter 3 (Causality vs. Correlation)**: the naive difference in means
#   in Part 1 contrasted with the causal estimators in Part 4 illustrates how
#   correlation alone misleads under selection bias
# - **Chapter 5 (Counterfactual Reasoning)**: Part 7 computes individual-level
#   counterfactuals, both as an ATE-based approximation and via a fitted
#   structural causal model in Part 7b
# - **Chapter 6 (Causal Identification)**: `identify_effect` applies the
#   backdoor criterion here; the API notebook also demonstrates frontdoor and
#   instrumental variable identification
# - **Chapter 8 (Sensitivity Analysis and Causal Model Validation)**: Parts 5
#   and 6 run the refutation suite and the unobserved-confounding sensitivity
#   test
#
# The book delegates causal fairness (Ch 13), causal explainability (Ch 15),
# and treatment policy optimization (Ch 19) to dedicated tutorials (AI Fairness
# 360, DiCE, EconML), so this tutorial does not cover them.

# %% [markdown]
# ## Summary
#
# This notebook applied DoWhy's four-step workflow to the Lalonde dataset:
#
# 1. Loaded observational data and identified selection bias
# 2. Defined a causal graph encoding confounder relationships
# 3. Identified the estimand via the backdoor criterion
# 4. Compared three estimators (propensity score, linear regression, IPW)
# 5. Ran refutation tests confirming estimate robustness
# 6. Tested sensitivity to unobserved confounding
# 7. Computed individual counterfactual outcomes both as an ATE-based
#    approximation and via a fitted structural causal model
#
# The estimated treatment effect of the job training program on earnings is
# consistent across methods and survives refutation tests.
