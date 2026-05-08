# Real-Time Tweet Sentiment Analysis using Apache Kafka and HuggingFace Transformers

## Author
- **Name**: Aashish Vinod
- **Course**: DATA605 Spring 2026
- **Project**: Real-Time Sentiment Analysis on Tweets using Apache Kafka

## Project Overview

This project builds a real-time tweet sentiment analysis pipeline using Apache Kafka
for stream ingestion and a pre-trained HuggingFace transformer model
(`cardiffnlp/twitter-roberta-base-sentiment`) for sentiment classification.

Tweets from the Sentiment140 dataset (1.6M labeled tweets) are published to a Kafka
topic by a producer. A Kafka consumer reads the stream, runs each tweet through the
sentiment model, and classifies it as positive, negative, or neutral in real time.
Results are aggregated and visualized using Spark SQL and matplotlib.

## Architecture

```
Sentiment140 Dataset (1.6M tweets)
        |
        v
  Kafka Producer
  (kafka-python)
        |
        v
   Kafka Topic: tweets
   (3 partitions)
        |
        v
  Kafka Consumer
        |
        v
  HuggingFace Sentiment Model
  (cardiffnlp/twitter-roberta-base-sentiment)
        |
        v
  Real-Time Classification
  (positive / negative / neutral)
        |
        v
  Spark SQL + Aggregations
        |
        v
  Visualizations + Accuracy Analysis
```

## Project Structure

```
sentiment_project/
 Dockerfile                      # Docker image configuration
 docker-compose.yml              # Zookeeper + Kafka + Jupyter
 requirements.txt                # Python dependencies
 kafka_sentiment_utils.py        # Core utility functions
 kafka_sentiment.API.ipynb       # API reference notebook
 kafka_sentiment.example.ipynb   # Full pipeline demo notebook
 README.md                       # This file
```

## Dataset

**Sentiment140**
- Source: Kaggle (https://www.kaggle.com/datasets/kazanova/sentiment140)
- Size: 1.6 million tweets
- Labels: 0 = negative, 4 = positive
- Access: Free download with Kaggle account

## Model

**cardiffnlp/twitter-roberta-base-sentiment**
- Pre-trained RoBERTa model fine-tuned on ~58M tweets
- Labels: LABEL_0 = negative, LABEL_1 = neutral, LABEL_2 = positive
- Source: HuggingFace Model Hub (free, no API key needed)

## How to Run

### Step 1: Place the dataset
Copy `training.1600000.processed.noemoticon.csv` into this project folder.

### Step 2: Build Docker image
```bash
docker-compose build
```

### Step 3: Start all services
```bash
docker-compose up -d
```

### Step 4: Open Jupyter Lab
```
http://localhost:8888
```

### Step 5: Run the notebooks
1. `kafka_sentiment.API.ipynb` — understand each component
2. `kafka_sentiment.example.ipynb` — full pipeline demo

### Step 6: Stop services
```bash
docker-compose down
```

## Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| kafka-python | 2.0.2 | Kafka producer/consumer |
| transformers | 4.35.0 | HuggingFace sentiment model |
| torch | 2.1.0 | PyTorch backend for transformers |
| pyspark | 3.5.1 | Spark SQL and aggregations |
| pandas | 2.1.0 | Data manipulation |
| numpy | 1.26.0 | Numerical computing |
| matplotlib | 3.7.0 | Visualization |
| seaborn | 0.13.0 | Statistical visualization |
| wordcloud | 1.9.2 | Word cloud visualization |
