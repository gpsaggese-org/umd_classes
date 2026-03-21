# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.0
#   kernelspec:
#     display_name: venv (3.12.2)
#     language: python
#     name: python3
# ---

# %%
import sys

print(sys.executable)

# %% [markdown]
# # LlamaIndex API Overview
#
# This notebook demonstrates the core API components of LlamaIndex and how they are composed to build a retrieval-augmented generation (RAG) pipeline.
#
# We focus on:
#
# - Model configuration
# - Document loading
# - Node parsing (chunking)
# - Index construction
# - Query engine configuration
# - Prompt customization
#
# This notebook uses open-source models and does not require API keys.

# %%
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core.prompts import PromptTemplate

import os

# %% [markdown]
# ## Model Configuration
#
# LlamaIndex separates responsibilities between:
#
# - **Embedding model**: Converts text into vector representations for similarity search.
# - **LLM (Language Model)**: Generates responses based on retrieved context.
# - **Settings**: Global configuration registry that wires components together.
#
# We configure both the embedding model and the LLM below.

# %%
embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

Settings.embed_model = embed_model

print("Embedding model loaded successfully.")

# %% [markdown]
# ## Language Model Configuration
#
# We use an open-source, instruction-tuned causal language model:
#
# **TinyLlama-1.1B-Chat**
#
# This model:
#
# - Is small enough to run locally
# - Supports instruction-style prompts
# - Works with `AutoModelForCausalLM`
# - Does not require API keys
#
# We register it globally using the `Settings` object.

# %%
llm = HuggingFaceLLM(
    model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    tokenizer_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    context_window=2048,
    max_new_tokens=128,
    generate_kwargs={"temperature": 0.0},
    device_map="auto",
)

Settings.llm = llm

print("LLM loaded successfully.")

# %% [markdown]
# ## Document Loading
#
# Documents are the primary input abstraction in LlamaIndex.
#
# `SimpleDirectoryReader`:
#
# - Reads files from a directory
# - Wraps them into `Document` objects
# - Prepares them for parsing and indexing
#
# For demonstration purposes, we create a small toy dataset.

# %%
# Create demo directory
os.makedirs("data/api_demo", exist_ok=True)

# Write a small sample file
with open("data/api_demo/sample.txt", "w") as f:
    f.write(
        "LlamaIndex is a framework for building LLM-powered applications. "
        "It supports document ingestion, indexing, and retrieval. "
        "Retrieval-augmented generation improves factual grounding."
    )

# Load documents
documents = SimpleDirectoryReader("data/api_demo").load_data()

print(f"Number of documents loaded: {len(documents)}")
documents

# %% [markdown]
# ## Node Parsing (Chunking)
#
# Before indexing, documents are split into smaller units called *nodes*.
#
# Chunking is important because:
#
# - Embeddings operate on smaller text segments
# - Retrieval happens at the node level
# - Chunk size affects retrieval quality and context precision
#
# We demonstrate custom chunk configuration below.

# %%
# Configure chunking behavior
parser = SentenceSplitter(
    chunk_size=100,
    chunk_overlap=20,
)

# Parse documents into nodes
nodes = parser.get_nodes_from_documents(documents)

print(f"Number of nodes created: {len(nodes)}")
print("\nFirst node text:\n")
print(nodes[0].text)

# %% [markdown]
# ## Index Construction
#
# `VectorStoreIndex`:
#
# - Computes embeddings for each node
# - Stores them in a vector index
# - Enables similarity-based retrieval
#
# The index operates at the node level.

# %%
index = VectorStoreIndex(nodes)

print("Index constructed successfully.")

# %% [markdown]
# ## Query Engine
#
# The Query Engine coordinates:
#
# 1. Query embedding
# 2. Similarity search over indexed nodes
# 3. Context injection into a prompt
# 4. Response generation via the LLM
#
# We configure retrieval parameters such as `similarity_top_k`.

# %%
query_engine = index.as_query_engine(similarity_top_k=1)

response = query_engine.query("What does LlamaIndex support?")

print(response)

# %% [markdown]
# ## Inspect Retrieved Source Nodes
#
# For transparency, LlamaIndex allows inspection of retrieved source nodes.
#
# This is useful for:
#
# - Debugging retrieval quality
# - Understanding context injection
# - Evaluating RAG behavior

# %%
for i, source_node in enumerate(response.source_nodes):
    print(f"--- Retrieved Node {i + 1} ---\n")
    print(source_node.node.text)
    print("\nScore:", source_node.score)
    print("\n")

# %% [markdown]
# ## Custom Prompt Template
#
# LlamaIndex allows customization of how retrieved context and queries
# are formatted before being sent to the LLM.
#
# This is useful for:
#
# - Adjusting instruction style
# - Improving response formatting
# - Controlling output structure

# %%
custom_prompt = PromptTemplate(
    "You are a technical assistant.\n\n"
    "Context:\n{context_str}\n\n"
    "Question: {query_str}\n"
    "Answer concisely:"
)

query_engine_custom = index.as_query_engine(
    similarity_top_k=1,
    text_qa_template=custom_prompt,
)

response_custom = query_engine_custom.query(
    "Explain retrieval-augmented generation."
)

print(response_custom)

# %% [markdown]
# ## Summary
#
# In this notebook, we demonstrated the core API components of LlamaIndex:
#
# - Model configuration via `Settings`
# - Document ingestion with `SimpleDirectoryReader`
# - Node parsing (chunking)
# - Vector index construction
# - Query engine orchestration
# - Retrieval transparency
# - Prompt customization
#
# This modular design allows flexible construction of retrieval-augmented generation systems.
#
# The next notebook demonstrates a complete end-to-end example using real-world data.

# %% [markdown]
#
