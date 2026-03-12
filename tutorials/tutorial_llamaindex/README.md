# LlamaIndex Tutorial

This tutorial demonstrates how to build a **Retrieval-Augmented Generation (RAG)** system using **LlamaIndex** and open-source models.

The goal is to understand how LlamaIndex structures the RAG pipeline, including:

- document ingestion
- chunking
- embedding generation
- vector indexing
- retrieval
- LLM-based answer generation

The tutorial is divided into two parts:

1. **API Tutorial** – demonstrates the core LlamaIndex abstractions using a small toy dataset.
2. **Example Tutorial** – builds a complete RAG system using real-world text data.

---

# Running the Tutorial with Docker

This tutorial can be executed inside Docker to ensure a **fully reproducible environment**.

## Step 1 — Navigate to the Tutorial Directory

Open a terminal and run:

```bash
cd tutorials/tutorial_llamaindex
```

---

## Step 2 — Build the Docker Image

Run:

```bash
docker build -t llamaindex-tutorial .
```

This command builds a Docker image containing:

- Python
- all project dependencies
- Jupyter Notebook

---

## Step 3 — Run the Docker Container

Start the container with:

```bash
docker run -p 8888:8888 llamaindex-tutorial
```

After running the command, the terminal will display a link similar to:

```
http://127.0.0.1:8888/?token=...
```

Open this link in your browser to access the Jupyter notebook environment.

---

## Step 4 — Run the Notebooks

Inside Jupyter, run the notebooks in the following order:

1. `llamaindex.API.ipynb`
2. `llamaindex.example.ipynb`

---

# Tutorial Structure

```
tutorial_llamaindex/
│
├── llamaindex.API.ipynb
├── llamaindex.example.ipynb
├── llamaindex.API.md
├── llamaindex.example.md
├── llamaindex_utils.py
├── Dockerfile
├── requirements.txt
└── data/
```

---

# API Tutorial

File:

```
llamaindex.API.ipynb
```

This notebook demonstrates the **core components of LlamaIndex** using a small toy dataset.

Topics covered:

- loading documents with `SimpleDirectoryReader`
- splitting documents into nodes
- generating embeddings
- building a `VectorStoreIndex`
- querying the index
- inspecting retrieved nodes
- customizing prompts

The objective of this notebook is to understand how **LlamaIndex APIs work independently**.

---

# Example Tutorial

File:

```
llamaindex.example.ipynb
```

This notebook demonstrates a **complete RAG pipeline** using real-world text data.

The notebook automatically downloads public domain books from **Project Gutenberg**, including:

- *Pride and Prejudice*
- *The Adventures of Sherlock Holmes*

The workflow includes:

1. downloading text data
2. loading documents
3. splitting documents into chunks
4. generating embeddings
5. building a vector index
6. retrieving relevant passages
7. generating answers using an LLM

This notebook shows how LlamaIndex can be used to build a **real-world RAG system**.

---

# Models Used

The tutorial uses open-source models so it can run locally without requiring API keys.

Embedding model:

```
sentence-transformers/all-MiniLM-L6-v2
```

Language model:

```
microsoft/phi-2
```

---

# Notes

Large datasets are **not stored in the repository**.

Instead, the notebooks automatically download the required texts when executed for the first time.  
This keeps the repository lightweight while ensuring reproducibility.

---

# Summary

This tutorial demonstrates how LlamaIndex simplifies the RAG architecture by providing abstractions for:

- document ingestion
- chunking
- vector indexing
- retrieval
- prompt orchestration

Compared to a naive implementation, LlamaIndex reduces boilerplate code and provides a modular framework for building LLM-powered applications.