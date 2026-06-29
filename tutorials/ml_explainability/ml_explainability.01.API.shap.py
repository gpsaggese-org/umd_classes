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
# # SHAP API
#
# A guided exploration of SHAP (SHapley Additive exPlanations):
# - **Explainer**: wraps a trained ML model and computes Shapley values
# - **Explanation**: holds SHAP values, baseline prediction, and feature data
# - **Plots**: visualize feature contributions locally (per prediction) and globally

# %% [markdown]
# ## Imports and Setup

# %%
# %load_ext autoreload
# %autoreload 2

import logging
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap

# TODO(ai_gp): Use import ... instead of from import
from sklearn.datasets import make_regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

warnings.filterwarnings("ignore")

# %%
import helpers.hdbg as hdbg
import helpers.hintrospection as hintros
import helpers.hnotebook as hnotebook

hdbg.init_logger(verbosity=logging.INFO)
_LOG = logging.getLogger(__name__)
hnotebook.config_notebook()

try:
    from IPython.display import display
except ImportError:
    display = print  # type: ignore

# %% [markdown]
# ## Library Overview
#
# - **What problem it solves**:
#   - Modern ML models (tree ensembles, neural nets) are accurate but opaque
#   - SHAP answers "why did the model predict X?" for any single prediction
#   - Decomposes predictions into per-feature contributions grounded in game
#     theory (Shapley values from cooperative game theory)
#
# - **Key abstraction**:
#   - Every prediction = baseline + sum of per-feature SHAP values
#   - Shapley values satisfy consistency, dummy, and efficiency axioms (no other
#     attribution satisfying all three exists)
#
# - **Mental model**:
#   ```
#   model: X -> prediction
#   Explainer(model, background) -> configured explainer
#   explainer(X) -> Explanation
#   Explanation.values       shape (n_samples, n_features): per-feature SHAP
#   Explanation.base_values  shape (n_samples,): E[model(X)] baseline
#   Explanation.data         shape (n_samples, n_features): original feature values
#   prediction[i] = base_values[i] + values[i].sum()
#   ```
#
# - **Key classes**:
#   - `shap.Explainer`: auto-selects best algorithm for the model type
#   - `shap.TreeExplainer`: fast and exact for tree-based models
#   - `shap.LinearExplainer`: exact for linear models
#   - `shap.KernelExplainer`: model-agnostic, works with any callable
#   - `shap.Explanation`: result object (values, base_values, data)

# %% [markdown]
# # Part 1: Toy Data Setup

# %% [markdown]
# ## Cell 1.1: Create a toy regression dataset
#
# **Goal**:
# - Build the minimal dataset needed to explore all SHAP primitives
# - Use regression (not classification) to keep SHAP values 2D and easy to inspect

# %%
# Four named features, 30 samples, pure regression target.
np.random.seed(42)
X, y = make_regression(
    n_samples=30,
    n_features=4,
    n_informative=3,
    noise=10.0,
    random_state=42,
)
X_df = pd.DataFrame(X, columns=["age", "income", "debt", "employment"])
y_s = pd.Series(y, name="target")

print("X_df.shape=", X_df.shape)
print("y_s.shape=", y_s.shape)
display(X_df.head(3))

# %%
# TODO(ai_gp): Perform some analysis of the data set (e.g., correlations between features, X and Y, ...)

# %% [markdown]
# ## Cell 1.2: Train models (one per explainer type)
#
# **Goal**:
# - Prepare one tree model, one linear model, and one black-box model
# - Use small models to make SHAP computation fast

# %%
# Tree model for TreeExplainer.
tree_model = DecisionTreeRegressor(max_depth=3, random_state=42)
tree_model.fit(X_df, y_s)
print("tree_model=", tree_model)

# %%
# Linear model for LinearExplainer.
linear_model = LinearRegression()
linear_model.fit(X_df, y_s)
print("linear_model=", linear_model)

# %%
# Random forest as a "black box" model for KernelExplainer.
rf_model = RandomForestRegressor(n_estimators=10, random_state=42)
rf_model.fit(X_df, y_s)
print("rf_model=", rf_model)

# %%
# TODO(ai_gp): For each model compute performance in sample and out of sample.

# %% [markdown]
# # Part 2: Primitive 1 - The Explainer

# %% [markdown]
# ## Cell 2.1: Construct a TreeExplainer
#
# **Mental model**:
# - `TreeExplainer` wraps a trained tree-based model
# - It traverses the tree structure to compute exact Shapley values in polynomial
#   time (no sampling needed)
# - No background data required: the tree encodes the full conditional distribution

# %%
# Smallest possible construction: just the model.
tree_explainer = shap.TreeExplainer(tree_model)
print("type(tree_explainer)=", type(tree_explainer))

# %% [markdown]
# ## Cell 2.2: Inspect the TreeExplainer

# %%
# expected_value is E[model(X)], the global baseline.
print("tree_explainer.expected_value=", tree_explainer.expected_value)
print("mean of y (approx baseline)=", round(y_s.mean(), 4))

# TODO(ai_gp): Explain the results and what they mean.

# %%
# Public interface of the explainer.
# TODO(ai_gp): Improve print_public_methods to create a dataframe with function, explanation, signature
hintros.print_public_methods(tree_explainer, use_markdown=True)

# %% [markdown]
# ## Cell 2.3: Construct a LinearExplainer
#
# **Mental model**:
# - `LinearExplainer` wraps a linear model together with background data
# - Background data captures feature means and covariances used to compute
#   conditional expectations

# %%
# LinearExplainer needs the model and background data.
linear_explainer = shap.LinearExplainer(linear_model, X_df)
print("type(linear_explainer)=", type(linear_explainer))
print("linear_explainer.expected_value=", linear_explainer.expected_value)

# %% [markdown]
# ## Cell 2.4: Construct a KernelExplainer (model-agnostic)
#
# **Mental model**:
# - `KernelExplainer` works with any callable - it treats the model as a black box
# - Approximates Shapley values by sampling perturbations of the input
# - Slower than TreeExplainer but works with any model (sklearn, TensorFlow, etc.)
# - Background data should be a small summary of the training distribution

# %%
# Summarize background data with k-means to speed up sampling.
background = shap.kmeans(X_df, k=5)
print("type(background)=", type(background))
print("background.data.shape=", background.data.shape)

# %%
# Wrap rf_model.predict as a callable.
kernel_explainer = shap.KernelExplainer(rf_model.predict, background)
print("type(kernel_explainer)=", type(kernel_explainer))
print("kernel_explainer.expected_value=", kernel_explainer.expected_value)

# %% [markdown]
# ## Cell 2.5: Construct shap.Explainer (auto-dispatch)
#
# **Mental model**:
# - `shap.Explainer` inspects the model type and auto-selects the best algorithm
# - If the model is a tree: uses TreeExplainer internally
# - If linear: uses LinearExplainer
# - Otherwise: falls back to PermutationExplainer or KernelExplainer

# %%
# Auto-dispatch based on model type.
auto_explainer = shap.Explainer(tree_model, X_df)
print("type(auto_explainer)=", type(auto_explainer))
# Internally dispatches to TreeExplainer for a DecisionTreeRegressor.

# %% [markdown]
# # Part 3: Primitive 2 - The Explanation Object

# %% [markdown]
# ## Cell 3.1: Compute SHAP values (get an Explanation)
#
# **Mental model**:
# - Calling `explainer(X)` returns an `Explanation` object
# - This bundles SHAP values, baseline, and original data into one structure

# %%
# Compute SHAP values for all 30 samples.
explanation = tree_explainer(X_df)
print("type(explanation)=", type(explanation))

# %% [markdown]
# ## Cell 3.2: Inspect Explanation.values

# %%
# .values: SHAP contribution of each feature for each sample.
print("type(explanation.values)=", type(explanation.values))
print("explanation.values.shape=", explanation.values.shape)
# Rows = samples, columns = features.
values_df = pd.DataFrame(explanation.values, columns=X_df.columns)
display(values_df.head(3))

# %% [markdown]
# ## Cell 3.3: Inspect Explanation.base_values

# %%
# .base_values: model's expected output (same for all samples).
print("explanation.base_values.shape=", explanation.base_values.shape)
print("explanation.base_values[0]=", round(explanation.base_values[0], 4))
print(
    "all identical?",
    np.allclose(explanation.base_values, explanation.base_values[0]),
)

# %% [markdown]
# ## Cell 3.4: Inspect Explanation.data

# %%
# .data: the original feature values passed to the explainer.
print("type(explanation.data)=", type(explanation.data))
print("explanation.data.shape=", explanation.data.shape)
display(pd.DataFrame(explanation.data, columns=X_df.columns).head(3))

# %% [markdown]
# ## Cell 3.5: Verify the additive decomposition
#
# **Key invariant**:
# - `prediction[i] = base_value + sum(shap_values[i])`
# - This always holds exactly for TreeExplainer (and LinearExplainer)

# %%
# Verify for sample index 0.
idx = 0
model_pred = tree_model.predict(X_df.iloc[[idx]])[0]
shap_sum = explanation.base_values[idx] + explanation.values[idx].sum()
print("model_pred=", round(model_pred, 6))
print("base + sum(shap)=", round(shap_sum, 6))
print("match?", np.isclose(model_pred, shap_sum))

# %% [markdown]
# ## Cell 3.6: Index the Explanation object
#
# - `explanation[i]` selects sample i (returns Explanation with shape (n_features,))
# - `explanation[:, j]` selects feature j across all samples (shape (n_samples,))
# - `explanation[i, j]` selects a single SHAP scalar

# %%
# Single sample.
sample_exp = explanation[0]
print("type(sample_exp)=", type(sample_exp))
print("sample_exp.values=", sample_exp.values)
print("sample_exp.base_values=", sample_exp.base_values)

# %%
# Single feature across all samples.
income_exp = explanation[:, "income"]
print("type(income_exp)=", type(income_exp))
print("income_exp.values.shape=", income_exp.values.shape)

# %%
# Single (sample, feature) scalar.
scalar_exp = explanation[0, "income"]
print("explanation[0, 'income'].values=", scalar_exp.values)

# %% [markdown]
# # Part 4: Primitive 3 - SHAP Plots

# %% [markdown]
# ## Cell 4.1: Waterfall plot (single prediction)
#
# **Goal**:
# - See how each feature pushes prediction above or below the baseline for one sample
# - Start at `E[f(X)]` (bottom), end at `f(x)` (model output)

# %%
# Waterfall plot for sample 0: shows individual feature contributions.
shap.plots.waterfall(explanation[0])
plt.close("all")

# %% [markdown]
# **Key observations**:
# - Each horizontal bar = one feature's SHAP contribution
# - Red: feature pushes prediction up
# - Blue: feature pushes prediction down
# - Total = base_value + signed sum of all bars = model output

# %% [markdown]
# ## Cell 4.2: Bar plot (global feature importance)
#
# **Goal**:
# - Rank features by their average absolute SHAP value across all samples
# - This is the global view: which features matter most overall?

# %%
# Bar plot: mean |SHAP value| per feature across all samples.
shap.plots.bar(explanation)
plt.close("all")

# %% [markdown]
# **Key observations**:
# - Bar length = mean(|SHAP value|) averaged across 30 samples
# - Longer bar = feature matters more globally
# - Does not show direction (sign), only magnitude

# %% [markdown]
# ## Cell 4.3: Beeswarm plot (global distribution of SHAP values)
#
# **Goal**:
# - Show the distribution of SHAP values per feature across all samples
# - Color encodes the feature value (red = high, blue = low)

# %%
# Beeswarm: one dot per (sample, feature), color = feature value.
shap.plots.beeswarm(explanation)
plt.close("all")

# %% [markdown]
# **Key observations**:
# - Each dot = one sample's SHAP value for a given feature
# - Horizontal spread = range of SHAP contributions for that feature
# - Red dots with high SHAP -> high feature value increases the prediction
# - Blue dots with low SHAP -> low feature value decreases the prediction

# %% [markdown]
# ## Cell 4.4: Scatter plot (feature dependence)
#
# **Goal**:
# - See how a single feature's value relates to its SHAP contribution
# - Reveals linear, monotonic, or threshold-based effects

# %%
# Scatter: x = feature value, y = SHAP contribution for "income".
shap.plots.scatter(explanation[:, "income"])
plt.close("all")

# %% [markdown]
# **Key observations**:
# - x-axis: raw feature value (income)
# - y-axis: SHAP contribution for income
# - A diagonal line -> monotonic effect; an S-curve -> threshold or saturation

# %% [markdown]
# # Part 5: Composition Examples

# %% [markdown]
# ## Cell 5.1: End-to-end with LinearExplainer
#
# Verify that LinearExplainer also satisfies the additive decomposition.

# %%
# Compute SHAP values with linear explainer.
linear_explanation = linear_explainer(X_df)
print("linear_explanation.values.shape=", linear_explanation.values.shape)

# %%
# Verify additivity for linear model.
pred_lin = linear_model.predict(X_df.iloc[[0]])[0]
shap_sum_lin = (
    linear_explanation.base_values[0] + linear_explanation.values[0].sum()
)
print("linear model pred=", round(pred_lin, 6))
print("base + sum(shap)=", round(shap_sum_lin, 6))
print("match?", np.isclose(pred_lin, shap_sum_lin))

# %% [markdown]
# ## Cell 5.2: Compare SHAP importances across models
#
# Different model types may rank features differently even on the same data.

# %%
# Build a comparison DataFrame: tree vs linear mean absolute SHAP.
tree_importance = pd.Series(
    np.abs(explanation.values).mean(axis=0),
    index=X_df.columns,
    name="tree",
)
linear_importance = pd.Series(
    np.abs(linear_explanation.values).mean(axis=0),
    index=X_df.columns,
    name="linear",
)
importance_df = pd.DataFrame([tree_importance, linear_importance]).T
display(importance_df.sort_values("tree", ascending=False))

# %% [markdown]
# ## Cell 5.3: Local explanation for a specific sample
#
# Build a per-sample breakdown table of feature values and their SHAP contributions.

# %%
# Table: feature value, SHAP value, and absolute SHAP for sample 5.
sample_idx = 5
local_df = pd.DataFrame(
    {
        "feature_value": X_df.iloc[sample_idx].values,
        "shap_value": explanation.values[sample_idx],
        "abs_shap": np.abs(explanation.values[sample_idx]),
    },
    index=X_df.columns,
).sort_values("abs_shap", ascending=False)
display(local_df)

# %% [markdown]
# ## Cell 5.4: Global importance as a sorted DataFrame

# %%
# Global feature ranking by mean absolute SHAP.
global_importance_df = pd.DataFrame(
    {
        "feature": X_df.columns,
        "mean_abs_shap": np.abs(explanation.values).mean(axis=0),
        "mean_shap": explanation.values.mean(axis=0),
    }
).sort_values("mean_abs_shap", ascending=False)
display(global_importance_df)

# %% [markdown]
# # Part 6: API Patterns

# %% [markdown]
# ## Cell 6.1: Fit-explain pattern
#
# The standard SHAP workflow: train model -> create explainer -> call on data.

# %%
# Train, wrap, explain in three lines.
m = DecisionTreeRegressor(max_depth=2, random_state=0)
m.fit(X_df, y_s)
expl = shap.TreeExplainer(m)
expl_vals = expl(X_df)
print("expl_vals.values.shape=", expl_vals.values.shape)

# %% [markdown]
# ## Cell 6.2: Slicing and indexing pattern

# %%
# Slice by sample index -> one sample's explanation.
s3 = explanation[3]
print("explanation[3].values=", s3.values)

# %%
# Slice by feature name -> all samples for that feature.
debt_shap = explanation[:, "debt"]
print("explanation[:, 'debt'].values.shape=", debt_shap.values.shape)

# %%
# Slice by both -> scalar SHAP value.
scalar_val = explanation[3, "income"]
print("explanation[3, 'income'].values=", scalar_val.values)

# %% [markdown]
# ## Cell 6.3: Background data summary with shap.kmeans

# %%
# Summarize X_df into k representative rows for use in KernelExplainer.
bg_3 = shap.kmeans(X_df, k=3)
print("type(bg_3)=", type(bg_3))
print("bg_3.data.shape=", bg_3.data.shape)
display(pd.DataFrame(bg_3.data, columns=X_df.columns))

# %% [markdown]
# # Part 7: Interactive Exploration

# %% [markdown]
# ## Cell 7.1: What does the Explanation object expose?

# %%
# Inspect public interface of the Explanation object.
hintros.print_public_methods(explanation, use_markdown=True)

# %% [markdown]
# ## Cell 7.2: What happens if you use a different sample?
#
# Each sample gets its own SHAP values - waterfall plots differ by sample.

# %%
# Waterfall for sample 10 vs sample 0.
shap.plots.waterfall(explanation[10])
plt.close("all")

# %%
# Build a comparison: SHAP values for sample 0 vs sample 10.
compare_df = pd.DataFrame(
    {
        "sample_0": explanation[0].values,
        "sample_10": explanation[10].values,
    },
    index=X_df.columns,
)
display(compare_df)

# %% [markdown]
# ## Cell 7.3: What is the sign of SHAP values?
#
# Positive SHAP -> feature increases prediction above baseline.
# Negative SHAP -> feature decreases prediction below baseline.

# %%
# Count positive vs negative SHAP values per feature across all samples.
sign_df = pd.DataFrame(
    {
        "n_positive": (explanation.values > 0).sum(axis=0),
        "n_negative": (explanation.values < 0).sum(axis=0),
    },
    index=X_df.columns,
)
display(sign_df)

# %% [markdown]
# # Part 8: Summary
#
# ## Summary: The Mental Model
#
# - **`Explainer` variants**: `TreeExplainer` (fastest, exact for trees),
#   `LinearExplainer` (exact for linear models), `KernelExplainer` (any callable,
#   slowest), and `shap.Explainer` (auto-dispatches) - all share the same
#   interface: call with data, get back an `Explanation`
# - **`Explanation` object**: the central data structure with three arrays:
#   `.values` (SHAP contributions, shape `(n_samples, n_features)`),
#   `.base_values` (model's average prediction), and `.data` (input feature values)
# - **Additive decomposition**: `prediction[i] = base_values[i] + values[i].sum()`
#   holds exactly - SHAP values are a faithful partition of each prediction
# - **Plots**: `waterfall` for single-prediction breakdown, `bar` for global
#   magnitude ranking, `beeswarm` for global distribution with direction, and
#   `scatter` for feature-level dependence analysis
