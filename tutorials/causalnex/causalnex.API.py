# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.1
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
# - https://causalnex.readthedocs.io/
# - https://causalnex.readthedocs.io/en/latest/03_tutorial/01_first_tutorial.html

# %%
# %load_ext autoreload
# %autoreload 2
# %matplotlib inline

# System libraries.
import logging

# Third-party libraries.
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

# Note: we need to import sklearn first to avoid conflicts with libgomp-d22c30c5.so.1.0.0: cannot allocate memory in static TLS block
import sklearn

_ = sklearn

# %%
# import helpers.hmodule as hmodule
# hmodule.install_module_if_not_present(
#     [""],
#     use_activate=True,
#     use_sudo=False,
#     venv_path="/opt/venv",
# )

# %% editable=true slideshow={"slide_type": ""}
# Helpers packages.

# Tutorial-specific packages.
import tutorials.causalnex.causalnex_utils as tcnut
import causalnex

print(causalnex.__version__)

_LOG = logging.getLogger(__name__)
tcnut.init_loggers(_LOG)

_LOG.info("Test _LOG.info")

# %% [markdown]
# ## Cell 1: Load Data

# %%
# Load the student performance dataset from https://archive.ics.uci.edu/dataset/320/student+performance
df = tcnut.load_student_performance_data(data_dir="data")
_LOG.info("Dataset shape: %s", df.shape)
display(df.head())

# %%
print(df.columns)

# %%
# !cat /git_root/tutorials/causalnex/data/info.txt 

# %%
# !cat /git_root/tutorials/causalnex/data/student.txt

# %%
metadata_df = pd.read_csv("/git_root/tutorials/causalnex/data/metadata.csv")
display(metadata_df)

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
sm.add_edges_from(
    [
        ("health", "absences"),
        ("health", "G1"),
        ("studytime", "G1"),
        ("studytime", "G2"),
        ("G1", "G2"),
        ("absences", "G1"),
        ("absences", "G2"),
    ]
)
print(f"Nodes: {list(sm.nodes)}")
print(f"Edges: {list(sm.edges)}")

# %%
# Plot the relationships using networkx.
if False:
    from causalnex.plots import plot_structure, NODE_STYLE, EDGE_STYLE
    
    viz = plot_structure(
        sm,
        all_node_attributes=NODE_STYLE.WEAK,
        all_edge_attributes=EDGE_STYLE.WEAK,
    )
    # viz.save_graph("graph.html")
    # display(HTML("graph.html"))

# %%
# Plot the relationships using networkx.
G = nx.DiGraph(sm)
plt.figure(figsize=(6, 4))

pos = nx.spring_layout(G, seed=42)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="lightblue",
    node_size=2000,
    font_size=10,
    arrows=True,
)

plt.title("Graph Visualization")

plt.show()

# %%
# Plot using pygraphviz.
# from networkx.drawing.nx_pydot import graphviz_layout
# import matplotlib.pyplot as plt
# pos = graphviz_layout(G, prog="dot")
# nx.draw(
#     G,
#     pos,
#     with_labels=True,
#     node_color="lightgreen",
#     node_size=2000,
#     arrows=True,
# )
# plt.show()

# %% [markdown]
# ## Cell 3: Data Discretization
#
# Convert continuous features into categorical buckets with meaningful labels.
# Bayesian Networks require discrete distributions for probability estimation.

# %%
# Create a copy of the dataframe for discretization.
df_discrete = df.copy()

# Discretize continuous variables into categorical buckets.
# Replace originals so column names match the structure model nodes.
df_discrete["studytime"] = pd.cut(
    df["studytime"],
    bins=[0, 1, 2, 3, 4],
    labels=["very_low", "low", "medium", "high"],
).astype(str)
df_discrete["absences"] = pd.cut(
    df["absences"],
    bins=[-1, 5, 10, 20, 100],
    labels=["low", "medium", "high", "very_high"],
).astype(str)
df_discrete["G1"] = pd.cut(
    df["G1"], bins=[-1, 10, 20], labels=["fail", "pass"]
).astype(str)
df_discrete["G2"] = pd.cut(
    df["G2"], bins=[-1, 10, 20], labels=["fail", "pass"]
).astype(str)
df_discrete["health"] = df["health"].astype(str)
_LOG.info("Discretized data shape: %s", df_discrete.shape)

display(df_discrete[["health", "studytime", "absences", "G1", "G2"]].head())

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
cols = ["health", "studytime", "absences", "G1", "G2"]
df_fit = df_discrete[cols].copy()
# Learn the categorical states for each node before fitting the CPDs.
bn = bn.fit_node_states(df_fit)
# Fit the network to the data.
bn.fit_cpds(
    df_fit,
    method="BayesianEstimator",
    bayes_prior="BDeu",
    equivalent_sample_size=10,
)
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
input_cols = [c for c in cols if c != "G2"]
predictions_df = bn.predict(test_data[cols], "G2")
_LOG.info("Test set size: %s", len(test_data))
_LOG.info("Predictions made: %s", len(predictions_df))
print(f"Test set size: {len(test_data)}")
print(f"Predictions made: {len(predictions_df)}")
print(predictions_df.head())

# %% [markdown]
# ## Cell 6: Inference & Querying
#
# Extract insights through conditional probability queries.
# Compute marginal and conditional probabilities given observations.

# %%
# Extract the CPD for G2 (second period grade) as a DataFrame.
cpd_g2 = bn.cpds.get("G2")
if cpd_g2 is not None:
    _LOG.info("CPD for G2 shape: %s", cpd_g2.shape)
    _LOG.info("G2 states: %s", list(cpd_g2.index))
    print(f"CPD shape: {cpd_g2.shape}")
    print(f"G2 states: {list(cpd_g2.index)}")
    print(cpd_g2.head())
# Perform inference with observations.
_ = bn.fit_cpds(
    train_data[cols],
    method="BayesianEstimator",
    bayes_prior="BDeu",
    equivalent_sample_size=10,
)
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
df_intervention["studytime"] = "high"
# Predict G2 outcomes under the intervention using the fitted network.
intervention_preds = bn.predict(df_intervention[cols], "G2")
pred_col = intervention_preds.columns[0]
# Compare outcomes before and after intervention.
pass_rate_before = (df_discrete["G2"] == "pass").sum() / len(df_discrete)
pass_rate_after = (intervention_preds[pred_col] == "pass").sum() / len(
    intervention_preds
)
improvement = (pass_rate_after - pass_rate_before) * 100
_LOG.info("Pass rate before intervention: %.1f%%", pass_rate_before * 100)
_LOG.info(
    "Pass rate after intervention (hypothetical): %.1f%%", pass_rate_after * 100
)
_LOG.info("Intervention effect: %.1f%% improvement", improvement)
print(f"Pass rate before: {pass_rate_before * 100:.1f}%")
print(f"Pass rate after: {pass_rate_after * 100:.1f}%")
print(f"Improvement: {improvement:.1f}%")

# %% [markdown]
# ## Cell 8: Network Visualization
#
# Visualize the causal structure and relationships.

# %%
import networkx as nx

# Create a figure to display the causal graph.
fig, ax = plt.subplots(figsize=(10, 8))
# Draw the structure model with nodes and edges using networkx.
pos = nx.spring_layout(sm, seed=42)
nx.draw(
    sm,
    pos=pos,
    with_labels=True,
    node_color="lightblue",
    node_size=3000,
    font_size=10,
    arrows=True,
    arrowsize=20,
    ax=ax,
)
ax.set_title(
    "Causal Structure: Student Performance", fontsize=14, fontweight="bold"
)
plt.tight_layout()
# Save the figure since the script runs headless without a display.
fig.savefig("/git_root/tutorials/causalnex/causal_structure.png")
plt.close(fig)
_LOG.info("Network visualization saved to causal_structure.png")
