#!/usr/bin/env python3
"""
Test script for warm storage (PostgreSQL + pgvector).

Usage:
    python -m app.storage.warm_storage.test_connection

This script:
1. Tests connection to PostgreSQL
2. Verifies pgvector extension is enabled
3. Shows storage statistics
4. Demonstrates basic operations
"""

import logging
import sys
from datetime import datetime

from app.storage.warm_storage import (
    get_postgres_client,
    get_filings_manager,
    FilingData,
    ChunkData,
    generate_filing_id,
    generate_chunk_id,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
_LOG = logging.getLogger(__name__)


def test_connection() -> bool:
    """Test PostgreSQL connection."""
    _LOG.info("Testing PostgreSQL connection...")
    client = get_postgres_client()

    if client.ping():
        _LOG.info("✓ Connected to PostgreSQL at %s:%d/%s",
                  client.host, client.port, client.database)
        return True
    else:
        _LOG.error("✗ Failed to connect to PostgreSQL")
        return False


def test_pgvector_extension() -> bool:
    """Verify pgvector extension is enabled."""
    _LOG.info("Checking pgvector extension...")
    client = get_postgres_client()

    try:
        with client.get_cursor() as cur:
            cur.execute("""
                SELECT extname FROM pg_extension
                WHERE extname = 'vector'
            """)
            result = cur.fetchone()
            if result:
                _LOG.info("✓ pgvector extension is enabled")
                return True
            else:
                _LOG.error("✗ pgvector extension not found")
                return False
    except Exception as e:
        _LOG.error("✗ Error checking pgvector: %s", e)
        return False


def test_storage_stats() -> None:
    """Display storage statistics."""
    _LOG.info("Fetching storage statistics...")
    manager = get_filings_manager()
    stats = manager.get_stats()

    _LOG.info("=" * 50)
    _LOG.info("Storage Statistics:")
    _LOG.info("  - Filings:      %d", stats.get("filings", 0))
    _LOG.info("  - Chunks:       %d", stats.get("chunks", 0))
    _LOG.info("  - XBRL Facts:   %d", stats.get("xbrl_facts", 0))
    _LOG.info("  - Unique Tickers: %d", stats.get("unique_tickers", 0))
    _LOG.info("  - Summary: %s", stats.get("summary", "N/A"))
    _LOG.info("=" * 50)


def demo_store_filing() -> None:
    """Demonstrate storing a filing with chunks."""
    _LOG.info("Demonstrating filing storage...")

    manager = get_filings_manager()

    # Create a sample filing
    filing_id = generate_filing_id(
        ticker="TEST",
        filing_type="10-K",
        filing_date=datetime(2024, 12, 31),
        accession_number="0000000000-24-000001",
    )

    filing = FilingData(
        id=filing_id,
        ticker="TEST",
        company_name="Test Company Inc.",
        filing_type="10-K",
        cik="0000000000",
        accession_number="0000000000-24-000001",
        filing_date=datetime(2024, 12, 31),
        period_of_report=datetime(2024, 12, 31),
        document_url="https://example.com/filing",
    )

    # Store filing
    if manager.store_filing(filing):
        _LOG.info("✓ Stored filing: %s", filing_id)

        # Create sample chunks with dummy embeddings
        dummy_embedding = [0.01 * i for i in range(768)]
        chunks = [
            ChunkData(
                id=generate_chunk_id(filing_id, 0),
                filing_id=filing_id,
                chunk_index=0,
                text="Test Company reported strong revenue growth in Q4 2024.",
                section="MD&A",
                embedding=dummy_embedding,
            ),
            ChunkData(
                id=generate_chunk_id(filing_id, 1),
                filing_id=filing_id,
                chunk_index=1,
                text="Net income increased by 15% year-over-year to $1.2 billion.",
                section="Financial Statements",
                embedding=dummy_embedding,
            ),
        ]

        count = manager.store_chunks(chunks)
        _LOG.info("✓ Stored %d chunks", count)

        # Retrieve and verify
        retrieved = manager.get_filing(filing_id)
        if retrieved:
            _LOG.info("✓ Retrieved filing: %s - %s",
                      retrieved.ticker, retrieved.filing_type)

        # Get chunks
        chunk_list = manager.get_chunks_for_filing(filing_id)
        _LOG.info("✓ Retrieved %d chunks for filing", len(chunk_list))

        # Cleanup demo data
        manager.delete_filing(filing_id)
        _LOG.info("✓ Cleaned up demo filing")
    else:
        _LOG.error("✗ Failed to store demo filing")


def main() -> int:
    """Run all tests."""
    _LOG.info("=" * 60)
    _LOG.info("Warm Storage Test Suite (PostgreSQL + pgvector)")
    _LOG.info("=" * 60)

    # Test connection
    if not test_connection():
        _LOG.error("Connection test failed - exiting")
        return 1

    # Test pgvector extension
    if not test_pgvector_extension():
        _LOG.error("pgvector test failed - exiting")
        return 1

    # Show stats
    test_storage_stats()

    # Demo operations
    demo_store_filing()

    _LOG.info("=" * 60)
    _LOG.info("All warm storage tests completed successfully!")
    _LOG.info("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
