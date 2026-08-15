"""
Utility functions for Faust-based stream processing workflows.

Import as:

import faust_utils as fauuti
"""

import csv
import json
import logging
import time
from typing import Dict, List, Optional

import faust
import pandas as pd
from kafka import KafkaConsumer, KafkaProducer
from transformers import pipeline as hf_pipeline

logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)


# #############################################################################
# Faust App Setup
# #############################################################################


def create_faust_app(app_id: str, broker: str = "kafka://localhost:9092") -> faust.App:
    """
    Create and configure a Faust application.

    :param app_id: unique identifier for the Faust app
    :param broker: Kafka broker URL
    :return: configured Faust App instance
    """
    _LOG.info("Creating Faust app '%s' connected to %s", app_id, broker)
    return faust.App(app_id, broker=broker)


# #############################################################################
# Tweet Data Loading
# #############################################################################


def load_tweets(csv_path: str, limit: int = 200) -> List[Dict]:
    """
    Load tweets from the Sentiment140 CSV dataset.

    Sentiment140 CSV columns: sentiment, id, date, query, user, text.
    Sentiment codes: 0 = negative, 2 = neutral, 4 = positive.

    :param csv_path: path to the CSV file
    :param limit: maximum number of tweets to load
    :return: list of tweet dicts with keys: sentiment, id, date, user, text
    """
    _LOG.info("Loading up to %d tweets from %s", limit, csv_path)
    tweets = []
    with open(csv_path, encoding="latin-1") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i >= limit:
                break
            tweets.append(
                {
                    "sentiment": row[0],
                    "id": row[1],
                    "date": row[2],
                    "user": row[4],
                    "text": row[5],
                }
            )
    _LOG.info("Loaded %d tweets", len(tweets))
    return tweets


def tweets_to_dataframe(tweets: List[Dict]) -> pd.DataFrame:
    """
    Convert a list of tweet dicts to a DataFrame with human-readable sentiment labels.

    Sentiment codes are mapped: 0 → negative, 2 → neutral, 4 → positive.

    :param tweets: list of tweet dicts
    :return: DataFrame with columns: sentiment, id, date, user, text
    """
    df = pd.DataFrame(tweets)
    label_map = {"0": "negative", "2": "neutral", "4": "positive"}
    df["sentiment"] = df["sentiment"].map(label_map).fillna("neutral")
    return df


# #############################################################################
# Kafka Producer
# #############################################################################


def create_kafka_producer(bootstrap_servers: str = "localhost:9092") -> KafkaProducer:
    """
    Create a Kafka producer that serializes messages as JSON bytes.

    :param bootstrap_servers: Kafka broker address
    :return: configured KafkaProducer instance
    """
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


def send_tweets_to_kafka(
    tweets: List[Dict],
    topic: str = "tweets",
    bootstrap_servers: str = "localhost:9092",
    delay: float = 0.1,
) -> None:
    """
    Send a list of tweets to a Kafka topic, simulating a real-time stream.

    :param tweets: list of tweet dicts
    :param topic: Kafka topic name
    :param bootstrap_servers: Kafka broker address
    :param delay: seconds to wait between messages to simulate streaming
    :return: None
    """
    producer = create_kafka_producer(bootstrap_servers)
    for i, tweet in enumerate(tweets):
        producer.send(topic, tweet)
        _LOG.info("Sent tweet %d: %s", i, tweet["text"][:50])
        time.sleep(delay)
    producer.flush()
    _LOG.info("Done sending %d tweets", len(tweets))


# #############################################################################
# Kafka Consumer
# #############################################################################


def create_kafka_consumer(
    topic: str,
    bootstrap_servers: str = "localhost:9092",
    timeout_ms: int = 5000,
) -> KafkaConsumer:
    """
    Create a Kafka consumer that deserializes JSON messages.

    No consumer group is used so the consumer always reads from the earliest
    offset without spending time on group coordination.

    :param topic: Kafka topic to consume from
    :param bootstrap_servers: Kafka broker address
    :param timeout_ms: milliseconds to wait for new messages before stopping iteration
    :return: configured KafkaConsumer instance
    """
    return KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        consumer_timeout_ms=timeout_ms,
        group_id=None,
    )


def poll_sentiment_results(
    consumer: KafkaConsumer, max_messages: int = 200
) -> pd.DataFrame:
    """
    Poll a Kafka topic and return messages as a DataFrame.

    :param consumer: KafkaConsumer connected to the sentiment_results topic
    :param max_messages: maximum number of messages to read
    :return: DataFrame with columns: text, original_sentiment, predicted_sentiment, confidence
    """
    rows = []
    for i, msg in enumerate(consumer):
        if i >= max_messages:
            break
        rows.append(msg.value)
    return pd.DataFrame(rows) if rows else pd.DataFrame()


# #############################################################################
# Sentiment Analysis
# #############################################################################


def load_sentiment_model(
    model_name: str = "cardiffnlp/twitter-roberta-base-sentiment-latest",
):
    """
    Load a HuggingFace sentiment analysis pipeline.

    Downloads the model on first call (~500 MB); cached locally on subsequent calls.

    :param model_name: HuggingFace model identifier
    :return: HuggingFace pipeline object
    """
    _LOG.info("Loading sentiment model: %s", model_name)
    return hf_pipeline("sentiment-analysis", model=model_name, tokenizer=model_name)


def analyze_sentiment(text: str, classifier) -> Dict:
    """
    Classify the sentiment of a single text string.

    Returns one of three categories: negative, neutral, or positive.

    :param text: input text to classify (truncated to 512 chars)
    :param classifier: HuggingFace sentiment pipeline from load_sentiment_model()
    :return: dict with keys 'sentiment' (str) and 'confidence' (float)
    """
    if not text or not text.strip():
        return {"sentiment": "neutral", "confidence": 0.0}
    result = classifier(text[:512])[0]
    return {
        "sentiment": result["label"].lower(),
        "confidence": round(float(result["score"]), 4),
    }


def analyze_tweets_batch(tweets: List[Dict], classifier) -> pd.DataFrame:
    """
    Run sentiment analysis on a list of tweets and return a results DataFrame.

    Sentiment140 codes (0, 2, 4) are mapped to human-readable labels so they
    can be compared directly against the model's predicted labels.

    :param tweets: list of tweet dicts with at least 'text' and 'sentiment' keys
    :param classifier: HuggingFace sentiment pipeline from load_sentiment_model()
    :return: DataFrame with columns: text, original_sentiment, predicted_sentiment, confidence
    """
    label_map = {"0": "negative", "2": "neutral", "4": "positive"}
    rows = []
    for tweet in tweets:
        result = analyze_sentiment(tweet["text"], classifier)
        rows.append(
            {
                "text": tweet["text"],
                "original_sentiment": label_map.get(tweet["sentiment"], tweet["sentiment"]),
                "predicted_sentiment": result["sentiment"],
                "confidence": result["confidence"],
            }
        )
    return pd.DataFrame(rows)


# #############################################################################
# Visualization Helpers
# #############################################################################


def sentiment_summary(
    df: pd.DataFrame, sentiment_col: str = "predicted_sentiment"
) -> pd.Series:
    """
    Count sentiment label occurrences in a DataFrame column.

    :param df: DataFrame containing a sentiment column
    :param sentiment_col: name of the column with sentiment labels
    :return: Series of counts indexed by sentiment label
    """
    return df[sentiment_col].value_counts()


def accuracy_score(df: pd.DataFrame) -> float:
    """
    Compute the fraction of tweets where predicted sentiment matches original label.

    :param df: DataFrame with columns 'original_sentiment' and 'predicted_sentiment'
    :return: accuracy as a float between 0 and 1
    """
    correct = (df["original_sentiment"] == df["predicted_sentiment"]).sum()
    return correct / len(df)
