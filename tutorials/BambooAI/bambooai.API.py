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
# # Summary
# - This notebook explains how to configure BambooAI and run the API workflow in Jupyter.
# - This notebook covers environment setup, key parameters, and prompt examples.
#

# %% [markdown]
# # BambooAI API Tutorial
# - **Usage**: Run cells top-to-bottom when possible.
# - **Cost note**: Cells that call an LLM can incur cost.
# - **Read-only mode**: You can read markdown cells safely without running code.
# - **Related notebook**: `bambooai.example.ipynb`: End-to-end walkthrough with additional feature demos.
#

# %% [markdown]
# ## What BambooAI Is
# - **Definition**: BambooAI is an open-source, LLM-powered data analysis agent for pandas workflows.
# - **Workflow**: BambooAI interprets natural-language prompts, plans steps, executes code, and returns tables or charts.
# - **Interactive data exploration**: Conversational DataFrame exploration through natural-language prompts.
# - **Automated code generation**: Code generation with error correction and iterative feedback loops.
# - **Semantic grounding and memory**: Analysis memory through vector DB integration or ontology-based grounding.
# - **Natural-language interface**: Data analysis through prompts with automatic Python generation.
# - **Adaptive execution loop**: Multi-step planning, error correction, and iterative code refinement.
# - **Vector memory support**: Vector database integration for knowledge storage and semantic recall.
# - **Ontology grounding**: `.ttl`-based domain grounding for context-aware analysis.
# - **Notebook and web support**: Flask web UI and Jupyter notebook integration.
# - **API providers**: OpenAI, Google (Gemini), Anthropic, Groq, Mistral.
# - **Local providers**: Ollama and selected local models.

# %% [markdown]
# ## Setup and dependencies
#
# - **Precondition**: Keep dataset files available in this tutorial directory.
# - **Precondition**: Set `EXECUTION_MODE` in `.env` before running notebook cells.
# - **`EXECUTION_MODE` values**: `local` for in-process execution; `api` for external executor mode.
# - **Recommendation**: Start with `local` if execution mode is unknown.
# - **Default dataset path**: `_DEFAULT_CSV = Path("testdata.csv")` in `bambooai_utils.py`.
# - **Dataset override**: Use `--csv-path` in `bambooai_utils.py` parser, or edit `_DEFAULT_CSV`.
# - **Minimum requirement**: Install dependencies through Docker and `requirements.txt`.
# - **Minimum requirement**: Set provider API keys in `.env`.
# - **`LLM_CONFIG.json`**: Maps agents to providers, models, and parameters.
# - **`LLM_CONFIG.json` setup**: Use the file directly or set `LLM_CONFIG` in `.env` with inline JSON.
# - **Configuration resolution**: BambooAI loads `LLM_CONFIG` env var first, then `LLM_CONFIG.json`, then package defaults.
# - **Prompt templates**: Create `PROMPT_TEMPLATES.json` from the sample file to customize prompts.

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

# Use print() so helper readiness is visible in notebook output.
print("Helpers ready: _mask, _get_dataframe, _get_artifacts_dir")
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
# Important clarifications:
#
# - **`vector_db=True` behavior**: Enables episodic memory and retrieval from prior conversations.
# - **`vector_db=True` flow**: BambooAI searches vector memory first, then falls back to model reasoning when no hit exists.
# - **Feedback loop**: BambooAI asks for a 1-10 score; high scores can influence future retrieval.
# - **Pinecone env example**: `VECTOR_DB_TYPE=pinecone`, `PINECONE_API_KEY=...` and sometimes `PINECONE_ENV`.
# - **Qdrant env example**: `VECTOR_DB_TYPE=qdrant`, `QDRANT_URL=...`, `QDRANT_API_KEY=...`.
# - **Pinecone embedding options**: `text-embedding-3-small` (OpenAI) or `all-MiniLM-L6-v2` (Hugging Face).
# - **`df_ontology` expectation**: Provide a `.ttl` ontology file with classes, properties, and relationships.
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
# - **Goal**: Run the smallest interactive BambooAI loop.
# - **Setup**: Build a minimal agent with minimal flags.
# - **Interaction**: Paste one prompt, then type `exit` or press `Ctrl+D` to stop.
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
# - **Goal**: Review key BambooAI parameters with examples and expected behavior.
#

# %% [markdown]
# ### 1. auxiliary_datasets 
#
# - **Use case**: Use `auxiliary_datasets` when the primary DataFrame needs lookup or join context.
# - **Example prompt**: Join auxiliary data on `country` and summarize average `monthly_spend_usd` by region.
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
# - **Definition**: `max_conversations` limits recent chat history retained in memory.
# - **Expected behavior**: Low values (for example, `1`) can drop older context.
# - **Expected behavior**: Higher values retain more prior turns.

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
# - **Use case**: Enable `search_tool` to pull external web context.
# - **Example prompt**: Find a short definition of `customer churn` and map it to this dataset.
# - **Expected behavior**: With tool configuration, BambooAI fetches and summarizes external context.
# - **Failure mode**: Without tool configuration, BambooAI can return tool errors or warnings.

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
# - **Use case**: Enable `planning` for multi-step or ambiguous tasks.
# - **Example prompt**: Compare revenue trends by region, identify top outliers, and explain possible causes.
# - **Expected behavior**: BambooAI outlines a plan, then executes steps.
# - **Trade-off**: For simple prompts, planning can add latency without improving outcomes.
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
# - **Definition**: `vector_db` enables retrieval over prior conversations and documents.
# - **Example prompt**: "Using what you learned earlier, summarize the top 2 churn drivers."
# - **Expected behavior**: With valid vector DB configuration, BambooAI retrieves past context.
# - **Failure mode**: Without credentials or DB configuration, initialization can fail.
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
# - **Definition**: `df_ontology` provides ontology grounding for schema meaning and value constraints.
# - **Example prompt**: Validate that `churned` and `has_premium` values match ontology constraints.
# - **Expected behavior**: BambooAI references ontology definitions and performs value checks.
# - **Failure mode**: Invalid ontology files can cause initialization failures.
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
# - **Definition**: `exploratory` enables expert routing for query handling.
# - **Example prompt**: Analyze churn drivers and suggest follow-up questions.
# - **Expected behavior**: BambooAI can ask clarifying questions or route to a specialist persona.
# - **Expected behavior**: With `exploratory=False`, behavior is more direct with less routing.
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
# - **Definition**: `custom_prompt_file` controls response structure and tone.
# - **Example prompt**: Return a 3-bullet summary and a numbered action plan.
# - **Expected behavior**: BambooAI follows structure defined in custom prompt templates.
# - **Failure mode**: Missing or malformed YAML can cause initialization failures.
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
# - **Goal**: Use these prompts for quick wins.
# - **Extended cookbook**: See `bambooai.example.ipynb` for a broader narrative flow.
# - **Basic EDA prompt**: "List the columns and their data types."
# - **Basic EDA prompt**: "Show summary stats for numeric columns and note any missing values."
# - **Visualization prompt**: "Plot a histogram of `monthly_spend_usd` with 30 bins and label axes."
# - **Advanced prompt**: "Detect anomalies in daily `monthly_spend_usd` using a 7-day rolling z-score; return flagged dates."
#
