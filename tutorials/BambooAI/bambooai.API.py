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

# %%
# %load_ext autoreload
# %autoreload 2

# System libraries.
import logging

# Third party libraries.
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# %%
import json
import os
import sys
from pathlib import Path

import plotly.io as pio
from dotenv import load_dotenv


# %%
import logging

# Local utility.
import bambooai_utils as utils

_LOG = logging.getLogger(__name__)
utils.init_logger(_LOG)


# %% [markdown]
# # BambooAI API Tutorial
#

# %% [markdown]
# A runnable, focused guide to BambooAI: what it is, how to configure it, and how to launch the conversation loop.
#
# How to use this notebook
# - Run top-to-bottom if you can.
# - Some cells call an LLM and may incur cost. You can still read the markdown safely without running.
#
# Related notebooks
# - `bambooai.example.ipynb` is a narrative, end-to-end walkthrough with more feature demos.
#

# %% [markdown]
# ## What BambooAI is
# BambooAI is an open-source, LLM-powered data analysis agent for pandas workflows. You ask questions in natural language, BambooAI plans the steps, generates or executes code, and returns tables or charts, depending on what you ask for.
#
# When to use it
# - You want an interactive, conversational way to explore a DataFrame.
# - You need automated code generation with error correction and iterative feedback loops.
# - You want analysis memory via a vector DB or semantic grounding via an ontology.
#
# Feature highlights
# - Natural language interface for data analysis with automatic Python generation.
# - Multi-step planning, error correction, and code editing loops.
# - Vector database integration for knowledge storage and semantic recall.
# - Ontology grounding via `.ttl` files for domain-specific semantics.
# - Web UI (Flask) and Jupyter notebook support.
#
# Model support
# - API providers: OpenAI, Google (Gemini), Anthropic, Groq, Mistral.
# - Local providers: Ollama and a selection of local models.
#

# %% [markdown]
# ## Setup and dependencies
#
# Make sure the dataset lives here and that your `.env` file defines `EXECUTION_MODE` before you execute the notebook.  The EXECUTION_MODE param controls where BambooAI executes generated code, based on your setup. Common values are `local` (run in-process) and `api` (run via a configured executor). If you are unsure, it is recommended to start with `local`.
#
# The default dataset path is `_DEFAULT_CSV = Path("testdata.csv")` in `bambooai_utils.py`. Override it with `--csv-path` (parser in `bambooai_utils.py`) or update `_DEFAULT_CSV` directly.
#
# **At minimum you need:**
# - Dependencies installed through Docker and `requirements.txt`.
# - API keys in `.env` for the LLM provider you choose.
# - `LLM_CONFIG.json` - This file maps agents to models, providers, and parameters. Use `LLM_CONFIG.json` as a starting point, or set `LLM_CONFIG` in `.env` to inline the JSON. 
#
# BambooAI reads its agent model settings from `LLM_CONFIG` (env var) or `LLM_CONFIG.json` in the working directory. If neither is present, it falls back to its package defaults. Prompt templates can be customized by creating `PROMPT_TEMPLATES.json` from the provided sample file.

# %%
# Configure environment, plotting, and helper import paths.
load_dotenv()

import helpers.hio as hio

plotly_renderer = os.getenv("PLOTLY_RENDERER", "jupyterlab")
pio.renderers.default = plotly_renderer
sns.set_style("whitegrid")
np.set_printoptions(suppress=True, precision=6)

# Use print() so setup diagnostics are visible in notebook output.
print(f"Plotly renderer: {pio.renderers.default}")
# print(f"Helpers root on path: {str(_HELPERS_ROOT) in sys.path}")
# Environment and path setup is now ready for downstream cells.



# %%
# Inspect the active LLM configuration source and summarize configured agents.
config_env = os.getenv("LLM_CONFIG", "").strip()
config_path = Path("LLM_CONFIG.json")
config = None

if config_env:
    config = json.loads(config_env)
    source = "LLM_CONFIG env var"
elif config_path.exists():
    config = json.loads(config_path.read_text())
    source = "LLM_CONFIG.json"

# Use print() so configuration status is visible in notebook output.
if config:
    print(f"{source} found. Agent configs:")
    for agent in config.get("agent_configs", []):
        details = agent.get("details", {})
        print(
            f"- {agent.get('agent')}: {details.get('provider')}/{details.get('model')}"
        )
else:
    print(
        "No LLM_CONFIG found. BambooAI will use its package defaults (see BambooAI docs/config)."
    )
# The output confirms whether configuration is sourced from env, file, or defaults.



# %% [markdown]
# ### API helper functions
#
# The BambooAI helpers are defined in `bambooai_utils.py`.
#

# %%
# Print helper docstrings to document the API wrapper functions used in this notebook.
from bambooai_utils import (
    _DEFAULT_CSV,
    _build_bamboo_agent,
    _load_dataframe,
    _parse,
    _resolve_execution_mode,
    _run_agent,
    _setup_env,
)

api_docs = {
    "_setup_env": _setup_env.__doc__,
    "_parse": _parse.__doc__,
    "_resolve_execution_mode": _resolve_execution_mode.__doc__,
    "_load_dataframe": _load_dataframe.__doc__,
    "_build_bamboo_agent": _build_bamboo_agent.__doc__,
    "_run_agent": _run_agent.__doc__,
}

# Use print() so API reference text is visible in notebook output.
for name, doc in api_docs.items():
    if doc:
        print(f"{name} docstring:\n{doc.strip()}\n")
    else:
        print(f"{name} has no docstring\n")
print(f"Default CSV path: {_DEFAULT_CSV}")
# The printed docstrings provide a quick API reference for the helper layer.



# %%
# Set the execution mode expected by the wrapper and verify the resolved value.
os.environ["EXECUTION_MODE"] = "local"  # Update as needed.
# Use print() so users can confirm the setting inline.
print("EXECUTION_MODE from env:", os.getenv("EXECUTION_MODE"))
# A non-empty value confirms the execution mode precondition is satisfied.



# %% [markdown]
# ## Sanity check
#
# Use this quick check to confirm environment configuration and dataset readiness before running the agent.

# %%
# Define notebook helpers for masking, dataframe loading, and artifact paths.
def _mask(value: str) -> str:
    """
    Mask a secret value for notebook display.
    """
    if not value:
        return "<not set>"
    if len(value) <= 6:
        return "*" * len(value)
    return f"{value[:3]}...{value[-2:]}"


def _get_dataframe() -> pd.DataFrame:
    """
    Return the current dataframe, loading the default CSV if needed.
    """
    global df
    if "df" not in globals():
        df = _load_dataframe(_DEFAULT_CSV)
    return df


def _get_artifacts_dir() -> Path:
    """
    Return the artifact directory, creating it if needed.
    """
    artifacts_dir = Path("artifacts")
    hio.create_dir(str(artifacts_dir), incremental=True)
    return artifacts_dir

# The helper functions are ready for the setup and feature cells below.



# %%
# Display masked environment settings used by BambooAI.
keys = [
    "EXECUTION_MODE",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "AZURE_OPENAI_API_KEY",
    "PINECONE_API_KEY",
    'GEMINI_API_KEY'
]

# Use print() so environment checks are visible inline.
print("Environment")
for key in keys:
    value = os.getenv(key, "")
    if key == "LLM_CONFIG":
        display_value = "<set>" if value else "<not set>"
    else:
        display_value = _mask(value)
    print(f"- {key}: {display_value}")
# Masked environment output confirms which settings are available.


# %% [markdown]
# ## Key parameters
# | Parameter | Type | Default | Impact |
# | --- | --- | --- | --- |
# | `df` | `pd.DataFrame` | `None` | Primary dataset for analysis. If not provided, BambooAI may attempt to source data from the internet or auxiliary datasets. |
# | `auxiliary_datasets` | `list[str]` | `None` | Additional datasets available during code execution. |
# | `max_conversations` | `int` | `4` | Number of user/assistant pairs retained in memory. |
# | `search_tool` | `bool` | `False` | Enables external search capability when needed. |
# | `planning` | `bool` | `False` | Enables multi-step planning for complex requests. |
# | `webui` | `bool` | `False` | Runs BambooAI as a Flask-based web app. |
# | `vector_db` | `bool` | `False` | Enables vector memory for recall or retrieval. |
# | `df_ontology` | `str` | `None` | Path to a `.ttl` ontology file for semantic grounding. |
# | `exploratory` | `bool` | `True` | Enables expert selection for query handling. |
# | `custom_prompt_file` | `str` | `None` | YAML file with custom prompt templates. |
#
# Few important clarifications:
#
# - `vector_db=True` enables episodic memory. Pinecone and Qdrant are supported via `.env` configuration. When set to True, the model will first attempt to search its vector DB for previous conversation for clues to answer questions. If nothing is found, it attempts to reason on its own and answer. At the end of each output, BambooAI asks users to rank the solution it provided on a scale of 1-10 (10 being awesome and 1 being really bad). If you rank it pretty high (>6), the model will try to reference it for future conversations to learn from.
#
#     - Pinecone example env vars: `VECTOR_DB_TYPE=pinecone`, `PINECONE_API_KEY=...` (some versions also use `PINECONE_ENV`).
#
#     - Qdrant example env vars: `VECTOR_DB_TYPE=qdrant`, `QDRANT_URL=...`, `QDRANT_API_KEY=...` (optional for local, required for cloud).
#
#     - Pinecone embeddings are supported with `text-embedding-3-small` (OpenAI) or `all-MiniLM-L6-v2` (HF).
#
# - `df_ontology` expects a `.ttl` ontology file (RDF/OWL) that defines classes, properties, and relationships.
#

# %%
# Load the dataset and show a small preview.
args = _parse().parse_args([])
csv_path = Path(args.csv_path) if args.csv_path else _DEFAULT_CSV
print("\nDataset")
print(f"- path: {csv_path}")
print(f"- exists: {csv_path.exists()}")

df = _load_dataframe(csv_path)
print(f"\nDataframe shape: {df.shape}")
display(df.head())
# Successful output confirms dataset readiness before agent runs.


# %% [markdown]
# ## Minimal Agent
#
# This is the smallest interactive run. It builds an minimal agent with minimal flags and starts the loop.
# When prompted, paste one simple question, then type `exit` or press Ctrl+D to stop.
#

# %%
# Build a minimal BambooAI agent for one interactive run.
df = _get_dataframe()

bamboo_quick = _build_bamboo_agent(
    df, planning=False, vector_db=False, search_tool=False
)
print(
    "BambooAI ready. When the loop starts, paste one prompt, then type 'exit' or press Ctrl+D to stop."
)
# The bamboo_quick object is ready for the next run cell.


# %%
# Run the minimal BambooAI conversation loop.
_run_agent(bamboo_quick)
# The conversation loop uses the agent configured in the previous cell.


# %% [markdown]
# ## Parameter Deep Dive
#
# This section walks through the most crucial and commonly used BambooAI parameters to understand their use, examples to show usage and expected behavior.
#

# %% [markdown]
# ### 1. auxiliary_datasets 
#
# **Use auxiliary datasets when the primary dataframe needs supporting information (lookups, joins, mapping tables).**
#
# Custom prompt example - Join the auxiliary dataset on `country` and summarize average `monthly_spend_usd` by region.
#

# %%
# Prepare a small auxiliary dataset artifact for join-style prompts.
df = _get_dataframe()

artifacts_dir = _get_artifacts_dir()
aux_path = artifacts_dir / "auxiliary_demo.csv"
aux_df = pd.DataFrame(
    {
        "country": ["US", "CA", "DE"],
        "region_label": ["North America", "North America", "Europe"],
    }
)
aux_df.to_csv(aux_path, index=False)
# Use print() so the generated artifact path is visible inline.
print("Wrote auxiliary dataset:", aux_path)
# The artifact is now available for auxiliary dataset experiments.


# %%
# Build an agent with auxiliary datasets enabled.
bamboo_aux = _build_bamboo_agent(
    df,
    auxiliary_datasets=[str(aux_path)],
    planning=False,
    vector_db=False,
    search_tool=False,
)
# Use print() so the agent readiness status is visible inline.
print("Auxiliary datasets agent ready.")
# The bamboo_aux object is ready for the next run cell.


# %%
# Run the auxiliary-datasets BambooAI conversation loop.
_run_agent(bamboo_aux)
# The conversation loop uses the agent configured in the previous cell.


# %% [markdown]
# ### 2. max_conversations
#
# **This limits how much recent chat history BambooAI keeps in memory.**
#
#
# What to expect
# - With a low value (e.g., 1), the agent may forget older context and ask you to restate details.
# - With higher values, it should retain more prior turns.

# %%
# Demonstrate short conversational memory with max_conversations set to 1.
df = _get_dataframe()

bamboo_short_memory = _build_bamboo_agent(
    df,
    max_conversations=1,
    planning=False,
)
# Use print() so the agent readiness status is visible inline.
print("Agent ready with max_conversations=1.")
# The bamboo_short_memory object is ready for the next run cell.


# %%
# Run the short-memory BambooAI conversation loop.
_run_agent(bamboo_short_memory)
# The conversation loop uses the agent configured in the previous cell.


# %% [markdown]
# ### 3. search_tool
#
# **Enable this when you want BambooAI to pull in external context from the web.**
#
# Example prompt - Find a short definition of `customer churn` and explain how it might map to our dataset.
#
# If the search tool is configured, the agent should fetch external context and cite or summarize it. If not configured, you may see a tool error or a warning.

# %%
# Demonstrate an agent configured to use external search when available.
df = _get_dataframe()

bamboo_search = _build_bamboo_agent(
    df,
    planning=False,
    vector_db=False,
    search_tool=True,
)
# Use print() so the agent readiness status is visible inline.
print("Search tool enabled agent ready.")
# The bamboo_search object is ready for the next run cell.


# %%
# Run the search-enabled BambooAI conversation loop.
_run_agent(bamboo_search)
# The conversation loop uses the agent configured in the previous cell.


# %% [markdown]
# ### 4. planning
#
# **Planning helps BambooAI solve multi-step or ambiguous tasks by outlining a plan before executing code.**
#
# Example prompt - Compare revenue trends by region, identify the top 3 outliers, and explain possible causes.
#
# What to expect
# - The agent should produce a plan, then execute steps to answer.
# - For simple prompts, planning add unnecessary latency without changing results.
#

# %%
# Demonstrate planning-enabled execution for multi-step prompts.
df = _get_dataframe()

bamboo_planning = _build_bamboo_agent(
    df,
    planning=True,
    vector_db=False,
    search_tool=False,
)
# Use print() so the agent readiness status is visible inline.
print("Planning-enabled agent ready.")
# The bamboo_planning object is ready for the next run cell.


# %%
# Run the planning-enabled BambooAI conversation loop.
_run_agent(bamboo_planning)
# The conversation loop uses the agent configured in the previous cell.


# %% [markdown]
# ### 5. vector_db
#
# **This parameter enables memory and retrieval over prior conversations and documents.**
#
# Custom prompt
# - "Using what you learned earlier, summarize the top 2 churn drivers."
#
# What to expect
# - With a configured vector DB, the agent can retrieve past context instead of re-deriving it.
# - Without proper credentials, initialization will fail.
#

# %%
# Demonstrate vector-database backed memory retrieval.
df = _get_dataframe()

bamboo_vector = _build_bamboo_agent(
    df,
    planning=True,
    vector_db=True,
    search_tool=False,
)
# Use print() so the agent readiness status is visible inline.
print("Vector DB enabled agent ready.")
# The bamboo_vector object is ready for the next run cell.


# %%
# Run the vector-db BambooAI conversation loop.
_run_agent(bamboo_vector)
# The conversation loop uses the agent configured in the previous cell.


# %% [markdown]
# ### 6. df_ontology
#
# **This parameter focuses on the ontology of the dataset and provides grounding in the form of schema-level meaning and constraints for columns and values.**
#
# Custom prompt
# - Validate that `churned` and `has_premium` values match the ontology. Flag any invalid values.
#
# What to expect
# - The agent should reference ontology definitions and perform value checks.
# - If the ontology file is invalid, initialization may fail.
#

# %%
# Create a minimal ontology artifact used for grounding checks.
df = _get_dataframe()

artifacts_dir = _get_artifacts_dir()
ontology_path = artifacts_dir / "mini_ontology.ttl"
ontology_path.write_text(
    """@prefix ex: <http://example.com/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:Customer a rdfs:Class .
ex:churned a rdfs:Property ;
  rdfs:domain ex:Customer ;
  rdfs:range xsd:boolean ;
  rdfs:label "churned" .
ex:has_premium a rdfs:Property ;
  rdfs:domain ex:Customer ;
  rdfs:range xsd:boolean ;
  rdfs:label "has_premium" .
ex:monthly_spend_usd a rdfs:Property ;
  rdfs:domain ex:Customer ;
  rdfs:range xsd:decimal ;
  rdfs:label "monthly_spend_usd" .
"""
)
# Use print() so the generated artifact path is visible inline.
print("Wrote ontology:", ontology_path)
# The ontology file is now available for df_ontology initialization.


# %%
# Build an ontology-grounded agent.
bamboo_ontology = _build_bamboo_agent(
    df,
    df_ontology=str(ontology_path),
    planning=True,
    exploratory=True,
)
# Use print() so the agent readiness status is visible inline.
print("Ontology grounded agent ready.")
# The bamboo_ontology object is ready for the next run cell.


# %%
# Run the ontology-grounded BambooAI conversation loop.
_run_agent(bamboo_ontology)
# The conversation loop uses the agent configured in the previous cell.


# %% [markdown]
# ### 7. exploratory
#
# **Exploratory mode enables expert selection for query handling (e.g., routing to a specialist).**
#
# Custom prompt
# - Analyze this dataset for churn drivers and suggest follow-up questions.
#
# What to expect
# - The agent may ask clarifying questions or choose a specialist persona before executing.
# - With `exploratory=False`, it should behave more directly without extra routing.
#

# %%
# Demonstrate exploratory mode with expert routing enabled.
df = _get_dataframe()

bamboo_exploratory = _build_bamboo_agent(
    df,
    exploratory=True,
    planning=False,
)
# Use print() so the agent readiness status is visible inline.
print("Exploratory mode agent ready.")
# The bamboo_exploratory object is ready for the next run cell.


# %%
# Run the exploratory-mode BambooAI conversation loop.
_run_agent(bamboo_exploratory)
# The conversation loop uses the agent configured in the previous cell.


# %% [markdown]
# ### 8. custom_prompt_file
#
# **Custom prompts let you control response structure and tone.**
#
# Example - Return a 3-bullet summary and a numbered action plan.
#
# What to expect
# - The agent should follow the style and structure defined in your prompt templates.
# - If the YAML file is missing or malformed, initialization may fail.
#

# %%
# Create a minimal custom prompt file artifact for style control.
df = _get_dataframe()

artifacts_dir = _get_artifacts_dir()
custom_prompt_path = artifacts_dir / "custom_prompts.yaml"
custom_prompt_path.write_text(
    "# Placeholder prompts for BambooAI\n"
    "planner_prompt: \"You are a careful planner.\"\n"
    "code_prompt: \"Write concise pandas code.\"\n"
)
# Use print() so the generated artifact path is visible inline.
print("Wrote custom prompts:", custom_prompt_path)
# Prompt template artifact is now available for agent initialization.


# %%
# Build an agent that consumes custom prompt templates.
bamboo_custom = _build_bamboo_agent(
    df,
    custom_prompt_file=str(custom_prompt_path),
    planning=False,
    exploratory=True,
)
# Use print() so the agent readiness status is visible inline.
print("Custom prompt agent ready.")
# The bamboo_custom object is ready for the next run cell.


# %%
# Run the custom-prompt BambooAI conversation loop.
_run_agent(bamboo_custom)
# The conversation loop uses the agent configured in the previous cell.


# %% [markdown]
# ## Prompt cookbook (short)
#
# Use these examples to get quick wins. For a larger cookbook and narrative flow, see `bambooai.example.ipynb`.
#
# Basic EDA
# - "List the columns and their data types."
# - "Show summary stats for numeric columns and note any missing values."
#
# Visualization
# - "Plot a histogram of `monthly_spend_usd` with 30 bins and label axes."
#
# Advanced
# - "Detect anomalies in daily `monthly_spend_usd` using a 7-day rolling z-score; return flagged dates."
#
