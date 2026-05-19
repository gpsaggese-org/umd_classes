# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # gCastle: Discovering Causality in Real Data
#
# This notebook demonstrates a complete causal discovery workflow using gCastle on a synthetic dataset simulating a real-world scenario.

# %% Setup
import logging

import matplotlib.pyplot as plt
import numpy as np

import tutorials.gCastle.gCastle_utils as tgcutil

logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)

plt.rcParams['figure.figsize'] = (12, 8)

# %% [markdown]
# ## Problem: Understanding Causal Relationships
#
# In this example, we have a dataset with 6 variables that may have causal relationships. Our goal is to:
# 1. Generate synthetic data with known ground truth
# 2. Apply multiple causal discovery algorithms
# 3. Evaluate which algorithm best recovers the true causal structure
# 4. Visualize and interpret the results

# %% [markdown]
# ## Part 1: Data Preparation

# %% Generate data
np.random.seed(2024)

num_samples = 1000
num_vars = 6
edge_density = 0.35

_LOG.info(f"Generating {num_samples} samples with {num_vars} variables...")
data, true_dag = tgcutil.generate_linear_gaussian_data(
    num_samples=num_samples,
    num_vars=num_vars,
    edge_density=edge_density,
    random_state=2024
)

true_adj = tgcutil.dag_to_adjacency(true_dag, num_vars)

print(f"\nDataset Summary:")
print(f"  Shape: {data.shape}")
print(f"  True causal edges: {int(true_adj.sum())}")
print(f"  Variables: {list(range(num_vars))}")

# %% [markdown]
# ### Visualize Ground Truth Causal Graph

# %% Plot true graph
tgcutil.plot_dag(true_adj, title="Ground Truth Causal Graph")
plt.tight_layout()
plt.show()

# %% [markdown]
# ### Normalize Data

# %% Normalize
_LOG.info("Normalizing data...")
normalized_data = tgcutil.normalize_data(data)

print(f"Normalized data statistics:")
print(f"  Mean (should be ~0): {normalized_data.mean(axis=0).mean():.6f}")
print(f"  Std (should be ~1): {normalized_data.std(axis=0).mean():.6f}")

# %% [markdown]
# ## Part 2: Causal Discovery

# %% Setup algorithms
from gcastle.algorithms import LinearGES, PC

algorithms = {
    "LinearGES": (LinearGES, {}),
    "PC (α=0.05)": (PC, {"alpha": 0.05}),
    "PC (α=0.01)": (PC, {"alpha": 0.01}),
}

print(f"Running {len(algorithms)} algorithms...\n")

# %% Run discovery
results_df = tgcutil.compare_algorithms(
    normalized_data,
    true_adj,
    algorithms
)

print("\n" + "="*60)
print("CAUSAL DISCOVERY RESULTS")
print("="*60)
print(results_df.to_string(index=False))
print("="*60)

# %% [markdown]
# ### Identify Best Algorithm

# %% Best result
best_idx = results_df['shd'].idxmin()
best_algo = results_df.loc[best_idx, 'algorithm']
best_shd = results_df.loc[best_idx, 'shd']

print(f"\nBest performing algorithm: {best_algo}")
print(f"  Structural Hamming Distance (SHD): {best_shd:.0f}")
print(f"  TPR: {results_df.loc[best_idx, 'tpr']:.4f}")
print(f"  FDR: {results_df.loc[best_idx, 'fdr']:.4f}")

# %% [markdown]
# ## Part 3: Evaluation and Visualization

# %% [markdown]
# ### Performance Comparison

# %% Plot metrics
tgcutil.plot_comparison_metrics(
    results_df,
    metrics_to_plot=["fdr", "tpr", "shd"],
    figsize=(14, 4)
)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Part 4: Interpretation and Insights
#
# ### Key Findings:
#
# 1. **Algorithm Performance**: Different algorithms achieve different trade-offs between precision (FDR) and recall (TPR)
# 2. **Parameter Sensitivity**: The PC algorithm shows sensitivity to the significance level (α)
# 3. **Causal Discovery Challenges**: Perfect recovery is rarely achieved; algorithms make trade-offs
#
# ### When to Use Each Algorithm:
#
# - **LinearGES**: Good general-purpose choice for linear relationships
# - **PC**: Constraint-based approach; sensitive to threshold parameters
# - **NOTEARS**: Better for nonlinear relationships

# %% Summary
print("\nSUMMARY:")
print("==========" )
print(f"Successfully discovered causal structure with {len(algorithms)} algorithms")
print(f"Best performance: {best_algo} with SHD = {best_shd:.0f}")
print("\nNext steps:")
print("1. Try different algorithms and parameters")
print("2. Use domain knowledge to refine results")
print("3. Validate discovered edges with domain experts")
