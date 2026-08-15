"""
High-level manager for SEC filings, chunks, and XBRL facts.

Provides typed methods for:
- Storing and retrieving SEC filings (10-K, 10-Q, 8-K, DEF 14A)
- Managing document chunks with vector embeddings
- Storing and querying XBRL facts
- Semantic search across filing content

This is the warm tier storage - data persists beyond the hot KeyDB cache.
"""

import hashlib
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

import psycopg2
from dotenv import load_dotenv

from app.storage.warm_storage.pgvector_client import PostgresClient, get_postgres_client

load_dotenv()

_LOG = logging.getLogger(__name__)


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class FilingData:
    """SEC filing metadata."""

    id: str
    ticker: str
    company_name: str
    filing_type: str  # 10-K, 10-Q, 8-K, DEF 14A
    cik: str
    accession_number: str
    filing_date: datetime
    period_of_report: Optional[datetime] = None
    document_url: Optional[str] = None
    file_size_bytes: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for database insertion."""
        return {
            "id": self.id,
            "ticker": self.ticker,
            "company_name": self.company_name,
            "filing_type": self.filing_type,
            "cik": self.cik,
            "accession_number": self.accession_number,
            "filing_date": self.filing_date.date() if self.filing_date else None,
            "period_of_report": self.period_of_report.date()
            if self.period_of_report
            else None,
            "document_url": self.document_url,
            "file_size_bytes": self.file_size_bytes,
        }


@dataclass
class ChunkData:
    """Document chunk with embedding."""

    id: str
    filing_id: str
    chunk_index: int
    text: str
    section: Optional[str] = None
    embedding: Optional[List[float]] = None
    token_count: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for database insertion."""
        return {
            "id": self.id,
            "filing_id": self.filing_id,
            "chunk_index": self.chunk_index,
            "text": self.text,
            "section": self.section,
            "embedding": self.embedding,
            "token_count": self.token_count,
        }


@dataclass
class XBRLFact:
    """XBRL fact from SEC filing."""

    id: str
    filing_id: str
    concept_name: str
    value: str
    value_numeric: Optional[float] = None
    unit: Optional[str] = None
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    instant_date: Optional[datetime] = None
    axis: Optional[str] = None
    member: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for database insertion."""
        return {
            "id": self.id,
            "filing_id": self.filing_id,
            "concept_name": self.concept_name,
            "value": self.value,
            "value_numeric": self.value_numeric,
            "unit": self.unit,
            "period_start": self.period_start.date() if self.period_start else None,
            "period_end": self.period_end.date() if self.period_end else None,
            "instant_date": self.instant_date.date() if self.instant_date else None,
            "axis": self.axis,
            "member": self.member,
        }


@dataclass
class SearchResults:
    """Semantic search results."""

    chunk_id: str
    filing_id: str
    text: str
    section: Optional[str]
    similarity: float
    ticker: str
    filing_type: str
    filing_date: datetime
    company_name: Optional[str]

    @classmethod
    def from_db(cls, row: Dict[str, Any]) -> "SearchResults":
        """Create from database row."""
        return cls(
            chunk_id=row["chunk_id"],
            filing_id=row["filing_id"],
            text=row["text"],
            section=row.get("section"),
            similarity=row["similarity"],
            ticker=row["ticker"],
            filing_type=row["filing_type"],
            filing_date=row["filing_date"],
            company_name=row.get("company_name"),
        )


# =============================================================================
# FilingsManager
# =============================================================================


class FilingsManager:
    """
    High-level manager for warm tier storage operations.

    Provides typed methods for storing and retrieving:
    - SEC filings metadata
    - Document chunks with embeddings
    - XBRL facts
    - Semantic search results
    """

    def __init__(self, client: Optional[PostgresClient] = None):
        """
        Initialize filings manager.

        Args:
            client: PostgreSQL client (uses singleton if not provided)
        """
        self.client = client or get_postgres_client()

    # -------------------------------------------------------------------------
    # Filing Operations
    # -------------------------------------------------------------------------

    def store_filing(self, filing: FilingData) -> bool:
        """
        Store an SEC filing in the database.

        Args:
            filing: Filing data object

        Returns:
            True if successful
        """
        filing_id = self.client.insert_filing(filing.to_dict())
        if filing_id:
            _LOG.info("Stored filing %s for %s", filing_id, filing.ticker)
            return True
        return False

    def get_filing(self, filing_id: str) -> Optional[FilingData]:
        """
        Retrieve a filing by ID.

        Args:
            filing_id: Filing identifier

        Returns:
            FilingData if found, None otherwise
        """
        data = self.client.get_filing(filing_id)
        if not data:
            return None

        return FilingData(
            id=data["id"],
            ticker=data["ticker"],
            company_name=data.get("company_name"),
            filing_type=data["filing_type"],
            cik=data.get("cik"),
            accession_number=data.get("accession_number"),
            filing_date=data["filing_date"],
            period_of_report=data.get("period_of_report"),
            document_url=data.get("document_url"),
            file_size_bytes=data.get("file_size_bytes"),
        )

    def get_filings_for_ticker(
        self,
        ticker: str,
        filing_types: Optional[List[str]] = None,
        limit: int = 10,
    ) -> List[FilingData]:
        """
        Get filings for a specific ticker.

        Args:
            ticker: Stock ticker symbol
            filing_types: Optional list of filing types to filter
            limit: Maximum results to return

        Returns:
            List of FilingData objects
        """
        filings = self.client.get_filings_by_ticker(ticker, filing_types, limit)
        result = []

        for f in filings:
            result.append(
                FilingData(
                    id=f["id"],
                    ticker=f["ticker"],
                    company_name=f.get("company_name"),
                    filing_type=f["filing_type"],
                    cik=f.get("cik"),
                    accession_number=f.get("accession_number"),
                    filing_date=f["filing_date"],
                    period_of_report=f.get("period_of_report"),
                    document_url=f.get("document_url"),
                    file_size_bytes=f.get("file_size_bytes"),
                )
            )

        return result

    def delete_filing(self, filing_id: str) -> bool:
        """
        Delete a filing and all associated chunks/facts.

        Args:
            filing_id: Filing to delete

        Returns:
            True if successful
        """
        return self.client.delete_filing(filing_id)

    # -------------------------------------------------------------------------
    # Chunk Operations
    # -------------------------------------------------------------------------

    def store_chunks(self, chunks: List[ChunkData]) -> int:
        """
        Store document chunks with embeddings.

        Args:
            chunks: List of chunk data objects

        Returns:
            Number of chunks stored
        """
        chunk_dicts = [c.to_dict() for c in chunks]
        count = self.client.insert_chunks(chunk_dicts)
        _LOG.info("Stored %d chunks", count)
        return count

    def get_chunks_for_filing(
        self,
        filing_id: str,
        include_embedding: bool = False,
    ) -> List[ChunkData]:
        """
        Get all chunks for a filing.

        Args:
            filing_id: Filing identifier
            include_embedding: Whether to include embedding vectors

        Returns:
            List of ChunkData objects
        """
        chunks = self.client.get_chunks_by_filing(filing_id, include_embedding)
        result = []

        for c in chunks:
            result.append(
                ChunkData(
                    id=c["id"],
                    filing_id=c["filing_id"],
                    chunk_index=c["chunk_index"],
                    text=c["text"],
                    section=c.get("section"),
                    embedding=c.get("embedding"),
                    token_count=c.get("token_count"),
                )
            )

        return result

    # -------------------------------------------------------------------------
    # XBRL Facts Operations
    # -------------------------------------------------------------------------

    def store_xbrl_facts(self, facts: List[XBRLFact]) -> int:
        """
        Store XBRL facts from a filing.

        Args:
            facts: List of XBRL fact objects

        Returns:
            Number of facts stored
        """
        fact_dicts = [f.to_dict() for f in facts]
        count = self.client.insert_xbrl_facts(fact_dicts)
        _LOG.info("Stored %d XBRL facts", count)
        return count

    def get_xbrl_facts(
        self,
        filing_id: str,
        concepts: Optional[List[str]] = None,
    ) -> List[XBRLFact]:
        """
        Get XBRL facts for a filing.

        Args:
            filing_id: Filing identifier
            concepts: Optional list of specific concepts to retrieve

        Returns:
            List of XBRLFact objects
        """
        if concepts:
            facts = self.client.get_xbrl_facts_by_concept(filing_id, concepts)
        else:
            # Get all facts for filing
            query = "SELECT * FROM xbrl_facts WHERE filing_id = %s"
            with self.client.get_cursor() as cur:
                cur.execute(query, [filing_id])
                facts = [dict(row) for row in cur.fetchall()]

        result = []
        for f in facts:
            result.append(
                XBRLFact(
                    id=f["id"],
                    filing_id=f["filing_id"],
                    concept_name=f["concept_name"],
                    value=f["value"],
                    value_numeric=f.get("value_numeric"),
                    unit=f.get("unit"),
                    period_start=f.get("period_start"),
                    period_end=f.get("period_end"),
                    instant_date=f.get("instant_date"),
                    axis=f.get("axis"),
                    member=f.get("member"),
                )
            )

        return result

    # -------------------------------------------------------------------------
    # Semantic Search
    # -------------------------------------------------------------------------

    def search_similar(
        self,
        query_embedding: List[float],
        ticker_filter: Optional[str] = None,
        limit: int = 10,
        threshold: float = 0.5,
    ) -> List[SearchResults]:
        """
        Search for similar chunks using vector embeddings.

        Args:
            query_embedding: Query vector (768 dimensions for nomic-embed-text)
            ticker_filter: Optional ticker to filter results
            limit: Maximum results to return
            threshold: Minimum similarity threshold (0-1)

        Returns:
            List of SearchResults objects
        """
        results = self.client.search_similar(
            query_embedding=query_embedding,
            table="chunks",
            limit=limit,
            threshold=threshold,
            ticker_filter=ticker_filter,
        )

        return [SearchResults.from_db(r) for r in results]

    def search_with_text(
        self,
        query_text: str,
        embeddings_model: Any,
        ticker_filter: Optional[str] = None,
        limit: int = 10,
        threshold: float = 0.5,
    ) -> List[SearchResults]:
        """
        Search using text query (embeds query then searches).

        Args:
            query_text: Text query string
            embeddings_model: Model to embed query (e.g., OllamaEmbedding)
            ticker_filter: Optional ticker to filter results
            limit: Maximum results to return
            threshold: Minimum similarity threshold

        Returns:
            List of SearchResults objects
        """
        # Embed the query
        query_embedding = embeddings_model.embed_query(query_text)

        # Search
        return self.search_similar(
            query_embedding=query_embedding,
            ticker_filter=ticker_filter,
            limit=limit,
            threshold=threshold,
        )

    # -------------------------------------------------------------------------
    # Statistics
    # -------------------------------------------------------------------------

    def get_stats(self) -> Dict[str, Any]:
        """
        Get storage statistics.

        Returns:
            Dict with counts and metadata
        """
        stats = self.client.get_stats()

        # Add human-readable summary
        stats["summary"] = (
            f"Filings: {stats.get('filings', 0)}, "
            f"Chunks: {stats.get('chunks', 0)}, "
            f"XBRL Facts: {stats.get('xbrl_facts', 0)}, "
            f"Tickers: {stats.get('unique_tickers', 0)}"
        )

        return stats

    def get_ticker_stats(self, ticker: str) -> Dict[str, Any]:
        """
        Get statistics for a specific ticker.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dict with ticker-specific stats
        """
        query = """
            SELECT
                COUNT(DISTINCT f.id) AS filing_count,
                COUNT(c.id) AS chunk_count,
                COUNT(xf.id) AS xbrl_fact_count,
                MIN(f.filing_date) AS earliest_filing,
                MAX(f.filing_date) AS latest_filing
            FROM filings f
            LEFT JOIN chunks c ON f.id = c.filing_id
            LEFT JOIN xbrl_facts xf ON f.id = xf.filing_id
            WHERE f.ticker = %s
        """

        try:
            with self.client.get_cursor() as cur:
                cur.execute(query, [ticker])
                result = cur.fetchone()
                if result:
                    return {
                        "ticker": ticker,
                        "filing_count": result["filing_count"],
                        "chunk_count": result["chunk_count"],
                        "xbrl_fact_count": result["xbrl_fact_count"],
                        "earliest_filing": result["earliest_filing"],
                        "latest_filing": result["latest_filing"],
                    }
        except psycopg2.Error as e:
            _LOG.error("Failed to get ticker stats: %s", e)

        return {"ticker": ticker, "error": "Failed to retrieve stats"}


# =============================================================================
# Helper Functions
# =============================================================================


def generate_filing_id(
    ticker: str,
    filing_type: str,
    filing_date: datetime,
    accession_number: str,
) -> str:
    """
    Generate a deterministic filing ID.

    Args:
        ticker: Stock ticker symbol
        filing_type: Type of filing (10-K, 8-K, etc.)
        filing_date: Filing date
        accession_number: SEC accession number

    Returns:
        Unique filing ID string
    """
    key = f"{ticker}:{filing_type}:{filing_date.isoformat()}:{accession_number}"
    return hashlib.sha256(key.encode()).hexdigest()[:32]


def generate_chunk_id(filing_id: str, chunk_index: int) -> str:
    """
    Generate a deterministic chunk ID.

    Args:
        filing_id: Parent filing ID
        chunk_index: Index of chunk in document

    Returns:
        Unique chunk ID string
    """
    key = f"{filing_id}:{chunk_index}"
    return hashlib.sha256(key.encode()).hexdigest()[:32]


def generate_xbrl_fact_id(
    filing_id: str, concept_name: str, period_end: datetime
) -> str:
    """
    Generate a deterministic XBRL fact ID.

    Args:
        filing_id: Parent filing ID
        concept_name: XBRL concept name
        period_end: Period end date

    Returns:
        Unique fact ID string
    """
    key = f"{filing_id}:{concept_name}:{period_end.isoformat()}"
    return hashlib.sha256(key.encode()).hexdigest()[:32]


# =============================================================================
# Singleton
# =============================================================================

_filings_manager: Optional[FilingsManager] = None


def get_filings_manager() -> FilingsManager:
    """
    Get the singleton FilingsManager instance.

    Returns:
        FilingsManager instance
    """
    global _filings_manager
    if _filings_manager is None:
        _filings_manager = FilingsManager()
        _LOG.info("FilingsManager initialized")
    return _filings_manager
