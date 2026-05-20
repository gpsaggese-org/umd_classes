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
# # gCastle: Discovering Market Structure
#
# This notebook demonstrates a complete causal discovery application:
# discovering the causal relationships between economic indicators.
#
# **Scenario**: Given time-series data of economic variables, identify
# which variables causally influence others. This is useful for:
# - Understanding economic dynamics
# - Policy analysis
# - Risk assessment
# - Forecasting

# %% [markdown]
# ## Setup

# %%
# Load extension for auto-reload on edit.
# %load_ext autoreload
# %autoreload 2
# %matplotlib inline

import logging
import warnings

import pandas as pd

import tutorials.gCastle.gCastle_utils as tgcasti

logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)
warnings.filterwarnings("ignore")

# %% [markdown]
# ## Part 1: Generate Economic Data
#
# We'll simulate a realistic economic system where variables have
# causal relationships, then discover these relationships.

# %%
# Generate synthetic economic data.
# Variables: GDP, Inflation, Unemployment, Interest_Rate, Stock_Market
n_nodes = 5
n_samples = 1000
node_names = [
    "GDP",
    "Inflation",
    "Unemployment",
    "Interest_Rate",
    "Stock_Market",
]

print(
    f"Generating {n_nodes}-variable economic system with {n_samples} observations..."
)

data, true_dag = tgcasti.generate_synthetic_data(
    n_nodes=n_nodes,
    n_edges=6,
    n_samples=n_samples,
    seed=123,
)

# Rename columns to meaningful names.
data.columns = node_names

print(f"\nGenerated data shape: {data.shape}")
print("\nData summary statistics:")
print(data.describe())

# %% [markdown]
# ## Part 2: Visualize the True Causal Structure
#
# Before running discovery algorithms, let's see what the ground truth DAG looks like.

# %%
# Visualize true causal relationships.
fig = tgcasti.visualize_dag(
    true_dag.to_numpy(),
    title="True Economic Causal Structure",
    node_labels=node_names,
    figsize=(10, 8),
)
print("This is the true causal structure we're trying to discover.")

# %% [markdown]
# ## Part 3: Run Multiple Discovery Algorithms

# %% [markdown]
# ### Constraint-Based Approach (PC)

# %%
# The PC algorithm uses statistical independence tests.
# It's robust but requires sufficient data.

_LOG.info("Running PC algorithm...")
pc_result = tgcasti.run_pc_algorithm(
    data.values,
    alpha=0.05,
)

pc_metrics = tgcasti.evaluate_causal_discovery(
    true_dag.to_numpy(),
    pc_result,
)

print("PC Algorithm Results:")
print(f"  F1 Score: {pc_metrics['F1']:.4f}")
print(f"  Structural Hamming Distance: {pc_metrics['SHD']:.1f}")
print(f"  False Discovery Rate: {pc_metrics['FDR']:.4f}")
print(f"  True Positive Rate: {pc_metrics['TPR']:.4f}")

# %% [markdown]
# ### Score-Based Approach (GES)

# %%
# GES optimizes a Bayesian score function.
# It's efficient and works well with moderate-sized datasets.

_LOG.info("Running GES algorithm...")
ges_result = tgcasti.run_ges_algorithm(data.values)

ges_metrics = tgcasti.evaluate_causal_discovery(
    true_dag.to_numpy(),
    ges_result,
)

print("GES Algorithm Results:")
print(f"  F1 Score: {ges_metrics['F1']:.4f}")
print(f"  Structural Hamming Distance: {ges_metrics['SHD']:.1f}")
print(f"  False Discovery Rate: {ges_metrics['FDR']:.4f}")
print(f"  True Positive Rate: {ges_metrics['TPR']:.4f}")

# %% [markdown]
# ### Gradient-Based Approach (NOTEARS)

# %%
# NOTEARS uses continuous optimization with acyclicity constraints.
# It's scalable and handles large datasets efficiently.

_LOG.info("Running NOTEARS algorithm...")
notears_result = tgcasti.run_notears_algorithm(
    data.values,
    lambda1=0.01,
    loss_type="l2",
)

notears_metrics = tgcasti.evaluate_causal_discovery(
    true_dag.to_numpy(),
    notears_result,
)

print("NOTEARS Algorithm Results:")
print(f"  F1 Score: {notears_metrics['F1']:.4f}")
print(f"  Structural Hamming Distance: {notears_metrics['SHD']:.1f}")
print(f"  False Discovery Rate: {notears_metrics['FDR']:.4f}")
print(f"  True Positive Rate: {notears_metrics['TPR']:.4f}")

# %% [markdown]
# ## Part 4: Thresholding Weighted Results
#
# Some algorithms return weighted edges. Apply a threshold to binarize them.

# %%
# Threshold the NOTEARS result (remove weak edges).
notears_binary = tgcasti.thresholded_dag(
    notears_result,
    threshold=0.2,
)

notears_binary_metrics = tgcasti.evaluate_causal_discovery(
    true_dag.to_numpy(),
    notears_binary,
)

print("NOTEARS (thresholded at 0.2):")
print(f"  F1 Score: {notears_binary_metrics['F1']:.4f}")
print(f"  Structural Hamming Distance: {notears_binary_metrics['SHD']:.1f}")

# %% [markdown]
# ## Part 5: Comprehensive Comparison

# %%
# Compare all discovered structures side-by-side.
algorithms_results = {
    "PC": pc_result,
    "GES": ges_result,
    "NOTEARS": notears_result,
}

fig = tgcasti.compare_dags(
    true_dag.to_numpy(),
    algorithms_results,
    node_labels=node_names,
)
fig.suptitle(
    "Causal Discovery Results: Economic Indicators",
    fontsize=14,
    fontweight="bold",
)

# %% [markdown]
# ## Part 6: Performance Summary

# %%
# Create a comprehensive performance comparison.
comparison_data = {
    "Algorithm": ["PC", "GES", "NOTEARS", "NOTEARS*"],
    "F1": [
        pc_metrics["F1"],
        ges_metrics["F1"],
        notears_metrics["F1"],
        notears_binary_metrics["F1"],
    ],
    "SHD": [
        pc_metrics["SHD"],
        ges_metrics["SHD"],
        notears_metrics["SHD"],
        notears_binary_metrics["SHD"],
    ],
    "TPR": [
        pc_metrics["TPR"],
        ges_metrics["TPR"],
        notears_metrics["TPR"],
        notears_binary_metrics["TPR"],
    ],
    "FDR": [
        pc_metrics["FDR"],
        ges_metrics["FDR"],
        notears_metrics["FDR"],
        notears_binary_metrics["FDR"],
    ],
}

comparison_df = pd.DataFrame(comparison_data)
print("\nPerformance Comparison Table")
print("(* = NOTEARS with thresholding)")
print(comparison_df.to_string(index=False))

# %% [markdown]
# ## Part 7: Interpreting Results
#
# The different algorithms have different strengths:
#
# - **PC (Constraint-based)**: Good for understanding independence structure
# - **GES (Score-based)**: Efficient and works well with modest sample sizes
# - **NOTEARS (Gradient-based)**: Highly scalable for large datasets
#
# The best algorithm depends on your data characteristics and problem constraints.

# %% [markdown]
# ## Summary
#
# In this notebook, we:
#
# 1. Generated a synthetic economic system with known causal structure
# 2. Applied three major classes of causal discovery algorithms
# 3. Compared their performance using standard evaluation metrics
# 4. Demonstrated how to threshold weighted results
# 5. Analyzed the trade-offs between different approaches
#
# Key takeaways:
# - Causal discovery is challenging; no single algorithm works best for all scenarios
# - Different algorithms make different assumptions and have different computational profiles
# - Evaluation metrics (F1, SHD, TPR, FDR) help assess discovery quality
# - gCastle provides a unified interface for comparing multiple approaches
#
# For more advanced topics, explore gCastle's documentation and consider:
# - Different loss types (nonlinear relationships)
# - Regularization parameters (lambda)
# - Hybrid approaches combining multiple algorithms
# - Real-world data applications
