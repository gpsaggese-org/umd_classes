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
# # BambooAI Example Notebook
#
# This notebook is a guided, end-to-end tour of BambooAI: a conversational data assistant for pandas workflows.
#
# What you'll do:
# - load a small dataset
# - run a minimal BambooAI session
# - explore planning, semantic search, ontology grounding, and custom prompts
# - run a full-featured session with all features combined
#
# Note on costs: cells that run the agent call an LLM and may incur cost. It's always ok to pause, read, and only run what you're comfortable with.
# Estimated runtime: 5-15 minutes depending on LLM latency.
#

# %% [markdown]
# ## Setup
#
# Expected working directory
# - Run this notebook from the repo root where `bambooai_utils.py` and `testdata.csv` live
#
# Where `bambooai_utils` comes from and how to run
# - `bambooai_utils.py` is an internal wrapper module included in this repo
# - Use your normal project install steps to install BambooAI and run notebooks from this directory
#
# Minimal `.env` template
# ```
# EXECUTION_MODE=local
# LLM_CONFIG=LLM_CONFIG.json
#
# # Optional, depending on your environment
# OPENAI_API_KEY=your_key_here
# AZURE_OPENAI_ENDPOINT=your_endpoint_here
# AZURE_OPENAI_API_KEY=your_key_here
# ```
#
# Required vs optional
# - `EXECUTION_MODE` is required by the wrapper
# - `LLM_CONFIG` is optional if `LLM_CONFIG.json` exists in the working directory
# - Provider keys depend on your LLM backend
#

# %% [markdown]
# **This cell will:**
# - configure helper paths
# - print Python, bambooai, and pandas versions
# - import `bambooai_utils` helpers and load `.env`
#

# %%
import os
import sys
from pathlib import Path
from IPython.display import display

# %pip install -q plotly bambooai
# In Docker use /app/helpers_root; locally use <repo>/helpers_root
helpers_root_docker = Path("/app/helpers_root")
helpers_root_local = Path.cwd() / "helpers_root"
for p in [helpers_root_docker, helpers_root_local]:
    if p.exists() and str(p) not in sys.path:
        sys.path.insert(0, str(p))

print("Working directory:", Path.cwd())

try:
    import importlib.metadata as md
except Exception:
    md = None

try:
    import bambooai

    version = (
        md.version("bambooai")
        if md
        else getattr(bambooai, "__version__", "unknown")
    )
    print("bambooai version:", version)
except Exception as e:
    print("bambooai import failed:", e)

from bambooai_utils import (
    _DEFAULT_CSV,
    _build_bamboo_agent,
    _load_dataframe,
    _run_agent,
    _setup_env,
    _parse,
    _resolve_execution_mode,
)

print("bambooai_utils imported successfully")

ARTIFACTS_DIR = Path("artifacts")

_setup_env()


# %% [markdown]
# ## Environment Validation
#
# Before running the agent, confirm your LLM settings. This cell only prints status; it does not call the LLM.
#

# %% [markdown]
# **This cell will:**
# - print key environment settings
# - warn if `LLM_CONFIG` or provider keys are missing
#

# %%
from pathlib import Path

print("EXECUTION_MODE:", os.getenv("EXECUTION_MODE", "<not set>"))
llm_config_env = os.getenv("LLM_CONFIG")
print("LLM_CONFIG env:", llm_config_env or "<not set>")
print("LLM_CONFIG.json exists:", Path("LLM_CONFIG.json").exists())

if not llm_config_env and not Path("LLM_CONFIG.json").exists():
    print("WARNING: No LLM_CONFIG env var and no LLM_CONFIG.json file found.")

key_vars = ["OPENAI_API_KEY", "AZURE_OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
present = [k for k in key_vars if os.getenv(k)]
if not present:
    print(
        "WARNING: No provider API keys found in env (checked OPENAI/AZURE/ANTHROPIC)."
    )
else:
    print("Provider keys set for:", ", ".join(present))


# %% [markdown]
# ## Data and Scenario
#
# `testdata.csv` is a small synthetic customer dataset for demo analysis. It includes demographics, engagement metrics, and churn indicators.
#
# Data dictionary
# - user_id: Unique user identifier
# - age: User age
# - gender: User gender
# - country: Country code
# - device_type: Device type
# - signup_days_ago: Days since signup
# - sessions_last_30d: Sessions in the last 30 days
# - avg_session_duration_min: Average session duration in minutes
# - pages_per_session: Average pages per session
# - has_premium: Premium subscription indicator
# - monthly_spend_usd: Monthly spend in USD
# - support_tickets_90d: Support tickets in last 90 days
# - churned: Churn label
#

# %% [markdown]
# **This cell will:**
# - create `testdata.csv` if it does not exist
#

# %%
from pathlib import Path
import pandas as pd
import random


def assert_or_create_testdata(path: str = "testdata.csv") -> Path:
    csv_path = Path(path)
    if csv_path.exists():
        return csv_path
    random.seed(42)
    n = 20

    def rint(a, b):
        return random.randint(a, b)

    def rfloat(a, b, nd=2):
        return round(random.uniform(a, b), nd)

    def rchoice(seq):
        return random.choice(seq)

    rows = []
    for i in range(n):
        rows.append(
            {
                "user_id": 1001 + i,
                "age": rint(18, 70),
                "gender": rchoice(["female", "male"]),
                "country": rchoice(["US", "CA", "DE", "IN"]),
                "device_type": rchoice(["mobile", "desktop", "tablet"]),
                "signup_days_ago": rint(1, 400),
                "sessions_last_30d": rfloat(1, 30, 1),
                "avg_session_duration_min": rfloat(1, 15, 2),
                "pages_per_session": rfloat(1, 8, 2),
                "has_premium": rchoice([0, 1]),
                "monthly_spend_usd": rfloat(5, 400, 2),
                "support_tickets_90d": rint(0, 5),
                "churned": rchoice([0, 1]),
            }
        )
    df_sample = pd.DataFrame(rows)
    df_sample.to_csv(csv_path, index=False)
    print("Created sample dataset:", csv_path)
    return csv_path


csv_path = assert_or_create_testdata("testdata.csv")


# %% [markdown]
# ## Quick EDA (local dataset)
#
# A quick look helps you trust the data before asking questions.
#

# %% [markdown]
# **This cell will:**
# - load the CSV into a DataFrame
# - show shape, missing values, and a preview
#

# %%
df = _load_dataframe(_DEFAULT_CSV)
print("Shape:", df.shape)
print("Missing values summary:")
print(df.isna().sum())
display(df.head())


# %% [markdown]
# ## BambooAI Conversation Loop
#
# `_run_agent(...)` starts `pd_agent_converse()`, an interactive chat loop.
# Type `exit` or `quit` when you are done, or interrupt the kernel to stop.
#

# %% [markdown]
# ## Minimal Quickstart Run
#
# This is the simplest configuration that demonstrates the tool working. It uses the internal wrapper helpers and default flags.
#
# Try these prompts and what to expect
# - Summarize columns, types, and missing values. Expect a schema summary.
# - Show top 5 rows and a brief dataset description. Expect a quick preview.
# - Plot distribution of monthly_spend_usd. Expect a histogram.
# - Compare churn rate by has_premium. Expect a grouped summary.
# - Identify outliers in avg_session_duration_min. Expect potential outlier list.
#

# %% [markdown]
# **This cell will:**
# - build a minimal BambooAI agent
# - start the interactive conversation loop
#

# %% [markdown]
# ### Parameter Deep Dives
# For parameter-by-parameter explanations and focused demos, see `bambooai.API.ipynb`.
#

# %%
args = _parse().parse_args([])
execution_mode = _resolve_execution_mode(
    args.execution_mode or os.getenv("EXECUTION_MODE", "")
)
os.environ["EXECUTION_MODE"] = execution_mode
print("Execution mode:", execution_mode)

planning = False  # default is True
vector_db = False
search_tool = False

bamboo_agent = _build_bamboo_agent(
    df,
    planning=planning,
    vector_db=vector_db,
    search_tool=search_tool,
)

_run_agent(bamboo_agent)


# %% [markdown]
# **This cell will:**
# - build a planning-enabled agent
# - start the interactive conversation loop
#

# %%
bamboo_planning = _build_bamboo_agent(
    df,
    planning=True,
    vector_db=False,
    search_tool=False,
)

_run_agent(bamboo_planning)


# %% [markdown]
# **This cell will:**
# - create an auxiliary dataset under `./artifacts/`
# - attempt a semantic-search-enabled run (with fallback if unavailable)
#

# %%
from bambooai import BambooAI

ARTIFACTS_DIR.mkdir(exist_ok=True)
aux_path = ARTIFACTS_DIR / "auxiliary_demo.csv"
aux_df = pd.DataFrame(
    {
        "country": ["US", "CA", "DE"],
        "region_label": ["North America", "North America", "Europe"],
    }
)
aux_df.to_csv(aux_path, index=False)
print("Wrote auxiliary dataset:", aux_path)

enable_vector_db = True
enable_search_tool = True

try:
    bamboo_semantic = BambooAI(
        df=df,
        auxiliary_datasets=[str(aux_path)],
        planning=True,
        vector_db=enable_vector_db,
        search_tool=enable_search_tool,
    )
except Exception as e:
    print(
        "Semantic search config failed, falling back with vector_db and search_tool disabled."
    )
    print("Error:", e)
    enable_vector_db = False
    enable_search_tool = False
    bamboo_semantic = BambooAI(
        df=df,
        auxiliary_datasets=[str(aux_path)],
        planning=True,
        vector_db=enable_vector_db,
        search_tool=enable_search_tool,
    )

_run_agent(bamboo_semantic)


# %% [markdown]
# **This cell will:**
# - create a small ontology file under `./artifacts/`
# - run BambooAI with ontology grounding enabled
#

# %%
from bambooai import BambooAI

ARTIFACTS_DIR.mkdir(exist_ok=True)
ontology_path = ARTIFACTS_DIR / "mini_ontology.ttl"
ontology_path.write_text(
    "@prefix ex: <http://example.com/> .\n"
    "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
    "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n"
    "ex:Customer a rdfs:Class .\n"
    "ex:churned a rdfs:Property ;\n"
    "  rdfs:domain ex:Customer ;\n"
    "  rdfs:range xsd:boolean ;\n"
    '  rdfs:label "churned" .\n'
    "ex:monthly_spend_usd a rdfs:Property ;\n"
    "  rdfs:domain ex:Customer ;\n"
    "  rdfs:range xsd:decimal ;\n"
    '  rdfs:label "monthly_spend_usd" .\n'
    "ex:has_premium a rdfs:Property ;\n"
    "  rdfs:domain ex:Customer ;\n"
    "  rdfs:range xsd:boolean ;\n"
    '  rdfs:label "has_premium" .\n'
)
print("Wrote ontology:", ontology_path)

bamboo_ontology = BambooAI(
    df=df,
    df_ontology=str(ontology_path),
    planning=True,
    exploratory=True,
)

_run_agent(bamboo_ontology)


# %% [markdown]
# **This cell will:**
# - create a custom prompt file under `./artifacts/`
# - run BambooAI with custom prompts enabled
#

# %%
from bambooai import BambooAI

ARTIFACTS_DIR.mkdir(exist_ok=True)
custom_prompt_path = ARTIFACTS_DIR / "custom_prompts.yaml"
custom_prompt_path.write_text(
    "# Placeholder prompts for BambooAI\n"
    'planner_prompt: "You are a careful planner."\n'
    'code_prompt: "Write concise pandas code."\n'
)
print("Wrote custom prompts:", custom_prompt_path)

bamboo_custom = BambooAI(
    df=df,
    custom_prompt_file=str(custom_prompt_path),
    planning=False,
    exploratory=True,
)

_run_agent(bamboo_custom)


# %% [markdown]
# ## Full Featured Run
#
# This run combines planning, semantic search, ontology grounding, and custom prompts.
# It expects the artifacts created in the feature sections above.
#

# %% [markdown]
# ### Curated prompts and expected behavior
#
# EDA and sanity checks. Expected behavior: schema overview and summary stats.
# - Summarize columns, types, missing percent, and show df.head()
# - Which columns are categorical vs numeric
#
# Business questions. Expected behavior: grouped analysis and narrative summary.
# - What factors correlate most with churn
# - Compare average spend by premium status
#
# Joining auxiliary_demo.csv. Expected behavior: join by country and analyze by region.
# - Add region labels to country and summarize churn by region
# - Show average spend by region
#
# Ontology grounded Q and A. Expected behavior: use ontology definitions and constraint checks.
# - Explain valid values for churned and has_premium
# - Flag any invalid values based on ontology
#
# Custom prompt style tests. Expected behavior: output format follows custom prompts.
# - Provide a concise bullet summary with 3 takeaways
# - Return a short action plan in numbered steps
#

# %% [markdown]
# **This cell will:**
# - assemble the full feature configuration
# - run the BambooAI conversation loop
#

# %%
from bambooai import BambooAI

aux_path = ARTIFACTS_DIR / "auxiliary_demo.csv"
ontology_path = ARTIFACTS_DIR / "mini_ontology.ttl"
custom_prompt_path = ARTIFACTS_DIR / "custom_prompts.yaml"

missing = [
    name
    for name, p in [
        ("auxiliary_demo.csv", aux_path),
        ("mini_ontology.ttl", ontology_path),
        ("custom_prompts.yaml", custom_prompt_path),
    ]
    if not p.exists()
]
if missing:
    print("Missing artifacts:", ", ".join(missing))
    print("Run the feature focus sections above to create them.")

aux_list = [str(aux_path)] if aux_path.exists() else []
df_ontology = str(ontology_path) if ontology_path.exists() else None
custom_prompt_file = (
    str(custom_prompt_path) if custom_prompt_path.exists() else None
)

try:
    enable_vector_db
except NameError:
    enable_vector_db = True
try:
    enable_search_tool
except NameError:
    enable_search_tool = True


def print_config_summary(config: dict) -> None:
    print("Config Summary")
    for key, value in config.items():
        print(f"- {key}: {value}")


base_config = {
    "df": df,
    "planning": True,
    "vector_db": enable_vector_db,
    "search_tool": enable_search_tool,
    "exploratory": True,
}
if aux_list:
    base_config["auxiliary_datasets"] = aux_list
if df_ontology:
    base_config["df_ontology"] = df_ontology
if custom_prompt_file:
    base_config["custom_prompt_file"] = custom_prompt_file

print_config_summary(base_config)

try:
    bamboo_full = BambooAI(**base_config)
except Exception as e:
    print(
        "Full featured config failed, falling back with vector_db and search_tool disabled."
    )
    print("Error:", e)
    base_config["vector_db"] = False
    base_config["search_tool"] = False
    bamboo_full = BambooAI(**base_config)

_run_agent(bamboo_full)


# %% [markdown]
# ## Troubleshooting
#
# Missing env vars
# - Ensure `EXECUTION_MODE` is set in `.env` or environment
# - Ensure provider keys are set for your LLM backend
#
# Missing files or wrong working directory
# - Run the notebook from the repo root
# - Re-run the data creation cell to regenerate missing files
#
# Import errors
# - Verify bambooai and pandas are installed in this environment
# - Restart the kernel after installing packages
#
# Agent hangs or no output
# - Confirm network access to your LLM backend
# - Check logs for rate limits or authentication errors
# - Try the Minimal Quickstart run to isolate failures
#
# Logs
# - Per-run logs typically live under `logs/`
# - A consolidated log may be written to `bambooai_consolidated_log.json`
#

# %% [markdown]
# ## Cleanup
#

# %% [markdown]
# **This cell will:**
# - delete files created under `./artifacts/`
#

# %%
for p in [
    ARTIFACTS_DIR / "auxiliary_demo.csv",
    ARTIFACTS_DIR / "mini_ontology.ttl",
    ARTIFACTS_DIR / "custom_prompts.yaml",
]:
    if p.exists():
        p.unlink()
        print("Deleted:", p)
    else:
        print("Not found:", p)

if ARTIFACTS_DIR.exists() and not any(ARTIFACTS_DIR.iterdir()):
    ARTIFACTS_DIR.rmdir()
    print("Removed empty directory:", ARTIFACTS_DIR)


# %% [markdown]
# ## Next Steps
#
# - Swap `testdata.csv` with your own dataset and re-run the quickstart
# - Explore the core code in `bambooai_utils.py` and `bambooai` package
#
