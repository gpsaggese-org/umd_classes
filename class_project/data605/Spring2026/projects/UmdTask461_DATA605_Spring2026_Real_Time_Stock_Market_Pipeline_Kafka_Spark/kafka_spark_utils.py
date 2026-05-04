"""
Utility functions for the Real-Time Stock Market Pipeline using Kafka and Spark.
"""
import json
import random
import time
from datetime import datetime
from typing import Dict, List

STOCK_SYMBOLS = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]

BASE_PRICES = {
    "AAPL": 175.0,
    "GOOGL": 140.0,
    "MSFT": 380.0,
    "AMZN": 185.0,
    "TSLA": 250.0,
}


def generate_stock_event(symbol: str) -> Dict:
    """
    Generate a simulated stock price event.

    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL')

    Returns:
        Dictionary containing stock event data
    """
    base_price = BASE_PRICES[symbol]
    change_pct = random.uniform(-0.02, 0.02)
    price = round(base_price * (1 + change_pct), 2)
    volume = random.randint(100, 10000)
    return {
        "symbol": symbol,
        "price": price,
        "volume": volume,
        "timestamp": datetime.now().isoformat(),
        "change_pct": round(change_pct * 100, 4),
    }


def generate_stock_stream(n_events: int = 100, delay: float = 0.0) -> List[Dict]:
    """
    Generate a stream of stock events for all symbols.

    Args:
        n_events: Number of events to generate
        delay: Delay between events in seconds

    Returns:
        List of stock event dictionaries
    """
    events = []
    for _ in range(n_events):
        symbol = random.choice(STOCK_SYMBOLS)
        event = generate_stock_event(symbol)
        events.append(event)
        if delay > 0:
            time.sleep(delay)
    return events


def serialize_event(event: Dict) -> bytes:
    """
    Serialize a stock event to JSON bytes for Kafka.

    Args:
        event: Stock event dictionary

    Returns:
        JSON-encoded bytes
    """
    return json.dumps(event).encode("utf-8")


def deserialize_event(data: bytes) -> Dict:
    """
    Deserialize a Kafka message to a stock event dictionary.

    Args:
        data: JSON-encoded bytes from Kafka

    Returns:
        Stock event dictionary
    """
    return json.loads(data.decode("utf-8"))


def compute_moving_average(prices: List[float], window: int = 5) -> List[float]:
    """
    Compute moving average of stock prices.

    Args:
        prices: List of stock prices
        window: Window size for moving average

    Returns:
        List of moving averages (None for initial values)
    """
    averages = []
    for i in range(len(prices)):
        if i < window - 1:
            averages.append(None)
        else:
            avg = sum(prices[i - window + 1:i + 1]) / window
            averages.append(round(avg, 2))
    return averages


def check_price_alert(price: float, symbol: str, threshold_pct: float = 1.5) -> Dict:
    """
    Check if a stock price has moved beyond a threshold.

    Args:
        price: Current stock price
        symbol: Stock ticker symbol
        threshold_pct: Alert threshold percentage

    Returns:
        Alert dictionary if threshold exceeded, else None
    """
    base_price = BASE_PRICES[symbol]
    change_pct = abs((price - base_price) / base_price * 100)
    if change_pct >= threshold_pct:
        direction = "UP" if price > base_price else "DOWN"
        return {
            "symbol": symbol,
            "alert": f"Price moved {direction} by {change_pct:.2f}%",
            "current_price": price,
            "base_price": base_price,
            "change_pct": round(change_pct, 4),
            "timestamp": datetime.now().isoformat(),
        }
    return None


def format_kafka_summary(events: List[Dict]) -> str:
    """
    Format a summary of Kafka events for display.

    Args:
        events: List of stock event dictionaries

    Returns:
        Formatted summary string
    """
    summary = [f"Total events: {len(events)}"]
    by_symbol = {}
    for e in events:
        sym = e["symbol"]
        if sym not in by_symbol:
            by_symbol[sym] = []
        by_symbol[sym].append(e["price"])
    for sym, prices in sorted(by_symbol.items()):
        avg = sum(prices) / len(prices)
        summary.append(
            f"{sym}: {len(prices)} events | "
            f"avg: ${avg:.2f} | min: ${min(prices):.2f} | max: ${max(prices):.2f}"
        )
    return "\n".join(summary)
