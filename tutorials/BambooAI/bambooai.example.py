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
import os
import random
import sys
import textwrap
from pathlib import Path

# Third party libraries.
import importlib.metadata as md
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import display
# The common notebook libraries are loaded.

# %%
# Import notebook-specific modules.
from bambooai import BambooAI

import bambooai_utils as butils
import helpers.hio as hio

display(["BambooAI", "bambooai_utils", "hio"])
# The BambooAI and local helper modules are available.

# %%
# Configure notebook logging.
_LOG = logging.getLogger(__name__)
butils.init_logger(_LOG)
_LOG.info("Notebook logging is configured.")
# Notebook logging is configured.

# %% [markdown]
# # BambooAI End-to-End Demo: Conversational Data Analysis
#
# # Summary
#
# This notebook demonstrates an end-to-end BambooAI workflow for customer churn analysis using natural-language questions, supporting context files, ontology grounding, custom prompts, and interactive agents.
#
# ## Workflow Goals
#
# - **Customer churn behavior**: Analyze churn behavior in a synthetic customer dataset.
# - **Premium comparison**: Compare premium and non-premium users.
# - **External context**: Enrich analysis with region and market-tier context.
# - **Domain semantics**: Apply ontology grounding to customer churn fields.
# - **Business insights**: Generate actionable business recommendations.

# %% [markdown]
# ## Setup
#
# - **Expected working directory**: Run this notebook from the repo root where `bambooai_utils.py` and `testdata.csv` live.
# - **Required configuration**: `EXECUTION_MODE` is required by the wrapper.
# - **Optional configuration**: `LLM_CONFIG` is optional if `LLM_CONFIG.json` exists in the working directory.
# - **Provider keys**: Provider keys depend on the selected LLM backend.

# %%
# Initialize notebook environment through the shared utility module.
butils._setup_env()
ARTIFACTS_DIR = Path("artifacts")
_LOG.info("Working directory: %s", Path.cwd())
_LOG.info("bambooai version: %s", md.version("bambooai"))
_LOG.info("Notebook logging initialized.")
# The notebook runtime context is visible in the output.

# %% [markdown]
# ## Sanity Check
#
# - **Goal**: Confirm the runtime configuration before starting any agent session.

# %%
# Display the current execution and credential configuration.
execution_mode_env = os.getenv("EXECUTION_MODE", "<not set>")
llm_config_env = os.getenv("LLM_CONFIG", "<not set>")
llm_config_exists = Path("LLM_CONFIG.json").exists()
key_vars = ["OPENAI_API_KEY", "AZURE_OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY"]
present_keys = [key for key in key_vars if os.getenv(key)]

_LOG.info("EXECUTION_MODE: %s", execution_mode_env)
_LOG.info("LLM_CONFIG env: %s", llm_config_env)
_LOG.info("LLM_CONFIG.json exists: %s", llm_config_exists)
_LOG.info("Provider keys set for: %s", ", ".join(present_keys) or "<none>")
# The output confirms whether the notebook has enough configuration to start BambooAI.

# %% [markdown]
# ## 2. Create a Sample Business Dataset
#
# - **Goal**: Generate a synthetic customer churn dataset that keeps the notebook self-contained.
#
#     - **`customer_id`**: Unique user ID.
#     - **`country`**: Customer country.
#     - **`age`**: Customer age.
#     - **`tenure_months`**: Customer tenure with the company.
#     - **`monthly_spend`**: Monthly spend amount.
#     - **`support_tickets_last_90d`**: Support interactions in the last 90 days.
#     - **`has_premium`**: Premium subscription flag.
#     - **`engagement_score`**: Synthetic product engagement score.
#     - **`churned`**: Customer churn outcome.
#
# ## Business Framing
#
# - **Premium impact**: Check whether premium membership reduces churn.
# - **Regional risk**: Check whether some regions have higher churn risk.
# - **Customer characteristics**: Identify characteristics associated with churn.
# - **Business actions**: Identify actions that could reduce churn.

# %%
# Define reproducible sample dataset parameters.
np.random.seed(42)

n = 500
countries = ["United States", "India", "Germany", "Brazil", "Canada", "UK"]
country_probs = [0.22, 0.18, 0.15, 0.15, 0.12, 0.18]

_LOG.info("Synthetic customer count: %s", n)
# The dataset size and country sampling inputs are ready.

# %%
# Create the synthetic customer feature dataframe.
df = pd.DataFrame({
    "customer_id": np.arange(10001, 10001 + n),
    "country": np.random.choice(countries, size=n, p=country_probs),
    "age": np.random.randint(18, 66, size=n),
    "tenure_months": np.random.randint(1, 61, size=n),
    "monthly_spend": np.round(np.random.normal(58, 18, size=n).clip(10, 150), 2),
    "support_tickets_last_90d": np.random.poisson(lam=1.8, size=n),
    "has_premium": np.random.choice([0, 1], size=n, p=[0.58, 0.42]),
    "engagement_score": np.round(np.random.normal(62, 15, size=n).clip(5, 100), 1),
})

display(df.head())
# The dataframe contains the base customer attributes.

# %%
# Build a churn logit from customer risk signals.
logit = (
    -1.0
    + 0.55 * (df["has_premium"] == 0).astype(int)
    + 0.04 * (3 - df["support_tickets_last_90d"].clip(upper=3))
    + 0.03 * (24 - df["tenure_months"].clip(upper=24))
    + 0.025 * (55 - df["engagement_score"]).clip(lower=0)
)

_LOG.info("Churn logit values: %s", len(logit))
# The churn logit captures base customer-level churn risk.

# %%
# Add the country-level churn risk adjustment.
country_risk = {
    "United States": 0.10,
    "India": 0.18,
    "Germany": 0.08,
    "Brazil": 0.20,
    "Canada": 0.07,
    "UK": 0.12,
}
logit += df["country"].map(country_risk)

display(pd.Series(country_risk, name="risk").to_frame())
# The country risk mapping has been applied to the churn logit.

# %%
# Convert the logit to a binary churn outcome.
prob = 1 / (1 + np.exp(-(logit - 1.8)))
df["churned"] = (np.random.rand(n) < prob).astype(int)

display(df.head())
_LOG.info("Dataframe shape: %s", df.shape)
# The dataset is ready for BambooAI analysis.

# %% [markdown]
# ## 3. Quick Data Sanity Check
#
# - **Goal**: Review the generated dataset before using BambooAI.

# %%
# Show a compact sanity check of the generated dataset.
display(df.info())
display(df.describe(include="all").T)
_LOG.info("Churn rate: %s", round(df["churned"].mean(), 3))
_LOG.info("Premium rate: %s", round(df["has_premium"].mean(), 3))
# The output summarizes schema, distributions, and headline rates.

# %% [markdown]
# ## 4. Prepare Supporting Context Files
#
# - **Goal**: Add supporting context that BambooAI can optionally use later for richer analysis.
#     - **Auxiliary dataset**: Country-to-region mapping.
#     - **Ontology file**: Domain semantics.
#     - **Custom prompt YAML**: Business-oriented response style.

# %%
# Define the asset directory and supporting file paths.
assets_dir = Path("bambooai_e2e_assets")
hio.create_dir(str(assets_dir))

aux_path = assets_dir / "country_region_reference.csv"
ontology_path = assets_dir / "customer_churn_ontology.ttl"
custom_prompt_path = assets_dir / "business_summary_prompt.yml"

_LOG.info("Asset directory: %s", assets_dir)
# The supporting file paths are ready.

# %%
# Create the auxiliary country-to-region reference dataset.
region_df = pd.DataFrame({
    "country": ["United States", "India", "Germany", "Brazil", "Canada", "UK"],
    "region": ["North America", "Asia", "Europe", "South America", "North America", "Europe"],
    "market_tier": ["Mature", "Growth", "Mature", "Growth", "Mature", "Mature"],
})
region_df.to_csv(aux_path, index=False)

display(region_df)
# The auxiliary dataset is written for later semantic-context analysis.

# %%
# Write the ontology file that describes churn-domain semantics.
ontology_text = textwrap.dedent("""
@prefix ex: <http://example.com/churn#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:Customer a rdfs:Class .
ex:PremiumCustomer a rdfs:Class ;
    rdfs:subClassOf ex:Customer .

ex:churned a rdfs:Property ;
    rdfs:label "customer churn outcome" .

ex:has_premium a rdfs:Property ;
    rdfs:label "premium subscription flag" .

ex:engagement_score a rdfs:Property ;
    rdfs:label "customer engagement score" .

ex:tenure_months a rdfs:Property ;
    rdfs:label "customer tenure in months" .

ex:support_tickets_last_90d a rdfs:Property ;
    rdfs:label "support burden in recent period" .
""").strip()

ontology_path.write_text(ontology_text, encoding="utf-8")
_LOG.info("Ontology file: %s", ontology_path)
# The ontology file is available for domain-grounded analysis.

# %%
# Write the custom prompt file for business-oriented responses.
custom_prompt_text = textwrap.dedent("""
planner_system_prompt: |
  You are assisting with customer churn analysis.
  When planning, prefer concise multi-step plans that focus on:
  1. identifying churn drivers,
  2. segmenting important customer groups,
  3. producing business-oriented takeaways.

analyst_system_prompt: |
  You are a business analyst working on churn reduction.
  Keep outputs concise, structured, and action-oriented.
  When appropriate, end with 2-4 practical recommendations.
""").strip()

custom_prompt_path.write_text(custom_prompt_text, encoding="utf-8")
_LOG.info("Custom prompt file: %s", custom_prompt_path)
# The custom prompt file is available for output style control.

# %% [markdown]
# ## 5. Baseline: Minimal BambooAI Workflow
#
# - **Goal**: Start with the simplest setup and keep most parameters disabled.
#
# ### Suggested Prompts
#
# - `Compare churn rates for premium vs non-premium users`
# - `Analyze churn by country`
# - `Does engagement score appear related to churn?`
# - `Compare churn across tenure groups`
# - `Summarize the main basic patterns in this dataset`

# %%
# Configure the minimal BambooAI workflow.
minimal_config = {
    "df": df,
    "planning": False,
}

display(pd.Series(minimal_config, name="value").to_frame())
# The minimal configuration is ready for agent construction.

# %%
# Construct the minimal BambooAI agent.
bamboo_minimal = BambooAI(**minimal_config)
_LOG.info(
    "Constructed minimal BambooAI agent: %s",
    type(bamboo_minimal).__name__,
)
# The minimal BambooAI agent is ready for interactive use.

# %%
# Start the minimal interactive conversation.
butils._run_agent(bamboo_minimal)
_LOG.info("Minimal workflow completed or exited by the user.")
# The minimal workflow is available for direct dataframe questions.

# %% [markdown]
# ## 6. Add Planning for Multi-step Reasoning
#
# - **Goal**: Enable `planning` for decomposition, structured reasoning, and stronger multi-step solutions.
# - **Churn drivers**: Identify variables associated with churn.
# - **Segments**: Compare customer groups.
# - **Findings**: Summarize analysis results.
# - **Recommendations**: Generate actions for churn reduction.
#
# ### Suggested Prompts
#
# - `Identify the main churn drivers and summarize the highest-risk customer groups`
# - `Compare churn by premium status, engagement, and tenure, then explain the biggest risk factors`
# - `Segment customers into meaningful groups and summarize which groups look most at risk`
# - `Analyze churn patterns and provide a short executive summary`

# %%
# Configure the planning-enabled BambooAI workflow.
planning_config = {
    "df": df,
    "planning": True,
}

display(pd.Series(planning_config, name="value").to_frame())
# The planning configuration is ready for agent construction.

# %%
# Construct the planning-enabled BambooAI agent.
bamboo_planning = BambooAI(**planning_config)
_LOG.info(
    "Constructed planning BambooAI agent: %s",
    type(bamboo_planning).__name__,
)
# The planning-enabled BambooAI agent is ready for interactive use.

# %%
# Start the planning-enabled interactive conversation.
butils._run_agent(bamboo_planning)
_LOG.info("Planning workflow completed or exited by the user.")
# The planning workflow is available for multi-step analysis questions.

# %% [markdown]
# ## 7. Add Auxiliary Context for Richer Analysis
#
# - **Goal**: Add reference files, metadata, mapping tables, or supplementary datasets for richer analysis.
# - **Auxiliary dataset**: Additional data file that provides extra context for the primary dataset.
# - **Expected effect**: Enable richer analysis and interpretation.
#
# ### Suggested Prompts
#
# - `Use the auxiliary dataset to analyze churn by region`
# - `Compare churn across market tiers`
# - `Summarize whether growth markets show different churn behavior than mature markets`
# - `Use the supporting context to provide a geography-based churn summary`

# %%
# Configure the auxiliary-context BambooAI workflow.
semantic_config = {
    "df": df,
    "planning": True,
    "vector_db": True,
    "search_tool": True,
    "auxiliary_datasets": [str(aux_path)],
}

display(pd.Series(semantic_config, name="value").to_frame())
# The auxiliary-context configuration is ready for agent construction.

# %%
# Construct the auxiliary-context BambooAI agent.
bamboo_semantic = BambooAI(**semantic_config)
_LOG.info(
    "Constructed semantic-context BambooAI agent: %s",
    type(bamboo_semantic).__name__,
)
# The auxiliary-context BambooAI agent is ready for interactive use.

# %%
# Start the auxiliary-context interactive conversation.
butils._run_agent(bamboo_semantic)
_LOG.info("Auxiliary-context workflow completed or exited by the user.")
# The auxiliary-context workflow is available for region and market-tier questions.

# %% [markdown]
# ## 8. Add Ontology for Domain Grounding
#
# - **Goal**: Use ontology grounding to clarify column meaning and business concepts.
# - **Domain-aware interpretation**: Explain churn fields in business terms.
# - **Grounded analysis**: Connect raw columns to domain semantics.
# - **Business framing**: Improve explanations of churn profiles and lifecycle factors.
#
# ### Suggested Prompts
#
# - `Interpret churn using the business meaning of premium status, engagement, and support load`
# - `Explain how the ontology changes the interpretation of churn-related fields`
# - `Summarize the customer lifecycle factors associated with churn`
# - `Use domain semantics to describe high-risk customer profiles`

# %%
# Configure the ontology-grounded BambooAI workflow.
ontology_config = {
    "df": df,
    "planning": True,
    "exploratory": True,
    "df_ontology": str(ontology_path),
}

display(pd.Series(ontology_config, name="value").to_frame())
# The ontology configuration is ready for agent construction.

# %%
# Construct the ontology-grounded BambooAI agent.
bamboo_ontology = BambooAI(**ontology_config)
_LOG.info(
    "Constructed ontology-grounded BambooAI agent: %s",
    type(bamboo_ontology).__name__,
)
# The ontology-grounded BambooAI agent is ready for interactive use.

# %%
# Start the ontology-grounded interactive conversation.
butils._run_agent(bamboo_ontology)
_LOG.info("Ontology-grounded workflow completed or exited by the user.")
# The ontology workflow is available for domain-semantics questions.

# %% [markdown]
# ## 9. Add Custom Prompts for Output Style Control
#
# - **Goal**: Present the same analysis differently for different audiences.
# - **Audiences**: Data scientists, analysts, executives, and product managers.
# - **Custom prompt style**: Concise outputs, business-oriented language, and practical recommendations.
#
# ### Suggested Prompts
#
# - `Summarize the churn problem for a business stakeholder`
# - `Provide three practical recommendations to reduce churn`
# - `Create an executive-style summary of churn patterns`
# - `Explain the main churn insights concisely and actionably`

# %%
# Configure the custom-prompt BambooAI workflow.
custom_prompt_config = {
    "df": df,
    "planning": True,
    "exploratory": True,
    "custom_prompt_file": str(custom_prompt_path),
}

display(pd.Series(custom_prompt_config, name="value").to_frame())
# The custom-prompt configuration is ready for agent construction.

# %%
# Construct the custom-prompt BambooAI agent.
bamboo_custom = BambooAI(**custom_prompt_config)
_LOG.info(
    "Constructed custom-prompt BambooAI agent: %s",
    type(bamboo_custom).__name__,
)
# The custom-prompt BambooAI agent is ready for interactive use.

# %%
# Start the custom-prompt interactive conversation.
butils._run_agent(bamboo_custom)
_LOG.info("Custom-prompt workflow completed or exited by the user.")
# The custom-prompt workflow is available for business-stakeholder summaries.

# %% [markdown]
# ## 10. Final Full E2E Workflow
#
# - **Goal**: Combine the earlier capabilities into a single workflow, combining:
#     - **Planning**: Multi-step reasoning.
#     - **Auxiliary context**: Business context.
#     - **Vector and semantic support**: Semantic enrichment.
#     - **Ontology grounding**: Domain grounding.
#     - **Custom prompt control**: Action-oriented outputs.
#
# ### Suggested Prompts
#
# - `Analyze churn drivers, compare premium vs non-premium users, and provide an executive summary`
# - `Use all available context to identify the highest-risk customer segments and recommend actions`
# - `Combine region context, ontology semantics, and churn analysis to produce a business report`
# - `Create a concise stakeholder summary of churn risk patterns and recommended next steps`

# %%
# Configure the full end-to-end BambooAI workflow.
full_config = {
    "df": df,
    "planning": True,
    "vector_db": True,
    "search_tool": True,
    "auxiliary_datasets": [str(aux_path)],
    "df_ontology": str(ontology_path),
    "custom_prompt_file": str(custom_prompt_path),
    "exploratory": True,
}

display(pd.Series(full_config, name="value").to_frame())
# The full end-to-end configuration is ready for agent construction.

# %%
# Construct the full-feature BambooAI agent.
bamboo_full = BambooAI(**full_config)
_LOG.info(
    "Constructed full-feature BambooAI agent: %s",
    type(bamboo_full).__name__,
)
# The full-feature BambooAI agent is ready for interactive use.

# %%
# Start the full end-to-end interactive conversation.
butils._run_agent(bamboo_full)
_LOG.info("Full workflow completed or exited by the user.")
# The full workflow is available for combined context, ontology, and prompt-control questions.
