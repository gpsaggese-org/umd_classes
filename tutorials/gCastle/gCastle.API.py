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
# # gCastle API Overview
#
# This notebook explores the core APIs and components of gCastle,
# a causal structure learning toolchain by Huawei Noah's Ark Lab.
#
# We'll learn how to:
# - Generate synthetic causal data with known ground truth
# - Run various causal discovery algorithms
# - Evaluate results using standard metrics
# - Visualize learned causal structures

# %% [markdown]
# ## Setup

# %%
# Load extension for auto-reload on edit.
# %load_ext autoreload
# %autoreload 2
# %matplotlib inline

import logging
import warnings

logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)
warnings.filterwarnings("ignore")

# %%
import helpers.hnotebook as hnotebo

hnotebo.config_notebook()

# %%
import castle

print(castle.__name__)
print("Version:", castle.__version__)

# %%
import tutorials.gCastle.gCastle_utils as tgcasti

# %% [markdown]
# ## Cell 1: Data Generation
#
# gCastle provides utilities to generate synthetic causal data with known DAGs.
# This is essential for testing and validating causal discovery algorithms.

# %%
# Generate synthetic data with interactive parameters.
data, true_dag = tgcasti.cell1_data_generation_interactive()

# print(f"\nGenerated data shape: {data.shape}")
# print(f"Data columns: {list(data.columns)}")
# print(f"\nTrue DAG adjacency matrix:")
# print(true_dag)

# %%
# The DAG visualization is shown interactively in the previous cell.

# %% [markdown]
# ## Cell 2: Constraint-Based Algorithm (PC)
#
# The PC (Peter-Clark) algorithm is a constraint-based approach that uses
# conditional independence tests to discover causal relationships. The key
# parameter is **alpha** (significance level): higher values → fewer edges detected.</cell_type="markdown">
# </invoke>

# %%
tgcasti.cell2_pc_algorithm_interactive(data.values, true_dag)

# %%
# Compute PC metrics with default alpha for later use
pc_adjacency = tgcasti.run_pc_algorithm(data.values, alpha=0.05)
pc_metrics = tgcasti.evaluate_causal_discovery(true_dag, pc_adjacency)

# %% [markdown]
# ## Cell 3: Score-Based Algorithm (GES)
#
# GES (Greedy Equivalence Search) uses a score-based approach,
# optimizing a score function over equivalence classes.

# %%
# Run the GES algorithm.
ges_adjacency = tgcasti.run_ges_algorithm(data.values)
ges_metrics = tgcasti.evaluate_causal_discovery(true_dag, ges_adjacency)

tgcasti.cell3_ges_algorithm_interactive(data.values, true_dag)

# %%
# Metrics already computed in previous cell - shown in visualization above

# %% [markdown]
# ## Cell 4: Gradient-Based Algorithms
#
# NOTEARS (No-Tears) and GOLEM are modern gradient-based algorithms
# that can handle large-scale problems efficiently.

# %%
# Run NOTEARS algorithm with L2 loss (linear relationships).
notears_adjacency = tgcasti.run_notears_algorithm(
    data.values,
    lambda1=0.0,
    loss_type="l2",
)
notears_metrics = tgcasti.evaluate_causal_discovery(true_dag, notears_adjacency)

tgcasti.cell4_notears_algorithm_interactive(data.values, true_dag)
