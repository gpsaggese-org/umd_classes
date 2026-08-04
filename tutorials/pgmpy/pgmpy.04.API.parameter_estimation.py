# ---
# jupyter:
#   jupytext:
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
# # PGMPy Parameter Estimation API
#
# A guided exploration of pgmpy's parameter estimation subsystem:
# - `DiscreteMLE`: Estimate CPDs using Maximum Likelihood Estimation (counting)
# - `DiscreteBayesianEstimator`: Estimate CPDs using Bayesian priors (Dirichlet smoothing)
# - `DiscreteEM`: Estimate CPDs with latent variables via Expectation Maximization
# - `model.fit()`: Convenience method wrapping estimator.fit()
#
# This module converts a graph structure + observational data into learned
# Conditional Probability Distributions (CPDs) ready for inference.

# %% [markdown]
# ## Imports and Setup

# %%
# %load_ext autoreload
# %autoreload 2

import logging
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# %%
# Use this for most notebooks.
import helpers.htutorial as htutori

htutori.config_notebook()


# Import pgmpy utilities.
import tutorials.pgmpy.pgmpy_utils as tpgpguti

# Initialize logger.
logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)

# Convert `display` into `print()` when running outside IPython.
try:
    from IPython.display import display
except ImportError:
    display = print  # type: ignore

# %%
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.parameter_estimator import (
    DiscreteMLE,
    DiscreteBayesianEstimator,
    DiscreteEM,
)

# %%
logging.getLogger("httpx").setLevel(logging.WARNING)

# %% [markdown]
# # Part 1: Library Overview
#
# ## What problem does parameter estimation solve?
#
# - Given a graph structure (nodes + edges) and observational data, estimate the
#   Conditional Probability Distributions (CPDs) for each node
# - Without estimated parameters, a Bayesian network is just a skeleton:
#   you cannot run inference, query probabilities, or simulate data
# - Three estimation strategies exist, suited to different data scenarios
#
# ## Key abstractions
#
# - **Estimator classes**: Each implements `fit(model, data)` which computes
#   CPDs and stores them in `parameters_` (a list of `TabularCPD`)
#   - `DiscreteMLE`: Simple counting -- best with abundant data
#   - `DiscreteBayesianEstimator`: Adds Dirichlet priors -- good for sparse data
#   - `DiscreteEM`: Handles latent variables or missing data
# - **Model.fit()**: Convenience wrapper that calls an estimator and adds CPDs
# - **TabularCPD**: The output -- a conditional probability table for one variable
#
# ## How the pieces fit together
#
# ```
# Structure (edges)  +  Data (pd.DataFrame)
#          |                   |
#          v                   v
#      DiscreteBayesianNetwork
#              |
#              v
#      estimator.fit(model, data)
#              |
#              v
#      estimator.parameters_  ->  List[TabularCPD]
#              |
#              v
#      model.add_cpds(*cpds)  ->  Ready for inference
# ```

# %% [markdown]
# # Part 2: Primitive-by-Primitive Exploration
#
# First, let's create a tiny graph and dataset that we will reuse throughout
# the notebook:
#
# - The "Student Exam" network: `Difficulty` -> `Grade`, `Intelligence` -> `Grade`
# - A root node `Intelligence` (2 states) and another root `Difficulty` (3 states)
# - `Grade` depends on both (2 x 3 = 6 parent combinations, 3 grade states)
# - We simulate a small dataset with 20 samples

# %%
# Build a tiny 3-node graph: Difficulty -> Grade <- Intelligence.
student_model = DiscreteBayesianNetwork(
    [("Difficulty", "Grade"), ("Intelligence", "Grade")]
)

# Show the structure.
print(f"Nodes: {sorted(student_model.nodes())}")
print(f"Edges: {sorted(student_model.edges())}")

# %%
# Create a tiny synthetic dataset.
# Difficulty: 0=easy, 1=medium, 2=hard
# Intelligence: 0=low, 1=high
# Grade: 0=F, 1=C, 2=A
rng = np.random.default_rng(42)
n_samples = 20

data = pd.DataFrame(
    {
        "Difficulty": rng.integers(0, 3, size=n_samples),
        "Intelligence": rng.integers(0, 2, size=n_samples),
    }
)
# Grade depends on Difficulty and Intelligence.
# High intelligence + easy difficulty -> higher grades.
data["Grade"] = 0
mask_high = (data["Intelligence"] == 1) & (data["Difficulty"] == 0)
data.loc[mask_high, "Grade"] = rng.integers(1, 3, size=mask_high.sum())
mask_mid = (data["Intelligence"] == 1) & (data["Difficulty"] == 1)
data.loc[mask_mid, "Grade"] = rng.integers(0, 2, size=mask_mid.sum())

print(f"Dataset shape: {data.shape}")
display(data.head(10))

# %% [markdown]
# ## Primitive 1: `DiscreteMLE`: Maximum Likelihood Estimation
#
# **Mental model**: The simplest estimator. It counts how often each state
# configuration appears in the data and normalizes to get probabilities.
# Equivalent to computing P(X | parents) = count(X, parents) / count(parents).
#
# - Fast and interpretable
# - Can produce zero probabilities for unseen parent configurations
# - Best with abundant data relative to the number of parent combinations

# %%
# Smallest construction: create and fit a DiscreteMLE estimator.
estimator_mle = DiscreteMLE()
estimator_mle.fit(student_model, data)

# The fitted parameters are stored in `parameters_`.
print(f"Type of parameters_: {type(estimator_mle.parameters_)}")
print(f"Number of CPDs: {len(estimator_mle.parameters_)}")

# %%
# Inspect the fitted parameters.
for cpd in estimator_mle.parameters_:
    print(f"\nVariable: {cpd.variable}")
    print(f"  Cardinality: {cpd.variable_card}")
    print(f"  Parents: {cpd.variables[1:]}")
    print(cpd)

# %%
# Inspect the estimator's internal state.
print("State names learned from data:")
for var, states in estimator_mle.state_names_.items():
    print(f"  {var}: {states}")

# %%
# Inspect the parameters_ list: each is a TabularCPD.
for cpd in estimator_mle.parameters_:
    print(f"\n{cpd.variable}:")
    print(f"  Evidence (parents): {cpd.variables[1:]}")
    print(f"  Values shape: {cpd.values.shape}")
    print(f"  Values:\n{cpd.values}")

# %% [markdown]
# ### Inspect the MLE CPDs in Detail
#
# The CPD for a root node (e.g., `Difficulty`) is just the empirical marginal:
# P(Difficulty=0) = count(0) / N
#
# The CPD for a child (e.g., `Grade`) is a conditional table:
# P(Grade | Difficulty, Intelligence)

# %%
# Display the Grade CPD as a DataFrame for clarity.
cpd_grade = estimator_mle.parameters_[0]
print(f"Variable: {cpd_grade.variable}")
print(f"Parents: {cpd_grade.variables[1:]}")
print("\nCPD values (Grade x [Difficulty, Intelligence] combinations):")
print(cpd_grade.get_values())

# %%
# Use the utility to display CPD as a DataFrame.
cpd_grade_df = tpgpguti.factor_to_dataframe(cpd_grade)
display(cpd_grade_df)

# %% [markdown]
# ### Important Methods: `state_counts()`
#
# The base `ParameterEstimator` provides `state_counts()` which shows raw
# counts before normalization.

# %%
# Access state counts via the base class.
# Note: the new API stores counts internally; we can inspect the raw data.
print("Raw value counts for each variable:")
for var in student_model.nodes():
    print(f"\n  {var}:")
    print(data[var].value_counts().to_string())

# %% [markdown]
# ### Explore: What happens with sparse data?
#
# When some parent configurations have zero observations, MLE assigns
# them probability 0. This can be problematic.

# %%
# Create tiny data with missing parent configurations.
tiny_data = pd.DataFrame(
    {
        "Difficulty": [0, 0, 0],
        "Intelligence": [0, 0, 0],
        "Grade": [0, 1, 2],
    }
)

estimator_tiny = DiscreteMLE()
estimator_tiny.fit(student_model, tiny_data)
print("CPDs with tiny data (only Difficulty=0, Intelligence=0 observed):")
for cpd in estimator_tiny.parameters_:
    print(f"\n{cpd.variable}:")
    print(cpd)

# %% [markdown]
# ## Primitive 2: `DiscreteBayesianEstimator`: Bayesian Estimation
#
# **Mental model**: Adds Dirichlet priors (pseudo-counts) to smooth the
# estimated distributions. When data is sparse, the prior ensures no
# parent configuration gets a zero probability.
#
# Three prior types:
# - `"BDeu"` (default): Uniform Dirichlet prior with `equivalent_sample_size`
#   controlling the prior strength. Pseudo-counts are distributed uniformly
#   across all parent configurations.
# - `"K2"`: Dirichlet prior with all pseudo-counts = 1 (uniform)
# - `"dirichlet"`: Custom pseudo-counts per variable

# %%
# Smallest construction: fit with BDeu prior (default).
estimator_bayes = DiscreteBayesianEstimator(
    prior_type="BDeu",
    equivalent_sample_size=5,
)
estimator_bayes.fit(student_model, data)

print(f"Number of CPDs: {len(estimator_bayes.parameters_)}")
for cpd in estimator_bayes.parameters_:
    print(f"\n{cpd.variable}:")
    print(cpd)

# %%
# Compare MLE vs Bayesian CPDs side by side for root nodes.
# For root nodes (no parents), the CPD is a simple 1-D probability vector.
# For conditional CPDs (like Grade), we compare them separately.
for var in ["Difficulty", "Intelligence"]:
    cpd_mle = [c for c in estimator_mle.parameters_ if c.variable == var][0]
    cpd_bayes = [c for c in estimator_bayes.parameters_ if c.variable == var][0]
    comp_df = pd.DataFrame(
        {
            "State": list(range(cpd_mle.variable_card)),
            "MLE": cpd_mle.get_values().flatten(),
            "Bayesian (BDeu)": cpd_bayes.get_values().flatten(),
        }
    )
    print(f"\n{var}:")
    display(comp_df)

# %% [markdown]
# ### Experiment: Varying `equivalent_sample_size`
#
# Larger equivalent sample size = stronger prior = more uniform estimates.

# %%
# Fit with different equivalent sample sizes.
for ess in [1, 5, 50]:
    est = DiscreteBayesianEstimator(
        prior_type="BDeu", equivalent_sample_size=ess
    )
    est.fit(student_model, data)
    cpd = [c for c in est.parameters_ if c.variable == "Difficulty"][0]
    print(f"ESS={ess}: P(Difficulty) = {cpd.get_values().flatten().round(3)}")

# %% [markdown]
# ### Experiment: K2 Prior (all pseudo-counts = 1)

# %%
# K2 prior: every pseudo-count = 1.
estimator_k2 = DiscreteBayesianEstimator(prior_type="K2")
estimator_k2.fit(student_model, data)

cpd_diff_k2 = [
    c for c in estimator_k2.parameters_ if c.variable == "Difficulty"
][0]
cpd_diff_mle = [
    c for c in estimator_mle.parameters_ if c.variable == "Difficulty"
][0]
print(
    f"MLE:      P(Difficulty) = {cpd_diff_mle.get_values().flatten().round(3)}"
)
print(f"K2:       P(Difficulty) = {cpd_diff_k2.get_values().flatten().round(3)}")

# %% [markdown]
# ### Experiment: Custom Dirichlet Pseudo-Counts
#
# For the root node `Difficulty` (3 states, no parents), the CPD shape is (3, 1).

# %%
# Custom pseudo-counts for each variable.
# For Difficulty: shape (3, 1) -- 3 states, no parents.
pseudo_difficulty = np.array([[2.0], [2.0], [2.0]])

# For Intelligence: shape (2, 1) -- 2 states, no parents.
pseudo_intelligence = np.array([[3.0], [3.0]])

# For Grade: shape (3, 2*3=6) -- 3 states, parents=2 and 3 states.
pseudo_grade = np.ones((3, 6))

estimator_custom = DiscreteBayesianEstimator(
    prior_type="dirichlet",
    pseudo_counts={
        "Difficulty": pseudo_difficulty,
        "Intelligence": pseudo_intelligence,
        "Grade": pseudo_grade,
    },
)
estimator_custom.fit(student_model, data)

print("CPDs with custom Dirichlet pseudo-counts:")
for cpd in estimator_custom.parameters_:
    print(f"\n{cpd.variable}:")
    print(cpd)

# %% [markdown]
# ## Primitive 3: `DiscreteEM`: Expectation Maximization
#
# **Mental model**: Handles latent (unobserved) variables. EM alternates
# between:
# - **E-step**: Estimate the distribution over latent states given current CPDs
# - **M-step**: Re-estimate CPDs using weighted MLE on the completed data
#
# This is useful when:
# - The dataset has missing values
# - The model contains latent (unobserved) variables
# - You want to learn a model with hidden causes

# %%
# Create a model with a latent variable.
# "StudyHabits" is latent: it affects Grade but is not observed in data.
latent_model = DiscreteBayesianNetwork(
    [
        ("Difficulty", "Grade"),
        ("Intelligence", "Grade"),
        ("StudyHabits", "Grade"),
    ],
    latents={"StudyHabits"},  # Mark as latent: not observed in data.
)

print(f"Model nodes: {sorted(latent_model.nodes())}")
print(f"Latent nodes: {latent_model.latents}")
print(f"Edges: {sorted(latent_model.edges())}")

# %%
# Fit with EM: use same data (StudyHabits column is absent).
estimator_em = DiscreteEM(
    latent_card={"StudyHabits": 2},  # StudyHabits has 2 states.
    show_progress=False,
    seed=42,
)
estimator_em.fit(latent_model, data)

print(f"Number of CPDs: {len(estimator_em.parameters_)}")
for cpd in estimator_em.parameters_:
    print(f"\n{cpd.variable}:")
    print(cpd)

# %%
# Note: EM returns CPDs for ALL variables, including the latent one.
cpd_study = [c for c in estimator_em.parameters_ if c.variable == "StudyHabits"][
    0
]
print(f"Latent variable CPD: {cpd_study.variable}")
print(f"  Parents: {cpd_study.variables[1:]}")
print(cpd_study)

# %% [markdown]
# ### Experiment: Different Initialization Strategies
#
# The `init_cpds` parameter controls how CPDs are initialized before EM
# iterations begin. Options: `"random"`, `"uniform"`, or a dict of specific CPDs.

# %%
# Compare random vs uniform initialization.
for init in ["random", "uniform"]:
    est = DiscreteEM(
        latent_card={"StudyHabits": 2},
        init_cpds=init,
        show_progress=False,
        seed=42,
    )
    est.fit(latent_model, data)
    # Extract the latent CPD.
    cpd = [c for c in est.parameters_ if c.variable == "StudyHabits"][0]
    print(
        f"init_cpds='{init}': P(StudyHabits) = {cpd.get_values().flatten().round(3)}"
    )

# %% [markdown]
# ### Experiment: EM with Missing Data
#
# EM can also handle partially observed data by treating missing values as latent.

# %%
# Introduce missing values in the Grade column.
data_missing = data.copy()
data_missing.loc[0:4, "Grade"] = np.nan
print("Data with missing values (first 8 rows):")
display(data_missing.head(8))

# %%
# Fit the original student model (no latent nodes) with missing data.
estimator_em_missing = DiscreteEM(
    show_progress=False,
    seed=42,
)
estimator_em_missing.fit(student_model, data_missing)

print("CPDs estimated with missing data via EM:")
for cpd in estimator_em_missing.parameters_:
    print(f"\n{cpd.variable}:")
    print(cpd)

# %% [markdown]
# ## Primitive 4: `model.fit()`: The Convenience Method
#
# **Mental model**: `model.fit()` is the recommended entry point for most users.
# It combines estimator creation, fitting, and CPD assignment into one call.
# The graph structure must already be defined.

# %%
# Smallest construction: fit a model in one line.
model_fitted = student_model.copy()
model_fitted.fit(data, estimator=DiscreteMLE())

print(f"Fitted model type: {type(model_fitted)}")
print(f"Number of CPDs: {len(model_fitted.get_cpds())}")

# %%
# Inspect the fitted model's CPDs.
for cpd in model_fitted.get_cpds():
    print(f"\n{cpd.variable}:")
    print(cpd)

# %%
# Switch to Bayesian estimation: only change the estimator argument.
model_bayes = student_model.copy()
model_bayes.fit(
    data,
    estimator=DiscreteBayesianEstimator(
        prior_type="BDeu",
        equivalent_sample_size=5,
    ),
)

for cpd in model_bayes.get_cpds():
    print(f"\n{cpd.variable}:")
    print(cpd)

# %% [markdown]
# ### Inspect What `model.fit()` Returns
#
# `model.fit()` returns the model itself (with CPDs added), enabling chaining.

# %%
result = student_model.copy().fit(data, estimator=DiscreteMLE())
print(f"fit() returns: {type(result)}")
print(f"Fitted model has CPDs: {len(result.get_cpds())}")
print(f"First CPD variable: {result.get_cpds()[0].variable}")

# %% [markdown]
# # Part 3: Composition Examples
#
# ## Example 1: Fit a Model with MLE, Then Query Probabilities
#
# Minimal end-to-end workflow: define structure -> fit -> inspect.

# %%
# Define structure.
exam_net = DiscreteBayesianNetwork(
    [("Difficulty", "Grade"), ("Intelligence", "Grade")]
)

# Fit with MLE.
exam_net.fit(data, estimator=DiscreteMLE())

# Inspect grade distribution given easy difficulty and low intelligence.
cpd = exam_net.get_cpds("Grade")
print("P(Grade | Difficulty, Intelligence):")
display(tpgpguti.factor_to_dataframe(cpd))

# %% [markdown]
# ## Example 2: Compare MLE vs Bayesian on Sparse Data
#
# With very few samples, Bayesian estimates with priors are more stable.

# %%
# Create very sparse data: only 3 rows.
sparse_data = pd.DataFrame(
    {
        "Difficulty": [0, 1, 0],
        "Intelligence": [0, 0, 1],
        "Grade": [2, 0, 1],
    }
)

# Fit with MLE.
sparse_mle = student_model.copy()
sparse_mle.fit(sparse_data, estimator=DiscreteMLE())

# Fit with Bayesian (BDeu).
sparse_bayes = student_model.copy()
sparse_bayes.fit(
    sparse_data,
    estimator=DiscreteBayesianEstimator(
        prior_type="BDeu",
        equivalent_sample_size=5,
    ),
)

# Compare root node CPDs only (simpler than comparing conditional CPDs).
for var in ["Difficulty", "Intelligence"]:
    cpd_mle = sparse_mle.get_cpds(var)
    cpd_bayes = sparse_bayes.get_cpds(var)
    comp_df = pd.DataFrame(
        {
            "State": list(range(cpd_mle.variable_card)),
            "MLE": cpd_mle.get_values().flatten(),
            "Bayesian (BDeu)": cpd_bayes.get_values().flatten(),
        }
    )
    print(f"\n{var}:")
    display(comp_df)

# %% [markdown]
# ## Example 3: EM with a Latent Node
#
# Suppose we suspect an unobserved "StudyHabits" variable affects Grade.
# We define the graph including it, mark it as latent, and use EM.

# %%
# Model with latent StudyHabits.
model_with_latent = DiscreteBayesianNetwork(
    [
        ("Difficulty", "Grade"),
        ("Intelligence", "Grade"),
        ("StudyHabits", "Grade"),
    ],
    latents={"StudyHabits"},
)

# Fit with EM.
em_result = model_with_latent.copy()
em_result.fit(
    data,
    estimator=DiscreteEM(
        latent_card={"StudyHabits": 2}, show_progress=False, seed=42
    ),
)

print(f"CPDs learned ({len(em_result.get_cpds())} total):")
for cpd in em_result.get_cpds():
    print(f"\n  {cpd.variable}:")
    print(f"    {cpd}")

# %% [markdown]
# ## Example 4: Use Fitted Model for Inference
#
# Once parameters are estimated, we can use the model for probabilistic inference.

# %%
from pgmpy.inference import VariableElimination

# Fit the original student model.
model_inf = student_model.copy()
model_inf.fit(data, estimator=DiscreteMLE())

# Perform inference: what is P(Grade=A) given easy difficulty?
inference = VariableElimination(model_inf)
result = inference.query(
    variables=["Grade"],
    evidence={"Difficulty": 0},
)
print("P(Grade | Difficulty=0):")
print(result)

# %%
# Query: what is P(Grade=A | high intelligence)?
result2 = inference.query(
    variables=["Grade"],
    evidence={"Intelligence": 1},
)
print("P(Grade | Intelligence=1):")
print(result2)

# %% [markdown]
# ## Example 5: Sequential Update with `fit_update()`
#
# `fit_update()` updates an existing model's parameters with new data using
# Bayesian estimation. The current CPDs serve as the prior.

# %%
# Fit on initial data.
model_update = student_model.copy()
model_update.fit(data.iloc[:10], estimator=DiscreteMLE())
print("After first 10 samples:")
for cpd in model_update.get_cpds():
    print(f"  {cpd.variable}: {cpd.get_values().flatten().round(3)}")

# %%
# Update with 5 more samples.
model_update.fit_update(data.iloc[10:15], n_prev_samples=10)
print("After updating with 5 more samples:")
for cpd in model_update.get_cpds():
    print(f"  {cpd.variable}: {cpd.get_values().flatten().round(3)}")

# Fit on all 15 to compare.
model_all = student_model.copy()
model_all.fit(data.iloc[:15], estimator=DiscreteMLE())
print("\nDirect fit on all 15 samples:")
for cpd in model_all.get_cpds():
    print(f"  {cpd.variable}: {cpd.get_values().flatten().round(3)}")

# %% [markdown]
# # Part 4: API Patterns
#
# ## 1. Estimator-Fit-Parameters Pattern
#
# All estimators follow the same pattern: construct -> fit -> access `parameters_`.
# This is a scikit-learn-style `fit()` API.

# %%
# The pattern in one expression.
params = DiscreteMLE().fit(student_model, data).parameters_
print(f"Parameters from one-liner: {len(params)} CPDs")

# %% [markdown]
# ## 2. Model-fit Convenience Pattern
#
# The model's `fit()` method handles estimator instantiation, fitting, and
# CPD assignment in one call. The only difference between methods is the
# `estimator=` argument.

# %%
# Switch estimators by changing one argument.
import time

for name, est in [
    ("MLE", DiscreteMLE()),
    ("Bayesian(BDeu)", DiscreteBayesianEstimator(prior_type="BDeu")),
]:
    t0 = time.time()
    result = student_model.copy().fit(data, estimator=est)
    dt = time.time() - t0
    print(f"{name:20s}: {len(result.get_cpds())} CPDs in {dt:.4f}s")

# %% [markdown]
# ## 3. TabularCPD Output Pattern
#
# All estimators return CPDs in the same format. Each CPD is a `TabularCPD`
# object that can be:
# - Printed (`print(cpd)`)
# - Converted to a numpy array (`cpd.get_values()`)
# - Displayed as a DataFrame (via `pgmpy_utils.factor_to_dataframe()`)

# %%
# Unified CPD inspection.
def show_cpd_summary(cpd_list):
    """
    Display a table summarizing all CPDs in a list.
    """
    rows = []
    for cpd in cpd_list:
        rows.append(
            {
                "Variable": cpd.variable,
                "Cardinality": cpd.variable_card,
                "Parents": ", ".join(cpd.variables[1:])
                if len(cpd.variables) > 1
                else "",
                "Values Shape": str(cpd.values.shape),
            }
        )
    display(pd.DataFrame(rows))


# Show summary for MLE result.
show_cpd_summary(estimator_mle.parameters_)

# %% [markdown]
# ## 4. Sparse Data Pattern
#
# When data is sparse relative to the total parent configuration space,
# Bayesian estimation is preferred over MLE because it avoids zero
# probabilities.

# %%
# Demonstration: MLE produces zeros, Bayesian avoids them.
sparse = pd.DataFrame(
    {
        "Difficulty": [0, 0, 0],
        "Intelligence": [0, 0, 0],
        "Grade": [0, 1, 2],
    }
)

mle_sparse = DiscreteMLE().fit(student_model, sparse).parameters_
bayes_sparse = (
    DiscreteBayesianEstimator(prior_type="K2")
    .fit(student_model, sparse)
    .parameters_
)

# Check if any CPD has zero values.
for cpd in mle_sparse:
    vals = cpd.get_values()
    has_zero = (vals == 0).any()
    print(f"MLE   {cpd.variable}: has zeros = {has_zero}")

for cpd in bayes_sparse:
    vals = cpd.get_values()
    has_zero = (vals == 0).any()
    print(f"K2    {cpd.variable}: has zeros = {has_zero}")

# %% [markdown]
# # Part 5: Interactive Exploration
#
# ## Experiment 1: What happens if you fit without specifying `state_names`?
#
# By default, estimators infer state names from the data. If some states
# are absent from the sample, they will be missing from the CPD.

# %%
# Data missing state "2" for Difficulty.
partial_data = pd.DataFrame(
    {
        "Difficulty": [0, 0, 1, 1],
        "Intelligence": [0, 1, 0, 1],
        "Grade": [0, 1, 0, 1],
    }
)

est_partial = DiscreteMLE()
est_partial.fit(student_model, partial_data)
print("State names (no '2' for Difficulty):")
for var, states in est_partial.state_names_.items():
    print(f"  {var}: {states}")

# %%
# Use state_names to declare all possible states explicitly.
est_full = DiscreteMLE(
    state_names={
        "Difficulty": [0, 1, 2],
        "Intelligence": [0, 1],
        "Grade": [0, 1, 2],
    }
)
est_full.fit(student_model, partial_data)
print("State names (all states declared):")
for var, states in est_full.state_names_.items():
    print(f"  {var}: {states}")

# The CPD for Difficulty now includes state 2 with probability 0.
cpd_diff = [c for c in est_full.parameters_ if c.variable == "Difficulty"][0]
print("\nP(Difficulty) with explicit states:")
print(cpd_diff)

# %% [markdown]
# ## Experiment 2: Use `dir()` to explore estimator API

# %%
# Explore the DiscreteMLE API.
mle_methods = [m for m in dir(DiscreteMLE()) if not m.startswith("_")]
print(f"DiscreteMLE methods: {mle_methods}")

# %%
# Explore the DiscreteBayesianEstimator API.
bayes_methods = [
    m for m in dir(DiscreteBayesianEstimator()) if not m.startswith("_")
]
print(f"DiscreteBayesianEstimator methods: {bayes_methods}")

# %%
# Explore the DiscreteEM API.
em_methods = [
    m for m in dir(DiscreteEM(show_progress=False)) if not m.startswith("_")
]
print(f"DiscreteEM methods: {em_methods}")

# %% [markdown]
# ## Experiment 3: What happens with a larger `equivalent_sample_size`?
#
# The larger the equivalent sample size, the more the prior dominates
# the likelihood.

# %%
# Sweep equivalent_sample_size and observe effect on root node CPD.
for ess in [0.1, 1, 5, 50, 500]:
    est = DiscreteBayesianEstimator(
        prior_type="BDeu",
        equivalent_sample_size=ess,
    )
    est.fit(student_model, data)
    cpd = [c for c in est.parameters_ if c.variable == "Intelligence"][0]
    p_high = cpd.get_values()[1, 0]
    print(f"ESS={ess:6.1f}: P(Intelligence=1) = {p_high:.4f}  (MLE = {0.55})")

# %% [markdown]
# ## Experiment 4: Verify Normalization
#
# CPDs should sum to 1 over the variable's states for each parent
# configuration.

# %%
# Check that all CPDs are properly normalized.
for cpd in estimator_mle.parameters_:
    vals = cpd.get_values()
    col_sums = vals.sum(axis=0)
    all_close = np.allclose(col_sums, 1.0)
    print(
        f"{cpd.variable}: column sums close to 1.0? {all_close}  (min={col_sums.min():.6f}, max={col_sums.max():.6f})"
    )

# %% [markdown]
# # Summary: The Mental Model
#
# - **`DiscreteMLE`**: "Count and normalize"
#   - Fast, interpretable, but can produce zero probabilities for unseen parent configs
#   - Best when data covers all parent configurations
#   - Constructor: `DiscreteMLE(state_names=None, n_jobs=1)`
#
# - **`DiscreteBayesianEstimator`**: "Count and smooth with a prior"
#   - Adds Dirichlet pseudo-counts to avoid zero probabilities
#   - Three prior types: `BDeu` (uniform, default), `K2` (all = 1), `dirichlet` (custom)
#   - `equivalent_sample_size` controls the prior strength
#   - Constructor: `DiscreteBayesianEstimator(prior_type="BDeu", equivalent_sample_size=5, ...)`
#
# - **`DiscreteEM`**: "Iterate over latent states"
#   - Alternates between E-step (impute latents) and M-step (re-estimate)
#   - Handles latent variables and missing data
#   - Constructor: `DiscreteEM(latent_card={...}, max_iter=100, ...)`
#
# - **`model.fit()`**: "One-call convenience"
#   - Pass an estimator instance (not class) as `estimator=`
#   - Returns the model with CPDs added
#   - Pattern: `model.fit(data, estimator=DiscreteMLE())`
#
# - All estimators share the same protocol:
#   `estimator.fit(model, data)` -> `estimator.parameters_` -> `List[TabularCPD]`
