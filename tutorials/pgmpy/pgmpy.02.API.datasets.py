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
# # PGMPy Datasets API
#
# A guided exploration of pgmpy's dataset loading subsystem:
# - `list_datasets()`: Discover available datasets with rich filters
# - `load_dataset()`: Load a dataset by name into a structured `Dataset` object
# - `Dataset` attributes: tabular data, ground-truth DAG, expert knowledge, metadata tags
#
# This module is the entry point for obtaining benchmark data used in causal
# discovery, structure learning, and parameter estimation.

# %% [markdown]
# ## Imports and Setup

# %%
# %load_ext autoreload
# %autoreload 2

import logging
import sys
import warnings

warnings.filterwarnings('ignore')

# %%
import pgmpy.datasets as ds
import pandas as pd
import numpy as np

# %%
# Use this for most notebooks.
import helpers.htutorial as htutori

htutori.config_notebook()

# Import pgmpy utilities.
import tutorials.pgmpy.pgmpy_utils as tpgpguti

# Initialize logger.
logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)

# Convert `display` into `print()` when running outside IPython.
try:
    from IPython.display import display
except ImportError:
    display = print  # type: ignore

# %%
import logging

logging.getLogger("httpx").setLevel(logging.WARNING)

# %% [markdown]
# # Part 1: Library Overview
#
# ## What problem does `pgmpy.datasets` solve?
#
# - Provides one-line access to 47+ curated benchmark datasets for graphical models
# - Eliminates the boilerplate of finding, downloading, and parsing standard datasets
# - Some datasets include the true causal graph (ground truth) for supervised evaluation
# - Some include expert domain knowledge (edge constraints) for causal discovery
#
# ## Key abstractions
#
# - **Catalog**: `list_datasets()` returns a list of dataset name strings
#   - Supports keyword filters: `is_discrete`, `is_continuous`, `has_ground_truth`, etc.
# - **Loader**: `load_dataset(name)` returns a single `Dataset` object
# - **Dataset**: A lightweight dataclass with five key fields:
#   - `name` (str): Dataset identifier
#   - `data` (pd.DataFrame): The actual tabular data
#   - `ground_truth` (DAG or None): True causal graph (when available)
#   - `expert_knowledge` (ExpertKnowledge or None): Domain edge constraints
#   - `tags` (dict): Metadata (n_variables, n_samples, data types, etc.)
#
# ## How the pieces fit together
#
# ```
# User -> list_datasets(is_discrete=True) -> ['college_plans', ...]
# User -> load_dataset('sachs_discrete')
#      -> Dataset(name='sachs_discrete',
#                 data=DataFrame(5400 x 11),
#                 ground_truth=DAG(11 nodes, 20 edges),
#                 tags={n_variables: 11, ...})
# ```

# %% [markdown]
# # Part 2: Primitive-by-Primitive Exploration
#
# ## Primitive 1: `list_datasets()`: The Catalog
#
# **Mental model**: A searchable registry of all available benchmark datasets.
# Returns a plain list of name strings suitable for passing to `load_dataset()`.

# %%
# Smallest construction: no arguments returns all 47+ datasets.
all_datasets = ds.list_datasets()
print(f"Total datasets available: {len(all_datasets)}")
print("\n".join(all_datasets))

# %%
# Filter by data type: discrete only.
discrete_ds = ds.list_datasets(is_discrete=True)
print(f"Discrete datasets ({len(discrete_ds)}): {discrete_ds}")

# %%
# Filter by data type: continuous only.
continuous_ds = ds.list_datasets(is_continuous=True)
print(f"Continuous datasets ({len(continuous_ds)}): {continuous_ds[:10]}")

# %%
# Filter by data type: mixed (both discrete and continuous columns).
mixed_ds = ds.list_datasets(is_mixed=True)
print(f"Mixed datasets ({len(mixed_ds)}): {mixed_ds}")

# %%
# Filter by presence of ground truth.
with_gt = ds.list_datasets(has_ground_truth=True)
print(f"Datasets with ground truth ({len(with_gt)}): {with_gt}")

# %%
# Filter by number of variables.
few_vars = ds.list_datasets(n_variables=5)
print(f"Datasets with exactly 5 variables: {few_vars}")

ten_vars = ds.list_datasets(n_variables=10)
print(f"Datasets with exactly 10 variables: {ten_vars}")

# %%
# Combine multiple filters for precise selection.
rare = ds.list_datasets(is_interventional=True)
print(f"Interventional datasets ({len(rare)}): {rare}")

simulated = ds.list_datasets(is_simulated=True)
print(f"Simulated datasets ({len(simulated)}): {simulated}")

# %% [markdown]
# ## Primitive 2: `load_dataset()`: The Loader
#
# **Mental model**: Given a name string from the catalog, load and return a fully
# populated `Dataset` object with tabular data and optional metadata.

# %%
# Smallest construction: load a simple dataset.
data = ds.load_dataset('galton_stature')
print(f"Loaded dataset: {data.name}")
print(f"Object type: {type(data)}")

# %%
# Inspect the object.
print(f"type(data): {type(data)}")
print(f"dir(data) basic attributes:", [a for a in dir(data) if not a.startswith('_')])

# %%
# Try loading a different dataset.
data2 = ds.load_dataset('pima_diabetes')
print(f"Loaded: {data2.name}")
print(f"type: {type(data2)}")
print(f"dir: {[a for a in dir(data2) if not a.startswith('_')]}")

# %% [markdown]
# ## Primitive 3: `Dataset.data`: The Tabular Data
#
# **Mental model**: The actual observations as a pandas DataFrame, ready for
# `estimator.fit(data)`.

# %%
# Load the Pima diabetes dataset.
data = ds.load_dataset('pima_diabetes')

# Inspect the data field.
print(f"type: {type(data.data)}")
print(f"shape: {data.data.shape}")
print(f"columns: {list(data.data.columns)}")
print(f"dtypes:\n{data.data.dtypes}")
print(f"\nfirst 5 rows:")
display(data.data.head())

# %%
# Check basic statistics.
print(f"Missing values: {data.data.isnull().sum().sum()}")
print(f"Summary statistics:")
display(data.data.describe())

# %% [markdown]
# ## Primitive 4: `Dataset.ground_truth`: The True Causal Graph
#
# **Mental model**: When available, this is a `DAG` object representing the true
# underlying causal structure. Used to evaluate how well a causal discovery
# algorithm recovered the correct graph.

# %%
# Load a dataset with ground truth.
data = ds.load_dataset('sachs_discrete')

# Inspect the ground truth.
print(f"ground_truth type: {type(data.ground_truth)}")
print(f"Number of nodes: {len(data.ground_truth.nodes())}")
print(f"Number of edges: {len(data.ground_truth.edges())}")
print(f"\nNodes: {sorted(list(data.ground_truth.nodes()))}")
print(f"\nEdges: {list(data.ground_truth.edges())}")

# %%
_ = tpgpguti.draw_pgmpy_model(data.ground_truth)

# %%
# Inspect the DAG: check predecessors and successors.
gt = data.ground_truth
print(f"Predecessors of 'erk': {list(gt.predecessors('erk'))}")
print(f"Successors of 'pkc': {list(gt.successors('pkc'))}")
print(f"Is 'pkc' a parent of 'jnk'?: {gt.has_edge('pkc', 'jnk')}")
print(f"Is 'jnk' a parent of 'pkc'?: {gt.has_edge('jnk', 'pkc')}")

# %%
# Check what happens when a dataset has no ground truth.
data2 = ds.load_dataset('galton_stature')
print(f"galton_stature ground_truth: {data2.ground_truth}")
# Returns None : the field is optional.

# %% [markdown]
# ## Primitive 5: `Dataset.expert_knowledge`: Domain Constraints
#
# **Mental model**: Prior knowledge about edges that must be present, must be
# absent, or temporal ordering, which is used to guide causal discovery algorithms.

# %%
# Load a dataset with expert knowledge.
data = ds.load_dataset('sachs_discrete')

# Inspect expert knowledge.
ek = data.expert_knowledge
print(f"expert_knowledge type: {type(ek)}")
print(f"forbidden_edges: {ek.forbidden_edges}")
print(f"required_edges count: {len(ek.required_edges)}")
print(f"required_edges (sample): {list(ek.required_edges)[:5]}")
print(f"search_space: {ek.search_space}")
print(f"temporal_order: {ek.temporal_order}")

# %%
# Check dataset without expert knowledge.
data2 = ds.load_dataset('galton_stature')
print(f"galton_stature expert_knowledge: {data2.expert_knowledge}")

# %% [markdown]
# ## Primitive 6: `Dataset.tags`: Metadata Dictionary
#
# **Mental model**: A dictionary of descriptive metadata about the dataset,
# including counts, boolean flags for data type, and provenance info.

# %%
# Load a dataset and inspect tags.
data = ds.load_dataset('sachs_discrete')
print(f"tags type: {type(data.tags)}")

# Print each tag key-value pair.
for key, value in data.tags.items():
    print(f"  {key}: {value}")

# %%
# Compare tags across different dataset types.
sachs_tags = ds.load_dataset('sachs_discrete').tags
galton_tags = ds.load_dataset('galton_stature').tags

# TODO(ai_gp): Convert it into a pandas df
print(f"{'Property':<25} {'sachs_discrete':<20} {'galton_stature':<20}")
print("-" * 65)
for key in sachs_tags:
    print(f"{key:<25} {str(sachs_tags[key]):<20} {str(galton_tags[key]):<20}")

# %% [markdown]
# # Part 3: Composition Examples
#
# ## Example 1: List a Category, Load the First Dataset, Inspect It
#
# Minimal workflow: discover -> load -> explore.

# %%
# Discover discrete datasets.
discrete = ds.list_datasets(is_discrete=True)
print(f"Discrete datasets: {discrete}")

# Load the first one.
ds1 = ds.load_dataset(discrete[0])
print(f"\nName: {ds1.name}")
print(f"Shape: {ds1.data.shape}")
print(f"Columns: {list(ds1.data.columns)}")
display(ds1.data.head())

# Print tags.
for k, v in ds1.tags.items():
    print(f"  {k}: {v}")

# %% [markdown]
# ## Example 2: Filter by Ground Truth, Load, Compare Data vs Graph

# %%
gt_ds = ds.list_datasets(has_ground_truth=True)
print(f"Datasets with ground truth: {gt_ds}")

# Use `sachs_discrete` since some ground-truth graphs have parsing issues.
ds2 = ds.load_dataset('sachs_discrete')

print(f"Dataset: {ds2.name}")
print(f"Data shape: {ds2.data.shape}")
print(f"Ground truth nodes: {len(ds2.ground_truth.nodes())}")
print(f"Ground truth edges: {len(ds2.ground_truth.edges())}")

# Show a few rows.
display(ds2.data.head(3))

# Show the graph edges.
print(f"Edges: {list(ds2.ground_truth.edges())}")

# %% [markdown]
# ## Example 3: Load a Large Continuous Dataset and Summarize

# %%
# Find continuous datasets.
cont = ds.list_datasets(is_continuous=True)
print(f"Continuous datasets: {len(cont)}")
print(f"  {cont}")

# Load a modest-sized one.
ds3 = ds.load_dataset('airfoil')
print(f"\nDataset: {ds3.name}")
print(f"Shape: {ds3.data.shape}")
print(f"Columns: {list(ds3.data.columns)}")
display(ds3.data.describe())

# %% [markdown]
# ## Example 4: Use Expert Knowledge + Ground Truth Together
#
# The Sachs dataset family includes both ground truth and expert knowledge,
# making it useful for benchmarking causal discovery algorithms.

# %%
# Load the mixed-type Sachs dataset.
ds4 = ds.load_dataset('sachs_mixed')

print(f"Dataset: {ds4.name}")
print(f"Data type: discrete, continuous, or mixed?")
print(f"  is_discrete: {ds4.tags['is_discrete']}")
print(f"  is_continuous: {ds4.tags['is_continuous']}")
print(f"  is_mixed: {ds4.tags['is_mixed']}")
print(f"\nShape: {ds4.data.shape}")

# Check ground truth structure.
gt = ds4.ground_truth
print(f"\nGround truth: {gt.nodes()} -> {gt.edges()}")

# Check expert knowledge.
ek = ds4.expert_knowledge
print(f"\nExpert knowledge:")
print(f"  Required edges: {len(ek.required_edges)}")
print(f"  Forbidden edges: {len(ek.forbidden_edges)}")

# %%
# Check that the same ground truth graph is shared across all Sachs variants.
sachs_variants = [n for n in ds.list_datasets() if n.startswith('sachs')]
print(f"Sachs variants: {sachs_variants}")

gt_edges = {}
for name in sachs_variants:
    try:
        d = ds.load_dataset(name)
        gt_edges[name] = len(d.ground_truth.edges())
        print(f"  {name}: {d.data.shape}, GT edges: {len(d.ground_truth.edges())}")
    except Exception as e:
        print(f"  {name}: ERROR - {type(e).__name__}")

# All Sachs variants share the same ground truth graph.
all_same = len(set(gt_edges.values())) == 1
print(f"\nAll variants share the same graph? {all_same}")

# %% [markdown]
# # Part 4: API Patterns
#
# ## 1. Catalog-Load Pattern
#
# The dominant pattern: `list_datasets()` (discover) -> `load_dataset()` (fetch).
# This is similar to `sklearn.datasets.fetch_*` or PyTorch's `torchvision.datasets`.

# %%
# The pattern in one line.
data = ds.load_dataset(ds.list_datasets(is_discrete=True)[0])
print(f"Loaded: {data.name}")

# %% [markdown]
# ## 2. Filter Criterion Pattern
#
# Filters are keyword arguments that function as predicates on the dataset metadata.
# Multiple filters combine with AND semantics.

# %%
# AND-combined filters: discrete AND has ground truth AND expert knowledge.
precise = ds.list_datasets(is_discrete=True, has_ground_truth=True)
print(f"Discrete datasets with ground truth: {precise}")

# %% [markdown]
# ## 3. Dataset as a Dataclass
#
# The `Dataset` object bundles data + metadata into one container:
# - `data`: Always present (pd.DataFrame)
# - `ground_truth`: Optional (DAG or None)
# - `expert_knowledge`: Optional (ExpertKnowledge or None)
# - `tags`: Always present (dict)

# %%
# Show the dataclass structure via a print.
print(ds.load_dataset('boston_housing'))
