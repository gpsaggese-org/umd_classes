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
# # txtai API Tour
#
# Standalone walkthrough of the txtai primitives we use in this project. Each
# cell exercises one concept in isolation so that someone new to txtai can
# read the cells top-to-bottom and understand what the building blocks do
# before seeing them composed in `txtai.example.ipynb`.
#
# ## txtai endpoints exercised in this notebook
#
# The notebook is organized around the small surface of the `txtai` library
# that the project depends on. Each section below maps to one cell.
#
# | # | Endpoint                                | What it does                                            | Cell |
# |---|-----------------------------------------|---------------------------------------------------------|------|
# | 1 | `txtai.embeddings.Embeddings(config)`   | Build a vector index plus content store                 |  1   |
# | 2 | `Embeddings.index(rows)`                | Bulk-load `(id, text, tags)` tuples into the index      |  2   |
# | 3 | `Embeddings.search(query, limit)`       | Pure semantic top-k                                     |  3   |
# | 4 | `Embeddings.search(sql, parameters, …)` | SQL-style filter (`WHERE tags = 'sec'`) over the index  |  4   |
# | 5 | `Embeddings.save(path)` / `.load(path)` | Persist and reload an index from disk                   |  5   |
# | 5 | `Embeddings.count()`                    | Number of rows currently in the index                   |  5   |
# | 6 | `txtai.LLM(model)`                      | Optional OpenAI-compatible LLM wrapper                  |  6   |
#
# These are the only `txtai` calls the project relies on — everything else
# (routing, agents, retrieval) is built on top of them in
# `app/pipeline/embeddings.py` and `app/agents/research_agent.py`.

# %%
# %load_ext autoreload
# %autoreload 2

# System libraries.
import logging

# Third party libraries.
import numpy as np

# %%
# Local utility for notebook logging setup.
_LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

# %% [markdown]
# ## 1. Embeddings index
#
# `txtai.Embeddings` is the workhorse: a vector index plus a content store.
# We pass `content=True` so the original text is stored alongside the
# vectors, which lets us return it from search results without a separate
# document store.

# %%
from txtai.embeddings import Embeddings

# Create a fresh in-memory index using a small sentence-transformer.
embeddings = Embeddings(
    {
        "path": "sentence-transformers/all-MiniLM-L6-v2",
        "content": True,
    }
)
_LOG.info("Created Embeddings instance with model=%s", embeddings.config["path"])

# %% [markdown]
# ## 2. Index a few documents
#
# `index()` accepts an iterable of `(id, text, tags)` tuples. The `tags`
# field is what enables SQL-style metadata filtering later.

# %%
# Build a tiny corpus: three SEC-flavored snippets and three news-flavored ones.
docs = [
    (1, "Risk factors include macro uncertainty and supply chain disruption.", "sec"),
    (2, "Management discussed gross margin trends in the Q4 10-K filing.", "sec"),
    (3, "The 8-K disclosed a material acquisition closing next quarter.", "sec"),
    (4, "Analysts upgraded the stock to buy citing strong services growth.", "news"),
    (5, "Press release announces a partnership with a major chip maker.", "news"),
    (6, "Bearish commentary appeared after the latest earnings call.", "news"),
]
embeddings.index(docs)
_LOG.info("Indexed %d documents", len(docs))

# %% [markdown]
# ## 3. Plain semantic search
#
# `search(query, limit)` returns the top-k by cosine similarity, with the
# stored text inlined.

# %%
# Run a generic semantic query.
hits = embeddings.search("regulatory filings and risk", limit=3)
for h in hits:
    _LOG.info("score=%.3f text=%s", h["score"], h["text"][:80])

# %% [markdown]
# ## 4. SQL-style metadata filter
#
# Because `content=True` and we passed tags, txtai exposes a SQL surface.
# We can WHERE-clause on the `tags` column to scope a search to a single
# source — this is exactly how `app/agents/research_agent.py` keeps SEC and
# News retrievals separated.

# %%
# Restrict the same query to the news partition only.
sec_only = embeddings.search(
    "select id, text, score from txtai where similar(:q) and tags = 'sec'",
    parameters={"q": "regulatory filings and risk"},
    limit=3,
)
for h in sec_only:
    _LOG.info("score=%.3f tag=sec text=%s", h["score"], h["text"][:80])

# %% [markdown]
# ## 5. Persist and reload
#
# The shared production index lives on disk so multiple processes (the
# collector, the API, the eval script) can hit it without rebuilding.

# %%
# Save and reload the index round-trip.
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "demo_index"
    embeddings.save(str(path))
    reloaded = Embeddings()
    reloaded.load(str(path))
    _LOG.info("Reloaded index has %d rows", reloaded.count())

# %% [markdown]
# ## 6. LLM wrapper (optional)
#
# `txtai.LLM` is a thin abstraction over OpenAI-compatible endpoints (or
# local Ollama). The synthesizer in `research_agent.py` uses it when
# `LLM_BASE_URL`/`LLM_API_KEY`/`LLM_MODEL` are set, and falls back to an
# extractive template when they are not.

# %%
# This cell is illustrative only — actual instantiation is gated on env vars.
import os

if os.getenv("LLM_API_KEY") and os.getenv("LLM_BASE_URL"):
    from txtai import LLM

    llm = LLM(model=os.getenv("LLM_MODEL", "gpt-4o-mini"))
    _LOG.info("LLM wrapper ready: %s", llm)
else:
    _LOG.info("LLM credentials not set; skipping. The pipeline still runs extractively.")

# %% [markdown]
# ## Summary
#
# - `Embeddings(content=True)` gives us vectors plus a SQL-queryable
#   content store backed by SQLite
# - Tagged documents enable per-source filtering with `WHERE tags = ...`
# - `save()` / `load()` round-trip an index so the API server reads the
#   same artifact the collectors wrote
# - `LLM` is optional; the system degrades to extractive answers without it
