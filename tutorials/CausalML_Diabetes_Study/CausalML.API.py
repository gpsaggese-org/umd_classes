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
# # CausalML API: Quick Start
#
# This notebook provides a runnable walkthrough of the `CausalNavigator` API.
# Each section pairs the API documentation with a live code cell so you can
# test every method end-to-end.
#
# The `CausalML` module is a high-level wrapper around the `causalml` library
# designed to simplify causal inference workflows for observational studies. It
# includes the `CausalNavigator` class for heterogeneous treatment effect
# estimation, diagnostic methods for assumption validation, and helper
# functions for data preprocessing and visualisation.

# %% [markdown]
# ## Architecture
#
# While `causalml` provides powerful meta-learners (S/T/X-Learners), the
# native API requires significant boilerplate for data preprocessing,
# assumption checking, and visualisation. `CausalNavigator` standardises that
# workflow into a single class.
#
# The core pipeline has three layers:
#
# 1. **Diagnostic Layer**: Verifies causal assumptions (specifically Common
#    Support) before estimation
# 2. **Estimation Layer**: Wraps `causalml.inference.meta` classes
#    (`BaseXRegressor`, etc.) and injects XGBoost as the standard base learner
# 3. **Interpretation Layer**: Provides built-in methods to visualise
#    heterogeneity, abstracting away `matplotlib` complexity

# %% [markdown]
# ## Setup

# %%
# %load_ext autoreload
# %autoreload 2


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import logging
import utils

import warnings
warnings.filterwarnings("ignore")

_LOG = logging.getLogger(__name__)
utils.init_logger(_LOG)

# %%
import os

# TODO(gp): Use import X.
from utils import (
    CausalNavigator,
    download_cdc_data_if_needed,
    load_cdc_data,
    preprocess_for_causal,
)

# %% [markdown]
# ### Load data set.

# %%
# Download and load the dataset.
filename = "diabetes_binary_health_indicators_BRFSS2015.csv"
data_path = os.path.join("data", "unprocessed", filename)
download_cdc_data_if_needed(data_path)
df_raw = load_cdc_data(data_path)


# %%
df_raw.head(3)

# %%
# TODO(ai_gp): Add a short explanation of the data above, e.g., what are features, what are target vars.

# %% [markdown]
# ## Prepare data set

# %% [markdown]
# **Function**: `preprocess_for_causal(df, ...)`
#
# - **Purpose**: Splits the dataframe into components for causal analysis:
#   - **X (Covariates)** - features used to control for confounding
#   - **T (Treatment)** - the binary intervention vector
#   - **Y (Outcome)** - the target variable

# %%
# Prepare data for causal analysis.
treatment_col = "PhysActivity"
outcome_col = "Diabetes_binary"
covariate_cols = [
    "HighBP",
    "HighChol",
    "Age",
    "Income",
    "Sex",
    "GenHlth",
    "BMI",
]


df_clean, X, T, Y = preprocess_for_causal(
    df_raw,
    treatment_col=treatment_col,
    outcome_col=outcome_col,
    covariate_cols=covariate_cols,
)

# %% [markdown]
# ## Prepare Demo Data
#
# Set seed for reproducibility and subsample for speed.
#
# **Parameters**:
#
# - `learner_type`: Meta-learner to use: `'S'`, `'T'`, or `'X'`
# - `control_name`: Label for the untreated group (used in plots)
# - `treatment_name`: Label for the treated group (used in plots)

# %%
# Set seed for reproducibility and subsample for speed.
np.random.seed(42)
sample_indices = np.random.choice(X.index, size=10000, replace=False)
X_demo = X.loc[sample_indices]
T_demo = T.loc[sample_indices]
Y_demo = Y.loc[sample_indices]
print(f"API Demo Data Loaded. Shape: {X_demo.shape}")
print(X_demo.head())

# Initialize the CausalNavigator.
navigator = CausalNavigator(
    learner_type="X", control_name="Sedentary", treatment_name="Active"
)

# %% [markdown]
# ### `check_overlap(X, T)`
#
# **Purpose**: Validates the Positivity/Overlap assumption.
#
# - **Inputs**: Covariate matrix `X`, Treatment vector `T`
# - **Output**: A density plot of Propensity Scores
# - **Why use this**: If the distributions do not overlap, causal estimation is
#   invalid. This method enforces safety before modelling - the treated and
#   control groups must share common support across the feature space.

# %%
# Check if there is "Common Support" between the treated and control groups.
navigator.check_overlap(X_demo, T_demo)

# %% [markdown]
# ### `fit_estimate(X, T, Y)`
#
# **Purpose**: Trains the meta-learner and estimates CATE (Conditional Average
# Treatment Effect).
#
# - **Inputs**: Covariates `X`, Treatment `T`, Outcome `Y`
# - **Output**: `numpy.array` of CATE values - one per observation
# - **Design choice**: XGBoost is used as the base learner because it handles
#   non-linearities in the response surface effectively, which is crucial for
#   the X-Learner

# %%
# Estimate effects.
cate_estimates = navigator.fit_estimate(X_demo, T_demo, Y_demo)
print(f"\nAverage Treatment Effect (ATE): {cate_estimates.mean():.4f}")

# %% [markdown]
# ### `get_cate_df(df_original)`
#
# **Purpose**: Helper to merge the estimated effects back into the original
# dataframe.
#
# - **Inputs**: Original dataframe
# - **Output**: Dataframe with a new `cate` column
#
# ### `plot_heterogeneity(df_with_cate, col, bins=5)`
#
# **Purpose**: Visualises how the treatment effect varies across a specific
# feature.
#
# - **Inputs**: Dataframe with CATE, column name, optional bins
# - **Output**: A bar chart showing CATE by group with confidence intervals

# %%
# Visualize results.
df_results = navigator.get_cate_df(X_demo)
navigator.plot_heterogeneity(df_results, col="Age")

# %% [markdown]
# ### `run_placebo_test(X, T, Y, n_simulations=10)`
#
# **Purpose**: Robustness check (Refutation).
#
# - **Logic**: Randomly shuffles the treatment array to break any true causal
#   link, then re-trains the model
# - **Success criteria**: The "Placebo ATE" should cluster around 0; the
#   "Actual ATE" should be far outside this distribution
# - **Interpretation**: If the actual effect falls *inside* the placebo
#   distribution, the result is statistically indistinguishable from noise

# %%
# Robustness check: shuffle T to see if the model finds an effect where none
# exists.
navigator.run_placebo_test(X_demo, T_demo, Y_demo, n_simulations=3)

# %% [markdown]
# ### `run_sensitivity_analysis(X, T, Y)`
#
# **Purpose**: Quantifies the stability of the causal estimate.
#
# - **Logic**: Iteratively removes one covariate at a time and re-calculates
#   the Average Treatment Effect (ATE)
# - **Output**: A horizontal bar chart showing the ATE for each scenario
#   compared to the baseline
# - **Interpretation**:
#   - **Stable** - bars cluster near the baseline (red line)
#   - **Sensitive** - a bar shifts significantly or crosses zero, indicating
#     that specific variable drives the result

# %%
# Sensitivity analysis: check how stable the result is when removing one
# covariate at a time.
navigator.run_sensitivity_analysis(X_demo, T_demo, Y_demo)

# %% [markdown]
# ### `compare_estimators(X, T, Y)`
#
# **Purpose**: Advanced model selection ("Horse Race").
#
# - **Methodology**: Splits data into Train (70%) and Test (30%); trains S, T,
#   X, R, and DR learners on the training set
# - **Metric**: Generates a **Cumulative Gain Chart (Uplift Curve)** on the
#   test set
# - **Why this metric**: Since ground-truth CATE is impossible to observe, RMSE
#   cannot be used. The Gain Chart measures how well a model sorts individuals
#   from "High Responder" to "Low Responder"
# - **Outputs**:
#   - **Uplift Curve Plot** - visual comparison of model performance
#   - **Qini/AUUC Score Table** - numerical ranking of models (Area Under
#     Uplift Curve)

# %%
# Estimator comparison ("Horse Race"): compare X-Learner against S, T, R, and
# DR Learners using Uplift Curves.
navigator.compare_estimators(X_demo, T_demo, Y_demo)
