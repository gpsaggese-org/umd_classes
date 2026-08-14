#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Auto-reload local modules (e.g., llamaindex_utils.py) on every cell execution
# Useful during development, no kernel restart needed after editing helper files
try:
    from IPython import get_ipython  # type: ignore
    ip = get_ipython()
    if ip is not None:
        ip.run_line_magic("load_ext", "autoreload")
        ip.run_line_magic("autoreload", "2")
except Exception:
    pass


# # LlamaIndex API Tutorial
# 
# This tutorial examines the core architecture of LlamaIndex from the ground up.
# Instead of treating the library as a black box, we trace each step of a
# Retrieval-Augmented Generation (RAG) pipeline through four pillars:
# 
# 1. **Documents & Nodes** - how raw text is ingested and chunked
# 2. **Embeddings** - how text is converted into semantic vector representations
# 3. **VectorStoreIndex** - how chunks are indexed for similarity search
# 4. **Retrievers & QueryEngine** - how a query finds context and generates an answer
# 
# ### Pipeline Architecture
# ```mermaid
# graph LR
#     A[Raw Text] -->|Data Loaders| B(Documents)
#     B -->|Node Parsers| C(Nodes)
#     C -->|Embedding Model| D[(Vector Index)]
#     D -->|Retriever| E(Query Engine)
# ```
# 
# > **Environment:** Ollama (`llama3`) as the local LLM +
# > `BAAI/bge-small-en-v1.5` (HuggingFace) as the embedding model.
# > No external API key required.

# ## 0. Setup
# 
# We configure two core components that power the entire pipeline:
# 
# - **LLM:** Ollama running `llama3` locally - handles answer generation in the QueryEngine
# - **Embedding Model:** `BAAI/bge-small-en-v1.5` via HuggingFace - converts text to vectors for similarity search
# 
# Both run fully locally. No OpenAI API key or internet connection required after initial model download.

# In[7]:


import logging
from llamaindex_utils import setup_environment, configure_ollama

# Suppress verbose logs from LlamaIndex and HuggingFace during model loading
setup_environment(verbosity=logging.WARNING)

# Configure the global LLM (Ollama/llama3) and embedding model (BAAI/bge-small-en-v1.5)
# These are set on llama_index.core.Settings and used automatically by all downstream components
configure_ollama(model_name="llama3")

print("LLM and embedding model configured. Ready to build the pipeline.")


# ## 1. Documents & Nodes
# 
# A **Document** is a wrapper around raw text along with optional metadata (e.g. source, author, date).
# 
# LLMs have a fixed context window, they cannot process an entire document at once. LlamaIndex solves this using a **NodeParser**, which splits a Document into smaller, overlapping chunks called **Nodes**. Each Node inherits the parent Document's metadata, so the source is never lost during retrieval.
# 
# Two key parameters control how splitting works:
# - `chunk_size` - maximum number of tokens per Node
# - `chunk_overlap` - how many tokens are shared between consecutive Nodes (prevents losing context at boundaries)
# 
# In the cell below, we explicitly instantiate a `SentenceSplitter` to see this chunking process in action.

# In[3]:


from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter

# Create a Document with two semantically distinct paragraphs and source metadata
raw_text = (
    "LlamaIndex is a data framework designed to connect LLMs with external data sources. "
    "It provides tools for ingestion, indexing, and querying over custom datasets. "
    "The framework is highly modular, allowing developers to swap components like LLMs and embedding models. "
    "It is widely used for building production-grade RAG pipelines.\n\n"
    "Nodes are the atomic unit of data in LlamaIndex. "
    "Each Node represents a chunk of text derived from a parent Document. "
    "Nodes inherit metadata from their parent, ensuring traceability during retrieval. "
    "The chunking strategy directly affects retrieval quality and LLM response accuracy."
)
doc = Document(text=raw_text, metadata={"source": "tutorial"})

# SentenceSplitter chunks the Document into Nodes while respecting sentence boundaries
# chunk_size: max tokens per Node | chunk_overlap: shared tokens between consecutive Nodes
parser = SentenceSplitter(chunk_size=64, chunk_overlap=10)
nodes = parser.get_nodes_from_documents([doc])

print(f"Original Document length: {len(raw_text)} characters")
print(f"Number of Nodes generated: {len(nodes)}\n")

for i, node in enumerate(nodes):
    print(f"--- Node {i+1} ---")
    print(f"ID: {node.node_id}")
    print(f"Text: {node.text[:120]}...")
    print(f"Metadata: {node.metadata}")
    print()


# ## 2. Embeddings
# 
# How does the system know *which* Node is relevant to your question?
# 
# Every piece of text, both the Nodes in the index and your incoming query is converted into an **embedding**: a fixed-length vector of floating point numbers that encodes the semantic meaning of the text. The embedding model was configured globally in the setup cell via `Settings.embed_model` and is used automatically by all downstream components.
# 
# Two texts that are semantically similar will produce vectors that point in roughly the same direction in vector space. This is measured using **cosine similarity**, the closer the angle between two vectors, the more semantically related the texts are.
# 
# This is how retrieval works:
# 1. At index time every Node is embedded and stored
# 2. At query time the query is embedded using the same model
# 3. The Retriever finds the Nodes whose vectors are closest to the query vector
# 
# Below we generate a raw embedding to inspect what the model actually produces.

# In[4]:


import numpy as np
from llama_index.core import Settings

embed_model = Settings.embed_model

# Two semantically related texts and one unrelated text
text_a = "LlamaIndex is a framework for building RAG pipelines."
text_b = "RAG systems retrieve documents to augment LLM responses."
text_c = "The weather in Paris is warm during summer."

# Generate embedding vectors for all three
emb_a = np.array(embed_model.get_text_embedding(text_a))
emb_b = np.array(embed_model.get_text_embedding(text_b))
emb_c = np.array(embed_model.get_text_embedding(text_c))

print(f"Embedding dimension: {len(emb_a)}")
print(f"First 5 values of vector A: {emb_a[:5].tolist()}\n")

# Cosine similarity: measures angle between two vectors
# Score of 1.0 = identical direction, 0.0 = unrelated
def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

sim_ab = cosine_similarity(emb_a, emb_b)
sim_ac = cosine_similarity(emb_a, emb_c)

print(f"Similarity (A vs B - both about RAG): {sim_ab:.4f}")
print(f"Similarity (A vs C - unrelated topic): {sim_ac:.4f}")
print(f"\nConclusion: The retriever will rank B over C when answering questions about RAG.")


# ## 3. VectorStoreIndex
# 
# `VectorStoreIndex` is the central component of the pipeline. It combines everything we have stepped through so far into a single automated workflow:
# 
# 1. Takes one or more `Document` objects as input
# 2. Runs them through the `NodeParser` to produce `Nodes`
# 3. Embeds each `Node` using the configured embedding model
# 4. Stores the resulting vectors in memory for similarity search
# 
# By default, the index is **in-memory only**. It is rebuilt from scratch each time the notebook runs and is not persisted to disk. For production use cases, LlamaIndex supports persistent storage backends (e.g. saving to disk via `StorageContext`, or connecting to a vector database like Pinecone or Weaviate).
# 
# In the cell below, we build the index from the `Document` created in Section 1.

# In[5]:


from llama_index.core import VectorStoreIndex

print("Building index - chunking documents, generating embeddings, storing vectors...")

# from_documents() internally runs the full pipeline:
# Document -> NodeParser -> Nodes -> EmbeddingModel -> VectorStore
# We pass the same parser to ensure consistent chunking
index = VectorStoreIndex.from_documents(
    [doc],
    transformations=[parser]
)

# nodes comes from the earlier SentenceSplitter output (Documents & Nodes section)
num_nodes = len(nodes)
num_docs = 1  # we passed in 1 document to from_documents()

print(f"Documents indexed: {num_docs}")
print(f"Nodes stored in vector index: {num_nodes}")
print(f"\nIndex is ready. Each node is now searchable by semantic similarity.")


# ## 4. Retrievers & QueryEngine
# 
# The final stage of the pipeline has two distinct steps:
# 
# **Step 1 - Retrieval:**
# The **Retriever** takes the incoming query, embeds it using the same embedding model from Section 2, and computes cosine similarity against every Node vector in the index. It returns the top `k` most similar Nodes as raw context. The parameter `similarity_top_k` controls how many Nodes are retrieved.
# 
# **Step 2 - Synthesis:**
# The **QueryEngine** wraps the Retriever and adds a synthesis step. It takes the retrieved Nodes, constructs a prompt combining the context and the original query, and passes it to the LLM (Ollama/llama3) to generate a final answer.
# 
# In the cell below, we run both steps explicitly. First, inspecting the raw retrieved context, then observing the synthesized answer to understand what the LLM actually receives as input.

# In[6]:


query = "What is LlamaIndex and what tools does it provide?"

# Step 1: Retrieval
# The retriever embeds the query and finds the top-k most similar Nodes
# similarity_top_k=1 returns only the single most relevant Node
retriever = index.as_retriever(similarity_top_k=1)
retrieved_nodes = retriever.retrieve(query)

print("STEP 1: RAW RETRIEVED CONTEXT\n")
for i, node in enumerate(retrieved_nodes):
    print(f"Node {i+1} (similarity score: {node.score:.4f}):")
    print(node.node.text)
    print()

# Step 2: Synthesis
# The QueryEngine wraps the Retriever and passes the retrieved context
# to the LLM (Ollama/llama3) to synthesize a final answer
# Note: the same query is used so we can directly compare raw context vs LLM answer
query_engine = index.as_query_engine()
response = query_engine.query(query)

print("\nSTEP 2: LLM SYNTHESIZED ANSWER\n")
print(response)


# ## Summary
# 
# This notebook traced the full architecture of a LlamaIndex RAG pipeline from the ground up, examining each component individually before seeing them work together.
# 
# | Section | Component | Key Takeaway |
# |---|---|---|
# | 1 | Documents & Nodes | Raw text is wrapped in `Document` objects and chunked into `Nodes` by a `NodeParser`. `chunk_size` and `chunk_overlap` directly affect retrieval quality. |
# | 2 | Embeddings | Text is converted into fixed-length vectors by an embedding model. Cosine similarity between vectors determines which Nodes are relevant to a query. |
# | 3 | VectorStoreIndex | Automates the full ingestion pipeline - chunking, embedding, and storing Nodes in an in-memory vector store ready for similarity search. |
# | 4 | Retrievers & QueryEngine | The Retriever fetches the most similar Nodes using vector similarity. The QueryEngine combines retrieved context with the query and passes it to the LLM for answer synthesis. |
# 
# The next notebook `llamaindex.example.ipynb` applies these concepts to real-world Wikipedia data and builds an advanced ReAct Agent on top of this same architecture.