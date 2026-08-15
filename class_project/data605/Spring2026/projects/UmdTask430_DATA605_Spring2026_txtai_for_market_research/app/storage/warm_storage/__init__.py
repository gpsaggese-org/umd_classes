"""
Warm storage layer using PostgreSQL + pgvector.

This package provides persistent storage for:
- SEC filings metadata
- Document chunks with vector embeddings
- XBRL facts (structured financial data)
- Semantic search via pgvector

Modules:
- pgvector_client: Low-level PostgreSQL client with connection pooling
- filings_manager: High-level manager for filings, chunks, and XBRL facts
"""

from app.storage.warm_storage.pgvector_client import PostgresClient, get_postgres_client
from app.storage.warm_storage.filings_manager import (
    FilingsManager,
    get_filings_manager,
    FilingData,
    ChunkData,
    XBRLFact,
    SearchResults,
    generate_filing_id,
    generate_chunk_id,
    generate_xbrl_fact_id,
)

__all__ = [
    # Client
    "PostgresClient",
    "get_postgres_client",
    # Manager
    "FilingsManager",
    "get_filings_manager",
    # Data classes
    "FilingData",
    "ChunkData",
    "XBRLFact",
    "SearchResults",
    # ID generators
    "generate_filing_id",
    "generate_chunk_id",
    "generate_xbrl_fact_id",
]
