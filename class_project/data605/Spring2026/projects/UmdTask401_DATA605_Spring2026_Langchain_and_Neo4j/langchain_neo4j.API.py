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
# # LangChain + Neo4j API Notebook
#
# This notebook documents the key APIs used in the LangChain + Neo4j 
# knowledge graph project. It serves as a reference guide for the 
# following tools:
#
# - `neo4j` Python driver: connecting to and querying Neo4j
# - `langchain_neo4j`: Neo4jGraph wrapper and GraphCypherQAChain
# - `langchain_ollama`: local LLM via Ollama
# - `langchain_core`: PromptTemplate for custom prompts
#
# Reference: langchain_neo4j.example.ipynb

# %% [markdown]
# ## Imports

# %%
import logging
import neo4j
import langchain_neo4j
import langchain_ollama
from neo4j import GraphDatabase
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
import helpers.hdbg as hdbg
import helpers.hnotebook as hnotebook

# %% [markdown]
# ## Configuration

# %%
# Neo4j connection settings.
# host.docker.internal resolves to the host machine from inside Docker,
# allowing the Jupyter container to reach the separately running Neo4j container.
# On Linux add --add-host=host.docker.internal:host-gateway to docker_jupyter.sh.
NEO4J_URI = "bolt://host.docker.internal:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "password"
print(f"Connecting to Neo4j at: {NEO4J_URI}")

# %%
hdbg.init_logger(verbosity=logging.INFO)
_LOG = logging.getLogger(__name__)
hnotebook.config_notebook()

# %% [markdown]
# ## 1. Neo4j Python Driver
#
# The `neo4j` package provides the official Python driver for connecting 
# to a Neo4j database. The main entry point is `GraphDatabase.driver()`.
#
# Key parameters:
# - `uri`: the Bolt protocol URI of the Neo4j instance
# - `auth`: tuple of (username, password)
#
# Reference: https://neo4j.com/docs/api/python-driver/current/

# %%
import langchain_neo4j_utils as lnu

# Use utility function to connect.
driver = lnu.get_driver(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)

# %% [markdown]
# ## 2. Running Cypher Queries
#
# Queries are executed inside a session using `session.run()`. 
# Results are returned as a cursor that can be iterated over.
#
# Key session methods:
# - `session.run(query)`: execute a read query
# - `session.execute_write(fn)`: execute a write transaction
# - `session.execute_read(fn)`: execute a read transaction

# %%
# Run a simple read query using a session.
with driver.session() as session:
    result = session.run("MATCH (m:Movie) RETURN m.title AS title LIMIT 3")
    for record in result:
        print(record["title"])

# %%
# Run a parameterized query using $param syntax.
# Parameterized queries are safer and more efficient than string formatting.
with driver.session() as session:
    result = session.run(
        "MATCH (m:Movie)-[:IN_GENRE]->(g:Genre {name: $genre}) RETURN m.title LIMIT 3",
        genre="Comedy"
    )
    for record in result:
        print(record["m.title"])

# %%
# Use execute_write for write transactions.
# The function receives a transaction object (tx) and runs queries on it.
def create_test_node(tx):
    """Create a test node and return its name."""
    tx.run("MERGE (t:TestNode {name: 'api_test'})")
    result = tx.run("MATCH (t:TestNode {name: 'api_test'}) RETURN t.name AS name")
    return result.single()["name"]

with driver.session() as session:
    name = session.execute_write(create_test_node)
    print(f"Created node: {name}")

# Clean up the test node.
with driver.session() as session:
    session.run("MATCH (t:TestNode {name: 'api_test'}) DELETE t")
    print("Test node deleted.")

# %% [markdown]
# ## 3. Neo4jGraph (LangChain Wrapper)
#
# `Neo4jGraph` is a LangChain wrapper around the Neo4j driver that 
# simplifies integration with LangChain chains. It exposes the graph 
# schema and provides a `query()` method.
#
# Key parameters:
# - `url`: Bolt URI
# - `username`: Neo4j username
# - `password`: Neo4j password
# - `refresh_schema`: whether to auto-fetch schema on init
#
# Reference: https://python.langchain.com/docs/integrations/graphs/neo4j_cypher/

# %%
# Use utility function to get graph wrapper with schema pre-set.
graph = lnu.get_neo4j_graph(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)
print(graph.schema)

# %%
# Use graph.query() to run Cypher directly through the wrapper.
results = graph.query("MATCH (g:Genre) RETURN g.name AS genre LIMIT 5")
for r in results:
    print(r["genre"])

# %% [markdown]
# ## 4. ChatOllama (Local LLM)
#
# `ChatOllama` connects to a locally running Ollama instance and exposes 
# it as a LangChain chat model. Ollama must be running on the host machine.
#
# Key parameters:
# - `model`: the Ollama model name (e.g. "llama3.2:1b")
# - `base_url`: URL of the Ollama server
#
# Note: Inside Docker, use `host.docker.internal` instead of `localhost` 
# to reach the host machine's Ollama server.
#
# Reference: https://ollama.com/

# %%
# Initialize the local LLM via Ollama.
llm = ChatOllama(
    model="llama3.2:1b",
    base_url="http://host.docker.internal:11434"
)
print(f"LLM initialized: {llm.model}")

# %%
# Invoke the LLM directly with a simple prompt.
response = llm.invoke("What is Neo4j used for? Answer in one sentence.")
print(response.content)

# %% [markdown]
# ## 5. PromptTemplate
#
# `PromptTemplate` allows defining reusable prompt templates with 
# named input variables. It is used to customize how the LLM is 
# instructed to generate Cypher queries.
#
# Key parameters:
# - `input_variables`: list of variable names used in the template
# - `template`: the prompt string with `{variable}` placeholders
#
# Note: Use `{{` and `}}` to include literal curly braces in the template.
#
# Reference: https://python.langchain.com/docs/concepts/prompt_templates/

# %%
# Define a simple prompt template with one variable.
simple_prompt = PromptTemplate(
    input_variables=["topic"],
    template="Explain {topic} in one sentence."
)
# Format the prompt with a concrete value.
formatted = simple_prompt.format(topic="graph databases")
print(formatted)

# %%
# Define the Cypher generation prompt used in this project.
# Uses two variables: schema (the graph structure) and question (user input).
CYPHER_PROMPT = PromptTemplate(
    input_variables=["schema", "question"],
    template="""You are a Neo4j Cypher expert. Output ONLY a valid Cypher query.

Graph schema:
{schema}

Question: {question}
Cypher query:"""
)
# Show the prompt formatted with example inputs.
print(CYPHER_PROMPT.format(
    schema="(:Movie)-[:IN_GENRE]->(:Genre)",
    question="List action movies."
))

# %% [markdown]
# ## 6. GraphCypherQAChain
#
# `GraphCypherQAChain` is the core LangChain chain that combines the 
# LLM and Neo4j graph to answer natural language questions. It:
#
# 1. Uses the LLM to convert the question into a Cypher query
# 2. Runs the Cypher query against Neo4j
# 3. Uses the LLM again to convert the results into a natural language answer
#
# Key parameters:
# - `llm`: the language model to use
# - `graph`: the Neo4jGraph instance
# - `verbose`: print intermediate steps
# - `allow_dangerous_requests`: required to enable Cypher execution
# - `cypher_prompt`: custom PromptTemplate for Cypher generation
#
# Reference: https://python.langchain.com/docs/integrations/graphs/neo4j_cypher/

# %%
# Use utility function to build the full QA chain.
chain = lnu.get_qa_chain(graph)
print(f"Chain type: {type(chain).__name__}")
print(f"Input keys: {chain.input_keys}")
print(f"Output keys: {chain.output_keys}")

# %%
# Invoke the chain with a natural language question.
# The chain handles Cypher generation and result interpretation automatically.
response = chain.invoke("How many movies are in the Comedy genre?")
print(f"Answer: {response['result']}")

# %% [markdown]
# ## 7. Driver Cleanup
#
# Always close the Neo4j driver when done to release the connection pool.

# %%
# Close the driver connection.
driver.close()
print("Driver closed.")
