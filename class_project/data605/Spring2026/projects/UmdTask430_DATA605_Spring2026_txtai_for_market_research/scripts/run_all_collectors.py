#!/usr/bin/env python3
"""
Comprehensive Market Research Data Collection Script

Runs collectors to gather data from:
- SEC EDGAR (10-K, 10-Q, 8-K, DEF 14A filings)
- News articles (NewsAPI, Alpha Vantage)

Usage:
    python -m scripts.run_all_collectors --tickers AAPL,MSFT,TSLA --sec-limit 500
    python -m scripts.run_all_collectors --sector tech --sec-limit 1000
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.collectors import SECCollector, NewsCollector

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
_LOG = logging.getLogger(__name__)

# Sector definitions
SECTORS = {
    "tech": ["AAPL", "MSFT", "GOOGL", "META", "NVDA", "ADBE", "CRM", "ORCL"],
    "finance": ["JPM", "BAC", "WFC", "GS", "MS", "C", "BLK", "V"],
    "healthcare": ["JNJ", "UNH", "PFE", "MRK", "ABBV", "TMO", "ABT", "LLY"],
    "consumer": ["AMZN", "WMT", "HD", "PG", "KO", "PEP", "COST", "MCD"],
    "ev": ["TSLA", "RIVN", "LCID", "NIO", "XPEV", "LI"],
}

# Default filing types for SEC collection
DEFAULT_FILING_TYPES = ["10-K", "10-Q", "8-K", "DEF 14A"]


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Comprehensive Market Research Data Collection"
    )

    # Ticker selection
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--tickers",
        type=str,
        default="AAPL",
        help="Comma-separated tickers (default: AAPL)"
    )
    group.add_argument(
        "--sector",
        type=str,
        choices=list(SECTORS.keys()),
        help="Collect all tickers from a sector"
    )

    # Collection limits
    parser.add_argument(
        "--sec-limit",
        type=int,
        default=500,
        help="Max SEC filings per ticker (default: 500)"
    )
    parser.add_argument(
        "--news-limit",
        type=int,
        default=50,
        help="Max news articles per ticker (default: 50)"
    )
    parser.add_argument(
        "--days-back",
        type=int,
        default=30,
        help="Days back for news (default: 30)"
    )

    # Selective collection
    parser.add_argument(
        "--sec-only",
        action="store_true",
        help="Only run SEC collector"
    )
    parser.add_argument(
        "--skip-sec",
        action="store_true",
        help="Skip SEC collector"
    )
    parser.add_argument(
        "--skip-news",
        action="store_true",
        help="Skip news collector"
    )

    # Storage options
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

    # Output
    parser.add_argument(
        "--output-stats",
        type=str,
        default="collection_stats.json",
        help="Output file for collection statistics"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable debug logging"
    )

    return parser.parse_args()


def get_ticker_list(args) -> list[str]:
    """Get list of tickers to collect."""
    if args.sector:
        return SECTORS[args.sector]
    if args.tickers:
        return [t.strip() for t in args.tickers.split(",")]
    return ["AAPL"]


def run_sec_collector(ticker: str, args) -> dict:
    """Run SEC EDGAR collector."""
    _LOG.info(f"  [{ticker}] SEC EDGAR: Fetching up to {args.sec_limit} filings...")

    collector = SECCollector()
    results = collector.collect(
        ticker=ticker,
        filing_types=DEFAULT_FILING_TYPES,
        limit=args.sec_limit,
        max_filings=args.sec_limit + 500,  # Fetch extra to account for filtering
        store_cold=not args.no_cold,
        store_warm=not args.no_warm,
        store_search=not args.no_search,
    )

    return {
        "source": "sec",
        "fetched": results.get("fetched", 0),
        "stored_cold": results.get("stored_cold", 0),
        "stored_warm": results.get("stored_warm", 0),
        "indexed": results.get("indexed", 0),
    }


def run_news_collector(ticker: str, args) -> dict:
    """Run News collector."""
    _LOG.info(f"  [{ticker}] News: Fetching up to {args.news_limit} articles...")

    collector = NewsCollector()
    results = collector.collect(
        ticker=ticker,
        days_back=args.days_back,
        limit=args.news_limit,
        store_cold=not args.no_cold,
        store_warm=not args.no_warm,
        store_search=not args.no_search,
    )

    return {
        "source": "news",
        "fetched": results.get("fetched", 0),
        "stored_cold": results.get("stored_cold", 0),
        "stored_warm": results.get("stored_warm", 0),
        "indexed": results.get("indexed", 0),
    }


def main() -> int:
    """Main entry point."""
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    load_dotenv()

    # Get ticker list
    tickers = get_ticker_list(args)

    _LOG.info("=" * 70)
    _LOG.info("COMPREHENSIVE MARKET RESEARCH DATA COLLECTION")
    _LOG.info("=" * 70)
    _LOG.info("Tickers: %d (%s)", len(tickers), ", ".join(tickers[:5]) + ("..." if len(tickers) > 5 else ""))
    _LOG.info("SEC Limit: %d filings/ticker", args.sec_limit)
    _LOG.info("News Limit: %d articles/ticker", args.news_limit)
    _LOG.info("Days Back: %d", args.days_back)
    _LOG.info("=" * 70)

    # Determine which collectors to run
    run_sec = not args.skip_sec or args.sec_only
    run_news = not args.skip_news and not args.sec_only

    if args.sec_only:
        _LOG.info("Running: SEC ONLY")
    else:
        collectors = []
        if run_sec: collectors.append("SEC")
        if run_news: collectors.append("News")
        _LOG.info("Running collectors: %s", ", ".join(collectors))

    _LOG.info("=" * 70)

    # Initialize collectors
    all_stats = {}
    start_time = time.time()

    for i, ticker in enumerate(tickers):
        _LOG.info("\n[%d/%d] Processing ticker: %s", i + 1, len(tickers), ticker)
        _LOG.info("-" * 50)

        ticker_stats = {}

        try:
            # SEC Collector
            if run_sec:
                stats = run_sec_collector(ticker, args)
                ticker_stats["sec"] = stats
                _LOG.info(f"  -> SEC: {stats['fetched']} fetched, {stats['stored_warm']} stored warm")

            # News Collector
            if run_news:
                stats = run_news_collector(ticker, args)
                ticker_stats["news"] = stats
                _LOG.info(f"  -> News: {stats['fetched']} fetched, {stats['stored_warm']} stored warm")

        except Exception as e:
            _LOG.error(f"Error collecting for {ticker}: {e}")
            ticker_stats["error"] = str(e)

        all_stats[ticker] = ticker_stats

        # Delay between tickers (rate limiting)
        if i < len(tickers) - 1:
            delay = 3.0  # seconds
            _LOG.info(f"  Waiting {delay}s before next ticker...")
            time.sleep(delay)

    # Calculate totals
    elapsed = time.time() - start_time

    _LOG.info("\n" + "=" * 70)
    _LOG.info("COLLECTION COMPLETE")
    _LOG.info("=" * 70)

    # Aggregate stats by source
    totals_by_source = {}
    for ticker, stats in all_stats.items():
        for source, source_stats in stats.items():
            if source == "error":
                continue
            if source not in totals_by_source:
                totals_by_source[source] = {"fetched": 0, "stored_warm": 0, "indexed": 0}
            for key in ["fetched", "stored_warm", "indexed"]:
                totals_by_source[source][key] += source_stats.get(key, 0)

    _LOG.info("\nTotals by Source:")
    grand_total = 0
    for source, totals in totals_by_source.items():
        _LOG.info(f"  {source.upper()}: {totals['fetched']} fetched, {totals['stored_warm']} stored warm, {totals['indexed']} indexed")
        grand_total += totals['fetched']

    _LOG.info(f"\nGrand Total: {grand_total} documents collected")
    _LOG.info(f"Total Time: {elapsed:.1f} seconds ({elapsed/60:.1f} minutes)")
    _LOG.info("=" * 70)

    # Save statistics
    output_data = {
        "timestamp": datetime.now().isoformat(),
        "tickers": tickers,
        "results": all_stats,
        "totals_by_source": totals_by_source,
        "grand_total": grand_total,
        "elapsed_seconds": elapsed,
    }

    with open(args.output_stats, "w") as f:
        json.dump(output_data, f, indent=2)
    _LOG.info(f"Statistics saved to {args.output_stats}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
