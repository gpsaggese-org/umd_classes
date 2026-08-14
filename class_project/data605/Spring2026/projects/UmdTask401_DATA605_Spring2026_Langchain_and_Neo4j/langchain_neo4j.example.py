# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # LangChain + Neo4j
#
# ## Overview
# This notebook demonstrates how to build a knowledge graph-based 
# question + answering system using LangChain and Neo4j. We will:
#
# 1. Load the MovieLens dataset into a Neo4j graph database
# 2. Design a graph schema with Movie, Genre, and User nodes
# 3. Use LangChain to query the graph using natural language
# 4. Ask questions about movies and get answers powered by a local LLM (Ollama)
#
# ## Dataset
# - **Source**: MovieLens 20M Dataset (GroupLens)
# - **Contains**: 27,000 movies, 20 million ratings
# - **We use**: All movies + 100,000 ratings sample

# %% [markdown]
# ## Imports
# Import the necessary libraries for this project:
# - `pandas` for loading and processing the MovieLens CSV files
# - `neo4j` for connecting directly to the graph database
# - `langchain_community` for the GraphCypherQAChain and Neo4jGraph wrappers
# - `langchain_ollama` for running a local LLM via Ollama

# %%
import pandas as pd
from neo4j import GraphDatabase
from langchain_ollama import ChatOllama
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain

# %% [markdown]
# ## 1. Connect to Neo4j
# Connect to a local Neo4j instance running in a separate Docker container.
# Note: use the container's IP address instead of `localhost` because the 
# Jupyter environment runs inside Docker and cannot reach the host machine's 
# `localhost` directly.

# %%
import langchain_neo4j_utils as lnu

# Connect to Neo4j using the utility function.
NEO4J_URI = "bolt://host.docker.internal:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "password"

driver = lnu.get_driver(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)

# %% [markdown]
# ## 2. Load MovieLens Dataset
# Load the MovieLens dataset from CSV files. The dataset contains 27,000 
# movies and 20 million ratings. Sample 100,000 ratings to keep ingestion 
# manageable.

# %%
# Load MovieLens CSV files using the utility function.
movies_df, ratings_df = lnu.load_movielens(
    movies_path="movielens/movie.csv",
    ratings_path="movielens/rating.csv",
    ratings_sample=100000
)
movies_df.head()

# %% [markdown]
# ## 3. Ingest Movies and Genres into Neo4j
# Load all 27,278 movies and their genre relationships into the graph.
# Each movie is split on the `|`-delimited genres string and connected
# via `IN_GENRE` relationships. `MERGE` prevents duplicates on repeated runs.

# %%
# Ingest movies into Neo4j using the utility function.
with driver.session() as session:
    movies = movies_df.to_dict("records")
    session.execute_write(lnu.ingest_movies, movies)
    print("Movies ingested!")

# %% [markdown]
# ## 4. Explore the Graph with Direct Cypher
# Before using LangChain, verify the graph structure by running raw Cypher
# queries. This confirms the schema is correct and gives intuition about
# what the LLM will later need to replicate automatically.

# %%
# Verify graph load: count nodes and inspect sample relationships.
with driver.session() as session:
    # Count total movies and genres.
    total_movies = session.run("MATCH (m:Movie) RETURN count(m) AS total").single()["total"]
    total_genres = session.run("MATCH (g:Genre) RETURN count(g) AS total").single()["total"]
    print(f"Total movies: {total_movies}")
    print(f"Total genres: {total_genres}")

    # Sample five Action movies.
    print("\nSample Action movies:")
    result = session.run('''
        MATCH (m:Movie)-[:IN_GENRE]->(g:Genre {name: "Action"})
        RETURN m.title LIMIT 5
    ''')
    for r in result:
        print(f"  {r['m.title']}")

    # Confirm genres for a specific movie.
    print("\nGenres for Toy Story (1995):")
    result = session.run('''
        MATCH (m:Movie {title: "Toy Story (1995)"})-[:IN_GENRE]->(g:Genre)
        RETURN g.name
    ''')
    for r in result:
        print(f"  {r['g.name']}")

# %% [markdown]
# ## 5. Genre Distribution
# Visualize the distribution of movies across genres to understand our dataset.
# Drama and Comedy dominate the MovieLens dataset.

# %%
import matplotlib.pyplot as plt

with driver.session() as session:
    result = session.run("""
        MATCH (m:Movie)-[:IN_GENRE]->(g:Genre)
        RETURN g.name AS genre, count(m) AS total
        ORDER BY total DESC
        LIMIT 10
    """)
    data = [(r["genre"], r["total"]) for r in result]

genres = [d[0] for d in data]
counts = [d[1] for d in data]

plt.figure(figsize=(12, 6))
plt.bar(genres, counts, color="steelblue")
plt.title("Top 10 Genres in MovieLens Dataset")
plt.xlabel("Genre")
plt.ylabel("Number of Movies")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 6. Ingest User Ratings
# Enrich the graph by adding `User` nodes and `RATED` relationships.
# Each rating connects a `User` to a `Movie` with a `rating` property (0.5–5.0).
# The utility function uses `MERGE` to prevent duplicates; ingestion is
# skipped automatically if ratings are already present.

# %%
# Ingest ratings into Neo4j using the utility function.
with driver.session() as session:
    total = session.run("MATCH ()-[:RATED]->() RETURN count(*) AS total").single()["total"]
    if total == 0:
        print("Ingesting ratings...")
        ratings = ratings_df.to_dict("records")
        session.execute_write(lnu.ingest_ratings, ratings)
        print("Done!")
    else:
        print(f"Ratings already ingested: {total}")

# %% [markdown]
# ## 7. Top Rated Movies
# Query the graph for the highest rated movies, filtering to only include 
# movies with at least 50 ratings to avoid movies with a single perfect score 
# skewing the results.

# %%
with driver.session() as session:
    result = session.run("""
        MATCH (u:User)-[r:RATED]->(m:Movie)
        WITH m, avg(r.rating) AS avg_rating, count(r) AS num_ratings
        WHERE num_ratings >= 50
        RETURN m.title AS title, avg_rating, num_ratings
        ORDER BY avg_rating DESC
        LIMIT 10
    """)
    for r in result:
        print(f"{r['title']}: {r['avg_rating']:.2f} ({r['num_ratings']} ratings)")

# %%
with driver.session() as session:
    result = session.run("""
        MATCH (u:User)-[r:RATED]->(m:Movie)
        WITH m, avg(r.rating) AS avg_rating, count(r) AS num_ratings
        WHERE num_ratings >= 50
        RETURN m.title AS title, avg_rating, num_ratings
        ORDER BY avg_rating DESC
        LIMIT 10
    """)
    data = [(r["title"], r["avg_rating"]) for r in result]

titles = [d[0].split("(")[0].strip() for d in data]  # strip year
ratings = [d[1] for d in data]

plt.figure(figsize=(12, 6))
plt.barh(titles[::-1], ratings[::-1], color="steelblue")
plt.title("Top 10 Highest Rated Movies (min. 50 ratings)")
plt.xlabel("Average Rating")
plt.xlim(4.0, 4.6)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 8. Build the LangChain QA Chain
# Assemble `GraphCypherQAChain` using `lnu.get_qa_chain()`. Under the hood this:
# 1. Initialises `ChatOllama` (local `llama3.2:1b` model via Ollama)
# 2. Attaches a few-shot `PromptTemplate` that guides the model toward correct Cypher
# 3. Wires the LLM and graph together so natural language questions are
#    automatically converted to Cypher, executed, and summarised in plain English

# %%
# Build the Neo4jGraph wrapper and QA chain using utility functions.
graph = lnu.get_neo4j_graph(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)
chain = lnu.get_qa_chain(graph)

# %% [markdown]
# ## 9. Ask Natural Language Questions About Movies
# Pass plain English questions to the chain. LangChain translates each
# question into a Cypher query, runs it against Neo4j, and returns a
# natural language answer powered by the local LLM.

# %%
chain.invoke("List movies in the Action genre.")

# %%
queries = [
    "What genres does Toy Story belong to?",
    "What are the top rated movies?",
    "How many movies are in the Drama genre?",
]
for q in queries:
    print(f"\nQ: {q}")
    result = chain.invoke(q)
    print(f"A: {result['result']}")
