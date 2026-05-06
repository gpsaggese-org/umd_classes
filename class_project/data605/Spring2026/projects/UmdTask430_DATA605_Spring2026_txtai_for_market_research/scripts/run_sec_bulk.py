#!/usr/bin/env python3
"""
Bulk SEC EDGAR Collector

Scrape SEC filings for multiple companies with filtering options.

Usage:
    # Scrape predefined groups
    python -m scripts.run_sec_bulk --group faang
    python -m scripts.run_sec_bulk --group banks
    python -m scripts.run_sec_bulk --group all

    # Scrape a custom list of tickers
    python -m scripts.run_sec_bulk --tickers AAPL MSFT GOOGL AMZN

    # Filter by filing type and date range
    python -m scripts.run_sec_bulk --group faang --filing-types 10-K
    python -m scripts.run_sec_bulk --tickers TSLA --filing-types 10-K,8-K --after 2022-01-01
    python -m scripts.run_sec_bulk --tickers AAPL --filing-types 10-K --before 2023-12-31

    # Control concurrency and limits
    python -m scripts.run_sec_bulk --group faang --limit 5 --workers 3

    # Dry run — shows what would be scraped without storing
    python -m scripts.run_sec_bulk --group banks --dry-run

    # Skip already-scraped tickers (checks filings table first)
    python -m scripts.run_sec_bulk --group all --skip-existing

Environment Variables Required:
    POSTGRES_HOST, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
    MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY
    OPENAI_API_KEY or OLLAMA_HOST
"""

import argparse
import logging
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.collectors import SECCollector
from app.storage import get_postgres_client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
_LOG = logging.getLogger(__name__)

# ── Predefined ticker groups ──────────────────────────────────────────────────

TICKER_GROUPS = {
    "faang": ["META", "AAPL", "AMZN", "NFLX", "GOOGL"],

    "big_tech": ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "ORCL", "IBM", "INTC"],

    "banks": ["JPM", "BAC", "WFC", "GS", "MS", "C", "USB", "PNC", "TFC", "COF"],

    "healthcare": ["JNJ", "UNH", "PFE", "ABBV", "MRK", "TMO", "ABT", "DHR", "BMY", "AMGN"],

    "energy": ["XOM", "CVX", "COP", "EOG", "SLB", "MPC", "PSX", "VLO", "OXY", "HAL"],

    "retail": ["WMT", "AMZN", "COST", "TGT", "HD", "LOW", "TJX", "ROST", "DG", "DLTR"],

    "ev": ["TSLA", "RIVN", "LCID", "NIO", "XPEV", "F", "GM", "STLA"],

    "semiconductors": ["NVDA", "AMD", "INTC", "QCOM", "AVGO", "TXN", "MU", "AMAT", "KLAC", "LRCX"],

    "sp500_sample": [
        "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "META", "BRK-B", "LLY",
        "AVGO", "JPM", "TSLA", "UNH", "XOM", "V", "MA", "JNJ", "PG", "HD",
        "COST", "MRK",
    ],

    # All groups combined (deduplicated)
    "all": [],
}

# Populate "all" from all other groups
_all_tickers: list[str] = []
for _group, _tickers in TICKER_GROUPS.items():
    if _group != "all":
        _all_tickers.extend(_tickers)
TICKER_GROUPS["all"] = list(dict.fromkeys(_all_tickers))  # preserve order, dedupe


# ── Argument parsing ──────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bulk SEC EDGAR collector — scrape multiple companies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # ── Ticker selection
    ticker_group = parser.add_mutually_exclusive_group(required=True)
    ticker_group.add_argument(
        "--tickers", "-t",
        nargs="+",
        metavar="TICKER",
        help="One or more ticker symbols  e.g. AAPL MSFT GOOGL",
    )
    ticker_group.add_argument(
        "--group", "-g",
        choices=list(TICKER_GROUPS.keys()),
        help=f"Predefined group. Available: {', '.join(TICKER_GROUPS.keys())}",
    )

    # ── Filing filters
    parser.add_argument(
        "--filing-types", "-f",
        type=str,
        default="10-K,8-K,DEF 14A",
        help="Comma-separated filing types (default: 10-K,8-K,DEF 14A)",
    )
    parser.add_argument(
        "--after",
        type=str,
        default=None,
        metavar="YYYY-MM-DD",
        help="Only fetch filings on or after this date",
    )
    parser.add_argument(
        "--before",
        type=str,
        default=None,
        metavar="YYYY-MM-DD",
        help="Only fetch filings on or before this date",
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=10,
        help="Max filings per ticker per type (default: 10)",
    )

    # ── Storage flags
    parser.add_argument("--no-cold",   action="store_true", help="Skip MinIO cold storage")
    parser.add_argument("--no-warm",   action="store_true", help="Skip PostgreSQL warm storage")
    parser.add_argument("--no-search", action="store_true", help="Skip txtai search index")

    # ── Run behaviour
    parser.add_argument(
        "--workers", "-w",
        type=int,
        default=2,
        help="Parallel workers for different tickers (default: 2). "
             "Keep low — each worker makes concurrent async requests to EDGAR.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Seconds to wait between tickers (default: 2.0)",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip tickers that already have filings in the database",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be scraped without actually storing anything",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable debug logging",
    )

    return parser.parse_args()


# ── Environment validation ─────────────────────────────────────────────────────

def validate_environment() -> bool:
    required = [
        "POSTGRES_HOST", "POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD",
        "MINIO_ENDPOINT", "MINIO_ACCESS_KEY", "MINIO_SECRET_KEY",
    ]
    missing = [v for v in required if not os.getenv(v)]

    if not os.getenv("OPENAI_API_KEY") and not os.getenv("OLLAMA_HOST"):
        missing.append("OPENAI_API_KEY or OLLAMA_HOST")

    if missing:
        _LOG.error("Missing environment variables: %s", ", ".join(missing))
        return False
    return True


# ── Existing ticker check ─────────────────────────────────────────────────────

def get_existing_tickers() -> set[str]:
    """Return tickers that already have at least one filing in the DB."""
    try:
        pg = get_postgres_client()
        with pg.get_cursor() as cur:
            cur.execute("SELECT DISTINCT ticker FROM filings")
            return {row["ticker"] for row in cur.fetchall()}
    except Exception as e:
        _LOG.warning("Could not query existing tickers: %s", e)
        return set()


# ── Date filtering ────────────────────────────────────────────────────────────

def apply_date_filter(
    collector: SECCollector,
    ticker: str,
    filing_types: list[str],
    limit: int,
    after: str | None,
    before: str | None,
    store_cold: bool,
    store_warm: bool,
    store_search: bool,
) -> dict[str, int]:
    """
    Collect filings and post-filter by date range.

    SEC submissions API doesn't support date range params directly,
    so we fetch then filter in-memory before storing.
    """
    # Temporarily monkey-patch _fetch_data to apply date filter
    original_fetch = collector._fetch_data

    def filtered_fetch(t, **kwargs):
        docs = original_fetch(t, **kwargs)
        filtered = []
        for doc in docs:
            filing_date = doc.get("metadata", {}).get("filing_date", "")
            if after and filing_date and filing_date < after:
                continue
            if before and filing_date and filing_date > before:
                continue
            filtered.append(doc)
        if after or before:
            _LOG.info(
                "[%s] Date filter (%s → %s): %d/%d filings kept",
                t, after or "any", before or "any", len(filtered), len(docs),
            )
        return filtered

    collector._fetch_data = filtered_fetch

    result = collector.collect(
        ticker=ticker,
        filing_types=filing_types,
        limit=limit,
        store_cold=store_cold,
        store_warm=store_warm,
        store_search=store_search,
    )

    # Restore original method
    collector._fetch_data = original_fetch
    return result


# ── Per-ticker scrape ─────────────────────────────────────────────────────────

def scrape_ticker(
    ticker: str,
    filing_types: list[str],
    limit: int,
    after: str | None,
    before: str | None,
    store_cold: bool,
    store_warm: bool,
    store_search: bool,
) -> dict:
    """Run the full collection pipeline for a single ticker."""
    _LOG.info("━" * 50)
    _LOG.info("Scraping %s  |  types=%s  |  limit=%d", ticker, filing_types, limit)

    t0 = time.perf_counter()
    try:
        collector = SECCollector()
        results = apply_date_filter(
            collector=collector,
            ticker=ticker,
            filing_types=filing_types,
            limit=limit,
            after=after,
            before=before,
            store_cold=store_cold,
            store_warm=store_warm,
            store_search=store_search,
        )
        elapsed = time.perf_counter() - t0
        results["ticker"]  = ticker
        results["elapsed"] = round(elapsed, 1)
        results["status"]  = "ok"
        _LOG.info(
            "✓ %s done in %.1fs — fetched=%d cold=%d warm=%d indexed=%d",
            ticker, elapsed,
            results.get("fetched", 0),
            results.get("stored_cold", 0),
            results.get("stored_warm", 0),
            results.get("indexed", 0),
        )
    except Exception as e:
        elapsed = time.perf_counter() - t0
        _LOG.exception("✗ %s failed after %.1fs: %s", ticker, elapsed, e)
        results = {
            "ticker":  ticker,
            "elapsed": round(elapsed, 1),
            "status":  "error",
            "error":   str(e),
            "fetched": 0, "stored_cold": 0, "stored_warm": 0, "indexed": 0,
        }

    return results


# ── Summary table ─────────────────────────────────────────────────────────────

def print_summary(all_results: list[dict], total_elapsed: float) -> None:
    _LOG.info("")
    _LOG.info("=" * 65)
    _LOG.info("BULK COLLECTION SUMMARY")
    _LOG.info("=" * 65)
    _LOG.info(
        "%-8s %-8s %-6s %-6s %-8s %-8s %s",
        "TICKER", "STATUS", "FETCHED", "COLD", "WARM", "INDEXED", "TIME(s)",
    )
    _LOG.info("-" * 65)

    totals = {"fetched": 0, "stored_cold": 0, "stored_warm": 0, "indexed": 0}

    for r in all_results:
        status_icon = "✓" if r["status"] == "ok" else "✗"
        _LOG.info(
            "%-8s %-8s %-6d %-6d %-8d %-8d %.1f",
            r["ticker"],
            f"{status_icon} {r['status']}",
            r.get("fetched", 0),
            r.get("stored_cold", 0),
            r.get("stored_warm", 0),
            r.get("indexed", 0),
            r.get("elapsed", 0),
        )
        for key in totals:
            totals[key] += r.get(key, 0)

    _LOG.info("-" * 65)
    _LOG.info(
        "%-8s %-8s %-6d %-6d %-8d %-8d %.1f",
        "TOTAL", "",
        totals["fetched"], totals["stored_cold"],
        totals["stored_warm"], totals["indexed"],
        total_elapsed,
    )
    _LOG.info("=" * 65)

    errors = [r for r in all_results if r["status"] == "error"]
    if errors:
        _LOG.warning("Failed tickers: %s", ", ".join(r["ticker"] for r in errors))


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    load_dotenv()

    if not args.dry_run and not validate_environment():
        return 1

    # Resolve ticker list
    tickers: list[str] = args.tickers if args.tickers else TICKER_GROUPS[args.group]
    filing_types = [ft.strip() for ft in args.filing_types.split(",")]

    # Skip existing tickers if requested
    if args.skip_existing and not args.dry_run:
        existing = get_existing_tickers()
        before_count = len(tickers)
        tickers = [t for t in tickers if t not in existing]
        skipped = before_count - len(tickers)
        if skipped:
            _LOG.info("Skipping %d already-scraped tickers", skipped)

    if not tickers:
        _LOG.info("No tickers to scrape (all already exist or list is empty).")
        return 0

    # ── Dry run ──
    if args.dry_run:
        _LOG.info("DRY RUN — nothing will be stored")
        _LOG.info("Tickers (%d): %s", len(tickers), ", ".join(tickers))
        _LOG.info("Filing types: %s", ", ".join(filing_types))
        _LOG.info("Limit per ticker: %d", args.limit)
        _LOG.info("Date range: %s → %s", args.after or "any", args.before or "any")
        _LOG.info("Workers: %d", args.workers)
        return 0

    # ── Live run ──
    _LOG.info("=" * 65)
    _LOG.info("BULK SEC COLLECTION")
    _LOG.info("=" * 65)
    _LOG.info("Tickers     : %s", ", ".join(tickers))
    _LOG.info("Filing types: %s", ", ".join(filing_types))
    _LOG.info("Limit       : %d per ticker", args.limit)
    _LOG.info("Date range  : %s → %s", args.after or "any", args.before or "any")
    _LOG.info("Workers     : %d", args.workers)
    _LOG.info("Cold storage: %s", "disabled" if args.no_cold   else "enabled")
    _LOG.info("Warm storage: %s", "disabled" if args.no_warm   else "enabled")
    _LOG.info("Search index: %s", "disabled" if args.no_search else "enabled")
    _LOG.info("=" * 65)

    all_results: list[dict] = []
    t0_total = time.perf_counter()

    if args.workers > 1:
        # Parallel scraping across tickers
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(
                    scrape_ticker,
                    ticker,
                    filing_types,
                    args.limit,
                    args.after,
                    args.before,
                    not args.no_cold,
                    not args.no_warm,
                    not args.no_search,
                ): ticker
                for ticker in tickers
            }
            for future in as_completed(futures):
                result = future.result()
                all_results.append(result)
                # Brief pause between completions to stay polite to EDGAR
                time.sleep(args.delay)
    else:
        # Sequential — easier to read logs, safer for EDGAR rate limits
        for i, ticker in enumerate(tickers):
            result = scrape_ticker(
                ticker=ticker,
                filing_types=filing_types,
                limit=args.limit,
                after=args.after,
                before=args.before,
                store_cold=not args.no_cold,
                store_warm=not args.no_warm,
                store_search=not args.no_search,
            )
            all_results.append(result)

            # Delay between tickers (except after the last one)
            if i < len(tickers) - 1:
                _LOG.info("Waiting %.1fs before next ticker…", args.delay)
                time.sleep(args.delay)

    total_elapsed = time.perf_counter() - t0_total
    print_summary(all_results, total_elapsed)
    return 0


if __name__ == "__main__":
    sys.exit(main())