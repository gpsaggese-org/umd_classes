#!/usr/bin/env python3
"""
SEC EDGAR Collector Script

Run the SEC collector to fetch and store filings for a given ticker.

Usage:
    python -m scripts.run_sec_collector --ticker AAPL --filing-types 10-K,8-K --limit 10
    python -m scripts.run_sec_collector -t TSLA -f 10-K -l 5

Environment Variables Required:
    - OPENAI_API_KEY: For embeddings
    - POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
    - MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY
    - KEYDB_HOST, KEYDB_PORT (or use defaults)
"""

import argparse
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.collectors import SECCollector

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
_LOG = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="SEC EDGAR Collector for txtai Market Research Platform"
    )
    parser.add_argument(
        "-t", "--ticker",
        type=str,
        default="AAPL",
        help="Stock ticker symbol (default: AAPL)"
    )
    parser.add_argument(
        "-f", "--filing-types",
        type=str,
        default="10-K,8-K,DEF 14A",
        help="Comma-separated filing types (default: 10-K,8-K,DEF 14A)"
    )
    parser.add_argument(
        "-l", "--limit",
        type=int,
        default=20,
        help="Maximum number of filings to fetch per type (default: 20)"
    )
    parser.add_argument(
        "--no-cold",
        action="store_true",
        help="Skip cold storage (MinIO)"
    )
    parser.add_argument(
        "--no-warm",
        action="store_true",
        help="Skip warm storage (PostgreSQL)"
    )
    parser.add_argument(
        "--no-search",
        action="store_true",
        help="Skip search index (txtai)"
    )
    parser.add_argument(
        "--use-cache",
        action="store_true",
        help="Use cached results if available"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable debug logging"
    )

    return parser.parse_args()


def validate_environment() -> bool:
    """Validate required environment variables."""
    required = [
        "OPENAI_API_KEY",
        "POSTGRES_HOST",
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "MINIO_ENDPOINT",
        "MINIO_ACCESS_KEY",
        "MINIO_SECRET_KEY",
    ]

    missing = []
    for var in required:
        if not os.getenv(var):
            missing.append(var)

    if missing:
        _LOG.error("Missing required environment variables: %s", ", ".join(missing))
        _LOG.info("Copy .env.example to .env and fill in the values")
        return False

    return True


def main() -> int:
    """Main entry point."""
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    _LOG.info("=" * 60)
    _LOG.info("SEC EDGAR Collector")
    _LOG.info("=" * 60)

    # Load environment variables
    load_dotenv()

    # Validate environment
    if not validate_environment():
        return 1

    # Parse filing types
    filing_types = [ft.strip() for ft in args.filing_types.split(",")]

    _LOG.info("Configuration:")
    _LOG.info("  Ticker:        %s", args.ticker)
    _LOG.info("  Filing Types:  %s", ", ".join(filing_types))
    _LOG.info("  Limit:         %d per type", args.limit)
    _LOG.info("  Cold Storage:  %s", "disabled" if args.no_cold else "enabled")
    _LOG.info("  Warm Storage:  %s", "disabled" if args.no_warm else "enabled")
    _LOG.info("  Search Index:  %s", "disabled" if args.no_search else "enabled")
    _LOG.info("  Use Cache:     %s", "yes" if args.use_cache else "no")
    _LOG.info("=" * 60)

    # Initialize collector
    _LOG.info("Initializing SEC collector...")
    collector = SECCollector()

    # Run collection
    _LOG.info("Starting collection for %s...", args.ticker)
    try:
        results = collector.collect(
            ticker=args.ticker,
            filing_types=filing_types,
            limit=args.limit,
            store_cold=not args.no_cold,
            store_warm=not args.no_warm,
            store_search=not args.no_search,
            use_cache=args.use_cache,
        )

        _LOG.info("=" * 60)
        _LOG.info("Collection Results:")
        _LOG.info("  Documents Fetched:   %d", results.get("fetched", 0))
        _LOG.info("  Stored in Cold:      %d", results.get("stored_cold", 0))
        _LOG.info("  Stored in Warm:      %d", results.get("stored_warm", 0))
        _LOG.info("  Indexed for Search:  %d", results.get("indexed", 0))
        _LOG.info("=" * 60)

        if results.get("fetched", 0) == 0:
            _LOG.warning("No filings were fetched. Check the SEC API or try a different ticker.")
            return 0

        _LOG.info("SEC collection completed successfully!")
        return 0

    except Exception as e:
        _LOG.exception("Collection failed: %s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
