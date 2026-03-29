# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
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
# # LlamaIndex Example: Retrieval-Augmented Generation on Real Text
#
# In this notebook, we build a complete Retrieval-Augmented Generation (RAG) system using real-world data from Project Gutenberg.
#
# We will:
#
# - Automatically download public domain books
# - Preprocess and clean the text
# - Build a vector index
# - Query across multiple documents
# - Inspect retrieved context
# - Evaluate retrieval behavior
#
# This example demonstrates how LlamaIndex can be applied to real textual corpora.

# %% [markdown]
# ## Model Setup
#
# We configure:
#
# - A lightweight embedding model for semantic similarity
# - A local instruction-tuned language model for generation
#
# Both models run locally and do not require API keys.

# %%
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface import HuggingFaceLLM
import os
import requests

# Embedding model
embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# LLM model
llm = HuggingFaceLLM(
    model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    tokenizer_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    context_window=2048,
    max_new_tokens=128,
    generate_kwargs={"temperature": 0.0},
    device_map="auto",
)

Settings.embed_model = embed_model
Settings.llm = llm

print("Models configured successfully.")

# %% [markdown]
# ## Download Project Gutenberg Books
#
# We download two public domain books:
#
# - Pride and Prejudice
# - The Adventures of Sherlock Holmes
#
# These texts will serve as our knowledge base.
#
# We store them locally inside the `data/gutenberg` directory.

# %%
# Create dataset directory
os.makedirs("data/gutenberg", exist_ok=True)

books = {
    "pride_and_prejudice.txt": "https://www.gutenberg.org/files/1342/1342-0.txt",
    "sherlock_holmes.txt": "https://www.gutenberg.org/files/1661/1661-0.txt",
}


def clean_gutenberg_text(text):
    start_marker = "*** START OF"
    end_marker = "*** END OF"

    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)

    if start_idx != -1 and end_idx != -1:
        text = text[start_idx:end_idx]

    return text


for filename, url in books.items():
    response = requests.get(url)
    raw_text = response.text
    cleaned_text = clean_gutenberg_text(raw_text)

    with open(f"data/gutenberg/{filename}", "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    print(f"Downloaded and cleaned: {filename}")

# %%
for filename in books.keys():
    path = f"data/gutenberg/{filename}"
    size_kb = os.path.getsize(path) / 1024
    print(f"{filename}: {size_kb:.2f} KB")

# %% [markdown]
# ## Load Documents
#
# We load the cleaned text files using `SimpleDirectoryReader`.
#
# Each file becomes a `Document` object containing:
#
# - Text content
# - Metadata (file name, path, etc.)
#
# These documents will be parsed into nodes for indexing.

# %%
documents = SimpleDirectoryReader("data/gutenberg").load_data()

print(f"Number of documents loaded: {len(documents)}")

for doc in documents:
    print(doc.metadata["file_name"])

# %% [markdown]
# ## Chunking Large Documents
#
# Large documents must be split into smaller chunks before indexing.
#
# Why?
#
# - Embedding models operate on limited context windows
# - Retrieval happens at the chunk (node) level
# - Smaller chunks allow more precise retrieval
#
# We configure a reasonable chunk size for long-form text.

# %%
parser = SentenceSplitter(
    chunk_size=512,
    chunk_overlap=50,
)

nodes = parser.get_nodes_from_documents(documents)

print(f"Total nodes created: {len(nodes)}")

# %% [markdown]
# ## Build the Vector Index
#
# We now construct a `VectorStoreIndex` from the parsed nodes.
#
# This step:
#
# - Computes embeddings for each node
# - Stores them in a vector index
# - Enables semantic similarity search

# %%
index = VectorStoreIndex(nodes)

print("Vector index built successfully.")

# %% [markdown]
# ## Query the Combined Corpus
#
# We now query across both books using semantic retrieval.
#
# The system will:
#
# 1. Embed the question
# 2. Retrieve the most relevant chunks
# 3. Inject them into the prompt
# 4. Generate a response

# %%
query_engine = index.as_query_engine(similarity_top_k=3)

response = query_engine.query("Who is Mr. Darcy?")

print(response)

# %% [markdown]
# ## Inspect Retrieved Chunks
#
# To understand how the system arrived at its answer,
# we inspect the retrieved source nodes.
#
# This allows us to see:
#
# - Which document was used
# - What text supported the response
# - The similarity score

# %%
for i, source_node in enumerate(response.source_nodes):
    print(f"\n--- Retrieved Node {i + 1} ---")
    print("File:", source_node.node.metadata.get("file_name"))
    print("Score:", source_node.score)
    print("\nText snippet:\n")
    print(source_node.node.text[:500])
    print("\n" + "=" * 60)

# %% [markdown]
# ## Query a Different Book
#
# We now query about Sherlock Holmes to verify that
# retrieval works across multiple documents.

# %%
response_holmes = query_engine.query("Describe Sherlock Holmes' personality.")

print(response_holmes)

# %% [markdown]
# ## Effect of Retrieval Depth (top_k)
#
# We compare responses using different retrieval depths.
#
# Higher `top_k` includes more context,
# which may improve completeness but increase latency.

# %%
# top_k = 1
query_engine_k1 = index.as_query_engine(similarity_top_k=1)
response_k1 = query_engine_k1.query("Who is Mr. Darcy?")

print("=== top_k = 1 ===")
print(response_k1)
print("\n")

# top_k = 3
query_engine_k3 = index.as_query_engine(similarity_top_k=3)
response_k3 = query_engine_k3.query("Who is Mr. Darcy?")

print("=== top_k = 3 ===")
print(response_k3)

# %% [markdown]
# ## Summary
#
# In this example, we built a complete retrieval-augmented generation (RAG) system using real-world text.
#
# We demonstrated:
#
# - Automatic dataset download
# - Text preprocessing
# - Chunking large documents
# - Vector index construction
# - Cross-document querying
# - Retrieval inspection
# - The effect of retrieval depth (`top_k`)
#
# This example illustrates how LlamaIndex can be applied to real textual corpora to build grounded question-answering systems.

# %% [markdown]
#
