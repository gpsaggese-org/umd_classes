# LlamaIndex: Learn in 60 Minutes

Welcome to the **LlamaIndex Historical QA Tutorial**! This project is designed to teach you how to use LlamaIndex, a powerful framework for building applications that connect Large Language Models (LLMs) with private or domain-specific data.

In this tutorial, we build a Question-Answering (QA) system that extracts and synthesizes information from a **curated Wikipedia corpus of historical events**.

---

## Key Concepts

Before diving in, here are the four core LlamaIndex building blocks you will encounter:

| Concept | What It Is |
|---|---|
| `Document` | A wrapper around any raw text or data source (e.g., a Wikipedia article) |
| `Node` | A smaller chunk that LlamaIndex splits a Document into for efficient retrieval |
| `VectorStoreIndex` | Converts Nodes into numerical embeddings and stores them for semantic search |
| `QueryEngine` | Accepts a natural language question, retrieves relevant Nodes, and passes them to an LLM for an answer |

---

## Project Structure

| File | Purpose |
|---|---|
| `llamaindex.API.ipynb` | Beginner-friendly tutorial introducing the core LlamaIndex API concepts. **Start here!** |
| `llamaindex.API.md` | Markdown companion to `llamaindex.API.ipynb` (project-specific notes + run guide) |
| `llamaindex.example.ipynb` | End-to-end Historical Events QA system with Wikipedia data, querying, and evaluation |
| `llamaindex.example.md` | Markdown companion to `llamaindex.example.ipynb` (walkthrough + outputs + app notes) |
| `llamaindex.API.py` & `llamaindex.example.py` | Python script equivalents of the notebooks for headless execution |
| `llamaindex_utils.py` | Shared helper functions: environment setup and Ollama model configuration |
| `requirements.txt` | All Python dependencies with pinned versions for reproducibility |
| `docker_build.sh` | Script to build the Docker container image |
| `docker_jupyter.sh` | Script to launch Jupyter Lab inside the Docker container |
| `docker_streamlit.sh` | Script to launch the Streamlit chat app inside the Docker container |
| `app.py` | Streamlit chat UI that loads the persisted index and runs a ReAct agent |
| `storage/` | Persisted vector index (created by `llamaindex.example.ipynb` on first successful run; typically not committed) |

---

## Prerequisites

### 1. Install Ollama (Local LLM - Required)

This project uses **Ollama** to run the LLM fully locally, in compliance with the project guideline that prohibits cloud resources. The code inside Docker connects to Ollama running on your host machine via `host.docker.internal`.

1. Download and install [Ollama](https://ollama.com/) for your OS (Mac/Linux/Windows).
2. Open a terminal on your host machine and pull the model:
   ```bash
   ollama pull llama3
   ```
3. Keep Ollama running in the background while executing the notebooks.

### 2. Running with Docker (Required)

All code must be run inside the provided Docker container for reproducibility.

```bash
# Step 1: Build the container (only needed once, or after changing requirements.txt)
./docker_build.sh

# Step 2: Launch Jupyter Lab inside the container
./docker_jupyter.sh

# Step 3: Open your browser and go to:
# http://127.0.0.1:8888/lab
```

---

## Architectural Decisions

| Decision | Rationale |
|---|---|
| **Wikipedia API** | Chosen over a static CSV for dynamic, real-world unstructured data ingestion |
| **Ollama (llama3)** | Fully local LLM - zero cost, zero cloud dependency, complies with project guidelines |
| **BAAI/bge-small-en-v1.5 embeddings** | Fast, high-quality local embedding model that runs inside Docker |
| **`auto_suggest=False`** | Prevents Wikipedia API from auto-correcting page names to unintended topics |
| **ReAct Agent** | Elevates the QA pipeline into an autonomous assistant capable of multi-tool reasoning |

---

## Usage Guide

1. **Start with `llamaindex.API.ipynb`** (~15 min): Learn the building blocks. Create Documents, build a VectorStoreIndex, and run your first query.
2. **Move to `llamaindex.example.ipynb`** (~30 min): See the full pipeline. Fetch Wikipedia articles, index them, run historical queries, evaluate accuracy, and explore conversational follow-ups with visualizations.
3. **(Optional) Run the Streamlit app**: After `llamaindex.example.ipynb` creates `./storage`, you can launch an interactive chat UI:

   ```bash
   ./docker_streamlit.sh
   ```

   Then open `http://127.0.0.1:8501`.

### Notes on reproducibility and connectivity

- The project is **local-LLM** (Ollama) and does not require an OpenAI API key.
- **Wikipedia ingestion requires network access** on the first run (or if `./storage` is deleted).
- Once `./storage` exists, the index can be loaded from disk without re-embedding.

---

Enjoy learning LlamaIndex!