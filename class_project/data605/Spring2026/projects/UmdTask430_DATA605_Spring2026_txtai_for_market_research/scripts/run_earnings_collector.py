#!/usr/bin/env python3
"""
Earnings Call Transcript Collector Script.

Fetches earnings transcripts from Alpha Vantage and stores them across all
storage tiers.

Usage:
    python -m scripts.run_earnings_collector --ticker AAPL --quarters 4
    python -m scripts.run_earnings_collector -t MSFT --year 2024 --quarter 1

Environment Variables Required:
    - ALPHAVANTAGE_API_KEY: free tier supports EARNINGS_CALL_TRANSCRIPT (25/day)
    - POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
    - MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY
    - OPENAI_API_KEY or OLLAMA_HOST (one of, for embeddings)
"""

import argparse
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Add project root to path.
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.collectors import EarningsCollector

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
_LOG = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Earnings Call Transcript Collector for txtai Market Research"
    )
    parser.add_argument(
        "-t", "--ticker", type=str, default="AAPL", help="Stock ticker (default: AAPL)"
    )
    parser.add_argument(
        "-q",
        "--quarters",
        type=int,
        default=4,
        help="Number of trailing quarters to fetch (default: 4)",
    )
    parser.add_argument(
        "--year",
        type=int,
        default=None,
        help="Explicit fiscal year (use with --quarter)",
    )
    parser.add_argument(
        "--quarter",
        type=int,
        choices=[1, 2, 3, 4],
        default=None,
        help="Explicit fiscal quarter 1-4 (use with --year)",
    )
    parser.add_argument(
        "--no-cold", action="store_true", help="Skip cold storage (MinIO)"
    )
    parser.add_argument(
        "--no-warm", action="store_true", help="Skip warm storage (PostgreSQL)"
    )
    parser.add_argument(
        "--no-search", action="store_true", help="Skip search index (txtai)"
    )
    parser.add_argument(
        "--use-cache", action="store_true", help="Use cached results if available"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable debug logging"
    )
    return parser.parse_args()


def validate_environment() -> bool:
    """Validate required environment variables."""
    required = [
        "ALPHAVANTAGE_API_KEY",
        "POSTGRES_HOST",
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "MINIO_ENDPOINT",
        "MINIO_ACCESS_KEY",
        "MINIO_SECRET_KEY",
    ]
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    has_ollama = bool(os.getenv("OLLAMA_HOST"))
    missing = [v for v in required if not os.getenv(v)]
    if not has_openai and not has_ollama:
        missing.append("OPENAI_API_KEY or OLLAMA_HOST (need one for embeddings)")
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
    _LOG.info("Earnings Transcript Collector")
    _LOG.info("=" * 60)
    load_dotenv()
    if not validate_environment():
        return 1
    # year+quarter is all-or-nothing.
    if (args.year is None) ^ (args.quarter is None):
        _LOG.error("--year and --quarter must be provided together")
        return 1
    _LOG.info("Configuration:")
    _LOG.info("  Ticker:         %s", args.ticker)
    if args.year is not None:
        _LOG.info("  Quarter:        %sQ%s", args.year, args.quarter)
    else:
        _LOG.info("  Trailing Qs:    %d", args.quarters)
    _LOG.info("  Cold Storage:   %s", "disabled" if args.no_cold else "enabled")
    _LOG.info("  Warm Storage:   %s", "disabled" if args.no_warm else "enabled")
    _LOG.info("  Search Index:   %s", "disabled" if args.no_search else "enabled")
    _LOG.info("  Use Cache:      %s", "yes" if args.use_cache else "no")
    _LOG.info("=" * 60)
    collector = EarningsCollector()
    try:
        results = collector.collect(
            ticker=args.ticker,
            quarters=args.quarters,
            year=args.year,
            quarter=args.quarter,
            store_cold=not args.no_cold,
            store_warm=not args.no_warm,
            store_search=not args.no_search,
            use_cache=args.use_cache,
        )
        _LOG.info("=" * 60)
        _LOG.info("Collection Results:")
        _LOG.info("  Transcripts Fetched: %d", results.get("fetched", 0))
        _LOG.info("  Stored in Cold:      %d", results.get("stored_cold", 0))
        _LOG.info("  Stored in Warm:      %d", results.get("stored_warm", 0))
        _LOG.info("  Indexed for Search:  %d", results.get("indexed", 0))
        _LOG.info("=" * 60)
        if results.get("fetched", 0) == 0:
            _LOG.warning(
                "No transcripts were fetched. Possible causes: "
                "Alpha Vantage rate limit (25/day on free tier), no transcript "
                "available for the requested quarter, or invalid ticker."
            )
            return 0
        _LOG.info("Earnings collection completed successfully!")
        return 0
    except Exception as e:
        _LOG.exception("Collection failed: %s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
