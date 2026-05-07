# LangChain + Neo4j: Knowledge Graph Question Answering

## Overview

This project builds a **knowledge graph-based question-answering system** using
LangChain and Neo4j. It demonstrates how to load a real-world dataset into a
graph database, model relationships between entities, and enable natural language
querying using a local large language model (LLM).

---

## Table of Contents

1. [Background](#background)
2. [Architecture](#architecture)
3. [Dataset](#dataset)
4. [Graph Schema](#graph-schema)
5. [Prerequisites](#prerequisites)
6. [Quick Start](#quick-start)
7. [Setup](#setup)
8. [Running the Project](#running-the-project)
9. [Notebooks](#notebooks)
10. [Key Design Decisions](#key-design-decisions)
11. [Results](#results)
12. [References](#references)

---

## Background

### What is Neo4j?

Neo4j is a **graph database** that stores data as nodes and relationships rather
than rows and columns. This makes it ideal for data with complex, interconnected
relationships — such as movies, genres, and user ratings.

In a relational database, finding "all Action movies rated above 4 stars by users
who also liked Inception" would require multiple JOIN operations across several
tables. In Neo4j, this is a natural graph traversal expressed in **Cypher**, Neo4j's
declarative query language.

### What is LangChain?

LangChain is a framework for building applications powered by large language models
(LLMs). It provides abstractions for chaining together components like prompts,
models, and data sources. In this project we use LangChain's `GraphCypherQAChain`,
which:

1. Takes a natural language question as input
2. Uses an LLM to generate a Cypher query
3. Runs the query against Neo4j
4. Uses the LLM again to summarize the results in plain English

### What is Ollama?

Ollama is a tool for running open-source LLMs locally on your machine. This project
uses `llama3.2:1b` — a 1.3GB model that runs on CPU — so no cloud API or GPU is
required.

---

## Architecture

```
User Question
      │
      ▼
 PromptTemplate  ──►  ChatOllama (llama3.2:1b)
      │                       │
      │              Generated Cypher Query
      │                       │
      ▼                       ▼
 Neo4jGraph  ◄──────  GraphCypherQAChain
      │
      ▼
 Query Results
      │
      ▼
 ChatOllama (llama3.2:1b)
      │
      ▼
 Natural Language Answer
```

Three processes run in parallel: a **Neo4j container** (graph database),
a **Jupyter container** (notebooks + Python), and **Ollama** (LLM, runs
natively on the host). Both containers reach Ollama and each other via
`host.docker.internal`.

---

## Dataset

**MovieLens 20M Dataset** — GroupLens Research

- Source: [Kaggle](https://www.kaggle.com/datasets/grouplens/movielens-20m-dataset)
- 27,278 movies with titles and genres
- 20 million ratings from 138,000 users (we sample 100,000)
- Files used: `movie.csv`, `rating.csv`

Download the dataset and place the CSV files in the `movielens/` directory:

```
movielens/
├── movie.csv
└── rating.csv
```

---

## Graph Schema

The knowledge graph contains three node types and two relationship types:

```
(User)-[:RATED {rating: FLOAT}]->(Movie)-[:IN_GENRE]->(Genre)
```

| Element | Type | Properties |
|---|---|---|
| Movie | Node | movieId (INT), title (STRING) |
| Genre | Node | name (STRING) |
| User | Node | userId (INT) |
| RATED | Relationship | rating (FLOAT, 0.5–5.0) |
| IN_GENRE | Relationship | none |

**Example nodes:**
- `(:Movie {movieId: 1, title: "Toy Story (1995)"})`
- `(:Genre {name: "Animation"})`
- `(:User {userId: 42})`

**Example relationships:**
- `(User {userId: 42})-[:RATED {rating: 4.5}]->(Movie {title: "Toy Story (1995)"})`
- `(Movie {title: "Toy Story (1995)"})-[:IN_GENRE]->(Genre {name: "Comedy"})`

---

## Prerequisites

- [Docker](https://www.docker.com/) installed and running
- [Ollama](https://ollama.com/) installed on your host machine
- MovieLens CSV files placed in the `movielens/` directory (see [Dataset](#dataset))

One-time Ollama setup:
```bash
ollama pull llama3.2:1b
```

---

## Quick Start

```bash
ollama serve          # start the local LLM (skip if already running)
./docker_neo4j.sh     # start Neo4j
./docker_build.sh     # build the Jupyter image (first time only)
./docker_jupyter.sh   # launch Jupyter at http://localhost:8888
```

Then open `http://localhost:8888`, navigate to `curr_dir/`, and run the
notebooks in order.

---

## Setup

### 1. Start Ollama

```bash
ollama serve
```

If you see `address already in use`, Ollama is already running — no action needed.

### 2. Start Neo4j

```bash
./docker_neo4j.sh
```

This script creates the container on the first run and
simply restarts it on subsequent runs. Verify Neo4j is up by visiting
`http://localhost:7474` (~20 seconds after running).

> **Linux users:** Docker on Linux does not support `host.docker.internal`
> by default. Add `--add-host=host.docker.internal:host-gateway` to the
> `docker run` command inside `docker_neo4j.sh` and to `docker_jupyter.sh`
> so the two containers can reach the host network.

### 3. Build the Jupyter Docker Image

Only needed once (or after changing `requirements.txt` or `Dockerfile`):

```bash
./docker_build.sh
```

### 4. Launch Jupyter

```bash
./docker_jupyter.sh
```

Open `http://localhost:8888` and navigate to `curr_dir/`.

---

## Running the Project

Run the notebooks in this order:

1. **`langchain_neo4j.API.ipynb`** — reference guide for each API used
2. **`langchain_neo4j.example.ipynb`** — full end-to-end project walkthrough

> **Note:** The first time you run the example notebook, data ingestion
> (movies + ratings) will take a few minutes since it writes 27,000 movie
> nodes and 100,000 rating relationships. Subsequent runs skip ingestion
> automatically — `MERGE` prevents duplicate nodes.

---

## Notebooks

### `langchain_neo4j.API.ipynb`

A reference guide covering each API used in this project:

- **Neo4j Python Driver** — `GraphDatabase.driver()`, sessions, transactions
- **Cypher queries** — MATCH, MERGE, parameterized queries
- **Neo4jGraph** — LangChain's graph wrapper, schema configuration
- **ChatOllama** — initializing and invoking a local LLM
- **PromptTemplate** — building reusable prompt templates
- **GraphCypherQAChain** — combining LLM + graph for natural language QA

### `langchain_neo4j.example.ipynb`

The full project walkthrough:

1. Connect to Neo4j
2. Load MovieLens CSV files
3. Ingest movies and genres as graph nodes
4. Explore the graph with direct Cypher queries
5. Visualize genre distribution
6. Ingest user ratings
7. Query top-rated movies
8. Build the LangChain QA chain with few-shot prompt engineering
9. Ask natural language questions about movies

### `langchain_neo4j_utils.py`

Utility functions used by both notebooks:

| Function | Description |
|---|---|
| `get_driver()` | Connect to Neo4j and verify connectivity |
| `get_neo4j_graph()` | Create LangChain Neo4jGraph with schema |
| `load_movielens()` | Load movie and rating CSVs into DataFrames |
| `ingest_movies()` | Write Movie and Genre nodes to Neo4j |
| `ingest_ratings()` | Write User nodes and RATED relationships |
| `get_cypher_prompt()` | Build few-shot PromptTemplate for Cypher generation |
| `get_qa_chain()` | Assemble the full GraphCypherQAChain |

---

## Key Design Decisions

### Why a graph database instead of SQL?

Movie-genre-user relationships are naturally graph-shaped. In Neo4j, traversing
"find all users who rated Action movies above 4 stars" is a single pattern match.
In SQL this would require joining movies, ratings, and a genre mapping table.

### Why manual schema instead of `refresh_schema=True`?

LangChain's auto-generated schema was too verbose for the small `llama3.2:1b` model
and caused it to generate incorrect Cypher. A hand-crafted, minimal schema with
explicit relationship directions improved accuracy significantly.

### Why few-shot prompting?

The `llama3.2:1b` model (1.3GB) is too small to reliably generate correct Cypher
from schema descriptions alone. Adding concrete Q&A examples directly in the prompt
guides the model toward the correct pattern. This is a practical demonstration of
how **prompt engineering compensates for model size limitations**.

---

## Expected Results

Sample natural language queries and results:

**Q: List movies in the Action genre.**
> Returns 10 Action movies

**Q: What genres does Toy Story belong to?**
> Animation, Children, etc.

**Q: How many movies are in the Drama genre?**
> 13,344 movies

**Q: What are the top rated movies?**
> Returns movies with highest average ratings from the sampled ratings data.

## Actual Results due to small model
> Based on the provided list of movies, here are some Action movies:\n\n1. Dragon Ball: The Curse Of The Blood Rubies (Doragon bôru: Shenron no densetsu)\n2. Dragon Ball Z: Bio-Broly\n3. Bionicle: The Legend Reborn
> Toy Story belongs to the animation and children's film genres.
> I don't know the answer to this question as no information is provided about the ratings or preferences of specific individuals or groups.
>  I don't have enough information to provide an accurate answer. Can I help you with anything else?

---

## Package Versions

| Package | Version |
|---|---|
| neo4j | 6.1.0 |
| langchain-neo4j | 0.9.0 |
| langchain-ollama | 1.1.0 |
| langchain-core | 1.3.2 |
| pandas | 3.0.2 |
| matplotlib | 3.10.9 |
| Neo4j (Docker) | 5.26.24 |
| Ollama model | llama3.2:1b |

---

## References

- [LangChain Documentation](https://python.langchain.com/docs/)
- [Neo4j Documentation](https://neo4j.com/docs/)
- [Neo4j Python Driver](https://neo4j.com/docs/api/python-driver/current/)
- [Ollama](https://ollama.com/)
- [MovieLens Dataset](https://www.kaggle.com/datasets/grouplens/movielens-20m-dataset)
- [LangChain Neo4j Integration](https://python.langchain.com/docs/integrations/graphs/neo4j_cypher/)