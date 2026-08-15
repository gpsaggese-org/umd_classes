import streamlit as st
from kafka import KafkaConsumer
import json
import pandas as pd
import time

st.set_page_config(page_title="Tweet Sentiment Dashboard", layout="wide")
st.title("Tweet Sentiment Analysis — Live Dashboard")

if "counts" not in st.session_state:
    st.session_state.counts = {"positive": 0, "negative": 0, "neutral": 0}
if "tweets" not in st.session_state:
    st.session_state.tweets = []
if "consumer" not in st.session_state:
    st.session_state.consumer = KafkaConsumer(
        "sentiment_results",
        bootstrap_servers="localhost:9092",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        consumer_timeout_ms=500,
        group_id="streamlit_dashboard",
    )

consumer = st.session_state.consumer

for msg in consumer:
    data = msg.value
    sentiment = data.get("predicted_sentiment", "neutral")
    if sentiment in st.session_state.counts:
        st.session_state.counts[sentiment] += 1
    st.session_state.tweets.append(
        {
            "text": data.get("text", "")[:80],
            "predicted sentiment": sentiment,
            "confidence": round(data.get("confidence", 0), 3),
        }
    )

counts = st.session_state.counts
total = sum(counts.values())

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tweets", total)
col2.metric("Positive", counts["positive"])
col3.metric("Negative", counts["negative"])
col4.metric("Neutral", counts["neutral"])

if total > 0:
    df_counts = pd.DataFrame(
        list(counts.items()), columns=["Sentiment", "Count"]
    ).set_index("Sentiment")
    st.bar_chart(df_counts, color=["#4CAF50"])

if st.session_state.tweets:
    st.subheader("Recent Tweets")
    df = pd.DataFrame(st.session_state.tweets[::-1][:50])
    st.dataframe(df, use_container_width=True)

time.sleep(2)
st.rerun()
