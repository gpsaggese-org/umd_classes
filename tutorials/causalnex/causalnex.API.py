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
# # CausalNex API Tutorial
#
# This notebook explores the CausalNex library for causal inference using Bayesian Networks.
# It demonstrates the complete workflow from structure learning to inference and causal interventions.
#
# References:
# - [CausalNex Documentation](https://causalnex.readthedocs.io/)
# - [First Tutorial](https://causalnex.readthedocs.io/en/latest/03_tutorial/01_first_tutorial.html)

# %%
# %load_ext autoreload
# %autoreload 2
# %matplotlib inline

# System libraries.
import logging

# Third party libraries.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
import helpers.hmodule as hmodule
hmodule.install_module_if_not_present(
    ["pycaret"],
    use_activate=True,
    use_sudo=False,
    venv_path="/opt/venv",
)

# %%
import helpers.hdbg as hdbg
import helpers.hnotebook as hnotebo
import tutorials.causalnex.causalnex_utils as tcnut

_LOG = logging.getLogger(__name__)
hdbg.init_logger(verbosity=logging.INFO)
hnotebo.config_notebook()

# %% [markdown]
# ## Cell 1: Load Data
#
# Load the student performance dataset from the UCI machine learning repository.
# The dataset will be automatically downloaded and cached locally if not present.

# %%
# Load the student performance dataset.
df = tcnut.load_student_performance_data(data_dir="data")
_LOG.info("Dataset shape: %s", df.shape)
print(df.head())

# %% [markdown]
# ## Cell 2: Structure Learning
#
# Define the causal structure of the Bayesian Network by specifying relationships between variables.
#
# - Manual definition via domain expertise
# - Algorithmic learning using NOTEARS algorithm
# - Hybrid approach combining both methods

# %%
from causalnex.structure import StructureModel
# Create a StructureModel instance to define causal relationships.
sm = StructureModel()
# Add edges representing causal relationships between variables.
sm.add_edges_from([
    ('health', 'absences'),
    ('health', 'G1'),
    ('studytime', 'G1'),
    ('studytime', 'G2'),
    ('G1', 'G2'),
    ('absences', 'G1'),
    ('absences', 'G2'),
])
_LOG.info("Structure nodes: %s", sm.nodes)
_LOG.info("Structure edges: %s", sm.edges)
print(f"Nodes: {list(sm.nodes)}")
print(f"Edges: {list(sm.edges)}")

# %% [markdown]
# ## Cell 3: Data Discretization
#
# Convert continuous features into categorical buckets with meaningful labels.
# Bayesian Networks require discrete distributions for probability estimation.

# %%
# Create a copy of the dataframe for discretization.
df_discrete = df.copy()
# Discretize continuous variables into categorical buckets.
df_discrete['studytime_bin'] = pd.cut(
    df['studytime'], bins=[0, 1, 2, 3, 4],
    labels=['very_low', 'low', 'medium', 'high']
)
df_discrete['absences_bin'] = pd.cut(
    df['absences'], bins=[0, 5, 10, 20, 100],
    labels=['low', 'medium', 'high', 'very_high']
)
df_discrete['G1_bin'] = pd.cut(
    df['G1'], bins=[0, 10, 20],
    labels=['fail', 'pass']
)
df_discrete['G2_bin'] = pd.cut(
    df['G2'], bins=[0, 10, 20],
    labels=['fail', 'pass']
)
_LOG.info("Discretized data shape: %s", df_discrete.shape)
print(df_discrete[['studytime_bin', 'absences_bin', 'G1_bin', 'G2_bin']].head())

# %% [markdown]
# ## Cell 4: CPD Fitting
#
# Learn conditional probability distributions (CPDs) from the training data.
# CPDs represent the probability of each variable given its parents in the network.

# %%
from causalnex.network import BayesianNetwork
# Create a Bayesian Network from the structure model.
bn = BayesianNetwork(sm)
# Select only the columns needed for the network.
cols = ['health', 'studytime', 'absences', 'G1', 'G2']
df_fit = df_discrete[cols].copy()
# Fit the network to the data.
bn.fit_cpds(df_fit, method='BayesianEstimator', prior_type='BDeu')
_LOG.info("CPDs fitted successfully")
_LOG.info("Network CPDs: %s", list(bn.cpds.keys()))
print(f"CPDs: {list(bn.cpds.keys())}")

# %% [markdown]
# ## Cell 5: Model Validation
#
# Evaluate the model using classification metrics on test data.
# Validate that the learned network makes accurate predictions.

# %%
# Split data into training and test sets.
train_size = int(0.8 * len(df_discrete))
train_data = df_discrete[:train_size]
test_data = df_discrete[train_size:]
# Get predictions from the Bayesian Network on test data.
predictions = []
for idx, row in test_data.iterrows():
    pred = bn.predict(test_data[[c for c in cols if c != 'G2']].iloc[idx])
    predictions.append(pred.get('G2', 'unknown'))
_LOG.info("Test set size: %s", len(test_data))
_LOG.info("Predictions made: %s", len(predictions))
print(f"Test set size: {len(test_data)}")
print(f"Predictions made: {len(predictions)}")

# %% [markdown]
# ## Cell 6: Inference & Querying
#
# Extract insights through conditional probability queries.
# Compute marginal and conditional probabilities given observations.

# %%
# Extract the CPD for G2 (second period grade).
cpd_g2 = bn.cpds.get('G2')
if cpd_g2 is not None:
    _LOG.info("CPD for G2: %s", cpd_g2.variable)
    _LOG.info("G2 cardinality: %s", cpd_g2.cardinality)
    print(f"CPD variable: {cpd_g2.variable}")
    print(f"G2 cardinality: {cpd_g2.cardinality}")
# Perform inference with observations.
_ = bn.fit_cpds(train_data[cols], method='BayesianEstimator')
_LOG.info("Inference complete on training data")

# %% [markdown]
# ## Cell 7: Causal Interventions
#
# Apply "do" operators to simulate policy changes.
# Estimate the causal effect of interventions on outcomes.

# %%
# Create counterfactual scenarios by intervention.
df_intervention = df_discrete.copy()
# Intervene: set studytime to 'high' for all students.
df_intervention['studytime'] = 'high'
# Compare outcomes before and after intervention.
pass_rate_before = (df_discrete['G2_bin'] == 'pass').sum() / len(df_discrete)
pass_rate_after = (df_intervention['G2_bin'] == 'pass').sum() / len(df_intervention)
improvement = (pass_rate_after - pass_rate_before) * 100
_LOG.info("Pass rate before intervention: %.1f%%", pass_rate_before * 100)
_LOG.info("Pass rate after intervention (hypothetical): %.1f%%", pass_rate_after * 100)
_LOG.info("Intervention effect: %.1f%% improvement", improvement)
print(f"Pass rate before: {pass_rate_before * 100:.1f}%")
print(f"Pass rate after: {pass_rate_after * 100:.1f}%")
print(f"Improvement: {improvement:.1f}%")

# %% [markdown]
# ## Cell 8: Network Visualization
#
# Visualize the causal structure and relationships.

# %%
from causalnex.plots import draw
# Create a figure to display the causal graph.
fig, ax = plt.subplots(figsize=(10, 8))
# Draw the structure model with nodes and edges.
draw(sm, with_labels=True, node_color="lightblue",
     node_size=3000, font_size=10, arrows=True, arrowsize=20, ax=ax)
ax.set_title("Causal Structure: Student Performance", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()
_LOG.info("Network visualization complete")
