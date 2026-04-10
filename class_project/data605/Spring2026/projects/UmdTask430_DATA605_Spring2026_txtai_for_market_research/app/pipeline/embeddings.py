"""
Shared EmbeddingsIndex configuration for txtai.

This module configures a single txtai.Embeddings instance backed by SQLite.
All agents share this index but filter by metadata tags (source: news|sec|web|social|earnings).
"""

import os
from pathlib import Path
from txtai.embeddings import Embeddings


def get_data_dir() -> Path:
    """Get the data directory path, creating it if necessary."""
    # Support both local and deployed environments
    base = Path(os.getenv("TXTAI_DATA_DIR", Path(__file__).parent.parent.parent / "data"))
    base.mkdir(parents=True, exist_ok=True)
    return base


def create_embeddings() -> Embeddings:
    """
    Create and return a configured txtai Embeddings instance.

    Configuration:
    - Path: SQLite database at data/index.db
    - Embedding model: Ollama nomic-embed-text (fast, good quality for semantic search)
    - Content format: text with metadata for filtering

    The 'content=True' setting stores the original text in the index,
    which allows us to retrieve full snippets without a separate database.
    """
    db_path = get_data_dir() / "index.db"

    # Get Ollama embedding model from environment
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    embed_model = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")

    embeddings = Embeddings(
        {
            "path": str(db_path),
            "method": f"ollama:{embed_model}@{ollama_host}",
            "content": True,  # Store original text in index
            "chunksize": 100,  # Batch size for embedding operations
        }
    )

    return embeddings


# Global singleton instance - shared across all modules
# This ensures all agents query the same index
_embeddings_instance: Embeddings | None = None


def get_embeddings() -> Embeddings:
    """
    Get the singleton Embeddings instance.

    Creates a new instance on first call, returns existing instance thereafter.
    This prevents multiple SQLite connections and ensures consistent state.
    """
    global _embeddings_instance
    if _embeddings_instance is None:
        _embeddings_instance = create_embeddings()
    return _embeddings_instance


def search(query: str, source_filter: str | None = None, limit: int = 5) -> list[dict]:
    """
    Search the embeddings index with optional source filtering.

    Args:
        query: The search query text
        source_filter: Optional metadata filter (news|sec|web|social|earnings)
        limit: Maximum number of results to return

    Returns:
        List of dicts with keys: id, text, score, metadata

    Note: Uses txtai's SQL-like filtering syntax for metadata filtering.
    """
    embeddings = get_embeddings()

    if source_filter:
        # txtai supports SQL-like WHERE clauses for metadata filtering
        # The 'tags' field contains the source metadata
        results = embeddings.search(
            f"{query} WHERE tags = '{source_filter}'",
            limit=limit
        )
    else:
        results = embeddings.search(query, limit=limit)

    return results


def upsert(documents: list[dict]) -> list[str]:
    """
    Index documents into the embeddings database.

    Args:
        documents: List of dicts with keys:
            - id: Unique document identifier
            - text: The text content to embed
            - tags: Source tag (news|sec|web|social|earnings)

    Returns:
        List of document IDs that were indexed

    Note: txtai's 'upsert' will insert new documents or update existing ones
    with the same ID.
    """
    embeddings = get_embeddings()

    # Transform to txtai's expected format: (id, text, tags)
    index_documents = []
    for doc in documents:
        index_documents.append({
            "id": doc["id"],
            "text": doc["text"],
            "tags": doc.get("tags", "unknown"),
            "metadata": doc.get("metadata", {})
        })

    ids = embeddings.upsert(index_documents)
    embeddings.save()  # Persist to SQLite

    return ids
