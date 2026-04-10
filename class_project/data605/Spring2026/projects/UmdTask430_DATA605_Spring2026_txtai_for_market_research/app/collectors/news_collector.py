"""
News collector for market research data.

Fetches headlines and articles from:
- NewsAPI (https://newsapi.org)
- Alpha Vantage News (https://www.alphavantage.co)

Stores across all storage tiers.
"""

import logging
import os
from datetime import datetime, timedelta
from typing import Optional

import httpx

from app.collectors.base_collector import BaseCollector

_LOG = logging.getLogger(__name__)


class NewsCollector(BaseCollector):
    """
    Collector for news articles.

    Stores:
    - Cold: Article HTML in MinIO
    - Warm: Article metadata in PostgreSQL articles table
    - Search: Embedded chunks in txtai
    - Hot: Fetch cache in KeyDB
    """

    def _get_source_tag(self) -> str:
        return "news"

    def _fetch_data(
        self,
        ticker: str,
        days_back: int = 7,
        limit: int = 50,
    ) -> list[dict]:
        """
        Fetch news articles for a given ticker.

        Args:
            ticker: Stock ticker symbol
            days_back: Number of days to look back
            limit: Maximum number of articles to return

        Returns:
            List of dicts with text and metadata
        """
        articles = []

        # Try NewsAPI first
        newsapi_key = os.getenv("NEWSAPI_KEY")
        if newsapi_key:
            fetched = self._fetch_newsapi(ticker, days_back, limit)
            articles.extend(fetched)

        # Try Alpha Vantage as fallback/supplement
        alphavantage_key = os.getenv("ALPHAVANTAGE_API_KEY")
        if alphavantage_key:
            fetched = self._fetch_alphavantage(ticker, limit)
            articles.extend(fetched)

        # Deduplicate by title
        seen = set()
        unique = []
        for article in articles:
            title_key = article["metadata"].get("title", "")[:50]
            if title_key not in seen:
                seen.add(title_key)
                unique.append(article)

        return unique[:limit]

    def _fetch_newsapi(
        self,
        ticker: str,
        days_back: int,
        limit: int,
    ) -> list[dict]:
        """Fetch from NewsAPI."""
        key = os.getenv("NEWSAPI_KEY")
        if not key:
            return []

        from_date = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")

        url = "https://newsapi.org/v2/everything"
        params = {
            "q": f'"{ticker}" OR "{ticker.replace("NASDAQ:", "")}"',
            "from": from_date,
            "sortBy": "relevancy",
            "language": "en",
            "apiKey": key,
            "pageSize": min(limit, 100),
        }

        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

            articles = []
            for item in data.get("articles", []):
                text_parts = [
                    item.get("title", ""),
                    item.get("description", ""),
                    item.get("content", ""),
                ]
                text = " ".join(filter(None, text_parts))

                if text:
                    articles.append({
                        "text": text,
                        "metadata": {
                            "title": item.get("title", ""),
                            "source": item.get("source", {}).get("name", ""),
                            "url": item.get("url", ""),
                            "published_at": item.get("publishedAt", ""),
                            "author": item.get("author", ""),
                        },
                    })

            return articles

        except httpx.HTTPError as e:
            _LOG.error("NewsAPI error: %s", e)
            return []

    def _fetch_alphavantage(
        self,
        ticker: str,
        limit: int,
    ) -> list[dict]:
        """Fetch from Alpha Vantage News API."""
        key = os.getenv("ALPHAVANTAGE_API_KEY")
        if not key:
            return []

        url = "https://www.alphavantage.co/query"
        params = {
            "function": "NEWS_SENTIMENT",
            "ticker": ticker,
            "apikey": key,
            "limit": min(limit, 50),
        }

        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

            articles = []
            for item in data.get("feed", []):
                text_parts = [
                    item.get("title", ""),
                    item.get("summary", ""),
                ]
                text = " ".join(filter(None, text_parts))

                if text:
                    articles.append({
                        "text": text,
                        "metadata": {
                            "title": item.get("title", ""),
                            "source": item.get("source", ""),
                            "url": item.get("url", ""),
                            "published_at": item.get("time_published", ""),
                            "sentiment_score": item.get("overall_sentiment_score"),
                        },
                    })

            return articles

        except httpx.HTTPError as e:
            _LOG.error("Alpha Vantage error: %s", e)
            return []

    def collect(
        self,
        ticker: str,
        days_back: int = 7,
        limit: int = 50,
        store_cold: bool = True,
        store_warm: bool = True,
        store_search: bool = True,
        use_cache: bool = False,
    ) -> dict[str, int]:
        """
        Run the full news collection pipeline.

        Args:
            ticker: Stock ticker symbol
            days_back: Days to look back
            limit: Maximum articles
            store_cold: Store in MinIO
            store_warm: Store in PostgreSQL
            store_search: Index in txtai
            use_cache: Use cached results

        Returns:
            Dict with counts
        """
        return super().collect(
            ticker=ticker,
            days_back=days_back,
            limit=limit,
            store_cold=store_cold,
            store_warm=store_warm,
            store_search=store_search,
            use_cache=use_cache,
        )
