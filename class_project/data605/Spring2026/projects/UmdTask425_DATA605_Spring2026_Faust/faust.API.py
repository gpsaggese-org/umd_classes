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
# # Faust API Overview
#
# Faust is a Python stream processing library built on top of Apache Kafka.
# It lets you build real-time data pipelines using simple async Python functions.
#
# This notebook covers the five core Faust API concepts:
# - **App** — the top-level application object
# - **Record** — typed schemas for Kafka messages
# - **Topic** — a named Kafka channel
# - **Agent** — an async function that processes a stream of messages
# - **Table** — a persistent, stateful key-value store
#
# All cells in this notebook can run without Kafka. Faust only connects to the
# broker when the worker process starts (via the terminal command).
#
# References:
# - [Faust Documentation](https://faust-streaming.github.io/faust/)
# - [Kafka Documentation](https://kafka.apache.org/documentation/)

# %%
# %load_ext autoreload
# %autoreload 2
# %matplotlib inline

# %% [markdown]
# ## Imports

# %%
import logging

import faust

import faust_utils as fauuti

logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)

# %% [markdown]
# ## 1. App
#
# A `faust.App` is the entry point for any Faust application.
# It connects to a Kafka broker and manages all topics, agents, and tables.
#
# Key parameters:
# - `id` — unique application name; used as the Kafka consumer group prefix
# - `broker` — Kafka URL in the form `kafka://host:port`

# %%
# Create a Faust app using the helper from faust_utils.
app = fauuti.create_faust_app("demo_app", broker="kafka://localhost:9092")
print(f"App id: {app.conf.id}")
print(f"Broker: {app.conf.broker}")

# %% [markdown]
# ## 2. Records
#
# A `faust.Record` is a typed schema for messages flowing through Kafka.
# It behaves like a dataclass and auto-serializes to/from JSON.
#
# Benefits over raw dicts:
# - Field types are documented and enforced
# - Nested records are supported
# - IDE autocomplete works on record fields

# %%
class Tweet(faust.Record):
    """Schema for a raw tweet consumed from the 'tweets' topic."""

    sentiment: str
    id: str
    date: str
    user: str
    text: str


class SentimentResult(faust.Record):
    """Schema for a processed tweet published to the 'sentiment_results' topic."""

    text: str
    original_sentiment: str
    predicted_sentiment: str
    confidence: float


# %%
# Instantiate a Tweet record and access its fields.
sample = Tweet(
    sentiment="0",
    id="12345",
    date="Mon Apr 06 22:19:45 PDT 2009",
    user="example_user",
    text="I love this library!",
)
print(sample)
print("text field:", sample.text)
print("sentiment field:", sample.sentiment)

# %% [markdown]
# ## 3. Topics
#
# A `Topic` is a named Kafka channel.
# Producers write messages to a topic; agents consume messages from a topic.
#
# `value_type` tells Faust which `Record` class to use when deserializing
# incoming messages.

# %%
# Define the two topics used in the sentiment pipeline.
tweets_topic = app.topic("tweets", value_type=Tweet)
sentiment_topic = app.topic("sentiment_results", value_type=SentimentResult)
print("Input topic :", tweets_topic)
print("Output topic:", sentiment_topic)

# %% [markdown]
# ## 4. Agents
#
# An `Agent` is an async generator function decorated with `@app.agent(topic)`.
# It runs in an infinite loop, processing one message at a time as messages arrive.
#
# The pattern is always:
# ```python
# @app.agent(some_topic)
# async def my_agent(stream):
#     async for message in stream:
#         # process message, optionally send to another topic
# ```
#
# Agents are the main unit of computation in Faust — each one is a microservice
# that reads from one topic and writes to another.

# %%
@app.agent(tweets_topic)
async def echo_agent(tweets):
    """
    Echo each tweet back to the sentiment topic as a SentimentResult.

    This is a simplified agent for illustration — the real pipeline uses
    a HuggingFace model to predict sentiment instead of echoing.

    :param tweets: async stream of Tweet records
    """
    async for tweet in tweets:
        result = SentimentResult(
            text=tweet.text,
            original_sentiment=tweet.sentiment,
            predicted_sentiment="positive",
            confidence=1.0,
        )
        await sentiment_topic.send(value=result)


print("Agent registered:", echo_agent)

# %% [markdown]
# ## 5. Tables
#
# A `Table` is a persistent key-value store backed by a Kafka changelog topic.
# Unlike agents (stateless), tables survive worker restarts.
#
# Common use: count events per category over a stream.

# %%
# Create a table that counts how many tweets have been processed per sentiment label.
sentiment_counts = app.Table("sentiment_counts", default=int)

@app.agent(sentiment_topic)
async def count_sentiments(results):
    """
    Accumulate sentiment label counts in a persistent Faust table.

    :param results: async stream of SentimentResult records
    """
    async for result in results:
        # Increment the count for this sentiment label.
        sentiment_counts[result.predicted_sentiment] += 1

print("Table:", sentiment_counts)

# %% [markdown]
# ## 6. Running the Worker
#
# The Faust worker runs as a long-lived process in a terminal — not inside a notebook.
# Start it with:
#
# ```bash
# # Terminal 1: start Kafka
# docker compose up -d
#
# # Terminal 2: start the Faust worker
# python3 -m faust -A faust_app worker -l info
#
# # Terminal 3: send tweets into Kafka
# python3 tweet_producer.py
# ```
#
# Once the worker is running you will see `SentimentResult` objects printed
# as each tweet flows through the pipeline.
#
# For the complete real-world example, see `faust.example.ipynb`.
