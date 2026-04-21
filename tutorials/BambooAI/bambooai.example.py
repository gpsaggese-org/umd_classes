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
# This notebook is a guided, end-to-end tour of BambooAI for analysis workflows.
#
# **Note:** Cells that run the agent call an LLM and may incur cost. For parameter-by-parameter explanations and focused demos, see `bambooai.API.ipynb`.

# %% [markdown]
# ## Setup
#
# Expected working directory
# - Run this notebook from the repo root where `bambooai_utils.py` and `testdata.csv` live.
#
# Required vs optional
# - `EXECUTION_MODE` is required by the wrapper.
# - `LLM_CONFIG` is optional if `LLM_CONFIG.json` exists in the working directory.
# - Provider keys depend on your LLM backend.

# %%
# %load_ext autoreload
# %autoreload 2

# System libraries.
import logging
import os
import random
import sys
from pathlib import Path

# Third party libraries.
import importlib.metadata as md
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import display

# Configure notebook plotting defaults.
# sns.set_style("whitegrid")
# plt.rcParams["figure.figsize"] = (12, 6)
# np.set_printoptions(suppress=True, precision=6)
# print("Notebook bootstrap complete.")

# %%
# Add local helper paths and import the notebook utilities.
# helpers_root_docker = Path("/app/helpers_root")
# helpers_root_local = Path.cwd() / "helpers_root"
# for candidate in [helpers_root_docker, helpers_root_local]:
#     if candidate.exists() and str(candidate) not in sys.path:
#         sys.path.insert(0, str(candidate))

# import bambooai
from bambooai import BambooAI

import bambooai_utils as butils
import helpers.hio as hio

ARTIFACTS_DIR = Path("artifacts")
print("Working directory:", Path.cwd())
print("bambooai version:", md.version("bambooai"))
# The project modules are now importable from the notebook.

# %%
# Initialize notebook logging through the shared utility module.
_LOG = logging.getLogger(__name__)
butils.init_logger(_LOG)
butils._setup_env()
print("Notebook logging initialized.")
# Logger output from the notebook and utility module now prints inline.

# %% [markdown]
# ## Sanity Check
#
# Confirm the runtime configuration before starting any agent session.

# %%
os.environ['OPENAI_API_KEY']='sk-proj'
os.environ['GEMINI_API_KEY']=''

# %%
# Display the current execution and credential configuration.
execution_mode_env = os.getenv("EXECUTION_MODE", "<not set>")
llm_config_env = os.getenv("LLM_CONFIG", "<not set>")
llm_config_exists = Path("LLM_CONFIG.json").exists()
key_vars = ["OPENAI_API_KEY", "AZURE_OPENAI_API_KEY", "ANTHROPIC_API_KEY","GEMINI_API_KEY"]
present_keys = [key for key in key_vars if os.getenv(key)]

print("EXECUTION_MODE:", execution_mode_env)
print("LLM_CONFIG env:", llm_config_env)
print("LLM_CONFIG.json exists:", llm_config_exists)
print("Provider keys set for:", ", ".join(present_keys) or "<none>")
# This confirms whether the notebook has enough configuration to start BambooAI.

# %% [markdown]
# ## Data and Scenario
#
# `testdata.csv` is a small synthetic customer dataset for demo analysis. It includes demographics, engagement metrics, and churn indicators.
#
# Data dictionary
# - user_id: Unique user identifier.
# - age: User age.
# - gender: User gender.
# - country: Country code.
# - device_type: Device type.
# - signup_days_ago: Days since signup.
# - sessions_last_30d: Sessions in the last 30 days.
# - avg_session_duration_min: Average session duration in minutes.
# - pages_per_session: Average pages per session.
# - has_premium: Premium subscription indicator.
# - monthly_spend_usd: Monthly spend in USD.
# - support_tickets_90d: Support tickets in last 90 days.
# - churned: Churn label.

# %%
# Create a small synthetic dataset if the demo CSV is missing.
def _create_testdata_if_missing(*, path: str = "testdata.csv") -> Path:
    """
    Create synthetic test data if the CSV is missing.

    :param path: output CSV path
    :return: path to the CSV file
    """
    csv_path = Path(path)
    if csv_path.exists():
        return csv_path
    random.seed(42)
    rows = []
    for idx in range(20):
        rows.append(
            {
                "user_id": 1001 + idx,
                "age": random.randint(18, 70),
                "gender": random.choice(["female", "male"]),
                "country": random.choice(["US", "CA", "DE", "IN"]),
                "device_type": random.choice(["mobile", "desktop", "tablet"]),
                "signup_days_ago": random.randint(1, 400),
                "sessions_last_30d": round(random.uniform(1, 30), 1),
                "avg_session_duration_min": round(random.uniform(1, 15), 2),
                "pages_per_session": round(random.uniform(1, 8), 2),
                "has_premium": random.choice([0, 1]),
                "monthly_spend_usd": round(random.uniform(5, 400), 2),
                "support_tickets_90d": random.randint(0, 5),
                "churned": random.choice([0, 1]),
            }
        )
    pd.DataFrame(rows).to_csv(csv_path, index=False)
    return csv_path


csv_path = _create_testdata_if_missing(path="testdata.csv")
print("Dataset path:", csv_path)
# The demo dataset is available for the rest of the notebook.

# %% [markdown]
# ## Quick EDA
#
# Take a quick look at the dataset before asking BambooAI questions about it.

# %%
# Load the dataframe and show the dataset dimensions.
df = butils._load_dataframe(butils._DEFAULT_CSV)
print("Shape:", df.shape)
display(df.dtypes.rename("dtype").to_frame())
# The dataframe loaded successfully and the schema is visible.

# %%
# Summarize missing values and preview the first rows.
display(df.isna().sum().rename("missing_values").to_frame())
display(df.head())
# The dataset appears ready for interactive analysis.

# %% [markdown]
# ## Conversation Loop
#
# `butils._run_agent(...)` an interactive chat loop.
# Type `exit` or `quit` when you are done, or interrupt the kernel to stop.

# %% [markdown]
# Try these prompts and what to expect
# - Summarize columns, types, and missing values. Expect a schema summary.
# - Show top 5 rows and a brief dataset description. Expect a quick preview.
# - Plot distribution of monthly_spend_usd. Expect a histogram.
# - Compare churn rate by has_premium. Expect a grouped summary.
# - Identify outliers in avg_session_duration_min. Expect a potential outlier list.

# %%
# Resolve the execution mode for the notebook session.
args = butils._parse().parse_args([])
execution_mode = butils._resolve_execution_mode(
    args.execution_mode or os.getenv("EXECUTION_MODE", "local")
)
os.environ["EXECUTION_MODE"] = execution_mode
print("Execution mode:", execution_mode)
# The notebook session now has an explicit execution mode.

# %%
# Build the minimal BambooAI configuration.
minimal_config = {
    "planning": False, #No planning enabled
    "vector_db": False, #No vector DB searches 
    "search_tool": False, #No web searche enabled
}
display(pd.Series(minimal_config, name="enabled").to_frame())
# This is the smallest configuration that still exercises the core workflow.

# %%
# Construct the minimal BambooAI agent and show its type.
bamboo_agent = butils._build_bamboo_agent(df, **minimal_config)
print("Constructed agent type:", type(bamboo_agent).__name__)
# The minimal BambooAI agent is ready for interaction.

# %%
# Start the minimal config conversation loop.
butils._run_agent(bamboo_agent)
# The minimal config agent interactive session is now running.

# %%
# Construct the planning-enabled BambooAI agent.
bamboo_planning = butils._build_bamboo_agent(
    df,
    planning=True,
    vector_db=False,
    search_tool=False,
)
print("Constructed planning agent type:", type(bamboo_planning).__name__)
# The planning-enabled agent is ready for interaction.

# %%
# Start the planning-enabled conversation loop.
butils._run_agent(bamboo_planning)
# The planning-enabled interactive session is now running.

# %% [markdown]
# ## Semantic Search Demo
#
# Create an auxiliary dataset and run BambooAI with semantic search features enabled.

# %%
# Create the auxiliary dataset used by the semantic-search configuration.
hio.create_dir(str(ARTIFACTS_DIR), incremental=True)
aux_path = ARTIFACTS_DIR / "auxiliary_demo.csv"
aux_df = pd.DataFrame(
    {
        "country": ["US", "CA", "DE"],
        "region_label": ["North America", "North America", "Europe"],
    }
)
aux_df.to_csv(aux_path, index=False)
display(aux_df)
print("Wrote auxiliary dataset:", aux_path)
# The semantic-search demo now has an auxiliary dataset to join against.

# %%
# Build the semantic-search BambooAI agent.
semantic_config = {
    "planning": True,
    "vector_db": True,
    "search_tool": True,
    "auxiliary_datasets": [str(aux_path)],
}
display(pd.Series(semantic_config, name="value").to_frame())
bamboo_semantic = BambooAI(df=df, **semantic_config)
print("Constructed semantic agent type:", type(bamboo_semantic).__name__)
# The semantic-search configuration is ready for interaction.

# %%
# Start the semantic-search conversation loop.
butils._run_agent(bamboo_semantic)
# The semantic-search interactive session is now running.

# %% [markdown]
# ## Ontology Demo
#
# Create a small ontology file and run BambooAI with ontology grounding enabled.

# %%
# Write a minimal ontology file for the dataframe fields.
hio.create_dir(str(ARTIFACTS_DIR), incremental=True)
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
print(ontology_path.read_text())
# The ontology file is now available for grounding dataframe questions.

# %%
# Build the ontology-grounded BambooAI agent.
ontology_config = {
    "planning": True,
    "exploratory": True,
    "df_ontology": str(ontology_path),
}
display(pd.Series(ontology_config, name="value").to_frame())
bamboo_ontology = BambooAI(df=df, **ontology_config)
print("Constructed ontology agent type:", type(bamboo_ontology).__name__)
# The ontology-grounded configuration is ready for interaction.

# %%
# Start the ontology-grounded conversation loop.
butils._run_agent(bamboo_ontology)
# The ontology-grounded interactive session is now running.

# %% [markdown]
# ## Custom Prompt Demo
#
# Create a custom prompt file and run BambooAI with custom prompts enabled.

# %%
# Write a small custom prompt file for the demo run.
hio.create_dir(str(ARTIFACTS_DIR), incremental=True)
custom_prompt_path = ARTIFACTS_DIR / "custom_prompts.yaml"
custom_prompt_path.write_text(
    "# Placeholder prompts for BambooAI\n"
    'planner_prompt: "You are a careful planner."\n'
    'code_prompt: "Write concise pandas code."\n'
)
print(custom_prompt_path.read_text())
# The custom prompt file is available for the next BambooAI run.

# %%
# Build the custom-prompt BambooAI agent.
custom_prompt_config = {
    "planning": False,
    "exploratory": True,
    "custom_prompt_file": str(custom_prompt_path),
}
display(pd.Series(custom_prompt_config, name="value").to_frame())
bamboo_custom = BambooAI(df=df, **custom_prompt_config)
print("Constructed custom prompt agent type:", type(bamboo_custom).__name__)
# The custom-prompt configuration is ready for interaction.

# %%
# Start the custom-prompt conversation loop.
butils._run_agent(bamboo_custom)
# The custom-prompt interactive session is now running.

# %% [markdown]
# ## Full Featured Run
#
# This run combines planning, semantic search, ontology grounding, and custom prompts.
# It expects the artifacts created in the feature sections above.
#
# Curated prompts and expected behavior
# - Summarize columns, types, missing percent, and show `df.head()`.
# - What factors correlate most with churn.
# - Add region labels to country and summarize churn by region.
# - Explain valid values for `churned` and `has_premium`.
# - Provide a concise bullet summary with 3 takeaways.

# %%
# Locate the optional artifacts that enrich the full BambooAI run.
aux_path = ARTIFACTS_DIR / "auxiliary_demo.csv"
ontology_path = ARTIFACTS_DIR / "mini_ontology.ttl"
custom_prompt_path = ARTIFACTS_DIR / "custom_prompts.yaml"
artifact_status = pd.Series(
    {
        "auxiliary_demo.csv": aux_path.exists(),
        "mini_ontology.ttl": ontology_path.exists(),
        "custom_prompts.yaml": custom_prompt_path.exists(),
    },
    name="exists",
)
display(artifact_status.to_frame())
# This shows which optional artifacts are available for the combined run.

# %%
# Assemble the full-feature BambooAI configuration from the available artifacts.
full_config = {
    "planning": True,
    "vector_db": True,
    "search_tool": True,
    "exploratory": True,
}
if aux_path.exists():
    full_config["auxiliary_datasets"] = [str(aux_path)]
if ontology_path.exists():
    full_config["df_ontology"] = str(ontology_path)
if custom_prompt_path.exists():
    full_config["custom_prompt_file"] = str(custom_prompt_path)

display(pd.Series(full_config, name="value").to_frame())
# The combined configuration is ready to instantiate.

# %%
# Build the full-feature BambooAI agent.
bamboo_full = BambooAI(df=df, **full_config)
print("Constructed full agent type:", type(bamboo_full).__name__)
# The full-feature BambooAI agent is ready for interaction.

# %%
# Start the full-feature conversation loop.
butils._run_agent(bamboo_full)
# The full-feature interactive session is now running.

# %% [markdown]
# ## Troubleshooting
#
# Missing env vars
# - Ensure `EXECUTION_MODE` is set in `.env` or environment.
# - Ensure provider keys are set for your LLM backend.
#
# Missing files or wrong working directory
# - Run the notebook from the repo root.
# - Re-run the data creation cell to regenerate missing files.
#
# Import errors
# - Verify BambooAI and pandas are installed in this environment.
# - Restart the kernel after changing your environment.
#
# Agent hangs or no output
# - Confirm network access to your LLM backend.
# - Check logs for rate limits or authentication errors.
# - Try the minimal quickstart run to isolate failures.

# %% [markdown]
# ## Cleanup
#
# Remove the generated artifacts if you want to reset the demo state.

# %%
# Delete the generated artifacts from the notebook run.
for path in [
    ARTIFACTS_DIR / "auxiliary_demo.csv",
    ARTIFACTS_DIR / "mini_ontology.ttl",
    ARTIFACTS_DIR / "custom_prompts.yaml",
]:
    if path.exists():
        path.unlink()
        print("Deleted:", path)
    else:
        print("Not found:", path)
# The generated files have been removed if they existed.

# %%
# Remove the artifact directory if it is now empty.
if ARTIFACTS_DIR.exists() and not any(ARTIFACTS_DIR.iterdir()):
    ARTIFACTS_DIR.rmdir()
    print("Removed empty directory:", ARTIFACTS_DIR)
else:
    print("Artifact directory still contains files:", ARTIFACTS_DIR)
# The artifact directory state is now explicit.
