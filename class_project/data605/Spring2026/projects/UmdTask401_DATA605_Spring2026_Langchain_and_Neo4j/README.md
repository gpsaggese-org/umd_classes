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
6. [Setup](#setup)
7. [Running the Project](#running-the-project)
8. [Notebooks](#notebooks)
9. [Key Design Decisions](#key-design-decisions)
10. [Results](#results)
11. [References](#references)

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

The Jupyter container and Neo4j container run separately via Docker. Ollama runs
natively on the host machine. Inside Docker, `host.docker.internal` is used to
reach the host's Ollama server.

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
- `llama3.2:1b` model pulled in Ollama
- MovieLens dataset downloaded and placed in `movielens/`

Pull the required Ollama model:
```bash
ollama pull llama3.2:1b
```

---

## Setup

### 1. Start Ollama

Ollama must be running on your host machine before starting Jupyter:

```bash
ollama serve
```

If you see `address already in use`, Ollama is already running — no action needed.

### 2. Start Neo4j

Run Neo4j in a Docker container:

```bash
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:5.26.24
```

If the container already exists from a previous run:

```bash
docker start neo4j
```

Verify Neo4j is running by visiting `http://localhost:7474` in your browser.

> **Linux users:** Docker on Linux does not support `host.docker.internal` by
> default. Add `--add-host=host.docker.internal:host-gateway` to the
> `docker run` command above and to `docker_jupyter.sh` so the Jupyter
> container can reach Neo4j on the host network.

### 3. Build the Jupyter Docker Image

From your project directory:

```bash
./docker_build.sh
```

### 4. Start Jupyter

```bash
./docker_jupyter.sh
```

Then open `http://localhost:8888` in your browser and navigate to `curr_dir/`.

---

## Running the Project

Run the notebooks in this order:

1. **`langchain_neo4j.API.ipynb`** — learn the individual APIs
2. **`langchain_neo4j.example.ipynb`** — run the full end-to-end project

> **Note:** The first time you run the example notebook, data ingestion
> (movies + ratings) will take a few minutes. Subsequent runs skip ingestion
> automatically since `MERGE` prevents duplicate nodes.

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

## Results

Sample natural language queries and results:

**Q: List movies in the Action genre.**
> Returns 10 Action movies including Kill Bill: Vol. 1 and Sucker Punch.

**Q: What genres does Toy Story belong to?**
> Adventure, Animation, Children, Comedy, Fantasy

**Q: How many movies are in the Drama genre?**
> 13,344 movies

**Q: What are the top rated movies?**
> Returns movies with highest average ratings from the sampled ratings data.

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