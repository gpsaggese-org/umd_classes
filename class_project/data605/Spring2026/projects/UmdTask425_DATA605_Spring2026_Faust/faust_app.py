# This script creates a Faust app that consumes from the tweets Kafka topic.
import faust
from transformers import pipeline


app = faust.App('sentiment_analysis_app', broker='kafka://localhost:9092')

class Tweet(faust.Record):
    sentiment: str
    id: str
    date: str
    user: str
    text: str

class SentimentResult(faust.Record):
    text: str
    original_sentiment: str
    predicted_sentiment: str
    confidence: float


tweets_topic = app.topic('tweets', value_type=Tweet)
sentiment_topic = app.topic('sentiment_results', value_type=SentimentResult)

# 3-class sentiment model: negative / neutral / positive
sentiment_classifier = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest"
)

def analyze_sentiment(text: str) -> dict:
    """
    Returns standardized 3-category sentiment:
    negative, neutral, or positive
    """

    if not text or not text.strip():
        return {
            "sentiment": "neutral",
            "confidence": 0.0
        }

    result = sentiment_classifier(text[:512])[0]

    return {
        "sentiment": result["label"].lower(),
        "confidence": round(float(result["score"]), 4)
    }

# inside Faust agent
@app.agent(tweets_topic)
async def process_tweets(tweets):
    async for tweet in tweets:

        sentiment_result = analyze_sentiment(tweet.text)
        output = SentimentResult(
            text=tweet.text,
            original_sentiment=tweet.sentiment,
            predicted_sentiment=sentiment_result["sentiment"],
            confidence=sentiment_result["confidence"]
        )

        print(output)
        await sentiment_topic.send(value=output)