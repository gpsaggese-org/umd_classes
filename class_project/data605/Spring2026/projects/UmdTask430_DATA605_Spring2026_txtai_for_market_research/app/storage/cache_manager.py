"""
Cache manager for KeyDB hot tier.

Provides high-level cache operations for:
- Live price feeds (TTL 60s)
- Semantic cache (TTL 3600s)
- Session memory (TTL 1800s)

Key Patterns:
- prices:{ticker}       - Live stock prices
- cache:{md5_hash}      - Semantic query cache
- session:{session_id}  - Agent conversation state
"""

import hashlib
import json
import logging
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from app.storage.hot_storage.keydb_client import KeyDBClient, get_keydb_client

_LOG = logging.getLogger(__name__)


# TTL constants (in seconds)
TTL_PRICES = 60       # 1 minute for live price feeds
TTL_CACHE = 3600      # 1 hour for semantic cache
TTL_SESSION = 1800    # 30 minutes for agent sessions


@dataclass
class PriceData:
    """Live price data for a ticker."""
    ticker: str
    price: float
    change: float
    change_percent: float
    volume: int
    timestamp: datetime

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "ticker": self.ticker,
            "price": self.price,
            "change": self.change,
            "change_percent": self.change_percent,
            "volume": self.volume,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PriceData":
        """Create from dictionary."""
        return cls(
            ticker=data["ticker"],
            price=data["price"],
            change=data["change"],
            change_percent=data["change_percent"],
            volume=data["volume"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )


class CacheManager:
    """
    High-level cache manager for hot tier operations.

    Provides typed methods for each cache category with appropriate TTLs.
    """

    def __init__(self, client: Optional[KeyDBClient] = None):
        """
        Initialize cache manager.

        Args:
            client: KeyDB client (uses singleton if not provided)
        """
        self.client = client or get_keydb_client()

    # -------------------------------------------------------------------------
    # Price Cache (TTL: 60s)
    # -------------------------------------------------------------------------

    def set_price(self, ticker: str, price_data: PriceData) -> bool:
        """
        Cache live price data for a ticker.

        Args:
            ticker: Stock ticker symbol
            price_data: Price data object

        Returns:
            True if successful
        """
        key = f"prices:{ticker.upper()}"
        return self.client.set(key, price_data.to_dict(), ttl=TTL_PRICES)

    def get_price(self, ticker: str) -> Optional[PriceData]:
        """
        Get cached price data for a ticker.

        Args:
            ticker: Stock ticker symbol

        Returns:
            PriceData if cached and not expired, None otherwise
        """
        key = f"prices:{ticker.upper()}"
        data = self.client.get(key)
        if data:
            return PriceData.from_dict(data)
        return None

    def get_prices_batch(self, tickers: list[str]) -> dict[str, PriceData]:
        """
        Get cached prices for multiple tickers.

        Args:
            tickers: List of ticker symbols

        Returns:
            Dict mapping ticker to PriceData (only for cached tickers)
        """
        result = {}
        for ticker in tickers:
            price = self.get_price(ticker)
            if price:
                result[ticker.upper()] = price
        return result

    def clear_price(self, ticker: str) -> bool:
        """
        Clear cached price for a ticker.

        Args:
            ticker: Stock ticker symbol

        Returns:
            True if key was deleted
        """
        key = f"prices:{ticker.upper()}"
        return self.client.delete(key) > 0

    # -------------------------------------------------------------------------
    # Semantic Cache (TTL: 3600s)
    # -------------------------------------------------------------------------

    def _compute_cache_key(self, query: str, context: Optional[str] = None) -> str:
        """
        Compute MD5 hash for cache key.

        Args:
            query: Search query string
            context: Optional context string

        Returns:
            MD5 hash string
        """
        key_material = f"{query}:{context}" if context else query
        return hashlib.md5(key_material.encode()).hexdigest()

    def get_semantic(self, query: str, context: Optional[str] = None) -> Optional[Any]:
        """
        Get cached semantic search results.

        Args:
            query: Search query
            context: Optional context for more specific caching

        Returns:
            Cached results if found, None otherwise
        """
        key = f"cache:{self._compute_cache_key(query, context)}"
        return self.client.get(key)

    def set_semantic(
        self,
        query: str,
        results: Any,
        context: Optional[str] = None,
    ) -> bool:
        """
        Cache semantic search results.

        Args:
            query: Search query
            results: Results to cache (will be JSON serialized)
            context: Optional context for more specific caching

        Returns:
            True if successful
        """
        key = f"cache:{self._compute_cache_key(query, context)}"
        return self.client.set(key, results, ttl=TTL_CACHE)

    def clear_semantic(self, query: str, context: Optional[str] = None) -> bool:
        """
        Clear cached semantic results.

        Args:
            query: Search query
            context: Optional context

        Returns:
            True if key was deleted
        """
        key = f"cache:{self._compute_cache_key(query, context)}"
        return self.client.delete(key) > 0

    def clear_all_semantic(self) -> int:
        """
        Clear all semantic cache entries.

        Returns:
            Number of keys deleted
        """
        count = 0
        for key in self.client.scan_iter("cache:*"):
            if self.client.delete(key) > 0:
                count += 1
        return count

    # -------------------------------------------------------------------------
    # Session Memory (TTL: 1800s)
    # -------------------------------------------------------------------------

    def create_session(self, session_id: str, initial_data: Optional[dict] = None) -> bool:
        """
        Create a new session.

        Args:
            session_id: Unique session identifier
            initial_data: Optional initial session data

        Returns:
            True if successful
        """
        key = f"session:{session_id}"
        data = {
            "created_at": datetime.utcnow().isoformat(),
            "last_accessed": datetime.utcnow().isoformat(),
            "access_count": 0,
            **(initial_data or {}),
        }
        return self.client.set(key, data, ttl=TTL_SESSION)

    def get_session(self, session_id: str) -> Optional[dict]:
        """
        Get session data.

        Args:
            session_id: Session identifier

        Returns:
            Session data dict if found, None otherwise
        """
        key = f"session:{session_id}"
        data = self.client.get(key)
        if data:
            # Update access metadata
            data["last_accessed"] = datetime.utcnow().isoformat()
            data["access_count"] = data.get("access_count", 0) + 1
            self.client.set(key, data, ttl=TTL_SESSION)  # Refresh TTL
        return data

    def update_session(self, session_id: str, updates: dict) -> bool:
        """
        Update session data.

        Args:
            session_id: Session identifier
            updates: Dict of fields to update

        Returns:
            True if successful
        """
        key = f"session:{session_id}"
        data = self.client.get(key)
        if data:
            data.update(updates)
            data["last_accessed"] = datetime.utcnow().isoformat()
            return self.client.set(key, data, ttl=TTL_SESSION)
        return False

    def add_to_session_history(
        self,
        session_id: str,
        role: str,
        content: str,
        max_history: int = 20,
    ) -> bool:
        """
        Add a message to session conversation history.

        Args:
            session_id: Session identifier
            role: Message role (user/assistant/system)
            content: Message content
            max_history: Maximum messages to keep in history

        Returns:
            True if successful
        """
        key = f"session:{session_id}"
        data = self.client.get(key)
        if not data:
            return False

        if "history" not in data:
            data["history"] = []

        data["history"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
        })

        # Trim history if needed
        if len(data["history"]) > max_history:
            data["history"] = data["history"][-max_history:]

        data["last_accessed"] = datetime.utcnow().isoformat()
        return self.client.set(key, data, ttl=TTL_SESSION)

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.

        Args:
            session_id: Session identifier

        Returns:
            True if session was deleted
        """
        key = f"session:{session_id}"
        return self.client.delete(key) > 0

    def get_active_sessions(self) -> list[str]:
        """
        Get list of active session IDs.

        Returns:
            List of session IDs
        """
        session_ids = []
        for key in self.client.scan_iter("session:*"):
            session_ids.append(key.replace("session:", ""))
        return session_ids

    # -------------------------------------------------------------------------
    # Generic Cache Operations
    # -------------------------------------------------------------------------

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value by key.

        Args:
            key: Cache key
            default: Default value if not found

        Returns:
            Cached value or default
        """
        return self.client.get(key, default)

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set a value with optional TTL.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds

        Returns:
            True if successful
        """
        return self.client.set(key, value, ttl=ttl)

    def delete(self, *keys: str) -> int:
        """
        Delete keys.

        Args:
            keys: Keys to delete

        Returns:
            Number of keys deleted
        """
        return self.client.delete(*keys)

    def exists(self, *keys: str) -> int:
        """
        Check if keys exist.

        Args:
            keys: Keys to check

        Returns:
            Number of keys that exist
        """
        return self.client.exists(*keys)

    def clear_all(self) -> int:
        """
        Clear all cache entries (prices, semantic, sessions).

        Returns:
            Number of keys deleted
        """
        count = 0
        for pattern in ["prices:*", "cache:*", "session:*"]:
            for key in self.client.scan_iter(pattern):
                if self.client.delete(key) > 0:
                    count += 1
        return count

    def get_stats(self) -> dict:
        """
        Get cache statistics.

        Returns:
            Dict with counts for each cache type
        """
        stats = {
            "prices": 0,
            "semantic": 0,
            "sessions": 0,
        }

        for key in self.client.scan_iter("prices:*"):
            stats["prices"] += 1

        for key in self.client.scan_iter("cache:*"):
            stats["semantic"] += 1

        for key in self.client.scan_iter("session:*"):
            stats["sessions"] += 1

        stats["total"] = sum(stats.values())
        return stats


# Global singleton instance
_cache_manager: Optional[CacheManager] = None


def get_cache_manager() -> CacheManager:
    """
    Get the singleton CacheManager instance.

    Returns:
        CacheManager instance
    """
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
        _LOG.info("CacheManager initialized")
    return _cache_manager
