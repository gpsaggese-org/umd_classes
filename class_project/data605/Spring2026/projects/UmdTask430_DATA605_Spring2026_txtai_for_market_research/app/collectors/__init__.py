"""
Data collectors for market research platform.

Each collector fetches data from a source and stores it across all storage tiers:
- Cold: MinIO for raw document archive
- Warm: PostgreSQL for structured data + pgvector
- Hot: KeyDB for caching
- Search: txtai EmbeddingsIndex for semantic search

Usage:
    from app.collectors import SECCollector, NewsCollector

    collector = SECCollector()
    collector.collect("AAPL", filing_types=["10-K", "8-K"])
"""

from app.collectors.base_collector import BaseCollector
from app.collectors.sec_collector import SECCollector
from app.collectors.news_collector import NewsCollector
from app.collectors.web_collector import WebCollector
from app.collectors.social_collector import SocialCollector

__all__ = [
    "BaseCollector",
    "SECCollector",
    "NewsCollector",
    "WebCollector",
    "SocialCollector",
]
