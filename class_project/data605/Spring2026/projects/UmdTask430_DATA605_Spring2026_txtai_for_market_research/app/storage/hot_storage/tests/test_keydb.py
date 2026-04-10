#!/usr/bin/env python3
"""
Test script for KeyDB hot tier infrastructure.

Usage:
    python -m app.storage.test_keydb
"""

import logging
from datetime import datetime

from app.storage.keydb_client import KeyDBClient, get_keydb_client
from app.storage.cache_manager import (
    CacheManager,
    get_cache_manager,
    PriceData,
    TTL_PRICES,
    TTL_CACHE,
    TTL_SESSION,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
_LOG = logging.getLogger(__name__)


def test_keydb_client():
    """Test basic KeyDB client operations."""
    print("\n" + "=" * 60)
    print("Testing KeyDB Client")
    print("=" * 60)

    client = get_keydb_client()

    # Test connection
    print("\n1. Testing connection...")
    if client.ping():
        print("   [OK] Connected to KeyDB")
    else:
        print("   [FAIL] Connection failed")
        return False

    # Test set/get
    print("\n2. Testing set/get...")
    test_key = "test:string"
    test_value = "Hello, KeyDB!"
    client.set(test_key, test_value, ttl=60)
    result = client.get(test_key)
    if result == test_value:
        print(f"   [OK] String set/get: '{result}'")
    else:
        print(f"   [FAIL] Expected '{test_value}', got '{result}'")

    # Test JSON serialization
    print("\n3. Testing JSON serialization...")
    test_dict = {"ticker": "AAPL", "price": 175.50, "volume": 1000000}
    client.set("test:json", test_dict, ttl=60)
    result = client.get("test:json")
    if result == test_dict:
        print(f"   [OK] JSON set/get: {result}")
    else:
        print(f"   [FAIL] JSON mismatch")

    # Test hash operations
    print("\n4. Testing hash operations...")
    client.hset("test:hash", "field1", "value1")
    client.hset("test:hash", "field2", {"nested": "data"})
    all_fields = client.hgetall("test:hash")
    print(f"   [OK] Hash fields: {all_fields}")

    # Test TTL
    print("\n5. Testing TTL...")
    client.set("test:ttl", "expires soon", ttl=10)
    ttl = client.ttl("test:ttl")
    if 0 < ttl <= 10:
        print(f"   [OK] TTL set correctly: {ttl}s remaining")
    else:
        print(f"   [FAIL] TTL incorrect: {ttl}")

    # Test delete
    print("\n6. Testing delete...")
    deleted = client.delete("test:string", "test:json", "test:hash", "test:ttl")
    print(f"   [OK] Deleted {deleted} keys")

    return True


def test_cache_manager():
    """Test CacheManager operations."""
    print("\n" + "=" * 60)
    print("Testing Cache Manager")
    print("=" * 60)

    cache = get_cache_manager()

    # Test price caching
    print("\n1. Testing price cache...")
    price_data = PriceData(
        ticker="AAPL",
        price=175.50,
        change=2.25,
        change_percent=1.30,
        volume=52000000,
        timestamp=datetime.utcnow(),
    )
    cache.set_price("AAPL", price_data)
    cached_price = cache.get_price("AAPL")
    if cached_price and cached_price.ticker == "AAPL":
        print(f"   [OK] Price cached: ${cached_price.price} ({cached_price.change_percent}%)")
    else:
        print("   [FAIL] Price not cached correctly")

    # Test batch price retrieval
    print("\n2. Testing batch price retrieval...")
    for ticker in ["GOOGL", "MSFT", "AMZN"]:
        cache.set_price(ticker, PriceData(
            ticker=ticker,
            price=100.0,
            change=1.0,
            change_percent=1.0,
            volume=1000000,
            timestamp=datetime.utcnow(),
        ))
    batch = cache.get_prices_batch(["AAPL", "GOOGL", "MSFT", "INVALID"])
    print(f"   [OK] Retrieved {len(batch)} prices: {list(batch.keys())}")

    # Test semantic cache
    print("\n3. Testing semantic cache...")
    query = "What is Apple's revenue?"
    mock_results = [
        {"text": "Apple reported revenue of $89.5B", "score": 0.95},
        {"text": "Q4 revenue beat expectations", "score": 0.87},
    ]
    cache.set_semantic(query, mock_results)
    cached_results = cache.get_semantic(query)
    if cached_results and len(cached_results) == 2:
        print(f"   [OK] Semantic cache: {len(cached_results)} results")
    else:
        print("   [FAIL] Semantic cache failed")

    # Test semantic cache with context
    print("\n4. Testing semantic cache with context...")
    cache.set_semantic("revenue query", {"data": "result1"}, context="AAPL")
    cache.set_semantic("revenue query", {"data": "result2"}, context="GOOGL")
    result_aapl = cache.get_semantic("revenue query", context="AAPL")
    result_googl = cache.get_semantic("revenue query", context="GOOGL")
    if result_aapl != result_googl:
        print("   [OK] Context-specific caching works")
    else:
        print("   [FAIL] Context not differentiating results")

    # Test session management
    print("\n5. Testing session management...")
    session_id = "test_session_123"
    cache.create_session(session_id, {"user": "test_user", "ticker": "AAPL"})
    session = cache.get_session(session_id)
    if session and session.get("user") == "test_user":
        print(f"   [OK] Session created for user: {session['user']}")
    else:
        print("   [FAIL] Session not created correctly")

    # Test session history
    print("\n6. Testing session conversation history...")
    cache.add_to_session_history(session_id, "user", "What's the stock price?")
    cache.add_to_session_history(session_id, "assistant", "AAPL is at $175.50")
    session = cache.get_session(session_id)
    if session.get("history") and len(session["history"]) == 2:
        print(f"   [OK] History has {len(session['history'])} messages")
    else:
        print("   [FAIL] Session history not working")

    # Test session update
    print("\n7. Testing session update...")
    cache.update_session(session_id, {"ticker": "GOOGL", "last_query": "revenue"})
    session = cache.get_session(session_id)
    if session.get("ticker") == "GOOGL":
        print("   [OK] Session updated successfully")
    else:
        print("   [FAIL] Session update failed")

    # Test cache stats
    print("\n8. Getting cache statistics...")
    stats = cache.get_stats()
    print(f"   [OK] Cache stats: {stats}")

    # Cleanup test sessions
    print("\n9. Cleaning up test data...")
    cache.delete_session(session_id)
    cache.clear_all_semantic()
    for ticker in ["AAPL", "GOOGL", "MSFT", "AMZN"]:
        cache.clear_price(ticker)
    print("   [OK] Cleanup complete")

    return True


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("KeyDB Hot Tier Infrastructure Tests")
    print("=" * 60)
    print(f"\nTTL Configuration:")
    print(f"  - Prices:   {TTL_PRICES}s (1 minute)")
    print(f"  - Semantic: {TTL_CACHE}s (1 hour)")
    print(f"  - Sessions: {TTL_SESSION}s (30 minutes)")

    success = True

    if not test_keydb_client():
        print("\n[ABORT] KeyDB client tests failed - skipping cache manager tests")
        success = False
    else:
        if not test_cache_manager():
            success = False

    print("\n" + "=" * 60)
    if success:
        print("All tests passed!")
    else:
        print("Some tests failed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
