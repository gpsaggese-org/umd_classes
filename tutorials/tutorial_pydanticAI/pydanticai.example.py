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
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from dotenv import find_dotenv, load_dotenv


# %%
# Import notebook-specific libraries.
import asyncio
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from IPython.display import Markdown, display
import nest_asyncio
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

import helpers.hio as hio


# %%
import logging

# Local utility.
import pydanticai_example_utils as utils

_LOG = logging.getLogger(__name__)
utils.init_logger(_LOG)

display("Notebook logging initialized.")
# Notebook and utility logging are now configured.


# %% [markdown]
# # Summary
#
# - This notebook shows how to build a grounded Atlas support assistant with retrieval, structured outputs, validation, guardrails, and personalization
#
# # PydanticAI Example Notebook: Atlas Support Assistant (E2E)
#
# - Goal: build a small support assistant for the synthetic product **Atlas**
# - Workflow:
#   - Generate a synthetic knowledge base
#   - Load and chunk the docs
#   - Build a local embedding index
#   - Add retrieval as a **PydanticAI** tool
#   - Use structured outputs with citations
#   - Add validators, guardrails, and personalization
#
# - Outcome: an end-to-end pattern you can reuse for real retrieval-augmented assistants
#

# %% [markdown]
# ## Setup
#
# - `PydanticAI` agents need:
#   - A model identifier, such as `openai:gpt-4o-mini`
#   - A provider API key, such as `OPENAI_API_KEY`
# - Create a ```.env``` file containing these variables to be called in the notebook
# - Everything else in this notebook is local and self-contained
#

# %%
# Enable nested event loops so async agent calls run inside the notebook.
nest_asyncio.apply()

display("Nested event loop support enabled.")
# Async notebook execution is now configured.


# %%
# Run notebook coroutines through the current event loop so the paired Python file compiles.
def _run_async(awaitable):
    return asyncio.get_event_loop().run_until_complete(awaitable)


display(_run_async)
# Notebook async calls can now run without top-level await statements.


# %%
# Load environment variables from a local dotenv file if one exists.
env_path = find_dotenv(usecwd=True)
load_dotenv(env_path, override=True)
_LOG.info("dotenv path: %s", env_path or "<not found>")
env_path or "<not found>"
# Environment variables are available to the model configuration cells.

# %% [markdown]
# ## Data and Scenario
#
# - This notebook uses a small product-docs corpus to stay self-contained
# - The corpus describes an imaginary product called **Atlas**
#

# %% [markdown]
# ### What this cell does
#
# - Creates a local folder `example_dataset/` and writes a small set of synthetic support documents
# - Uses one file per support knowledge-base article
# - Keeps the dataset small so retrieval behavior stays easy to inspect
#

# %%
# Create the local directory that stores the synthetic support documents.
DOCS_DIR = Path("example_dataset/")
hio.create_dir(str(DOCS_DIR), incremental=True)

display(DOCS_DIR)
# The example dataset directory is now available.


# %%
# Define the synthetic Atlas support documents used throughout the notebook.
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

display(sorted(DOCS))
# The notebook now has a compact synthetic document corpus.


# %%
# Materialize the synthetic documents on disk if they do not already exist.
for name, text in DOCS.items():
    path = DOCS_DIR / name
    if not path.exists():
        path.write_text(text.strip() + "\n", encoding="utf-8")

display(sorted(p.name for p in DOCS_DIR.glob("*.md")))
# The synthetic knowledge-base files are now stored on disk.


# %% [markdown]
# - We load Markdown files into a standard in-memory format:
#
#   - `doc_id`: stable identifier for citations
#   - `title`: human-readable name
#   - `text`: document content
#
# - A consistent document schema makes it easier to build retrieval tools and return structured citations
#

# %% [markdown]
# ## Chunking and Local Embeddings
#
# - We split each document into chunks and computes a deterministic vector for each chunk
# - This helps:
#   - Ensure it is fully local and reproducible
#   - Ensure it is good enough to demonstrate retrieval and grounding
#

# %%
# Define the chunk schema used for retrieval and citations.
@dataclass
class DocChunk:
    doc_id: str
    chunk_id: int
    text: str
    vector: list[float]


display(DocChunk)
# The notebook now has a typed schema for retrieved chunks.


# %%
# Load the markdown documents and convert them into embedded chunks.
docs = utils.load_docs(DOCS_DIR)
chunks = utils.chunk_docs(docs, DocChunk, max_chars=700)

display(
    {
        "num_docs": len(docs),
        "num_chunks": len(chunks),
        "first_chunk": (chunks[0].doc_id, chunks[0].chunk_id),
    }
)
# The raw documents are now available as retrieval-ready chunks.


# %% [markdown]
# ## Build a lightweight search index / Retrieval
#
# - We then searche the chunk index for the most relevant pieces of text for a query
#

# %%
# Define the schema for previewing ranked retrieval matches.
class DocMatch(BaseModel):
    doc_id: str
    chunk_id: int
    score: float
    text: str


display(DocMatch.model_json_schema())
# Retrieval results will now have a structured schema.


# %%
# Search the chunk index with a realistic support question.
preview = utils.search_chunks(
    chunks,
    "How do I download invoices?",
    DocMatch,
    top_k=3,
)

display(pd.DataFrame([match.model_dump() for match in preview]))
# The preview shows which document chunks rank highest for the query.


# %% [markdown]
# ## Dependencies and Output Schema
#
# - Dependencies are runtime context passed into the agent at execution time
# - The output schema keeps answers and citations in a predictable format
#

# %%
# Define the dependency and output schemas used by the agent.
@dataclass
class DocDeps:
    chunks: list[DocChunk]
    user: Optional["UserProfile"] = None  # Optional personalization.


class SourceRef(BaseModel):
    doc_id: str
    chunk_id: int
    quote: str


class AnswerWithSources(BaseModel):
    answer: str
    sources: list[SourceRef] = Field(default_factory=list)
    follow_up_questions: list[str] = Field(
        default_factory=list
    )  # Optional prompts for follow-up guidance.


@dataclass
class UserProfile:
    plan: str
    region: str


display(AnswerWithSources.model_json_schema())
# The agent interface is now defined with structured dependencies and output.


# %% [markdown]
# ## Retrieval Tool
#
# - We then wrap the retrieval into a tool so the agent can call it during reasoning
# - Tools connect the model to real functionality
#

# %%
# Bind the retrieval helper into a tool the agent can invoke.
def search_docs_tool(
    ctx: RunContext[DocDeps], query: str, top_k: int = 3
):
    return utils.search_docs(
        ctx,
        query,
        top_k=top_k,
        doc_match_cls=DocMatch,
    )

display(search_docs_tool)
# The retrieval function is now packaged as a callable tool.


# %% [markdown]
# ## Agent Configuration and Validation
#
# - This agent combines retrieval tools, structured outputs, and a validator that enforces citation rules
#

# %%
# Configure the Atlas support agent with retrieval and structured output.
agent = Agent(
    MODEL_ID,
    deps_type=DocDeps,
    tools=[search_docs_tool],
    output_type=AnswerWithSources,
    instructions=(
        "You are Atlas Support. "
        "Use the `search_docs` tool to find relevant text. "
        "Answer briefly. If you use document info, include 1-3 sources with "
        "doc_id, chunk_id, and short quotes."
    ),
)
agent.output_validator(utils.enforce_sources)

display(agent)
# The support agent is now ready to answer grounded questions.


# %% [markdown]
# - The validator runs after the model produces a schema-valid `AnswerWithSources` object
#
# - The schema checks structure
# - The validator checks reliability rules such as source coverage
#

# %% [markdown]
# ## End-to-End Query
#
# - Here we run the agent asynchronously
# - Key pattern:
#   - Retrieval grounding
#   - Structured outputs
#   - Reliability checks
#

# %%
# Ask an end-to-end support question using the retrieval-augmented agent.
deps = DocDeps(chunks=chunks)
out = _run_async(utils.ask("How do I download invoices?", deps, agent))

display(out)
# The agent returned a structured answer object.


# %%
# Render the answer and citations in a notebook-friendly format.
source_lines = [
    f"- `{source.doc_id}` chunk {source.chunk_id}: "
    f"{source.quote[:120].replace(chr(10), ' ')}"
    for source in out.sources
]
follow_up_lines = [f"- {question}" for question in out.follow_up_questions]
answer_sections = [
    "### Answer",
    out.answer,
    "",
    "### Sources",
    *source_lines,
]
if follow_up_lines:
    answer_sections.extend(["", "### Follow-up questions", *follow_up_lines])

display(Markdown("\n".join(answer_sections)))
# The notebook now displays the answer alongside its citations.


# %% [markdown]
# ## Consuming Structured Output
#
# - Structured results help downstream systems store citations and audit answers without parsing raw text
#

# %%
# Build an intentionally invalid answer object for validator inspection.
invalid_answer = AnswerWithSources(
    answer="According to the policy...",
    sources=[],
)

display(invalid_answer)
# This object is missing sources even though the answer claims to reference policy text.


# %%
# Run the validator to show how it rejects unsupported document-backed claims.
utils.enforce_sources(invalid_answer)


# %% [markdown]
# ### What happened
#
# - The validator raises `ModelRetry` when an answer cites documentation without including sources
#

# %% [markdown]
# ## Streaming Output
#
# - Streaming returns tokens progressively
# - Progressive output improves perceived latency in chat interfaces
#

# %%
# Create a small streaming agent for a short demonstration.
stream_agent = Agent(
    MODEL_ID,
    instructions="Write one short paragraph about unit tests.",
)

display(stream_agent)
# The streaming demonstration agent is now configured.


# %%
# Stream a short response into the notebook output area.
_run_async(utils.stream_demo(stream_agent))


# %% [markdown]
# ## Conversation memory (multi-turn)
#
# - Reuse message history to keep context across turns
#

# %%
# Ask an initial question and validate the grounded response.
deps = DocDeps(chunks=chunks)
first = _run_async(agent.run("Where do I enable 2FA?", deps=deps))
utils.enforce_sources(first.output)

display(first.output)
# The first turn establishes grounded context for the next question.


# %%
# Reuse the first turn's message history in a follow-up question.
follow_up = _run_async(
    agent.run(
        "Does that work on the Starter plan?",
        deps=deps,
        message_history=first.new_messages(),
    )
)
utils.enforce_sources(follow_up.output)

display(follow_up.output)
# The follow-up answer reuses prior context through message history.


# %% [markdown]
# ## Guardrails (lightweight)
#
# - Reject out-of-scope questions without calling the model
#

# %%
# Run a guardrail check against an out-of-scope prompt.
guarded = _run_async(
    utils.run_guarded(
        "Write me a poem about the ocean.",
        DocDeps(chunks=chunks),
        agent,
        AnswerWithSources,
    )
)

display(guarded)
# The guardrail returns a bounded response without invoking the main workflow.


# %% [markdown]
# ## Dynamic updates
#
# - Add new docs, rebuild the index, and query again
#

# %%
# Add a new support document to the local knowledge base.
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

display(new_doc)
# The knowledge base now includes an integrations document.


# %%
# Reload the documents and rebuild the retrieval chunks.
docs = utils.load_docs(DOCS_DIR)
chunks = utils.chunk_docs(docs, DocChunk, max_chars=700)

display({"num_docs": len(docs), "num_chunks": len(chunks)})
# The retrieval index now includes the newly added document.


# %%
# Query the updated knowledge base about integrations support.
deps = DocDeps(chunks=chunks)
res = _run_async(agent.run("Do you support S3?", deps=deps))
out = res.output

display(out)
# The updated index returns a grounded answer about S3 support.


# %% [markdown]
# ## Personalization via Dependencies
#
# - Here we pass a `UserProfile` through dependencies so the agent can tailor answers
# - Dependencies are a clean way to inject user context, tenant context, and configuration into tools
#

# %%
# Create personalized dependencies for a Starter-plan user.
personalized_deps = DocDeps(
    chunks=chunks,
    user=UserProfile(plan="Starter", region="US"),
)

display(
    {
        "user": personalized_deps.user,
        "num_chunks": len(personalized_deps.chunks),
        "sample_chunk": (
            personalized_deps.chunks[0].doc_id,
            personalized_deps.chunks[0].chunk_id,
        ),
    }
)
# The personalized dependency summary is easier to inspect than the full chunk payload.


# %%
# Ask a question that depends on the supplied user profile.
personalized = _run_async(
    utils.ask(
        "What are my rate limits and storage limits?",
        personalized_deps,
        agent,
    )
)

display(personalized)
# The final answer can now reflect user-specific context.

