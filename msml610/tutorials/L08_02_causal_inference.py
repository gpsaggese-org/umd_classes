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
# ## Imports

# %%
# %load_ext autoreload
# %autoreload 2

import logging

import matplotlib.pyplot as plt
import seaborn as sns

# Set plotting style.
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# %%
import helpers.hmodule as hmodule

import msml610_utils as ut
import L08_02_causal_inference_utils as mtl0cireout

ut.config_notebook()

# Initialize logger.
logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)

# %%
hmodule.install_module_if_not_present(
    "dataframe_image",
    use_activate=True,
)

hmodule.install_module_if_not_present(
    "networkx",
    use_activate=True,
)

hmodule.install_module_if_not_present(
    "pgmpy",
    use_activate=True,
)

# %%
import networkx as nx

import pgmpy.base as pgmpy_base

# %%
model = nx.DiGraph([
    ("C", "A"),
    ("C", "B"),
    ("D", "A"),
    ("B", "E"),
    ("F", "E"),
    ("A", "G"),
])

mtl0cireout.plot_graph_highlight(model)

# %%
# Convert your NetworkX graph to pgmpy DAG.
dag = pgmpy_base.DAG(model.edges())

print("Are D and C dependent?")
print(not dag.is_dconnected("D", "C"))

# %%
subgraph = mtl0cireout.reachable_subgraph(model, ["A", "D", "C"])
mtl0cireout.plot_graph_highlight(
    subgraph,
    node1="D",
    node2="C",
    conditioning_node_set=["A"],
)

# %%
print("Are D and C dependent given A?")
print(not dag.is_dconnected("D", "C", observed={"A"}))

# %%
print("Are D and C dependent given G?")
print(not dag.is_dconnected("D", "C", observed={"G"}))

# %%
print("Are G and D dependent?")
print(not dag.is_dconnected("G", "D"))

# %%
print("Are G and D dependent given A?")
print(not dag.is_dconnected("G", "D", observed=["A"]))

# %%
print("Are G and F dependent?")
print(dag.is_dconnected("G", "F"))

# %%
print("Are G and F dependent given E?")
print(dag.is_dconnected("G", "F", observed=["E"]))

# %%
