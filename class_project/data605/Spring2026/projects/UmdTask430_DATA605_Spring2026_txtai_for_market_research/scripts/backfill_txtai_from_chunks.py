#!/usr/bin/env python3
"""
Backfill txtai search index from PostgreSQL chunks table.

The warm tier already contains ~14,863 SEC chunks (with text + filing
metadata). The txtai index is empty, which leaves all search-backed
agents starved. This script reads chunks in batches and indexes them
into txtai with source tag "sec" and per-doc metadata.

Re-embeds with sentence-transformers/all-mpnet-base-v2 on CPU; expect
roughly 10-30 minutes for the full 14k-chunk backfill.

Usage:
    python -m scripts.backfill_txtai_from_chunks
    python -m scripts.backfill_txtai_from_chunks --batch-size 500 --limit 1000
"""

import argparse
import logging
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.pipeline.embeddings import get_data_dir, get_embeddings, upsert
from app.storage import get_postgres_client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
_LOG = logging.getLogger(__name__)


_FETCH_QUERY = """
    SELECT
        c.id,
        c.text,
        c.section,
        f.ticker,
        f.filing_type,
        f.filing_date,
        f.accession_number
    FROM chunks c
    JOIN filings f ON c.filing_id = f.id
    WHERE c.text IS NOT NULL AND LENGTH(c.text) > 0
    ORDER BY c.id
    LIMIT %s OFFSET %s
"""

# SEC-issued form types — anything else collected via the news pipeline is
# tagged as "news" so the txtai source filter still works.
_SEC_FILING_TYPES = {
    "10-K",
    "10-K/A",
    "10-Q",
    "10-Q/A",
    "8-K",
    "8-K/A",
    "DEF 14A",
    "DEFA14A",
    "DEF 14C",
    "S-1",
    "S-3",
    "S-4",
    "S-8",
    "20-F",
    "20-F/A",
    "40-F",
    "6-K",
    "13F-HR",
    "13F-HR/A",
    "SC 13D",
    "SC 13D/A",
    "SC 13G",
    "SC 13G/A",
    "SD",
}


def _classify_source(filing_type: str) -> str:
    """Return the txtai source tag for a row's filing_type."""
    if filing_type in _SEC_FILING_TYPES:
        return "sec"
    return "news"


def _count_chunks(client) -> int:
    """Count chunks eligible for indexing."""
    with client.get_cursor() as cur:
        cur.execute(
            "SELECT COUNT(*) AS n FROM chunks "
            "WHERE text IS NOT NULL AND LENGTH(text) > 0"
        )
        return cur.fetchone()["n"]


def _fetch_batch(client, batch_size: int, offset: int) -> list[dict]:
    """Fetch one batch of chunks joined with filing metadata."""
    with client.get_cursor() as cur:
        cur.execute(_FETCH_QUERY, (batch_size, offset))
        rows = cur.fetchall()
    documents = []
    for row in rows:
        filing_date = row["filing_date"]
        filing_type = row["filing_type"] or ""
        source = _classify_source(filing_type)
        documents.append(
            {
                "id": row["id"],
                "text": row["text"],
                "tags": source,
                "metadata": {
                    "ticker": row["ticker"],
                    "filing_type": filing_type,
                    "filing_date": str(filing_date) if filing_date else None,
                    "section": row["section"],
                    "accession_number": row["accession_number"],
                    "source": source,
                },
            }
        )
    return documents


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Backfill txtai index from chunks table"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=500,
        help="Chunks per upsert call (default: 500)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Cap total chunks indexed (default: all)",
    )
    parser.add_argument(
        "--from-scratch",
        action="store_true",
        help="Delete existing txtai index files before backfilling",
    )
    return parser.parse_args()


def main() -> int:
    load_dotenv()
    args = _parse_args()
    if args.from_scratch:
        data_dir = get_data_dir()
        for f in data_dir.iterdir():
            if f.is_file():
                _LOG.info("Removing %s", f)
                f.unlink()
    pg_client = get_postgres_client()
    total_eligible = _count_chunks(pg_client)
    target = min(total_eligible, args.limit) if args.limit else total_eligible
    _LOG.info("Eligible chunks in warm tier: %d", total_eligible)
    _LOG.info("Will index: %d (batch=%d)", target, args.batch_size)
    # Warm up embeddings model so the first batch isn't artificially slow.
    embeddings = get_embeddings()
    _LOG.info("Embeddings model loaded")
    indexed = 0
    offset = 0
    started = time.time()
    while indexed < target:
        remaining = target - indexed
        this_batch = min(args.batch_size, remaining)
        batch = _fetch_batch(pg_client, this_batch, offset)
        if not batch:
            _LOG.info("No more rows at offset=%d", offset)
            break
        t0 = time.time()
        upsert(batch, save=False)
        indexed += len(batch)
        offset += len(batch)
        elapsed = time.time() - t0
        rate = len(batch) / elapsed if elapsed > 0 else 0
        eta_seconds = (target - indexed) / rate if rate > 0 else 0
        _LOG.info(
            "Indexed %d/%d (%.1f%%) batch_time=%.1fs rate=%.1f/s eta=%.0fs",
            indexed,
            target,
            100.0 * indexed / target,
            elapsed,
            rate,
            eta_seconds,
        )
    # Persist ANN index files once at the end.
    _LOG.info("Saving txtai index to %s", get_data_dir())
    embeddings.save(str(get_data_dir()))
    total_elapsed = time.time() - started
    _LOG.info(
        "Backfill complete: %d chunks in %.1fs (%.1f/s)",
        indexed,
        total_elapsed,
        indexed / total_elapsed if total_elapsed > 0 else 0,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
