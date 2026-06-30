# ---
# jupyter:
#   jupytext:
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
# # LIME API
#
# A guided exploration of LIME (Local Interpretable Model-agnostic Explanations):
# - **Explainer**: wraps a trained ML model and perturbs feature space locally
# - **Explanation**: holds feature weights from local linear surrogate and local accuracy
# - **Plots**: visualize feature contributions for a single prediction (not global)

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
import lime
import lime.lime_tabular

import sklearn.datasets
import sklearn.linear_model
import sklearn.ensemble

warnings.filterwarnings("ignore")

# %%
import helpers.hdbg as hdbg
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
#   - Modern ML models (tree ensembles, neural nets, black-box models) are accurate but opaque
#   - LIME answers "why did the model predict X?" for a single prediction by building a local interpretable surrogate
#   - Creates a linear approximation around a single instance by perturbing features
#
# - **Key abstraction**:
#   - For one prediction: perturb feature values around the instance
#   - Get model predictions for perturbed samples
#   - Fit a local weighted linear model on perturbations -> reveals feature weights
#   - Feature weights show which features matter locally

# %% [markdown]
# - **Mental model**:
# // TODO(ai_gp): Make this into a markdown table (object, description, comments)
#   - model: X -> prediction
#   - LimeTabularExplainer(model, X_train) -> configured explainer
#   - explainer.explain_instance(x) -> Explanation
#   - Explanation object:
#     - .as_list(): list of (feature, weight) tuples
#     - .as_pyplot_figure(): visualization of feature weights
#     - local_pred: model prediction on weighted perturbations
#     - score: R^2 accuracy of local linear model
#
# - **Key classes**:
#   - `lime.lime_tabular.LimeTabularExplainer`: main explainer for tabular data (used throughout this notebook)
#   - `lime.lime_image.LimeImageExplainer`: for image data
#   - `lime.lime_text.LimeTextExplainer`: for text data
#   - Explanation object: result from `.explain_instance()` (feature weights, local accuracy)

# %% [markdown]
# # Part 1: Toy Data Setup

# %% [markdown]
# ## Cell 1.1: Create a toy regression dataset
#
# **Goal**:
# - Build the minimal dataset needed to explore all LIME primitives
# - Use regression (not classification) to keep interpretations simple and 2D

# %%
# Four named features, 30 samples, pure regression target.
np.random.seed(42)
X, y = sklearn.datasets.make_regression(
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
# TODO(ai_gp): Split this into 3 cells.
# Data analysis: feature statistics and correlations with target.
print("=== Feature Statistics ===")
print(X_df.describe())

print("\n=== Correlations with target ===")
corr_with_target = X_df.corrwith(y_s).sort_values(ascending=False)
display(corr_with_target)

print("\n=== Feature Correlations ===")
display(X_df.corr())

# %% [markdown]
# ## Cell 1.2: Train a linear regression model
#
# **Goal**:
# - Train a `LinearRegression` model on the toy dataset
# - This is the single model we will explain end-to-end throughout the notebook

# %%
# Train linear regression model.
linear_model = sklearn.linear_model.LinearRegression()
linear_model.fit(X_df, y_s)
print("linear_model=", linear_model)

# %%
# Show linear model coefficients and intercept.
coef_df = pd.DataFrame({
    "feature": X_df.columns,
    "coefficient": linear_model.coef_,
})
coef_df["abs_coef"] = np.abs(coef_df["coefficient"])
display(coef_df.sort_values("abs_coef", ascending=False))
print(f"Intercept: {linear_model.intercept_:.6f}")

# %% [markdown]
# # Part 2: Primitive 1 - The Explainer

# %% [markdown]
# ## Cell 2.1: Construct a LimeTabularExplainer
#
# **Mental model**:
# - `LimeTabularExplainer` wraps a model and feature statistics from training data
# - Training data defines feature ranges and distributions used to perturb instances
# - For each explanation request, LIME perturbs features around a single instance, fits a local linear model
# - The local model's coefficients become feature importance weights

# %%
# Construct LimeTabularExplainer with model and training data.
lime_explainer = lime.lime_tabular.LimeTabularExplainer(
    X_df.values,
    feature_names=X_df.columns.tolist(),
    verbose=False,
    mode="regression",
)
print("type(lime_explainer)=", type(lime_explainer))
print("lime_explainer.feature_names=", lime_explainer.feature_names)

# %% [markdown]
# ## Cell 2.2: Inspect the LimeTabularExplainer
#
# **Goal**:
# - Understand what the explainer knows about the data
# - Feature ranges and statistics used for perturbation

# %% [markdown]
# # Part 3: Primitive 2 - The Explanation Object

# %% [markdown]
# ## Explanation Object: Local Interpretable Model Breakdown
#
# An `Explanation` object holds results from explaining a single instance:
# 1. `.as_list()`: list of (feature_name, weight) tuples
#    - Each weight shows how much a feature pushed the prediction away from baseline
#    - Positive weight = feature increases prediction
#    - Negative weight = feature decreases prediction
#    - Weight magnitude = how much this feature influenced the local decision
#
# 2. `.local_pred`: Model's prediction on the instance
#    - Same as the original prediction for the instance
#
# 3. `.score`: R^2 accuracy of the local linear model
#    - How well does the linear approximation fit the model's behavior locally?
#    - Closer to 1.0 = linear approximation is accurate
#    - Closer to 0 = model is highly nonlinear near this instance
#
# **Key insight**: Unlike SHAP (which provides a global game-theoretic decomposition), LIME provides a **local** linear interpretation. Each explanation is valid only for instances near the explained point.

# %% [markdown]
# ## Cell 3.1: Explain a single instance using the explainer
#
# **Mental model**:
# - Calling `explainer.explain_instance(x, model.predict)` returns an `Explanation` object
# - LIME perturbs features around `x`, gets model predictions for perturbed samples
# - Fits a local weighted linear model: weights favor instances closer to `x`
# - The linear model's coefficients = feature importance for this instance

# %%
# Explain instance 0 using the trained linear model.
# This will perturb features and fit a local linear surrogate.
instance_idx = 0
explanation = lime_explainer.explain_instance(
    X_df.iloc[instance_idx].values,
    linear_model.predict,
    num_features=4,
)
print("type(explanation)=", type(explanation))

# %% [markdown]
# ## Cell 3.2: Inspect explanation.as_list()
#
# **Goal**:
# - Extract feature names and their weights from the local linear model
# - Understand which features matter locally for this prediction

# %%
# Extract feature weights as a list of (feature_name, weight) tuples.
feature_weights = explanation.as_list()
print("Feature weights (as_list):")
for feature_name, weight in feature_weights:
    print(f"  {feature_name}: {weight:.4f}")

# Convert to DataFrame for easier inspection.
weights_df = pd.DataFrame(
    [(fname, weight) for fname, weight in feature_weights],
    columns=["feature", "weight"]
)
weights_df["abs_weight"] = np.abs(weights_df["weight"])
display(weights_df.sort_values("abs_weight", ascending=False))

# %% [markdown]
# ## Cell 3.3: Inspect explanation local prediction and local model accuracy
#
# **Goal**:
# - Verify the model's actual prediction for this instance
# - Check how well the local linear model approximates the true model

# %%
# Local prediction and model accuracy.
actual_prediction = linear_model.predict(X_df.iloc[[instance_idx]])[0]
print(f"Actual model prediction: {actual_prediction:.6f}")
print(f"Explanation.local_pred: {explanation.local_pred[0]:.6f}")
print(f"Local model R^2 score: {explanation.score:.6f}")
print(f"\nInterpretation:")
print(f"  R^2 = {explanation.score:.4f} means the local linear model explains {explanation.score*100:.1f}% of variance.")
print(f"  Higher R^2 -> linear approximation is accurate locally.")

# %% [markdown]
# ## Cell 3.4: Build a full instance explanation table
#
# **Goal**:
# - Show feature value, LIME weight, and contribution for a single instance
# - Understand how feature values and weights combine locally

# %%
# Build a comprehensive explanation table for the instance.
instance_values = X_df.iloc[instance_idx].values
feature_names = X_df.columns.tolist()

# Extract weights in same order as features.
weights_dict = dict(explanation.as_list())
lime_weights = [weights_dict.get(fname, 0.0) for fname in feature_names]

explanation_table = pd.DataFrame({
    "feature": feature_names,
    "value": instance_values,
    "lime_weight": lime_weights,
    "abs_weight": np.abs(lime_weights),
})
explanation_table = explanation_table.sort_values("abs_weight", ascending=False)
display(explanation_table)

# %% [markdown]
# # Part 4: Primitive 3 - Visualization

# %% [markdown]
# ## Cell 4.1: Visualize local explanation as a bar chart
#
# **Goal**:
# - See which features pushed the prediction up or down for this instance
# - Horizontal bar chart: feature name vs local weight (positive = up, negative = down)

# %%
# Visualize explanation as a pyplot figure.
fig = explanation.as_pyplot_figure()
fig.set_size_inches(10, 5)
plt.tight_layout()
plt.show()
plt.close('all')

# %% [markdown]
# **Key observations**:
# - Each horizontal bar = one feature's LIME weight (contribution to local prediction)
# - Green/right: feature pushes prediction up
# - Red/left: feature pushes prediction down
# - Bar length = magnitude of local influence
# - This is instance-specific: another instance will have different weights

# %% [markdown]
# ## Cell 4.2: Manual feature importance bar plot
#
# **Goal**:
# - Create a custom bar plot showing feature weights for the explained instance
# - Compare positive and negative contributions

# %%
# Create a bar plot of LIME feature weights.
fig, ax = plt.subplots(figsize=(10, 5))

# Get feature names and weights in order of absolute magnitude.
feature_weight_list = explanation.as_list()
feature_names_sorted = [fname for fname, _ in sorted(feature_weight_list, key=lambda x: abs(x[1]), reverse=True)]
weights_sorted = [weight for _, weight in sorted(feature_weight_list, key=lambda x: abs(x[1]), reverse=True)]

# Color based on sign.
colors = ['green' if w > 0 else 'red' for w in weights_sorted]

ax.barh(feature_names_sorted, weights_sorted, color=colors, alpha=0.7)
ax.set_xlabel("Feature Weight (Local Importance)")
ax.set_title(f"LIME Local Explanation - Instance {instance_idx}")
ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.show()
plt.close('all')

# %% [markdown]
# **Key observations**:
# - Green bars: features that increase the prediction locally
# - Red bars: features that decrease the prediction locally
# - Sorted by absolute weight magnitude
# - This is a **local** explanation: only valid near instance {instance_idx}

# %% [markdown]
# # Part 5: API Patterns

# %% [markdown]
# ## Cell 5.1: Explain multiple instances and compare local explanations
#
# **Goal**:
# - Show that LIME explanations are instance-specific
# - Same features have different weights for different instances

# %%
# Explain three different instances and compare their feature weights.
instances_to_explain = [0, 5, 10]
explanations = {}

for idx in instances_to_explain:
    exp = lime_explainer.explain_instance(
        X_df.iloc[idx].values,
        linear_model.predict,
        num_features=4,
    )
    explanations[idx] = exp

# Compare weights across instances.
comparison_data = []
for idx in instances_to_explain:
    exp = explanations[idx]
    weights_dict = dict(exp.as_list())
    pred = linear_model.predict(X_df.iloc[[idx]])[0]
    for fname in X_df.columns:
        comparison_data.append({
            "instance": idx,
            "feature": fname,
            "weight": weights_dict.get(fname, 0.0),
            "prediction": pred,
        })

comparison_df = pd.DataFrame(comparison_data)
print("\nComparison of LIME weights across instances:")
display(comparison_df.pivot(index="feature", columns="instance", values="weight").round(3))

# %% [markdown]
# ## Cell 5.2: Extract prediction and confidence for a single instance
#
# **Goal**:
# - Show how to extract prediction, local accuracy, and feature list programmatically

# %%
# Extract explanation details programmatically.
sample_idx = 5
exp = lime_explainer.explain_instance(
    X_df.iloc[sample_idx].values,
    linear_model.predict,
    num_features=4,
)

# Prediction and confidence.
actual_pred = linear_model.predict(X_df.iloc[[sample_idx]])[0]
local_r2 = exp.score
feature_weights = exp.as_list()

print(f"Instance {sample_idx}:")
print(f"  Actual prediction: {actual_pred:.4f}")
print(f"  Local R^2 score: {local_r2:.4f} (linear approximation accuracy)")
print(f"  Top feature weights:")
for fname, weight in sorted(feature_weights, key=lambda x: abs(x[1]), reverse=True):
    print(f"    {fname}: {weight:+.4f}")

# %% [markdown]
# ## Cell 5.3: Compare LIME weights with model coefficients
#
# **Goal**:
# - For a linear model, LIME weights should align with model coefficients
# - For nonlinear models, they can differ due to local nonlinearity

# %%
# Compare LIME weights to the model's global coefficients.
# For linear models, they should be similar.

# Global model coefficients.
global_coef = dict(zip(X_df.columns, linear_model.coef_))

# Local LIME weights for instance 0.
exp_inst0 = lime_explainer.explain_instance(
    X_df.iloc[0].values,
    linear_model.predict,
    num_features=4,
)
local_weights = dict(exp_inst0.as_list())

# Compare.
comparison = pd.DataFrame({
    "feature": X_df.columns,
    "model_coef": [global_coef[fname] for fname in X_df.columns],
    "lime_weight_inst0": [local_weights.get(fname, 0.0) for fname in X_df.columns],
})
comparison["difference"] = comparison["model_coef"] - comparison["lime_weight_inst0"]
display(comparison.round(3))
print("\nNote: For linear models, LIME weights are typically close to model coefficients.")
print("For nonlinear models, local weights can differ significantly.")

# %% [markdown]
# # Part 6: LIME vs Other Explainers
#
# ## Key Differences
#
# ### LIME (This notebook)
# - **Approach**: Local linear approximation via perturbation
# - **Scope**: Instance-specific (local) explanations only
# - **Model dependency**: Model-agnostic; works with any black-box model
# - **Computation**: Perturb features, fit local linear model
# - **Output**: Feature weights from local surrogate
# - **Global patterns**: Cannot explain patterns across the dataset
# - **Nonlinearity handling**: Approximates locally; captures local nonlinearity
#
# ### SHAP (Available in parallel SHAP notebook)
# - **Approach**: Game-theoretic Shapley values
# - **Scope**: Can be local or global depending on explainer type
# - **Model dependency**: Some explainers are model-specific (TreeExplainer), others model-agnostic (KernelExplainer)
# - **Computation**: Exact for trees/linear, approximate for others via kernel method
# - **Output**: Shapley values (theoretically grounded, satisfies axioms)
# - **Global patterns**: Can compute global importance via mean(|values|)
# - **Nonlinearity handling**: Works on full problem; provides exact (tree) or approximate (kernel) solution
#
# ### When to Use LIME
# 1. **Black-box models**: When you have a model you cannot inspect (neural networks, API-based models, proprietary models)
# 2. **Simplicity**: When you need simple, fast local explanations
# 3. **Limited training data**: LIME requires only the instance being explained and model access
# 4. **Trust building**: To explain individual predictions to stakeholders
#
# ### When to Use SHAP
# 1. **Theoretical grounding**: When you want theoretically justified feature attributions
# 2. **Global insights**: When you need to understand feature importance across the dataset
# 3. **Model-specific**: When you have trees or linear models (TreeExplainer is exact and fast)
# 4. **Rich visualizations**: When you need beeswarm, scatter, and dependence plots

# %% [markdown]
# # Part 7: Summary
#
# ## Summary: The Mental Model
#
# - **LimeTabularExplainer (main focus)**: Wraps a model and training data; for each explanation, perturbs features locally around an instance, fits a weighted linear surrogate, and extracts feature weights from the surrogate. Requires only model access (black-box agnostic).
#
# - **Explanation object**: The central data structure from `.explain_instance()` with three key methods:
#   - `.as_list()`: list of (feature_name, weight) tuples showing local importance
#   - `.as_pyplot_figure()`: visualization of feature contributions
#   - `.score`: R^2 accuracy of the local linear approximation (how well does the linear model capture the true model's behavior locally?)
#
# - **Local interpretation**: LIME is fundamentally **local**: each explanation is valid only for instances near the explained point. Different instances can have very different feature weights, even for the same model and dataset.
#
# - **Perturbation-based**: LIME works by sampling perturbed versions of the instance (varying each feature randomly), getting model predictions for each perturbation, and fitting a weighted linear model (weights favor instances closer to the original).
#
# - **Model-agnostic**: LIME treats the model as a black box; only requires a predict function. Works with any model type: neural networks, random forests, ensemble methods, or even external APIs.
#
# - **Comparison to SHAP**: LIME is local and approximate; SHAP is game-theoretic and provides global insights. For black-box models or quick instance explanations, LIME is simpler. For global feature importance or model-specific explainers, SHAP is more powerful.
