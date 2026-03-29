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

# %% [markdown]
# # Description
#
# ## Learn LangChain in 60 Minutes — examples notebook
#
# What you’ll build (incrementally):
# - a tool-calling agent loop
# - LangGraph workflows: state, routing, reducers, and a ReAct loop from scratch
# - subagents + subgraphs (composition)
# - memory boundaries via checkpointers
# - human-in-the-loop interrupts + resume
# - Deep Agents demos (todos/filesystem/subagents/HITL/sandboxing)

# %% [markdown]
# # Imports

# %%
# %load_ext autoreload
# %autoreload 2


import langchain
import langchain_core

import langchain_API_utils as ut

# Initialize logger.
_LOG = ut.init_logger("learn_langchain.api")

ut.print_environment_info()


# %%
# Customize langchain.env to configure model.
import dotenv

dotenv.load_dotenv("langchain.env")

# %%
llm = ut.get_chat_model()
llm


# %%
from pathlib import Path

import pandas as pd

DATASET_PATH = Path("data/T1_slice.csv").resolve()
df = pd.read_csv(DATASET_PATH)

# Parse the time column to datetime for proper time-series handling.
TIME_COL = "Date/Time"
if TIME_COL in df.columns:
    df[TIME_COL] = pd.to_datetime(
        df[TIME_COL], format="%d %m %Y %H:%M", errors="coerce"
    )

print(f"Loaded dataset from {DATASET_PATH}")
print(f"Shape: {df.shape}")
df.head(5)


# %%
import shutil

# Make the dataset visible to Deep Agents filesystem tools under `/workspace/...`.
WORKSPACE_DIR = Path("workspace").resolve()
WORKSPACE_DATA_DIR = WORKSPACE_DIR / "data"
WORKSPACE_DATA_DIR.mkdir(parents=True, exist_ok=True)

WORKSPACE_DATASET_PATH = WORKSPACE_DATA_DIR / "T1_slice.csv"
if not WORKSPACE_DATASET_PATH.exists():
    shutil.copyfile(str(DATASET_PATH), str(WORKSPACE_DATASET_PATH))

print(f"Dataset available to sandbox tools at {WORKSPACE_DATASET_PATH}")

# %%
DATASET_META = ut.build_dataset_meta(df)
DATASET_META


# %% [markdown]
# ## Quick EDA (local dataset)
#
# A tiny bit of exploratory data analysis helps you trust the data you’re feeding into prompts.
#
# We’ll do a quick look (head/describe/plot) so you can see:
# - what columns exist
# - what the time column looks like
# - what “a reasonable question” about this dataset might be
#

# %%
import matplotlib.pyplot as plt

print("shape:", df.shape)
print("columns:", list(df.columns))
print("\nmissingness (top):")
print((df.isna().mean() * 100).sort_values(ascending=False).head(10).round(2))

numeric_cols = [c for c in df.columns if c != "Date/Time"]
print("\nsummary stats (numeric):")
display(df[numeric_cols].describe().T)

if "Date/Time" in df.columns and pd.api.types.is_datetime64_any_dtype(
    df["Date/Time"]
):
    cols = [
        c for c in ["LV ActivePower (kW)", "Wind Speed (m/s)"] if c in df.columns
    ]
    if cols:
        ax = df.plot(
            x="Date/Time",
            y=cols,
            subplots=True,
            figsize=(10, 6),
            title=[f"{c} over time" for c in cols],
            legend=False,
        )
        plt.tight_layout()


# %% [markdown]
# ## Docs-RAG mini pipeline (new integration)
#
# This section ports the core pattern from `tutorial_langchain` into this notebook:
#
# 1) read markdown docs
# 2) split into chunks
# 3) embed + index
# 4) retrieve relevant chunks at question time
#
# Use this when you want answers grounded in project docs rather than pure model memory.
#

# %%
import langchain_utils as tut_utils

# Define the tutorial documentation files that will be indexed for RAG retrieval.
docs_paths = [
    Path("README.md"),
    Path("langchain.API.md"),
    Path("langchain.example.md"),
]

# Load and parse markdown documents from disk.
raw_docs = tut_utils.load_markdown_documents(docs_paths)

# Split documents into overlapping chunks for dense retrieval and context window limits.
chunked_docs = tut_utils.split_documents(
    raw_docs, chunk_size=900, chunk_overlap=120
)

print(f"Loaded {len(raw_docs)} documents")
print(f"Split into {len(chunked_docs)} chunks")


# %%
# Initialize embeddings model and build vector store for semantic search.
embeddings = tut_utils.make_embeddings()
docs_store = tut_utils.build_vector_store(chunked_docs, embeddings)

# Create a retriever that fetches the top 3 most relevant chunks for each query.
retriever = docs_store.as_retriever(search_kwargs={"k": 3})

print(f"Vector store built with {len(chunked_docs)} embedded chunks")
print("Retriever ready for semantic search")

# %%
import langchain_core.output_parsers
import langchain_core.prompts
import langchain_core.runnables

# Define the RAG system prompt that grounds answers in retrieved documentation.
rag_prompt = langchain_core.prompts.ChatPromptTemplate.from_template(
    """You are answering from retrieved tutorial docs.
Use only the provided context. If context is insufficient, say so.

Context:
{context}

Question:
{question}
"""
)

# Compose the RAG chain: retrieve docs → format context → prompt LLM → parse output.
rag_chain = (
    {
        "context": retriever | tut_utils.format_docs,
        "question": langchain_core.runnables.RunnablePassthrough(),
    }
    | rag_prompt
    | llm
    | langchain_core.output_parsers.StrOutputParser()
)

print("RAG chain built and ready to invoke")

# %%
# Invoke the RAG chain with a question about the tutorial content.
rag_question = "How do HITL interrupts and resume work in this tutorial?"
rag_answer = rag_chain.invoke(rag_question)

# Print answer and trace which docs were retrieved to support it.
print("Answer (first 900 chars):")
print(rag_answer[:900])
print("\n" + "=" * 60)

# Show which documentation files were used to answer the question.
sources = [d.metadata.get("source") for d in retriever.invoke(rag_question)]
print(f"\nSources used: {sources}")

# %%
# Take a checksum snapshot of the current docs for change detection in incremental refresh.
docs_snapshot = tut_utils.snapshot_checksums(docs_paths)
print(f"Snapshot created for {len(docs_paths)} documentation files")

# %% [markdown]
# ### Incremental docs refresh
#
# A lightweight “dynamic update” pattern:
# - detect new/modified markdown files via checksum snapshots
# - chunk only changed files
# - add those chunks back into the existing vector store
#

# %%
refresh_doc = Path("tmp_runs/docs_refresh_demo.md")
refresh_doc.parent.mkdir(parents=True, exist_ok=True)
refresh_doc.write_text(
    "# Docs refresh demo\n\nThis file was added during the notebook run to demonstrate incremental index updates.",
    encoding="utf-8",
)

updated_paths = docs_paths + [refresh_doc]
updated_snapshot = tut_utils.snapshot_checksums(updated_paths)
changes = tut_utils.diff_checksum_snapshots(docs_snapshot, updated_snapshot)
print("changes:", changes)

changed_paths = [Path(path) for path in (changes["new"] + changes["modified"])]
if changed_paths:
    changed_docs = tut_utils.load_markdown_documents(changed_paths)
    changed_chunks = tut_utils.split_documents(
        changed_docs, chunk_size=900, chunk_overlap=120
    )
    tut_utils.add_documents_to_store(docs_store, changed_chunks)

docs_snapshot = updated_snapshot
print(
    "refresh query sources:",
    [
        d.metadata.get("source")
        for d in retriever.invoke("What is docs refresh demo?")
    ],
)


# %% [markdown]
# ## Basic tools (math + time)
#
# Before we build agent loops, we’ll define a couple tiny tools.
#
# Why start small?
# - tools are just functions
# - the schema is the contract
# - the agent loop becomes much easier to understand when you already trust the tools
#

# %%
import datetime
import math

import langchain_core.tools


@langchain_core.tools.tool
def utc_now() -> str:
    """Return the current UTC time as an ISO string."""
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


@tool
def mean(xs: list[float]) -> float:
    """Return the arithmetic mean of a non-empty list of numbers."""
    if not xs:
        raise ValueError("xs must be non-empty")
    return sum(float(x) for x in xs) / len(xs)


@tool
def sqrt(x: float) -> float:
    """Return sqrt(x)."""
    x = float(x)
    if x < 0:
        raise ValueError("x must be >= 0")
    return math.sqrt(x)


# %% [markdown]
# ## Agent loop: `create_agent` + tool calling
#
# This is the “hello world” of agentic behavior:
#
# 1) you give the model a goal
# 2) you give it tools
# 3) the model decides when to call tools vs when to answer directly
#
# As you run the next cell, look for evidence of the loop in the message history:
# - an AI message that requests a tool call
# - a tool message that returns results
# - a final AI message that uses those results
#

# %%
import langchain_core.messages
import langchain.agents

agent = langchain.agents.create_agent(
    model=llm,
    tools=[utc_now, mean, sqrt],
    system_prompt=(
        "You are a careful assistant. Use tools when computation or time is required. "
        "When you call a tool, use its output in your final answer."
    ),
)

inputs = {
    "messages": [
        langchain_core.messages.HumanMessage(
            content="Compute mean([1,2,3,4,10]) and sqrt(49). Also tell me the current UTC time."
        )
    ]
}
final_state = agent.invoke(inputs)
[
    (type(m).__name__, getattr(m, "content", "")[:120])
    for m in final_state["messages"]
][-4:]
