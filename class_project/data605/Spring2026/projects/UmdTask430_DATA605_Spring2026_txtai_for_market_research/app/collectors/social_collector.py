"""
Social media collector for Reddit and StockTwits.

Fetches posts from:
- Reddit: r/investing, r/stocks, r/wallstreetbets (via PRAW or Pushshift)
- StockTwits: Public API for stock discussions

Stores across all storage tiers.
"""

import logging
import os
from datetime import datetime, timedelta
from typing import Optional

import httpx

from app.collectors.base_collector import BaseCollector

_LOG = logging.getLogger(__name__)


class SocialCollector(BaseCollector):
    """
    Collector for social media posts.

    Stores:
    - Cold: Post snapshots in MinIO
    - Warm: Metadata in PostgreSQL
    - Search: Embedded posts in txtai
    - Hot: Fetch cache in KeyDB
    """

    def _get_source_tag(self) -> str:
        return "social"

    def _fetch_data(
        self,
        ticker: str,
        subreddits: Optional[list[str]] = None,
        limit: int = 50,
    ) -> list[dict]:
        """
        Fetch social media posts for a given ticker.

        Args:
            ticker: Stock ticker symbol
            subreddits: List of subreddits to search
            limit: Maximum number of posts to return

        Returns:
            List of dicts with text and metadata
        """
        if subreddits is None:
            subreddits = ["investing", "stocks"]

        posts = []

        # Fetch from Reddit
        reddit_posts = self._fetch_reddit(ticker, subreddits, limit // 2)
        posts.extend(reddit_posts)

        # Fetch from StockTwits
        stocktwits_posts = self._fetch_stocktwits(ticker, limit // 2)
        posts.extend(stocktwits_posts)

        # Sort by time, newest first
        posts.sort(
            key=lambda x: x["metadata"].get("created_at", ""),
            reverse=True,
        )

        return posts[:limit]

    def _fetch_reddit(
        self,
        ticker: str,
        subreddits: list[str],
        limit: int,
    ) -> list[dict]:
        """Fetch posts from Reddit."""
        posts = []

        # Check for PRAW credentials
        client_id = os.getenv("REDDIT_CLIENT_ID")
        client_secret = os.getenv("REDDIT_CLIENT_SECRET")

        if not client_id or not client_secret:
            # Fallback: use Pushshift API
            return self._fetch_reddit_pushshift(ticker, subreddits, limit)

        # Use PRAW if credentials available
        try:
            import praw

            reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent="txtai-market-research/1.0",
            )

            for subreddit_name in subreddits:
                try:
                    subreddit = reddit.subreddit(subreddit_name)

                    # Search for ticker mentions
                    search_query = f'"{ticker}" OR "${ticker}"'
                    results = subreddit.search(search_query, limit=limit // len(subreddits))

                    for post in results:
                        text = f"{post.title}\n\n{post.selftext}" if post.selftext else post.title

                        if text.strip():
                            posts.append({
                                "text": text,
                                "metadata": {
                                    "platform": "reddit",
                                    "subreddit": subreddit_name,
                                    "title": post.title,
                                    "url": f"https://reddit.com{post.permalink}",
                                    "score": post.score,
                                    "num_comments": post.num_comments,
                                    "created_at": datetime.fromtimestamp(post.created_utc).isoformat(),
                                    "author": str(post.author) if post.author else "deleted",
                                },
                            })

                except Exception as e:
                    _LOG.error("Error searching r/%s: %s", subreddit_name, e)
                    continue

        except ImportError:
            return self._fetch_reddit_pushshift(ticker, subreddits, limit)
        except Exception as e:
            _LOG.error("Reddit error: %s", e)
            return self._fetch_reddit_pushshift(ticker, subreddits, limit)

        return posts

    def _fetch_reddit_pushshift(
        self,
        ticker: str,
        subreddits: list[str],
        limit: int,
    ) -> list[dict]:
        """Fetch posts from Reddit via Pushshift API (fallback)."""
        posts = []

        base_url = "https://api.pushshift.io/reddit/search/submission"

        for subreddit_name in subreddits:
            try:
                params = {
                    "q": f'"{ticker}" OR "${ticker}"',
                    "subreddit": subreddit_name,
                    "size": min(limit // len(subreddits), 25),
                    "sort": "desc",
                    "sort_type": "score",
                }

                with httpx.Client(timeout=10.0) as client:
                    response = client.get(base_url, params=params)
                    response.raise_for_status()
                    data = response.json()

                for item in data.get("data", []):
                    text = item.get("title", "")
                    if item.get("selftext"):
                        text += "\n\n" + item.get("selftext", "")

                    if text.strip():
                        posts.append({
                            "text": text,
                            "metadata": {
                                "platform": "reddit",
                                "subreddit": subreddit_name,
                                "title": item.get("title", ""),
                                "url": f"https://reddit.com/r/{subreddit_name}/comments/{item.get('id', '')}",
                                "score": item.get("score", 0),
                                "num_comments": item.get("num_comments", 0),
                                "created_at": datetime.fromtimestamp(item.get("created_utc", 0)).isoformat(),
                                "author": item.get("author", "deleted"),
                            },
                        })

            except httpx.HTTPError as e:
                _LOG.error("Pushshift error for r/%s: %s", subreddit_name, e)
                continue

        return posts

    def _fetch_stocktwits(self, ticker: str, limit: int) -> list[dict]:
        """Fetch messages from StockTwits."""
        posts = []

        url = f"https://api.stocktwits.com/api/2/streams/symbol/{ticker}.json"

        params = {
            "limit": min(limit, 30),
            "filter": "recent",
        }

        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

            for msg in data.get("messages", []):
                text = msg.get("body", "")

                if text.strip():
                    sentiment = None
                    entities = msg.get("entities", {})
                    if "sentiment" in entities:
                        sentiment = entities["sentiment"].get("basic")

                    posts.append({
                        "text": text,
                        "metadata": {
                            "platform": "stocktwits",
                            "url": f"https://stocktwits.com/message/{msg.get('id', '')}",
                            "likes": msg.get("likes", {}).get("total", 0),
                            "created_at": msg.get("created_at", ""),
                            "author": msg.get("user", {}).get("username", "unknown"),
                            "sentiment": sentiment,
                            "cashtags": [s.get("symbol") for s in msg.get("symbols", [])],
                            "post_id": str(msg.get("id", "")),
                        },
                    })

        except httpx.HTTPError as e:
            _LOG.error("StockTwits error: %s", e)

        return posts

    def collect(
        self,
        ticker: str,
        subreddits: Optional[list[str]] = None,
        limit: int = 50,
        store_cold: bool = True,
        store_warm: bool = True,
        store_search: bool = True,
        use_cache: bool = False,
    ) -> dict[str, int]:
        """
        Run the full social media collection pipeline.

        Args:
            ticker: Stock ticker symbol
            subreddits: Subreddits to search
            limit: Maximum posts
            store_cold: Store in MinIO
            store_warm: Store in PostgreSQL
            store_search: Index in txtai
            use_cache: Use cached results

        Returns:
            Dict with counts
        """
        if subreddits is None:
            subreddits = ["investing", "stocks"]

        return super().collect(
            ticker=ticker,
            subreddits=subreddits,
            limit=limit,
            store_cold=store_cold,
            store_warm=store_warm,
            store_search=store_search,
            use_cache=use_cache,
        )
