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

from txtai import Textractor

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

    MAX_TOKENS_PER_CHUNK = 512
    chunker: Optional[Textractor] = None

    def __init__(self):
        self.minio: MinIOClient = get_minio_client()
        self.postgres: PostgresClient = get_postgres_client()
        self.cache: CacheManager = get_cache_manager()
        self.embeddings = get_embeddings()

    def _get_chunker(self) -> Textractor:
        if self.chunker is None:
            self.chunker = Textractor(sentences=True)
        return self.chunker

    def _generate_doc_id(self, source: str, content: str, ticker: str) -> str:
        key = f"{source}:{ticker}:{content[:500]}"
        return hashlib.sha256(key.encode()).hexdigest()[:32]

    def _generate_filing_id(self, ticker: str, accession: str, form_type: str) -> str:
        """Deterministic filing ID from accession number."""
        key = f"{ticker}:{accession}:{form_type}"
        return hashlib.sha256(key.encode()).hexdigest()[:32]

    def _chunk_text(self, text: str) -> list[str]:
        chunker = self._get_chunker()
        chunks = chunker(text)
        result = []
        current_chunk = ""
        chunk_chars = self.MAX_TOKENS_PER_CHUNK * 4

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
                ticker=ticker, url=url, content=content, metadata=metadata,
            )
        else:
            object_name = f"generic/{source}/{ticker}/{self._generate_doc_id(source, content, ticker)}.txt"
            return self.minio.put_object("raw_docs", object_name, content)

    def _build_filing_row(
        self,
        ticker: str,
        filing_id: str,
        metadata: dict[str, Any],
        file_size: int,
    ) -> dict[str, Any]:
        """
        Map sec_collector metadata keys → filings table columns.

        sec_collector returns:
            form_type, filing_date, report_date, accession_number,
            cik, url, company_name, description
        """
        def parse_date(val: Any) -> Optional[str]:
            """Return ISO date string or None."""
            if not val:
                return None
            if isinstance(val, str) and len(val) >= 10:
                return val[:10]
            return None

        return {
            "id":               filing_id,
            "ticker":           ticker,
            "company_name":     metadata.get("company_name", ""),
            # sec_collector uses "form_type"; filings table calls it "filing_type"
            "filing_type":      metadata.get("form_type", "unknown"),
            "cik":              metadata.get("cik", ""),
            "accession_number": metadata.get("accession_number", ""),
            "filing_date":      parse_date(metadata.get("filing_date")),
            # sec_collector uses "report_date"; filings table calls it "period_of_report"
            "period_of_report": parse_date(metadata.get("report_date")),
            "document_url":     metadata.get("url", ""),
            "file_size_bytes":  file_size,
        }

    def _store_to_warm_tier(
        self,
        ticker: str,
        chunks: list[dict[str, Any]],
        filing_metadata: Optional[dict[str, Any]] = None,
    ) -> int:
        """
        Store structured data in PostgreSQL in the correct order:
          1. INSERT INTO filings       (one row per document)
          2. INSERT INTO chunks        (many rows, FK → filings.id)
          3. INSERT INTO document_metadata (key/value pairs, FK → chunks.id)

        Previously this method only called insert_chunks(), skipping filings
        and document_metadata entirely, leaving filing_id = NULL on all chunks.
        """
        if not chunks:
            return 0

        # ── 1. Insert filing row (once per unique filing_id) ──────────────────
        seen_filing_ids: set[str] = set()
        filing_rows: list[dict[str, Any]] = []

        for chunk in chunks:
            fid = chunk.get("filing_id")
            if fid and fid not in seen_filing_ids:
                seen_filing_ids.add(fid)
                filing_rows.append(chunk["filing_row"])

        if filing_rows:
            try:
                self.postgres.insert_filings(filing_rows)
                _LOG.info("Inserted %d filing rows", len(filing_rows))
            except Exception as e:
                _LOG.error("Failed to insert filings: %s", e)
                # Don't continue — chunks FK-depend on filings existing
                return 0

        # ── 2. Insert chunks with embeddings ──────────────────────────────────
        db_chunks = []
        for chunk in chunks:
            try:
                embedding_result = self.embeddings.batchtransform([chunk["text"]])
                embedding = (
                    embedding_result[0].tolist()
                    if embedding_result is not None and len(embedding_result) > 0
                    else None
                )
            except Exception as e:
                _LOG.warning("Embedding failed for chunk %s: %s", chunk["id"], e)
                embedding = None

            db_chunks.append({
                "id":          chunk["id"],
                "filing_id":   chunk.get("filing_id"),   # FK → filings.id ✓
                "chunk_index": chunk.get("chunk_index", 0),
                "text":        chunk["text"],
                "section":     chunk.get("section", ""),
                "embedding":   embedding,
            })

        try:
            inserted = self.postgres.insert_chunks(db_chunks)
            _LOG.info("Inserted %d chunks", inserted)
        except Exception as e:
            _LOG.error("Failed to insert chunks: %s", e)
            return 0

        # ── 3. Insert document_metadata (key/value pairs per chunk) ───────────
        metadata_rows = []
        for chunk in chunks:
            chunk_meta = chunk.get("metadata", {})
            chunk_id   = chunk["id"]
            for key, value in chunk_meta.items():
                if value is None:
                    continue
                metadata_rows.append({
                    "id":       self._generate_doc_id("meta", f"{chunk_id}:{key}", ticker),
                    "chunk_id": chunk_id,
                    "key":      key,
                    "value":    str(value),
                })

        if metadata_rows:
            try:
                self.postgres.insert_document_metadata(metadata_rows)
                _LOG.info("Inserted %d document_metadata rows", len(metadata_rows))
            except Exception as e:
                # Non-fatal — metadata is supplementary
                _LOG.warning("Failed to insert document_metadata: %s", e)

        return inserted

    def _store_to_search_index(
        self,
        ticker: str,
        chunks: list[dict[str, Any]],
    ) -> list[str]:
        source = self._get_source_tag()
        documents = []
        for chunk in chunks:
            documents.append({
                "id":   chunk["id"],
                "text": chunk["text"],
                "tags": source,
                "metadata": {
                    "ticker": ticker,
                    "source": source,
                    **chunk.get("metadata", {}),
                },
            })
        return self.embeddings.upsert(documents)

    def _cache_results(self, ticker, query_key, results, ttl=3600):
        cache_key = f"fetch:{self._get_source_tag()}:{ticker}:{query_key}"
        return self.cache.set(cache_key, results, ttl=ttl)

    def _get_cached_results(self, ticker, query_key):
        cache_key = f"fetch:{self._get_source_tag()}:{ticker}:{query_key}"
        return self.cache.get(cache_key)

    @abstractmethod
    def _fetch_data(self, ticker: str, **kwargs) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def _get_source_tag(self) -> str:
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

        _LOG.info("Starting collection for %s ticker=%s", self._get_source_tag(), ticker)

        results = {"fetched": 0, "stored_cold": 0, "stored_warm": 0, "indexed": 0}

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
        _LOG.info("Fetched %d documents", len(raw_docs))

        all_chunks = []

        for doc in raw_docs:
            text = doc.get("text", "")
            if not text or len(text) < 10:
                continue

            metadata   = doc.get("metadata", {})
            source     = self._get_source_tag()

            # ── Generate a stable filing_id for this document ────────────────
            filing_id = self._generate_filing_id(
                ticker,
                metadata.get("accession_number", text[:100]),
                metadata.get("form_type", source),
            )

            # ── Build the filings table row for this document ────────────────
            filing_row = self._build_filing_row(
                ticker=ticker,
                filing_id=filing_id,
                metadata=metadata,
                file_size=len(text.encode("utf-8")),
            )

            # ── Cold storage ─────────────────────────────────────────────────
            if store_cold:
                object_path = self._store_to_cold_tier(ticker, text, metadata)
                if object_path:
                    results["stored_cold"] += 1

            # ── Chunk the document ───────────────────────────────────────────
            chunks = self._chunk_text(text)
            for i, chunk_text in enumerate(chunks):
                all_chunks.append({
                    "id":          self._generate_doc_id(source, chunk_text, ticker),
                    "filing_id":   filing_id,    # ← FK to filings.id now set ✓
                    "filing_row":  filing_row,   # ← carried for warm tier insert
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "text":        chunk_text,
                    "section":     "",
                    "metadata": {
                        **metadata,
                        "source": source,
                        "ticker": ticker,
                    },
                })

        # ── Warm tier (filings → chunks → document_metadata) ─────────────────
        if store_warm and all_chunks:
            inserted = self._store_to_warm_tier(ticker, all_chunks)
            results["stored_warm"] = inserted

        # ── Search index ──────────────────────────────────────────────────────
        if store_search and all_chunks:
            indexed_ids = self._store_to_search_index(ticker, all_chunks)
            results["indexed"] = len(indexed_ids) if indexed_ids else 0

        if store_search:
            from app.pipeline.embeddings import get_data_dir
            db_path = get_data_dir() / "index.db"
            self.embeddings.save(str(db_path))

        _LOG.info(
            "Collection complete: fetched=%d cold=%d warm=%d indexed=%d",
            results["fetched"], results["stored_cold"],
            results["stored_warm"], results["indexed"],
        )
        return results