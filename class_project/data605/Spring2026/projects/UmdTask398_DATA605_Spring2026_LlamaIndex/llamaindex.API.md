<!-- toc -->

- [Introduction](#introduction)
- [What this notebook covers](#what-this-notebook-covers)
- [Architecture overview](#architecture-overview)
- [Setup and prerequisites](#setup-and-prerequisites)
- [Key ideas to look for in the code](#key-ideas-to-look-for-in-the-code)
- [How to run](#how-to-run)
- [Expected output](#expected-output)
- [Troubleshooting](#troubleshooting)

<!-- tocstop -->

## Introduction

`llamaindex.API.ipynb` is the **concept-first** notebook for this project. It
walks through LlamaIndex’s core Retrieval-Augmented Generation (RAG) pipeline
step-by-step and shows how the main primitives fit together.

This notebook uses **local-first components**:

- **LLM**: Ollama (default model: `llama3`) running on the host machine
- **Embeddings**: `BAAI/bge-small-en-v1.5` via HuggingFace (runs inside Docker)

## What this notebook covers

- **Documents → Nodes**: how raw text becomes chunked nodes (via a node parser)
- **Embeddings**: turning text (and queries) into vectors for semantic search
- **`VectorStoreIndex`**: building an in-memory index from documents
- **Retrieval vs synthesis**: inspecting retrieved context and then the final
  LLM-generated answer via a query engine

## Architecture overview

```mermaid
graph LR
    A[Raw Text] -->|Data Loaders| B(Documents)
    B -->|Node Parsers| C(Nodes)
    C -->|Embedding Model| D[(Vector Index)]
    D -->|Retriever| E(Query Engine)
    E -->|LLM Ollama| F[Answer]
```

## Setup and prerequisites

- **Ollama installed on the host** and running
- **Models pulled locally** (example):

```bash
ollama pull llama3
```

- **Run inside Docker** (recommended/required for reproducibility in this repo):

```bash
./docker_build.sh
./docker_jupyter.sh
```

Then open JupyterLab (typically `http://127.0.0.1:8888/lab`) and run
`llamaindex.API.ipynb`.

## Key ideas to look for in the code

- **Global configuration**: `configure_ollama()` sets `llama_index.core.Settings.llm`
  and `Settings.embed_model` so downstream components pick them up automatically.
- **Chunking controls retrieval**: `chunk_size` and `chunk_overlap` impact what the
  retriever can “see” and therefore the quality of answers.
- **Retriever vs QueryEngine**:
  - Retriever returns top-\(k\) nodes (raw context)
  - Query engine synthesizes a final answer using the LLM

## How to run

- **Start JupyterLab in Docker** and run top-to-bottom:
  - `llamaindex.API.ipynb`
- Optional: run the script version:

```bash
python llamaindex.API.py
```

## Expected output

- Prints confirming:
  - LLM + embedding model are configured
  - nodes were created from the sample document
  - a vector index was built
  - retrieved context vs final synthesized answer

## Troubleshooting

- **Ollama connection errors**:
  - Ensure Ollama is running on the host
  - The container connects via `http://host.docker.internal:11434` (see
    `llamaindex_utils.py`)
- **Slow first run**:
  - The HuggingFace embedding model may download the first time; later runs
    are faster.