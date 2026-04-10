"""
Data ingestion pipeline for txtai market research platform.

This module orchestrates the full ingestion pipeline using collectors:
1. Fetch data from all sources (news, SEC, web, social)
2. Store raw documents in MinIO cold storage
3. Store structured data in PostgreSQL warm storage
4. Chunk documents to <= 512 tokens
5. Embed with txtai's sentence transformers
6. Upsert into the shared EmbeddingsIndex

Usage:
    python -m app.pipeline.ingest --ticker AAPL

Or use collectors directly:
    from app.collectors import SECCollector, NewsCollector

    sec = SECCollector()
    sec.collect("AAPL", filing_types=["10-K", "8-K"])
"""

import logging

from app.collectors import SECCollector, NewsCollector, WebCollector, SocialCollector

_LOG = logging.getLogger(__name__)


def ingest_all(
    ticker: str,
    store_cold: bool = True,
    store_warm: bool = True,
    store_search: bool = True,
) -> dict[str, dict[str, int]]:
    """
    Run the full ingestion pipeline for all data sources.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL")
        store_cold: Store raw documents in MinIO (default: True)
        store_warm: Store structured data in PostgreSQL (default: True)
        store_search: Index in txtai for semantic search (default: True)

    Returns:
        Dict mapping source name to collection results
    """
    results = {}

    # Define all data sources and their collectors
    collectors = [
        ("news", NewsCollector(), {}),
        ("sec", SECCollector(), {"filing_types": ["10-K", "8-K", "DEF 14A"]}),
        ("web", WebCollector(), {}),
        ("social", SocialCollector(), {"subreddits": ["investing", "stocks"]}),
    ]

    _LOG.info("Starting ingestion pipeline for %s...", ticker)

    for source_name, collector, kwargs in collectors:
        try:
            _LOG.info("  Collecting from %s...", source_name)
            result = collector.collect(
                ticker=ticker,
                store_cold=store_cold,
                store_warm=store_warm,
                store_search=store_search,
                **kwargs,
            )
            results[source_name] = result

        except Exception as e:
            _LOG.error("    Error collecting from %s: %s", source_name, e)
            results[source_name] = {
                "fetched": 0,
                "stored_cold": 0,
                "stored_warm": 0,
                "indexed": 0,
            }

    # Print summary
    total_fetched = sum(r.get("fetched", 0) for r in results.values())
    total_cold = sum(r.get("stored_cold", 0) for r in results.values())
    total_warm = sum(r.get("stored_warm", 0) for r in results.values())
    total_indexed = sum(r.get("indexed", 0) for r in results.values())

    _LOG.info("Ingestion complete:")
    _LOG.info("  Total fetched:   %d", total_fetched)
    _LOG.info("  Stored in cold:  %d", total_cold)
    _LOG.info("  Stored in warm:  %d", total_warm)
    _LOG.info("  Indexed:         %d", total_indexed)

    return results


def ingest_source(
    ticker: str,
    source: str,
    store_cold: bool = True,
    store_warm: bool = True,
    store_search: bool = True,
    **kwargs,
) -> dict[str, int]:
    """
    Run ingestion for a specific data source.

    Args:
        ticker: Stock ticker symbol
        source: Source name (news, sec, web, social)
        store_cold: Store in MinIO
        store_warm: Store in PostgreSQL
        store_search: Index in txtai
        **kwargs: Source-specific arguments

    Returns:
        Dict with counts: {'fetched', 'stored_cold', 'stored_warm', 'indexed'}
    """
    collectors = {
        "news": NewsCollector(),
        "sec": SECCollector(),
        "web": WebCollector(),
        "social": SocialCollector(),
    }

    if source not in collectors:
        raise ValueError(f"Unknown source: {source}. Valid: {list(collectors.keys())}")

    collector = collectors[source]
    return collector.collect(
        ticker=ticker,
        store_cold=store_cold,
        store_warm=store_warm,
        store_search=store_search,
        **kwargs,
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ingest market research data")
    parser.add_argument("--ticker", default="AAPL", help="Stock ticker symbol")
    parser.add_argument("--source", choices=["news", "sec", "web", "social", "all"], default="all",
                        help="Data source to ingest (default: all)")
    parser.add_argument("--no-cold", action="store_true", help="Skip cold storage (MinIO)")
    parser.add_argument("--no-warm", action="store_true", help="Skip warm storage (PostgreSQL)")
    parser.add_argument("--no-search", action="store_true", help="Skip search index (txtai)")
    args = parser.parse_args()

    # Load environment variables for API keys
    from dotenv import load_dotenv
    load_dotenv()

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    if args.source == "all":
        results = ingest_all(
            args.ticker,
            store_cold=not args.no_cold,
            store_warm=not args.no_warm,
            store_search=not args.no_search,
        )
        print("\nSummary by source:")
        for source, counts in results.items():
            print(f"  {source}: fetched={counts['fetched']}, cold={counts['stored_cold']}, "
                  f"warm={counts['stored_warm']}, indexed={counts['indexed']}")
    else:
        result = ingest_source(
            args.ticker,
            args.source,
            store_cold=not args.no_cold,
            store_warm=not args.no_warm,
            store_search=not args.no_search,
        )
        print(f"\n{args.source}: fetched={result['fetched']}, cold={result['stored_cold']}, "
              f"warm={result['stored_warm']}, indexed={result['indexed']}")
