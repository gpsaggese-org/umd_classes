"""
Utility functions for the Real-Time Tweet Sentiment Analysis Pipeline.
Uses Apache Kafka for streaming and HuggingFace Transformers for sentiment classification.
"""
import json
import random
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Kafka topic name
TOPIC_NAME = "tweets"

# Sentiment labels from cardiffnlp/twitter-roberta-base-sentiment
SENTIMENT_LABELS = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive",
}

# Sentiment colors for visualization
SENTIMENT_COLORS = {
    "positive": "#2ecc71",
    "neutral":  "#3498db",
    "negative": "#e74c3c",
}


def load_sentiment140(filepath: str, n_samples: int = 10000, random_state: int = 42) -> pd.DataFrame:
    """
    Load and preprocess the Sentiment140 dataset.

    Args:
        filepath: Path to training.1600000.processed.noemoticon.csv
        n_samples: Number of samples to load (default 10000 for speed)
        random_state: Random seed for reproducibility

    Returns:
        DataFrame with columns: text, label, sentiment
    """
    # Sentiment140 columns
    cols = ["label", "id", "date", "query", "user", "text"]
    df = pd.read_csv(filepath, encoding="latin-1", names=cols)

    # Map labels: 0 = negative, 4 = positive
    df = df[df["label"].isin([0, 4])].copy()
    df["sentiment"] = df["label"].map({0: "negative", 4: "positive"})

    # Sample equally from positive and negative
    n_each = n_samples // 2
    df_neg = df[df["sentiment"] == "negative"].sample(n_each, random_state=random_state)
    df_pos = df[df["sentiment"] == "positive"].sample(n_each, random_state=random_state)
    df_sampled = pd.concat([df_neg, df_pos]).sample(frac=1, random_state=random_state)

    return df_sampled[["text", "label", "sentiment"]].reset_index(drop=True)


def preprocess_tweet(text: str) -> str:
    """
    Clean and preprocess a tweet for sentiment analysis.

    Args:
        text: Raw tweet text

    Returns:
        Cleaned tweet text
    """
    import re
    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)
    # Remove @mentions
    text = re.sub(r"@\w+", "@user", text)
    # Remove extra whitespace
    text = " ".join(text.split())
    return text.strip()


def create_tweet_event(text: str, true_label: str, tweet_id: int) -> Dict:
    """
    Create a tweet event dictionary for Kafka.

    Args:
        text: Tweet text
        true_label: True sentiment label from dataset
        tweet_id: Unique tweet identifier

    Returns:
        Tweet event dictionary
    """
    return {
        "tweet_id": tweet_id,
        "text": preprocess_tweet(text),
        "true_label": true_label,
        "timestamp": datetime.now().isoformat(),
    }


def serialize_event(event: Dict) -> bytes:
    """
    Serialize a tweet event to JSON bytes for Kafka.

    Args:
        event: Tweet event dictionary

    Returns:
        JSON-encoded bytes
    """
    return json.dumps(event).encode("utf-8")


def deserialize_event(data: bytes) -> Dict:
    """
    Deserialize a Kafka message to a tweet event dictionary.

    Args:
        data: JSON-encoded bytes from Kafka

    Returns:
        Tweet event dictionary
    """
    return json.loads(data.decode("utf-8"))


def compute_sentiment_stats(results: List[Dict]) -> Dict:
    """
    Compute sentiment statistics from a list of classified tweets.

    Args:
        results: List of dicts with keys: text, predicted_sentiment, true_label, score

    Returns:
        Dictionary with sentiment statistics
    """
    df = pd.DataFrame(results)
    total = len(df)

    stats = {
        "total": total,
        "positive": int((df["predicted_sentiment"] == "positive").sum()),
        "negative": int((df["predicted_sentiment"] == "negative").sum()),
        "neutral":  int((df["predicted_sentiment"] == "neutral").sum()),
    }
    stats["positive_pct"] = round(stats["positive"] / total * 100, 2)
    stats["negative_pct"] = round(stats["negative"] / total * 100, 2)
    stats["neutral_pct"]  = round(stats["neutral"]  / total * 100, 2)

    # Accuracy (compare predicted vs true label, ignoring neutral)
    df_binary = df[df["true_label"].isin(["positive", "negative"])].copy()
    if len(df_binary) > 0:
        correct = (df_binary["predicted_sentiment"] == df_binary["true_label"]).sum()
        stats["accuracy"] = round(correct / len(df_binary) * 100, 2)
    else:
        stats["accuracy"] = None

    return stats


def format_sentiment_summary(stats: Dict) -> str:
    """
    Format sentiment statistics for display.

    Args:
        stats: Dictionary from compute_sentiment_stats()

    Returns:
        Formatted summary string
    """
    lines = [
        f"Total tweets analyzed : {stats['total']}",
        f"Positive              : {stats['positive']} ({stats['positive_pct']}%)",
        f"Negative              : {stats['negative']} ({stats['negative_pct']}%)",
        f"Neutral               : {stats['neutral']}  ({stats['neutral_pct']}%)",
    ]
    if stats.get("accuracy"):
        lines.append(f"Model accuracy        : {stats['accuracy']}%")
    return "\n".join(lines)
