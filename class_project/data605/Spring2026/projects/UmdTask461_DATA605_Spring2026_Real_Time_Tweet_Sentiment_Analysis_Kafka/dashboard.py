"""
Real-Time Tweet Sentiment Analysis Dashboard
Run with: streamlit run dashboard.py --server.port 8501
"""
import json
import time
import random
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, UnknownTopicOrPartitionError
from transformers import pipeline
from kafka_sentiment_utils import (
    load_sentiment140, preprocess_tweet, create_tweet_event,
    TOPIC_NAME, SENTIMENT_LABELS, SENTIMENT_COLORS,
)

# 
# Page config
# 
st.set_page_config(
    page_title="Real-Time Tweet Sentiment Dashboard",
    page_icon="",
    layout="wide",
)

st.title(" Real-Time Tweet Sentiment Analysis")
st.markdown("Apache Kafka + HuggingFace Transformers | DATA605 Spring 2026 | Aashish Vinod")
st.divider()

# 
# Sidebar controls
# 
st.sidebar.title("️ Controls")
n_tweets = st.sidebar.slider("Number of tweets to process", 50, 500, 100, 50)
batch_size = st.sidebar.slider("Batch size per update", 10, 50, 20, 10)
dataset_path = st.sidebar.text_input(
    "Dataset path",
    value="/app/training.1600000.processed.noemoticon.csv"
)
run_button = st.sidebar.button(" Run Pipeline", type="primary", use_container_width=True)
st.sidebar.divider()
st.sidebar.markdown("**About**")
st.sidebar.markdown("This dashboard streams tweets through Apache Kafka and classifies sentiment in real time using the `cardiffnlp/twitter-roberta-base-sentiment` model.")

# 
# Layout placeholders
# 
col1, col2, col3, col4 = st.columns(4)
positive_metric = col1.empty()
negative_metric = col2.empty()
neutral_metric  = col3.empty()
accuracy_metric = col4.empty()

st.divider()
col_left, col_right = st.columns(2)
pie_chart     = col_left.empty()
trend_chart   = col_right.empty()
st.divider()
tweet_table   = st.empty()

# 
# Initialize metrics
# 
positive_metric.metric(" Positive", "0", "0%")
negative_metric.metric(" Negative", "0", "0%")
neutral_metric.metric(" Neutral",   "0", "0%")
accuracy_metric.metric(" Accuracy", "N/A")

# 
# Main pipeline
# 
if run_button:
    KAFKA_BROKER = "kafka:29092"

    # Load data
    with st.spinner("Loading Sentiment140 dataset..."):
        df = load_sentiment140(dataset_path, n_samples=n_tweets * 2)
    st.success(f"Loaded {len(df)} tweets from Sentiment140!")

    # Load model
    with st.spinner("Loading HuggingFace RoBERTa model..."):
        sentiment_model = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment",
            tokenizer="cardiffnlp/twitter-roberta-base-sentiment",
            truncation=True,
            max_length=128,
            top_k=1,
        )
    st.success("Model loaded!")

    # Reset Kafka topic
    with st.spinner("Setting up Kafka topic..."):
        admin = KafkaAdminClient(bootstrap_servers=KAFKA_BROKER)
        try:
            admin.delete_topics([TOPIC_NAME])
            time.sleep(2)
        except Exception:
            pass
        try:
            admin.create_topics([NewTopic(name=TOPIC_NAME, num_partitions=3, replication_factor=1)])
        except Exception:
            pass
        admin.close()
    st.success("Kafka topic ready!")

    # Produce tweets
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8"),
    )
    df_produce = df.head(n_tweets)
    for i, row in df_produce.iterrows():
        event = create_tweet_event(row["text"], row["sentiment"], tweet_id=i)
        producer.send(TOPIC_NAME, key="tweet", value=event)
    producer.flush()
    producer.close()

    # Consume and classify in real time
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="dashboard-group",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        consumer_timeout_ms=8000,
    )

    results = []
    progress = st.progress(0, text="Classifying tweets...")

    for msg in consumer:
        event = msg.value
        text = event["text"]
        true_label = event["true_label"]

        result = sentiment_model(text[:128])[0]
        if isinstance(result, list):
            result = result[0]
        predicted = SENTIMENT_LABELS.get(result["label"], result["label"])
        score = round(result["score"], 4)

        results.append({
            "text": text[:80] + "..." if len(text) > 80 else text,
            "true_label": true_label,
            "predicted": predicted,
            "score": score,
            "correct": predicted == true_label,
        })

        # Update dashboard every batch_size tweets
        if len(results) % batch_size == 0 or len(results) == n_tweets:
            df_res = pd.DataFrame(results)
            total = len(df_res)
            pos = int((df_res["predicted"] == "positive").sum())
            neg = int((df_res["predicted"] == "negative").sum())
            neu = int((df_res["predicted"] == "neutral").sum())

            # Accuracy
            df_binary = df_res[df_res["true_label"].isin(["positive", "negative"])]
            df_binary = df_binary[df_binary["predicted"].isin(["positive", "negative"])]
            acc = df_binary["correct"].mean() * 100 if len(df_binary) > 0 else 0

            # Update metrics
            positive_metric.metric(" Positive", pos, f"{pos/total*100:.1f}%")
            negative_metric.metric(" Negative", neg, f"{neg/total*100:.1f}%")
            neutral_metric.metric(" Neutral",   neu, f"{neu/total*100:.1f}%")
            accuracy_metric.metric(" Accuracy", f"{acc:.1f}%")

            # Pie chart
            pie_fig = px.pie(
                values=[pos, neg, neu],
                names=["Positive", "Negative", "Neutral"],
                color_discrete_map={
                    "Positive": SENTIMENT_COLORS["positive"],
                    "Negative": SENTIMENT_COLORS["negative"],
                    "Neutral":  SENTIMENT_COLORS["neutral"],
                },
                title=f"Sentiment Distribution ({total} tweets processed)",
            )
            pie_chart.plotly_chart(pie_fig, use_container_width=True)

            # Trend chart
            window = min(30, total)
            df_res["is_positive"] = (df_res["predicted"] == "positive").astype(int)
            df_res["is_negative"] = (df_res["predicted"] == "negative").astype(int)
            df_res["rolling_pos"] = df_res["is_positive"].rolling(window, min_periods=1).mean() * 100
            df_res["rolling_neg"] = df_res["is_negative"].rolling(window, min_periods=1).mean() * 100

            trend_fig = go.Figure()
            trend_fig.add_trace(go.Scatter(
                y=df_res["rolling_pos"], mode="lines",
                name="Positive", line=dict(color=SENTIMENT_COLORS["positive"], width=2)
            ))
            trend_fig.add_trace(go.Scatter(
                y=df_res["rolling_neg"], mode="lines",
                name="Negative", line=dict(color=SENTIMENT_COLORS["negative"], width=2)
            ))
            trend_fig.update_layout(
                title=f"Real-Time Sentiment Trend (Rolling {window}-tweet window)",
                xaxis_title="Tweet Index",
                yaxis_title="Sentiment %",
                yaxis_range=[0, 100],
            )
            trend_chart.plotly_chart(trend_fig, use_container_width=True)

            # Recent tweets table
            tweet_table.dataframe(
                df_res[["text", "true_label", "predicted", "score"]].tail(10),
                use_container_width=True,
            )

            # Progress bar
            progress.progress(min(total / n_tweets, 1.0), text=f"Processed {total}/{n_tweets} tweets...")

    consumer.close()
    progress.progress(1.0, text="Pipeline complete!")
    st.balloons()
    st.success(f"Pipeline complete! Processed {len(results)} tweets with {acc:.1f}% accuracy.")
