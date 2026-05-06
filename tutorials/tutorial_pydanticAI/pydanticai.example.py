# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
# %load_ext autoreload
# %autoreload 2

import logging


import helpers.hnotebook as ut

ut.config_notebook()

# Initialize logger.
logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)

# %%
import pydanticai_example_utils as utils

# %% [markdown]
# # PydanticAI Example Notebook: Atlas Support Assistant (E2E)
#
# This notebook builds a small "support assistant" for a synthetic product called **Atlas**.
#
# We will:
# 1. Generate a synthetic knowledge base (Markdown docs)
# 2. Load + chunk the docs
# 3. Build a simple local embedding index (no external embedding service required)
# 4. Add retrieval as a **PydanticAI tool**
# 5. Use **structured outputs** (Pydantic schema) with **citations**
# 6. Add **validators** to enforce rules like "citations required"
# 7. Add optional **guardrails** and **personalization**
#
# The result is an end-to-end pattern you can reuse for real RAG assistants.

# %% [markdown]
# ## Setup
#
# This cell initializes the environment and imports all required libraries.
#
# PydanticAI agents need:
# - a model identifier (for example `openai:gpt-4o-mini`)
# - a provider API key (for example `OPENAI_API_KEY`)
#
# Everything else in this notebook is local and self-contained.
#

# %%
# !pip install -q pydantic-ai

# %%
import os
import functools
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

import nest_asyncio

nest_asyncio.apply()

from pydantic import BaseModel, Field
from pydantic_ai import Agent

MODEL_ID = os.getenv("PYDANTIC_AI_MODEL", "openai:gpt-4o-mini")
print("MODEL_ID:", MODEL_ID)
print("OPENAI_API_KEY set:", bool(os.getenv("OPENAI_API_KEY")))


# %% [markdown]
# ## Data and Scenario
#
# We build a tiny product docs corpus to keep the tutorial self-contained.
#
# We will build a tiny documentation set for an imaginary product called **Atlas**.
#

# %% [markdown]
# ### What this cell does
#
# - Creates a local folder `example_dataset/` and writes a small set of **synthetic product/support documents** as Markdown files.
# - Each file represents a support knowledge-base article (billing, troubleshooting, security, limits, etc.).
# - The dataset is intentionally small but diverse so retrieval can return the *right* document depending on the question.
#
# ### Importance
#
# PydanticAI becomes most useful when the agent is grounded in external context (RAG-style).
# These documents act as that context. In the next steps, we will:
#
# 1. Load these Markdown files into memory
# 2. Retrieve relevant chunks for a user query
# 3. Use a PydanticAI agent + tools to answer using retrieved text
# 4. Return a structured output with citations

# %%
DOCS_DIR = Path("example_dataset/")
DOCS_DIR.mkdir(parents=True, exist_ok=True)

DOCS = {
    "overview.md": """
# Atlas Overview

Atlas is a data sync service for small teams. It connects to CSV files and cloud buckets and keeps datasets up to date.

Getting started
- Create a workspace.
- Add a data source.
- Run the first sync.

Limits
- File uploads up to 50 MB.
- Up to 5 data sources on the Starter plan.
""",
    "billing.md": """
# Billing and Plans

Plans
- Starter: $20 per month, 5 data sources, email support.
- Team: $80 per month, 25 data sources, priority email support.
- Enterprise: custom pricing, SSO, dedicated success manager.

Invoices
- Invoices are issued on the first of each month.
- You can download invoices from Settings > Billing.
""",
    "troubleshooting.md": """
# Troubleshooting

Common issues
- Sync stuck at 0%: check your source credentials and try again.
- CSV upload fails: ensure the file is under 50 MB and encoded in UTF-8.
- Duplicate rows: enable the "deduplicate" toggle on the source.
""",
    "security.md": """
# Security

Authentication
- Atlas supports two-factor authentication (2FA) for Team and Enterprise plans.
- Enable it under Settings > Security.

Data retention
- Deleted sources are retained for 30 days.
""",
    "limits.md": """
# Usage Limits

Rate limits
- API requests are limited to 120 per minute on Team.
- Starter is limited to 30 per minute.

Storage
- Starter: 10 GB total storage.
- Team: 200 GB total storage.
""",
    "support.md": """
# Support

Support channels
- Starter: email support, replies within 2 business days.
- Team: priority email support, replies within 4 business hours.
- Enterprise: dedicated success manager and 24/7 support.

Escalations
- Use the support portal to open a ticket.
""",
}

for name, text in DOCS.items():
    path = DOCS_DIR / name
    if not path.exists():
        path.write_text(text.strip() + "\n")

print("Docs directory:", DOCS_DIR)
print("Files:", [p.name for p in DOCS_DIR.glob("*.md")])


# %% [markdown]
# We load all Markdown files into a standard in-memory format:
#
# - `doc_id`: stable identifier for citations
# - `title`: human-readable name
# - `text`: document content
#
# A consistent document schema makes it easy to:
# - pass documents into dependencies (`deps`)
# - build retrieval tools
# - return structured citations in the agent output

# %% [markdown]
# ## Chunking and Local Embeddings
#
# We split each document into chunks and compute a deterministic vector for each chunk.
#
# ### Why this approach
# - It is fully local and reproducible (no external embedding API required)
# - It is good enough to demonstrate retrieval and grounding
#
# ### Importance
# PydanticAI agents become far more reliable when they can retrieve relevant context via tools instead of guessing.

# %%
@dataclass
class DocChunk:
    doc_id: str
    chunk_id: int
    text: str
    vector: list[float]


docs = utils.load_docs(DOCS_DIR)
chunks = utils.chunk_docs(docs, DocChunk, max_chars=700)
print("Chunks:", len(chunks))
print("Example:", chunks[0].doc_id, chunks[0].chunk_id)


# %% [markdown]
# ## Build a lightweight search index / Retrieval
#
# We search the chunk index for the most relevant pieces of text for a query.
#


# %%
class DocMatch(BaseModel):
    doc_id: str
    chunk_id: int
    score: float
    text: str


preview = utils.search_chunks(
    chunks, "How do I download invoices?", DocMatch, top_k=3
)
print("Preview matches:")
for m in preview:
    print(m.doc_id, "chunk", m.chunk_id, "score=", round(m.score, 4))


# %% [markdown]
# ### Importance
#
# - We represent each document chunk as a vector and compute similarity with a query vector using dot product.
# - `search_chunks(...)` ranks chunks by similarity and returns the top matches.
#

# %% [markdown]
# ## Dependencies and Output Schema
#
# ### Dependencies (`DocDeps`)
# Dependencies are runtime context passed into the agent at execution time. Here we store:
# - the chunk index
# - an optional user profile (for personalization)
#
# ### Output schema (`AnswerWithSources`)
# The agent output is forced into a structured format:
# - `answer`: the response text
# - `sources`: citations with `doc_id`, `chunk_id`, and a short quote
# - `follow_up_questions`: optional list to support guardrails
#
#
# Structured outputs eliminate brittle parsing and make results usable in real applications.

# %%
@dataclass
class DocDeps:
    chunks: list[DocChunk]
    user: Optional["UserProfile"] = None  # optional personalization


class SourceRef(BaseModel):
    doc_id: str
    chunk_id: int
    quote: str


class AnswerWithSources(BaseModel):
    answer: str
    sources: list[SourceRef] = Field(default_factory=list)
    follow_up_questions: list[str] = Field(
        default_factory=list
    )  # enables guardrails section later


@dataclass
class UserProfile:
    plan: str
    region: str


# %% [markdown]
# ## Retrieval Tool
#
# We wrap retrieval into a tool so the agent can call it during reasoning.
# Tools are the bridge between an LLM and real functionality. Here the tool provides grounded context for RAG-style answers.

# %%
search_docs_tool = functools.partial(
    utils.search_docs,
    doc_match_cls=DocMatch,
)


# %% [markdown]
# ## Agent Configuration and Validation
#
# This agent has:
# - tools: retrieval
# - deps: chunk store and optional user profile
# - structured output: answer plus citations
# - validator: enforces citation rules and triggers retry
#
# The schema ensures output structure, and the validator ensures output quality. Together they turn a chatty model into a reliable system component.

# %%
agent = Agent(
    MODEL_ID,
    deps_type=DocDeps,
    tools=[search_docs_tool],
    output_type=AnswerWithSources,
    instructions=(
        "You are Atlas Support. "
        "Use the `search_docs` tool to find relevant text. "
        "Answer briefly. If you use document info, include 1-3 sources with doc_id, chunk_id, and short quotes."
    ),
)
agent.output_validator(utils.enforce_sources)


# %% [markdown]
# ## End-to-End Query
#
# We run the agent asynchronously using `await` (notebook-safe).
#
# ### What happened
# - The agent can call `search_docs` to retrieve relevant text
# - The model generates a structured response
# - The validator ensures citations exist if docs were referenced
#
# This is the full pattern: RAG grounding plus structured outputs plus reliability checks.

# %%
deps = DocDeps(chunks=chunks)
out = await utils.ask("How do I download invoices?", deps, agent)
out

# %%
print("Answer:\n", out.answer)
print("\nSources:")
for s in out.sources:
    print(
        f"- {s.doc_id} (chunk {s.chunk_id}): {s.quote[:120].replace('\\n', ' ')}"
    )
if out.follow_up_questions:
    print("\nFollow-ups:")
    for q in out.follow_up_questions:
        print("-", q)

# %% [markdown]
# ## Consuming Structured Output
#
# We print the answer and citations from the structured result object. Downstream systems can store citations, audit answers, and render sources cleanly without parsing raw text.

# %%
try:
    utils.enforce_sources(
        AnswerWithSources(answer="According to the policy...", sources=[])
    )
except Exception as e:
    print("Validator failure example:", e)

# %% [markdown]
# ### What happened (and why PydanticAI helps)
#
# This shows the validator catching an invalid output.
# In a real run, `ModelRetry` tells PydanticAI to retry until the output meets the citation rules.

# %% [markdown]
# ## Streaming Output
#
# Streaming returns tokens progressively, which improves perceived latency in chat interfaces.
#
# Streaming is useful for UI experiences and interactive assistants, especially when responses are longer.

# %%
stream_agent = Agent(
    MODEL_ID, instructions="Write one short paragraph about unit tests."
)
await utils.stream_demo(stream_agent)

# %% [markdown]
# ## Conversation memory (multi-turn)
#
# Reuse message history to keep context across turns.
#

# %%
deps = DocDeps(chunks=chunks)
first = await agent.run("Where do I enable 2FA?", deps=deps)
utils.enforce_sources(first.output)
follow_up = await agent.run(
    "Does that work on the Starter plan?",
    deps=deps,
    message_history=first.new_messages(),
)
utils.enforce_sources(follow_up.output)
print(follow_up.output)


# %% [markdown]
# ## Guardrails (lightweight)
#
# Reject out-of-scope questions without calling the model.
#

# %%
guarded = await utils.run_guarded(
    "Write me a poem about the ocean.",
    DocDeps(chunks=chunks),
    agent,
    AnswerWithSources,
)
print(guarded)


# %% [markdown]
# ## Dynamic updates
#
# Add new docs, rebuild the index, and query again.
#

# %%
from pathlib import Path


# %%
from pathlib import Path

# 1) Add the new doc
new_doc = DOCS_DIR / "integrations.md"
new_doc.write_text(
    """
# Integrations

Atlas supports S3 and Google Cloud Storage as data sources.
SFTP sources are available on Enterprise plans.
""".strip()
    + "\n",
    encoding="utf-8",
)

# 2) Reload docs in the expected dict format
docs = utils.load_docs(DOCS_DIR)  # must return list[dict] with doc_id/title/text
chunks = utils.chunk_docs(docs, DocChunk, max_chars=700)

# 3) Run the agent (notebook-safe)
deps = DocDeps(chunks=chunks)

res = await agent.run("Do you support S3?", deps=deps)
out = res.output

print("Answer:\n", out.answer)
print("\nSources:")
for s in out.sources:
    print(
        f"- {s.doc_id} (chunk {s.chunk_id}): {s.quote[:120].replace('\\n', ' ')}"
    )

# %% [markdown]
# ## Personalization via Dependencies
#
# We pass a `UserProfile` through dependencies so the agent can tailor answers. Dependencies are the clean way to inject user context, tenant context, and configuration into tools and agent behavior without global state or prompt hacks.

# %%
personalized_deps = DocDeps(
    chunks=chunks,
    user=UserProfile(plan="Starter", region="US"),
)

personalized = await utils.ask(
    "What are my rate limits and storage limits?",
    personalized_deps,
    agent,
)

personalized

# %% [markdown]
# # Summary
#
# You built a grounded support assistant using:
# - a synthetic knowledge base
# - deterministic local embeddings for retrieval
# - PydanticAI tools to fetch context
# - structured outputs with citations
# - validators to enforce reliability
# - optional guardrails and personalization
#
# This is the core E2E pattern for building production-grade assistants with PydanticAI.
