# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Faust: Real-Time Tweet Sentiment Analysis
#
# This notebook demonstrates a complete real-time sentiment analysis pipeline built with Faust.
#
# **Pipeline overview:**
# ```
# CSV dataset → tweet_producer.py → Kafka ("tweets")
#                                          ↓
#                                    faust_app.py (Faust worker)
#                                          ↓
#                                   Kafka ("sentiment_results")
#                                          ↓
#                                    dashboard.py (Streamlit)
# ```
#
# The notebook covers five parts:
# 1. Load and explore the Sentiment140 tweet dataset
# 2. Run sentiment analysis directly on a sample batch
# 3. Evaluate model accuracy against ground-truth labels
# 4. Visualize the sentiment distribution
# 5. Read live results from Kafka (requires the pipeline to be running)

# %%
# %load_ext autoreload
# %autoreload 2
# %matplotlib inline

# %%
import logging

import matplotlib.pyplot as plt
import pandas as pd

import faust_utils as fauuti

logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)

# %% [markdown]
# ## Part 1: Load and Explore the Dataset
#
# The Sentiment140 dataset contains 1.6 million tweets labeled with:
# - `0` → negative
# - `2` → neutral
# - `4` → positive
#
# We load a small sample for exploration.

# %%
CSV_PATH = "training.1600000.processed.noemoticon.csv"
# Load 50 tweets for this notebook.
tweets = fauuti.load_tweets(CSV_PATH, limit=50)
df_raw = fauuti.tweets_to_dataframe(tweets)
print(f"Loaded {len(df_raw)} tweets")
df_raw.head(10)

# %%
# Show the distribution of ground-truth sentiment labels.
print("Ground-truth label counts:")
print(df_raw["sentiment"].value_counts())

# %%
# Preview the text of the first few tweets.
for i, row in df_raw.head(5).iterrows():
    print(f"[{row['sentiment']:8s}] {row['text'][:80]}")

# %% [markdown]
# ## Part 2: Run Sentiment Analysis on a Sample Batch
#
# We load the HuggingFace model and classify 20 tweets directly.
# This demonstrates the core analysis logic without needing Kafka running.
#
# The model (`cardiffnlp/twitter-roberta-base-sentiment-latest`) was trained
# specifically on Twitter data, making it well-suited for this task.
# It outputs one of three labels: `negative`, `neutral`, `positive`.

# %%
# Load the Twitter-specific sentiment model (cached after first download).
classifier = fauuti.load_sentiment_model()

# %%
# Run sentiment analysis on the first 20 tweets.
sample_tweets = tweets[:20]
df_results = fauuti.analyze_tweets_batch(sample_tweets, classifier)
df_results

# %%
# Show a side-by-side comparison of original vs predicted labels.
comparison = df_results[["text", "original_sentiment", "predicted_sentiment", "confidence"]].copy()
comparison["text"] = comparison["text"].str[:60]
print(comparison.to_string(index=False))

# %% [markdown]
# ## Part 3: Evaluate Model Accuracy
#
# Compare the model's predicted sentiment against the Sentiment140 ground-truth labels.
#
# Note: the original labels are binary (negative/positive), while the model also
# predicts neutral — so some disagreement is expected.

# %%
# Compute overall accuracy on the sample.
acc = fauuti.accuracy_score(df_results)
correct = int(acc * len(df_results))
print(f"Accuracy: {acc:.1%}  ({correct}/{len(df_results)} correct)")

# %%
# Show only the tweets where the model disagreed with the original label.
mismatches = df_results[
    df_results["original_sentiment"] != df_results["predicted_sentiment"]
].copy()
mismatches["text"] = mismatches["text"].str[:60]
print(f"Mismatches: {len(mismatches)}")
mismatches[["text", "original_sentiment", "predicted_sentiment", "confidence"]]

# %% [markdown]
# ## Part 4: Visualize Results
#
# Plot the sentiment distribution and confidence scores from the model's predictions.

# %%
counts = fauuti.sentiment_summary(df_results)
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Bar chart of sentiment label counts.
colors = {"negative": "#e74c3c", "neutral": "#95a5a6", "positive": "#2ecc71"}
bar_colors = [colors.get(label, "#3498db") for label in counts.index]
counts.plot(kind="bar", ax=axes[0], color=bar_colors)
axes[0].set_title("Predicted Sentiment Distribution")
axes[0].set_xlabel("Sentiment")
axes[0].set_ylabel("Count")
axes[0].tick_params(axis="x", rotation=0)

# Box plot of confidence scores grouped by predicted sentiment.
df_results.boxplot(column="confidence", by="predicted_sentiment", ax=axes[1])
axes[1].set_title("Model Confidence by Sentiment")
axes[1].set_xlabel("Sentiment")
axes[1].set_ylabel("Confidence Score")

plt.suptitle("")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Part 5: Read Live Results from Kafka
#
# If the full pipeline is running (Kafka + Faust worker + tweet producer),
# this cell reads from the `sentiment_results` Kafka topic and displays a
# live snapshot of processed tweets.
#
# To start the pipeline, run in separate terminals:
# ```bash
# # Terminal 1
# docker compose up -d
#
# # Terminal 2
# python3 -m faust -A faust_app worker -l info
#
# # Terminal 3
# python3 tweet_producer.py
# ```

# %%
# %% [markdown]
# ## Part 6: Live Dashboard
#
# While the pipeline is running, you can also visualize the sentiment results
# in real time using the Streamlit dashboard.
#
# Open a new terminal in the project folder and run:
#
# ```bash
# python3 -m streamlit run dashboard.py
# ```
#
# The dashboard will open automatically in your browser and update every 2
# seconds with:
# - **Live sentiment counts** — total tweets processed, broken down by positive, negative, and neutral
# - **Bar chart** — sentiment distribution updated in real time
# - **Recent tweets table** — the last 50 processed tweets with predicted sentiment and confidence score
#
# The dashboard reads directly from the `sentiment_results` Kafka topic,
# the same topic the notebook reads from in Part 5.

# %%
try:
    consumer = fauuti.create_kafka_consumer(
        topic="sentiment_results",
        timeout_ms=5000,
    )
    df_live = fauuti.poll_sentiment_results(consumer, max_messages=200)
    if df_live.empty:
        print("No results found. Start the pipeline first (see instructions above).")
    else:
        print(f"Read {len(df_live)} results from Kafka")
        print("\nSentiment counts:")
        print(fauuti.sentiment_summary(df_live))
        df_live["text"] = df_live["text"].str[:60]
        display(df_live.head(10))
except Exception as e:
    print(f"Could not connect to Kafka: {e}")
    print("Start the pipeline first using the terminal commands above.")
