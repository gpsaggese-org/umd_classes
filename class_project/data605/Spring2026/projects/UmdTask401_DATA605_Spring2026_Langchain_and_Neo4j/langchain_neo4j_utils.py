"""
langchain_neo4j_utils.py

Utility functions for the LangChain + Neo4j knowledge graph project.

- Connect to Neo4j
- Ingest MovieLens data into the graph
- Run Cypher queries
- Build the LangChain QA chain

Import as:
    import langchain_neo4j_utils as lnu
"""

import logging
import pandas as pd
from neo4j import GraphDatabase
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Neo4j Connection
# -----------------------------------------------------------------------------

def get_driver(uri: str, username: str, password: str):
    """
    Create and verify a Neo4j driver connection.

    :param uri: Bolt URI of the Neo4j instance
    :param username: Neo4j username
    :param password: Neo4j password
    :return: connected Neo4j driver instance
    """
    logger.info("Connecting to Neo4j at %s", uri)
    driver = GraphDatabase.driver(uri, auth=(username, password))
    driver.verify_connectivity()
    logger.info("Connected to Neo4j successfully.")
    return driver


def get_neo4j_graph(uri: str, username: str, password: str) -> Neo4jGraph:
    """
    Create a LangChain Neo4jGraph wrapper with a manually set schema.

    :param uri: Bolt URI of the Neo4j instance
    :param username: Neo4j username
    :param password: Neo4j password
    :return: Neo4jGraph instance with schema set
    """
    logger.info("Initializing Neo4jGraph wrapper.")
    graph = Neo4jGraph(
        url=uri,
        username=username,
        password=password,
        refresh_schema=False,
    )
    graph.schema = """
Node properties:
- Movie {movieId: INTEGER, title: STRING}
- Genre {name: STRING}
- User {userId: INTEGER}

Relationships (use EXACTLY these relationship types, spelling and underscores matter):
- (:Movie)-[:IN_GENRE]->(:Genre)    # Note: IN_GENRE not "IN GENRE"
- (:User)-[:RATED {rating: FLOAT}]->(:Movie)
"""
    return graph


# -----------------------------------------------------------------------------
# Data Ingestion
# -----------------------------------------------------------------------------

def ingest_movies(tx, movies: list) -> None:
    """
    Ingest movie records into Neo4j as Movie and Genre nodes.

    Creates Movie nodes and Genre nodes connected by IN_GENRE relationships.
    Uses MERGE to avoid duplicates on repeated runs.

    :param tx: Neo4j transaction object
    :param movies: list of dicts with keys movieId, title, genres
    :return: None
    """
    tx.run("""
        UNWIND $movies AS movie
        MERGE (m:Movie {movieId: movie.movieId, title: movie.title})
        WITH m, movie
        UNWIND split(movie.genres, '|') AS genre
        MERGE (g:Genre {name: genre})
        MERGE (m)-[:IN_GENRE]->(g)
    """, movies=movies)


def ingest_ratings_batch(tx, ratings: list) -> None:
    """Internal: write one batch inside a transaction."""
    tx.run("""
        UNWIND $ratings AS r
        MERGE (u:User {userId: r.userId})
        MERGE (m:Movie {movieId: r.movieId})
        MERGE (u)-[:RATED {rating: r.rating}]->(m)
    """, ratings=ratings)


def ingest_ratings(driver, ratings: list, batch_size: int = 5000) -> None:
    """
    Ingest ratings in batches of 5000 for faster Neo4j writes.
    Takes driver directly instead of a transaction object.
    """
    total = len(ratings)
    for i in range(0, total, batch_size):
        batch = ratings[i: i + batch_size]
        with driver.session() as session:
            session.execute_write(ingest_ratings_batch, batch)
        logger.info("Ingested ratings %d / %d", min(i + batch_size, total), total)


def load_movielens(movies_path: str, ratings_path: str, ratings_sample: int = 100000):
    """
    Load MovieLens CSV files into DataFrames.

    :param movies_path: path to movie.csv
    :param ratings_path: path to rating.csv
    :param ratings_sample: number of ratings rows to load (default 100000)
    :return: tuple of (movies_df, ratings_df)
    """
    logger.info("Loading movies from %s", movies_path)
    movies_df = pd.read_csv(movies_path)
    logger.info("Loaded %d movies.", len(movies_df))
    logger.info("Loading ratings from %s (sample: %d)", ratings_path, ratings_sample)
    ratings_df = pd.read_csv(ratings_path, nrows=ratings_sample)
    logger.info("Loaded %d ratings.", len(ratings_df))
    return movies_df, ratings_df


# -----------------------------------------------------------------------------
# LangChain QA Chain
# -----------------------------------------------------------------------------

def get_cypher_prompt() -> PromptTemplate:
    """
    Build the few-shot PromptTemplate for Cypher generation.

    Uses explicit examples to guide small LLMs toward correct Cypher syntax.

    :return: PromptTemplate with schema and question as input variables
    """
    return PromptTemplate(
        input_variables=["schema", "question"],
        template="""You are a Neo4j Cypher expert. Output ONLY a valid Cypher query, nothing else. No explanation.

Graph schema:
{schema}

Examples (follow these exactly):
Q: List movies in the Action genre.
A: MATCH (m:Movie)-[:IN_GENRE]->(g:Genre {{name: "Action"}}) RETURN m.title LIMIT 10

Q: List movies in the Comedy genre.
A: MATCH (m:Movie)-[:IN_GENRE]->(g:Genre {{name: "Comedy"}}) RETURN m.title LIMIT 10

Q: What genres does Toy Story belong to?
A: MATCH (m:Movie {{title: "Toy Story (1995)"}})-[:IN_GENRE]->(g:Genre) RETURN g.name

Q: What genres does Jumanji belong to?
A: MATCH (m:Movie {{title: "Jumanji (1995)"}})-[:IN_GENRE]->(g:Genre) RETURN g.name

Q: What are the top rated movies?
A: MATCH (u:User)-[r:RATED]->(m:Movie) WITH m, avg(r.rating) AS avg_rating RETURN m.title, avg_rating ORDER BY avg_rating DESC LIMIT 10

Q: How many movies are in the Drama genre?
A: MATCH (m:Movie)-[:IN_GENRE]->(g:Genre {{name: "Drama"}}) RETURN count(m) AS total

Q: How many movies are in the Action genre?
A: MATCH (m:Movie)-[:IN_GENRE]->(g:Genre {{name: "Action"}}) RETURN count(m) AS total

Now answer this:
Q: {question}
A:"""
    )


def get_qa_chain(graph: Neo4jGraph, model: str = "llama3.2:1b", base_url: str = "http://host.docker.internal:11434") -> GraphCypherQAChain:
    """
    Build and return a GraphCypherQAChain for natural language querying.

    :param graph: initialized Neo4jGraph instance
    :param model: Ollama model name (default llama3.2:1b)
    :param base_url: Ollama server URL
    :return: configured GraphCypherQAChain
    """
    logger.info("Initializing LLM: %s", model)
    llm = ChatOllama(model=model, base_url=base_url)
    prompt = get_cypher_prompt()
    logger.info("Building GraphCypherQAChain.")
    chain = GraphCypherQAChain.from_llm(
        llm,
        graph=graph,
        verbose=True,
        allow_dangerous_requests=True,
        cypher_prompt=prompt,
    )
    return chain