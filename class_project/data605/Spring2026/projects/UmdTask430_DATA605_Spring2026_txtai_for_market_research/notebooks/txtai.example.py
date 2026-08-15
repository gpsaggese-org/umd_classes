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
# # txtai Market Research — End-to-End Example
#
# Walks through the full project pipeline against AAPL:
#
# 1. Ingest a small batch of SEC filings + news articles
# 2. Confirm the documents land in the txtai index
# 3. Drive the agentic research pipeline (router -> retrievers -> synthesizer)
# 4. Inspect routing, retrievals, and the synthesized answer
#
# Prerequisites: `docker-compose up -d` must be running so KeyDB,
# PostgreSQL+pgvector, and MinIO are reachable. Secrets must be present in
# `.env` (`SEC_USER_AGENT`, `NEWSAPI_KEY`, `ALPHAVANTAGE_API_KEY`,
# `OPENAI_API_KEY`).
#
# ## Endpoints exercised in this notebook
#
# The notebook touches three layers of the project. Knowing which call
# lives where makes it easy to swap in a different driver (CLI, HTTP,
# Streamlit) for the same pipeline.
#
# ### Python entry points (used directly by this notebook)
#
# | Symbol                                       | Source                              | Purpose                                                  | Cell |
# |----------------------------------------------|-------------------------------------|----------------------------------------------------------|------|
# | `app.collectors.SECCollector.collect(...)`   | `app/collectors/sec_collector.py`   | Pull filings into MinIO + Postgres + txtai               |  1   |
# | `app.pipeline.embeddings.get_embeddings()`   | `app/pipeline/embeddings.py`        | Singleton `txtai.Embeddings` index used by every agent   |  2   |
# | `app.pipeline.embeddings.search(query, k)`   | `app/pipeline/embeddings.py`        | Thin wrapper around `Embeddings.search`                  |  2   |
# | `app.agents.research_agent.run_research_sync(query)` | `app/agents/research_agent.py` | Sync route -> retrieve -> synthesize, returns one dict   |  3   |
# | `app.agents.research_agent.run_research(query)`      | `app/agents/research_agent.py` | Generator form, yields one event per pipeline stage      |  4   |
#
# ### HTTP endpoints (the same pipeline, exposed for UIs)
#
# Defined in `app/api/server.py` — not invoked from this notebook, but the
# request bodies match the function signatures above.
#
# | Verb / Path             | Body                  | Behavior                                                                |
# |-------------------------|-----------------------|-------------------------------------------------------------------------|
# | `GET  /`                | -                     | Health probe, returns the registered endpoint map                       |
# | `POST /research`        | `{"query": "..."}`    | Calls `run_research_sync`, returns a JSON dict with the full trace      |
# | `POST /research/stream` | `{"query": "..."}`    | SSE stream of `route` -> `retrieve` -> `synthesize` -> `done` events    |
#
# ### txtai primitives under the hood
#
# Every retrieval cell ultimately resolves to a `txtai.Embeddings` call:
#
# - `Embeddings.search(query, limit)` for plain semantic top-k
# - `Embeddings.search("... where tags = 'sec'", parameters=..., limit=...)`
#   for per-source scoping inside the SEC and News sub-agents
# - `Embeddings.save(path)` / `.load(path)` for the on-disk index in `data/`
# - Optional `txtai.LLM(model)` in the synthesizer when LLM credentials are set
#
# See `notebooks/txtai.API.ipynb` for each of those primitives in isolation.

# %%
# %load_ext autoreload
# %autoreload 2

# System libraries.
import logging
import os
import sys
from pathlib import Path

# Third party libraries.
from dotenv import load_dotenv

# %%
# Make the project root importable when running the notebook from notebooks/.
project_root = Path.cwd().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# %%
# Load secrets from .env and configure notebook logging.
load_dotenv(project_root / ".env")
_LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
_LOG.info("OPENAI_API_KEY present: %s", bool(os.getenv("OPENAI_API_KEY")))
_LOG.info("SEC_USER_AGENT present: %s", bool(os.getenv("SEC_USER_AGENT")))

# %% [markdown]
# ## 1. Ingest a small batch
#
# Pull a handful of recent SEC filings for AAPL into MinIO + PostgreSQL +
# the txtai index. Limit kept small so the cell finishes in a couple of
# minutes.

# %%
# Run the SEC collector for one ticker.
import importlib, app.collectors.sec_collector as sc                                                                                                                                                               
importlib.reload(sc) 
from app.collectors import SECCollector

sec = SECCollector()
sec_summary = sec.collect(
    ticker="AAPL",
    filing_types=["10-K", "8-K"],
    limit=2,
)
_LOG.info("SEC collection summary: %s", sec_summary)

# %% [markdown]
# ## 2. Confirm the index has content
#
# `get_embeddings()` returns the singleton index used by every agent.

# %%
# Spot-check the index by issuing one semantic query.
from app.pipeline.embeddings import get_embeddings, search

embeddings = get_embeddings()
_LOG.info("Index row count: %d", embeddings.count())
hits = search("Apple revenue trend", limit=3)
for h in hits:
    _LOG.info("score=%.3f text=%s", h["score"], (h.get("text") or "")[:120])

# %% [markdown]
# ## 3. Run the agentic pipeline synchronously
#
# `run_research_sync` is the same entry point the FastAPI `/research`
# handler calls. It returns a single dict with the full trace.

# %%
# Drive the full route -> retrieve -> synthesize pipeline.
from app.agents.research_agent import run_research_sync

result = run_research_sync("What are the key risks discussed in Apple's latest 10-K?")
_LOG.info("Route: %s", result.get("route"))
_LOG.info("Used LLM: %s", result.get("used_llm"))
_LOG.info("Chunk count: %d", result.get("chunk_count", 0))
print(result.get("answer", ""))

# %% [markdown]
# ## 4. Stream the same query
#
# `run_research` is the generator form. The FastAPI SSE endpoint and the
# Streamlit UI consume this so they can show each stage as it happens.

# %%
# Iterate over the streaming events and log each one as it arrives.
from app.agents.research_agent import run_research

for event in run_research("Any analyst upgrades for AAPL recently?"):
    step = event["step"]
    if step == "synthesize":
        _LOG.info("[%s] answer=%s", step, event["payload"].get("answer", "")[:160])
    elif step == "retrieve":
        chunks = event["payload"].get("chunks", [])
        _LOG.info("[%s] agent=%s chunks=%d", step, event["payload"].get("agent"), len(chunks))
    else:
        _LOG.info("[%s] payload keys=%s", step, list(event["payload"].keys()))

# %% [markdown]
# ## Summary
#
# - The full ingest -> index -> search -> agent pipeline runs end-to-end
#   from a notebook with no API server required
# - The same `run_research_sync` function powers the FastAPI handler and
#   the Streamlit UI; this notebook is the primary smoke test for the
#   research pipeline
# - To extend: add another collector (`app/collectors/my_collector.py`),
#   re-run the ingest cell, and the agent picks up the new chunks
#   automatically because they share the txtai index
