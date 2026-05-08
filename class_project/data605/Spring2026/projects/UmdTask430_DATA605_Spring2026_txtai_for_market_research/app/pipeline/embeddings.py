"""
Shared EmbeddingsIndex configuration for txtai.

This module configures a single txtai.Embeddings instance backed by SQLite.
All agents share this index but filter by metadata tags (source: news|sec).
"""

import os
from pathlib import Path
from txtai.embeddings import Embeddings


def get_data_dir() -> Path:
    """Get the data directory path, creating it if necessary."""
    # Support both local and deployed environments
    base = Path(
        os.getenv("TXTAI_DATA_DIR", Path(__file__).parent.parent.parent / "data")
    )
    base.mkdir(parents=True, exist_ok=True)
    return base


def create_embeddings() -> Embeddings:
    """
    Create and return a configured txtai Embeddings instance.

    If a saved index exists in the data directory (config + documents +
    embeddings files), load it. Otherwise create a fresh index.

    - Embedding model: sentence-transformers/all-mpnet-base-v2 (768-dim,
      matches pgvector schema)
    - content=True stores original text in SQLite alongside the ANN index
    """
    data_dir = get_data_dir()
    config_file = data_dir / "config.json"
    if config_file.exists():
        # Load persisted index from disk.
        embeddings = Embeddings()
        embeddings.load(str(data_dir))
        return embeddings
    # No saved index: create a new one.
    embeddings = Embeddings(
        {
            "path": "sentence-transformers/all-mpnet-base-v2",
            "content": True,
            "chunksize": 100,
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

    :param query: the search query text
    :param source_filter: optional source tag filter (e.g. ``"news"`` or
                          ``"sec"``); ``None`` searches across everything
    :param limit: maximum number of results to return
    :return: list of dicts with keys ``id``, ``text``, ``score``, ``tags``,
             ``metadata`` (decoded from the on-disk JSON ``data`` column)
    """
    import json

    embeddings = get_embeddings()
    # Use parameterized SQL so apostrophes / quotes / colons in the user's
    # query don't break txtai's SQL parser. Pulling the ``data`` column
    # surfaces our custom per-chunk metadata (ticker, filing_type,
    # filing_date) which txtai does not expose by default.
    params: dict[str, str] = {"q": query}
    where_clauses = ["similar(:q)"]
    if source_filter:
        where_clauses.append("tags = :src")
        params["src"] = source_filter
    where_sql = " AND ".join(where_clauses)
    sql = (
        "SELECT id, text, score, tags, data FROM txtai "
        f"WHERE {where_sql} LIMIT {int(limit)}"
    )
    raw = embeddings.search(sql, parameters=params, limit=limit)
    # Decode the ``data`` blob and lift the inner ``metadata`` dict to top
    # level so callers don't have to know about txtai's internal layout.
    out = []
    for row in raw:
        data_str = row.get("data") or "{}"
        try:
            data = json.loads(data_str) if isinstance(data_str, str) else data_str
        except Exception:
            data = {}
        out.append(
            {
                "id": row.get("id"),
                "text": row.get("text") or data.get("text", ""),
                "score": row.get("score"),
                "tags": row.get("tags") or data.get("tags"),
                "metadata": data.get("metadata") or {},
            }
        )
    return out


def upsert(documents: list[dict], *, save: bool = True) -> list[str]:
    """
    Index documents into the embeddings database.

    Args:
        documents: List of dicts with keys:
            - id: Unique document identifier
            - text: The text content to embed
            - tags: Source tag (news|sec)
        save: If True, persist the ANN index files after upsert.
              Set False during batched backfills, then call
              get_embeddings().save(get_data_dir()) once at the end.

    Returns:
        List of document IDs that were indexed.

    Note: txtai's 'upsert' inserts new documents or updates existing ones
    with the same ID. The content (text + metadata) is stored in the
    SQLite database at index_path; the ANN index is persisted via save().
    """
    embeddings = get_embeddings()
    # Transform to txtai's expected dict format.
    index_documents = []
    for doc in documents:
        index_documents.append(
            {
                "id": doc["id"],
                "text": doc["text"],
                "tags": doc.get("tags", "unknown"),
                "metadata": doc.get("metadata", {}),
            }
        )
    embeddings.upsert(index_documents)
    if save:
        # Persist ANN index files to the data directory.
        embeddings.save(str(get_data_dir()))
    return [doc["id"] for doc in index_documents]
