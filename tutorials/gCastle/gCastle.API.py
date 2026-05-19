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
# # gCastle API Overview
#
# This notebook explores the core components and API of gCastle, a causal structure learning library by Huawei Noah's Ark Lab.
#
# **What you'll learn:**
# - How to generate synthetic causal data
# - How to run causal discovery algorithms
# - How to evaluate causal discovery results
# - How to visualize causal graphs

# %% Setup
import logging
import numpy as np
import matplotlib.pyplot as plt

import tutorials.gCastle.gCastle_utils as tgcutil

logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)

plt.rcParams['figure.figsize'] = (10, 6)

# %% [markdown]
# ## Data Generation
#
# Generate synthetic data from a linear Gaussian causal model with a random DAG.

# %% Generate data
np.random.seed(42)

num_samples = 500
num_vars = 5
edge_density = 0.4

data, true_dag = tgcutil.generate_linear_gaussian_data(
    num_samples=num_samples,
    num_vars=num_vars,
    edge_density=edge_density,
    random_state=42
)

print(f"Data shape: {data.shape}")
print(f"Number of edges in true DAG: {len(true_dag.edges())}")
print(f"Edges: {list(true_dag.edges())}")

# %% [markdown]
# ### Visualize True Causal Graph

# %% Plot true DAG
true_adj = tgcutil.dag_to_adjacency(true_dag, num_vars)
tgcutil.plot_dag(true_adj, title="True Causal Graph")
plt.show()

# %% [markdown]
# ## Data Normalization
#
# Most causal discovery algorithms benefit from normalized data.

# %% Normalize
normalized_data = tgcutil.normalize_data(data)

print(f"Data mean: {normalized_data.mean(axis=0).round(4)}")
print(f"Data std: {normalized_data.std(axis=0).round(4)}")

# %% [markdown]
# ## Evaluation Metrics
#
# Key metrics for evaluating causal discovery:
# - **FDR** (False Discovery Rate): Proportion of incorrectly discovered edges
# - **TPR** (True Positive Rate): Proportion of correctly discovered edges
# - **FPR** (False Positive Rate): Proportion of incorrect edges among non-edges
# - **SHD** (Structural Hamming Distance): Total number of differences

# %% Compute metrics
estimated_adj = np.zeros((num_vars, num_vars))
if true_adj[0, 1] == 1:
    estimated_adj[0, 1] = 1
estimated_adj[1, 2] = 1

metrics = tgcutil.compute_dag_metrics(estimated_adj, true_adj)

print("Metrics:")
for metric_name, metric_value in metrics.items():
    print(f"  {metric_name}: {metric_value:.4f}")

# %% [markdown]
# ## Causal Discovery Algorithms
#
# gCastle provides various algorithms for causal structure learning:
# - **LiNGAM**: Linear Non-Gaussian Acyclic Model
# - **GES**: Greedy Equivalence Search
# - **PC**: PC algorithm (constraint-based)
# - **NOTEARS**: Neural Ordered Transforms for Acyclic Relationships

# %% Import algorithms
from gcastle.algorithms import LinearGES, PC

algorithms = {
    "LinearGES": (LinearGES, {}),
    "PC": (PC, {"alpha": 0.05}),
}

# %% [markdown]
# ### Run and Compare Algorithms

# %% Compare algorithms
_LOG.info("Running causal discovery algorithms...")
results_df = tgcutil.compare_algorithms(
    normalized_data,
    true_adj,
    algorithms
)

print("\nComparison Results:")
print(results_df.to_string(index=False))

# %% [markdown]
# ### Visualize Results

# %% Plot comparison
tgcutil.plot_comparison_metrics(
    results_df,
    metrics_to_plot=["fdr", "tpr", "shd"]
)
plt.show()
