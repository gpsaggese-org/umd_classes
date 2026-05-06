"""
Cold storage for raw document archive.

MinIO (S3-compatible) object storage for:
- Raw SEC filings (original HTML/XML)
- News article HTML
"""

from app.storage.cold_storage.minio_client import MinIOClient, get_minio_client

__all__ = [
    "MinIOClient",
    "get_minio_client",
]
