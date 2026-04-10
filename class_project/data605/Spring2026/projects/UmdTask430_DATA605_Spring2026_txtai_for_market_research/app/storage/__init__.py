"""
Storage layer for txtai Market Research Platform.

This package provides multi-tier storage infrastructure:
- Hot tier: KeyDB (Redis-compatible) for live prices, semantic cache, sessions
- Warm tier: PostgreSQL + pgvector for filings, chunks, XBRL facts
- Cold tier: MinIO for raw filings archive
- Graph tier: Kuzu for company/filing/regulation relationships (planned)
"""

# Hot tier - KeyDB
from app.storage.hot_storage.keydb_client import KeyDBClient, get_keydb_client
from app.storage.cache_manager import CacheManager, get_cache_manager

# Warm tier - PostgreSQL + pgvector
from app.storage.warm_storage import (
    PostgresClient,
    get_postgres_client,
    FilingsManager,
    get_filings_manager,
)

# Cold tier - MinIO
from app.storage.cold_storage import MinIOClient, get_minio_client

__all__ = [
    # Hot tier
    "KeyDBClient",
    "get_keydb_client",
    "CacheManager",
    "get_cache_manager",
    # Warm tier
    "PostgresClient",
    "get_postgres_client",
    "FilingsManager",
    "get_filings_manager",
    # Cold tier
    "MinIOClient",
    "get_minio_client",
]
