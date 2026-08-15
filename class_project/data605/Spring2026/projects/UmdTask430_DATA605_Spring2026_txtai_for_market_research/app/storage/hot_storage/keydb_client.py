"""
KeyDB client for hot tier storage.

KeyDB is a Redis-compatible, high-performance in-memory database.
This module provides connection management with authentication support.

Hot Tier Keys:
- prices:{ticker}       - Live price feeds (TTL 60s)
- cache:{md5_hash}      - Semantic cache (TTL 3600s)
- session:{id}          - Agent memory/sessions (TTL 1800s)
"""

import json
import logging
import os
from typing import Any, Optional
from dotenv import load_dotenv

import redis

load_dotenv()

_LOG = logging.getLogger(__name__)


class KeyDBClient:
    """
    KeyDB client with connection pooling and authentication.

    KeyDB is Redis-compatible, so we use the redis-py client.
    Supports both single-node and cluster deployments.
    """

    def __init__(
        self,
        host: Optional[str] = os.getenv("KEYDB_HOST", "localhost"),
        port: Optional[int] = int(os.getenv("KEYDB_PORT", "6379")),
        password: Optional[str] = os.getenv("KEYDB_PASSWORD"),
        db: int = 0,
        socket_timeout: float = 5.0,
        socket_connect_timeout: float = 5.0,
        max_connections: int = 10,
    ):
        """
        Initialize KeyDB client with connection pool.

        Args:
            host: KeyDB server host (default: localhost or KEYDB_HOST env var)
            port: KeyDB server port (default: 6379 or KEYDB_PORT env var)
            password: Authentication password (default: KEYDB_PASSWORD env var)
            db: Database number (default: 0)
            socket_timeout: Socket timeout in seconds
            socket_connect_timeout: Connection timeout in seconds
            max_connections: Maximum connections in pool
        """
        self.host = host
        self.port = port
        self.password = password
        self.db = db

        self._pool: Optional[redis.ConnectionPool] = None
        self._client: Optional[redis.Redis] = None

        self._pool_kwargs = {
            "host": self.host,
            "port": self.port,
            "password": self.password,
            "db": self.db,
            "socket_timeout": socket_timeout,
            "socket_connect_timeout": socket_connect_timeout,
            "max_connections": max_connections,
            "decode_responses": True,
        }

    def _get_pool(self) -> redis.ConnectionPool:
        """Get or create connection pool."""
        if self._pool is None:
            self._pool = redis.ConnectionPool(**self._pool_kwargs)
        return self._pool

    def _get_client(self) -> redis.Redis:
        """Get or create Redis client."""
        if self._client is None:
            self._client = redis.Redis(connection_pool=self._get_pool())
        return self._client

    def ping(self) -> bool:
        """
        Test connection to KeyDB server.

        Returns:
            True if connection successful
        """
        try:
            client = self._get_client()
            return client.ping()
        except redis.ConnectionError as e:
            _LOG.error("KeyDB connection failed: %s", e)
            return False

    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
    ) -> bool:
        """
        Set a key-value pair with optional TTL.

        Args:
            key: Redis key
            value: Value to store (auto-serialized to JSON if not string)
            ttl: Time-to-live in seconds (optional)

        Returns:
            True if successful
        """
        client = self._get_client()

        # Serialize non-string values to JSON
        if not isinstance(value, str):
            value = json.dumps(value)

        try:
            if ttl:
                return client.setex(key, ttl, value)
            else:
                return client.set(key, value)
        except redis.RedisError as e:
            _LOG.error("KeyDB set error for key='%s': %s", key, e)
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value by key.

        Args:
            key: Redis key
            default: Default value if key not found

        Returns:
            Value (auto-deserialized from JSON) or default
        """
        client = self._get_client()

        try:
            value = client.get(key)
            if value is None:
                return default

            # Try to deserialize JSON
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value

        except redis.RedisError as e:
            _LOG.error("KeyDB get error for key='%s': %s", key, e)
            return default

    def delete(self, *keys: str) -> int:
        """
        Delete one or more keys.

        Args:
            keys: Keys to delete

        Returns:
            Number of keys deleted
        """
        client = self._get_client()

        try:
            return client.delete(*keys)
        except redis.RedisError as e:
            _LOG.error("KeyDB delete error: %s", e)
            return 0

    def exists(self, *keys: str) -> int:
        """
        Check if keys exist.

        Args:
            keys: Keys to check

        Returns:
            Number of keys that exist
        """
        client = self._get_client()

        try:
            return client.exists(*keys)
        except redis.RedisError as e:
            _LOG.error("KeyDB exists error: %s", e)
            return 0

    def ttl(self, key: str) -> int:
        """
        Get TTL for a key.

        Args:
            key: Redis key

        Returns:
            TTL in seconds, -1 if no TTL, -2 if key doesn't exist
        """
        client = self._get_client()

        try:
            return client.ttl(key)
        except redis.RedisError as e:
            _LOG.error("KeyDB ttl error for key='%s': %s", key, e)
            return -2

    def expire(self, key: str, ttl: int) -> bool:
        """
        Set TTL on an existing key.

        Args:
            key: Redis key
            ttl: Time-to-live in seconds

        Returns:
            True if TTL was set
        """
        client = self._get_client()

        try:
            return client.expire(key, ttl)
        except redis.RedisError as e:
            _LOG.error("KeyDB expire error for key='%s': %s", key, e)
            return False

    def incr(self, key: str, amount: int = 1) -> Optional[int]:
        """
        Increment a key atomically.

        Args:
            key: Redis key
            amount: Amount to increment by

        Returns:
            New value after increment
        """
        client = self._get_client()

        try:
            return client.incr(key, amount)
        except redis.RedisError as e:
            _LOG.error("KeyDB incr error for key='%s': %s", key, e)
            return None

    def hset(
        self,
        name: str,
        key: Optional[str] = None,
        value: Any = None,
        mapping: Optional[dict] = None,
    ) -> int:
        """
        Set hash field(s).

        Args:
            name: Hash name
            key: Field key (optional if mapping provided)
            value: Field value (optional if mapping provided)
            mapping: Dict of field-value pairs (optional)

        Returns:
            Number of fields set
        """
        client = self._get_client()

        # Serialize value if provided
        if key is not None and value is not None and not isinstance(value, str):
            value = json.dumps(value)

        try:
            return client.hset(name, key, value, mapping=mapping)
        except redis.RedisError as e:
            _LOG.error("KeyDB hset error for hash='%s': %s", name, e)
            return 0

    def hgetall(self, name: str) -> dict:
        """
        Get all fields from a hash.

        Args:
            name: Hash name

        Returns:
            Dict of field-value pairs
        """
        client = self._get_client()

        try:
            return client.hgetall(name)
        except redis.RedisError as e:
            _LOG.error("KeyDB hgetall error for hash='%s': %s", name, e)
            return {}

    def hget(self, name: str, key: str, default: Any = None) -> Any:
        """
        Get a single field from a hash.

        Args:
            name: Hash name
            key: Field key
            default: Default value if field not found

        Returns:
            Field value (auto-deserialized) or default
        """
        client = self._get_client()

        try:
            value = client.hget(name, key)
            if value is None:
                return default

            # Try to deserialize JSON
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value

        except redis.RedisError as e:
            _LOG.error("KeyDB hget error for hash='%s', key='%s': %s", name, key, e)
            return default

    def scan_iter(self, match: str, count: int = 100):
        """
        Scan keys matching a pattern.

        Args:
            match: Pattern to match (e.g., "prices:*")
            count: Hint for number of keys per iteration

        Yields:
            Matching keys
        """
        client = self._get_client()

        try:
            for key in client.scan_iter(match=match, count=count):
                yield key
        except redis.RedisError as e:
            _LOG.error("KeyDB scan_iter error for pattern='%s': %s", match, e)

    def flushdb(self) -> bool:
        """
        Flush current database (dangerous - use with caution).

        Returns:
            True if successful
        """
        client = self._get_client()

        try:
            return client.flushdb()
        except redis.RedisError as e:
            _LOG.error("KeyDB flushdb error: %s", e)
            return False

    def close(self) -> None:
        """Close all connections in the pool."""
        if self._pool:
            self._pool.disconnect()
            self._pool = None
            self._client = None
            _LOG.info("KeyDB connections closed")


# Global singleton instance
_keydb_client: Optional[KeyDBClient] = None


def get_keydb_client() -> KeyDBClient:
    """
    Get the singleton KeyDB client instance.

    Creates a new instance on first call, returns existing instance thereafter.

    Returns:
        KeyDBClient instance
    """
    global _keydb_client
    if _keydb_client is None:
        _keydb_client = KeyDBClient()
        if _keydb_client.ping():
            _LOG.info(
                "Connected to KeyDB at %s:%d", _keydb_client.host, _keydb_client.port
            )
        else:
            _LOG.warning("KeyDB connection test failed")
    return _keydb_client
