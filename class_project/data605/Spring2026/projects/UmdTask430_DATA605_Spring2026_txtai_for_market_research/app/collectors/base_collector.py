"""
Base collector with common storage logic.

All collectors inherit from this base class which provides:
- Multi-tier storage (cold, warm, hot, search)
- Document chunking for embeddings
- Deduplication via deterministic IDs
- Progress tracking and logging
"""

import hashlib
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional

from txtai.pipeline import Pipeline as TxtAIChunking

from app.storage import (
    get_minio_client,
    get_postgres_client,
    get_cache_manager,
    get_embeddings,
)
from app.storage.cold_storage.minio_client import MinIOClient
from app.storage.warm_storage.pgvector_client import PostgresClient
from app.storage.cache_manager import CacheManager

_LOG = logging.getLogger(__name__)


class BaseCollector(ABC):
    """
    Abstract base class for all data collectors.

    Subclasses must implement:
    - _fetch_data(): Fetch raw data from the source
    - _get_source_tag(): Return source identifier (e.g., "sec", "news")
    """

    # Chunking configuration
    MAX_TOKENS_PER_CHUNK = 512
    CHUNKING_PIPELINE: Optional[TxtAIChunking] = None

    def __init__(self):
        """Initialize collector with storage clients."""
        self.minio: MinIOClient = get_minio_client()
        self.postgres: PostgresClient = get_postgres_client()
        self.cache: CacheManager = get_cache_manager()
        self.embeddings = get_embeddings()

    def _get_chunking_pipeline(self) -> TxtAIChunking:
        """Get or create the chunking pipeline (lazy initialization)."""
        if self.CHUNKING_PIPELINE is None:
            self.CHUNKING_PIPELINE = TxtAIChunking("chunking", sentences=True)
        return self.CHUNKING_PIPELINE

    def _generate_doc_id(self, source: str, content: str, ticker: str) -> str:
        """
        Generate a deterministic document ID for deduplication.

        Uses SHA256 hash to ensure:
        - Same document always gets same ID (idempotent)
        - Different sources/tickers get different IDs
        """
        key = f"{source}:{ticker}:{content[:500]}"
        return hashlib.sha256(key.encode()).hexdigest()[:32]

    def _chunk_text(self, text: str) -> list[str]:
        """
        Split text into chunks respecting sentence boundaries.

        Args:
            text: The text to chunk

        Returns:
            List of text chunks
        """
        chunker = self._get_chunking_pipeline()
        chunks = chunker(text)

        # Group chunks to maximize token budget
        result = []
        current_chunk = ""
        chunk_chars = self.MAX_TOKENS_PER_CHUNK * 4  # ~4 chars per token

        for chunk in chunks:
            if len(current_chunk) + len(chunk) <= chunk_chars:
                current_chunk += " " + chunk if current_chunk else chunk
            else:
                if current_chunk:
                    result.append(current_chunk.strip())
                current_chunk = chunk

        if current_chunk:
            result.append(current_chunk.strip())

        return result if result else [text]

    def _store_to_cold_tier(
        self,
        ticker: str,
        content: str,
        metadata: dict[str, Any],
    ) -> Optional[str]:
        """
        Store raw document in MinIO cold storage.

        Args:
            ticker: Stock ticker symbol
            content: Raw document content
            metadata: Document metadata

        Returns:
            Object path in MinIO, or None on failure
        """
        source = self._get_source_tag()
        url = metadata.get("url", "")

        if source == "sec":
            return self.minio.store_sec_filing(
                ticker=ticker,
                filing_type=metadata.get("form_type", "unknown"),
                accession_number=metadata.get("accession_number", ""),
                content=content,
                metadata=metadata,
            )
        elif source == "news":
            return self.minio.store_news_article(
                ticker=ticker,
                url=url,
                content=content,
                metadata=metadata,
            )
        elif source == "web":
            return self.minio.store_web_content(
                ticker=ticker,
                url=url,
                content=content,
                metadata=metadata,
            )
        elif source == "social":
            return self.minio.store_social_post(
                platform=metadata.get("platform", "unknown"),
                ticker=ticker,
                post_id=metadata.get("post_id", ""),
                content={**metadata, "content": content},
            )
        else:
            # Generic storage
            object_name = f"generic/{source}/{ticker}/{self._generate_doc_id(source, content, ticker)}.txt"
            return self.minio.put_object("raw_docs", object_name, content)

    def _store_to_warm_tier(
        self,
        ticker: str,
        chunks: list[dict[str, Any]],
        filing_metadata: Optional[dict[str, Any]] = None,
    ) -> int:
        """
        Store structured data in PostgreSQL.

        Args:
            ticker: Stock ticker symbol
            chunks: List of chunk dicts with text and metadata
            filing_metadata: Optional filing-level metadata

        Returns:
            Number of chunks inserted
        """
        if not chunks:
            return 0

        # Convert chunks to database format
        db_chunks = []
        for chunk in chunks:
            # Generate embedding for this chunk
            embedding_result = self.embeddings.embed([chunk["text"]])
            embedding = embedding_result[0] if embedding_result else None

            db_chunks.append({
                "id": chunk["id"],
                "filing_id": chunk.get("filing_id"),
                "chunk_index": chunk.get("chunk_index", 0),
                "text": chunk["text"],
                "section": chunk.get("section", ""),
                "embedding": embedding,
            })

        return self.postgres.insert_chunks(db_chunks)

    def _store_to_search_index(
        self,
        ticker: str,
        chunks: list[dict[str, Any]],
    ) -> list[str]:
        """
        Store chunks in txtai EmbeddingsIndex for semantic search.

        Args:
            ticker: Stock ticker symbol
            chunks: List of chunk dicts

        Returns:
            List of indexed document IDs
        """
        source = self._get_source_tag()

        # Transform to txtai format
        documents = []
        for chunk in chunks:
            documents.append({
                "id": chunk["id"],
                "text": chunk["text"],
                "tags": source,
                "metadata": {
                    "ticker": ticker,
                    "source": source,
                    **chunk.get("metadata", {}),
                },
            })

        return self.embeddings.upsert(documents)

    def _cache_results(
        self,
        ticker: str,
        query_key: str,
        results: Any,
        ttl: int = 3600,
    ) -> bool:
        """
        Cache fetch results in KeyDB.

        Args:
            ticker: Stock ticker symbol
            query_key: Cache key for the query
            results: Results to cache
            ttl: Time-to-live in seconds

        Returns:
            True if cached successfully
        """
        cache_key = f"fetch:{self._get_source_tag()}:{ticker}:{query_key}"
        return self.cache.set(cache_key, results, ttl=ttl)

    def _get_cached_results(
        self,
        ticker: str,
        query_key: str,
    ) -> Optional[Any]:
        """
        Get cached fetch results from KeyDB.

        Args:
            ticker: Stock ticker symbol
            query_key: Cache key for the query

        Returns:
            Cached results or None
        """
        cache_key = f"fetch:{self._get_source_tag()}:{ticker}:{query_key}"
        return self.cache.get(cache_key)

    @abstractmethod
    def _fetch_data(self, ticker: str, **kwargs) -> list[dict[str, Any]]:
        """
        Fetch raw data from the source.

        Args:
            ticker: Stock ticker symbol
            **kwargs: Source-specific parameters

        Returns:
            List of documents with 'text' and 'metadata' keys
        """
        pass

    @abstractmethod
    def _get_source_tag(self) -> str:
        """Return the source identifier (e.g., 'sec', 'news', 'web', 'social')."""
        pass

    def collect(
        self,
        ticker: str,
        store_cold: bool = True,
        store_warm: bool = True,
        store_search: bool = True,
        use_cache: bool = False,
        **kwargs,
    ) -> dict[str, int]:
        """
        Run the full collection pipeline.

        This is the main entry point that:
        1. Fetches data from the source
        2. Stores raw documents in cold tier (MinIO)
        3. Stores structured data in warm tier (PostgreSQL)
        4. Generates embeddings and stores in search index
        5. Caches results in hot tier (KeyDB)

        Args:
            ticker: Stock ticker symbol
            store_cold: Whether to store in cold tier (default: True)
            store_warm: Whether to store in warm tier (default: True)
            store_search: Whether to store in search index (default: True)
            use_cache: Whether to use cached results (default: False)
            **kwargs: Source-specific parameters

        Returns:
            Dict with counts: {'fetched', 'stored_cold', 'stored_warm', 'indexed'}
        """
        _LOG.info("Starting collection for %s ticker=%s", self._get_source_tag(), ticker)

        results = {
            "fetched": 0,
            "stored_cold": 0,
            "stored_warm": 0,
            "indexed": 0,
        }

        # Check cache first
        if use_cache:
            cache_key = str(sorted(kwargs.items()))
            cached = self._get_cached_results(ticker, cache_key)
            if cached:
                _LOG.info("Using cached results for %s", self._get_source_tag())
                raw_docs = cached
            else:
                raw_docs = self._fetch_data(ticker, **kwargs)
                self._cache_results(ticker, cache_key, raw_docs)
        else:
            raw_docs = self._fetch_data(ticker, **kwargs)

        results["fetched"] = len(raw_docs)
        _LOG.info("Fetched %d documents from %s", len(raw_docs), self._get_source_tag())

        # Prepare chunks for all documents
        all_chunks = []
        for doc in raw_docs:
            text = doc.get("text", "")
            if not text or len(text) < 10:
                continue

            # Chunk the document
            chunks = self._chunk_text(text)

            for i, chunk in enumerate(chunks):
                chunk_data = {
                    "id": self._generate_doc_id(self._get_source_tag(), chunk, ticker),
                    "text": chunk,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "metadata": {
                        **doc.get("metadata", {}),
                        "source": self._get_source_tag(),
                        "ticker": ticker,
                    },
                }
                all_chunks.append(chunk_data)

            # Store raw document in cold tier
            if store_cold:
                object_path = self._store_to_cold_tier(ticker, text, doc.get("metadata", {}))
                if object_path:
                    results["stored_cold"] += 1

        # Store chunks in warm tier (PostgreSQL)
        if store_warm and all_chunks:
            inserted = self._store_to_warm_tier(ticker, all_chunks)
            results["stored_warm"] = inserted

        # Store in search index
        if store_search and all_chunks:
            indexed_ids = self._store_to_search_index(ticker, all_chunks)
            results["indexed"] = len(indexed_ids)

        # Save embeddings to disk
        if store_search:
            self.embeddings.save()

        _LOG.info(
            "Collection complete for %s: fetched=%d, cold=%d, warm=%d, indexed=%d",
            self._get_source_tag(),
            results["fetched"],
            results["stored_cold"],
            results["stored_warm"],
            results["indexed"],
        )

        return results
