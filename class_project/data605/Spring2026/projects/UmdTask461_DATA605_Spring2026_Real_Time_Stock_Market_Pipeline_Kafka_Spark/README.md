# Real-Time Stock Market Pipeline using Apache Kafka and Spark Structured Streaming

## Author
- **Name**: Aashish Vinod
- **Course**: DATA605 Spring 2026
- **GitHub Issue**: [#461](https://github.com/gpsaggese/gpsaggese.github.io/issues/461)
- **PR**: [#478](https://github.com/gpsaggese/gpsaggese.github.io/pull/478)

## Project Overview
This project builds a **real-time stock market data pipeline** using:
- **Apache Kafka** — distributed message broker for streaming stock events
- **Apache Spark Structured Streaming** — real-time stream processing and windowed aggregations
- **Docker** — runs everything locally in a reproducible environment
- **Jupyter Notebooks** — interactive exploration and demonstration

The pipeline simulates live stock price events for 5 major stocks (AAPL, GOOGL, MSFT, AMZN, TSLA),
publishes them to a Kafka topic, and processes them with Spark to compute moving averages and price alerts.

## Architecture
```
Stock Price Simulator
        |
        v
  Kafka Producer
        |
        v
   Kafka Topic (stock-prices)
        |
        v
Spark Structured Streaming Consumer
        |
        v
Windowed Aggregations (Moving Averages, Price Alerts)
        |
        v
Results and Visualizations
```

## Project Structure
```
UmdTask461_DATA605_Spring2026_Real_Time_Stock_Market_Pipeline_Kafka_Spark/
├── Dockerfile                   # Docker image configuration
├── docker-compose.yml           # Multi-container setup (Kafka + Zookeeper + Jupyter)
├── requirements.txt             # Python dependencies
├── kafka_spark_utils.py         # Utility functions for the pipeline
├── kafka_spark.API.ipynb        # API reference notebook
├── kafka_spark.example.ipynb    # Full pipeline demonstration notebook
└── README.md                    # This file
```

## Prerequisites
- Docker Desktop installed and running
- Docker Compose v2+
- At least 8GB RAM available for Docker

## How to Run

### Step 1: Build the Docker image
```bash
docker-compose build
```

### Step 2: Start all services (Kafka + Zookeeper + Jupyter)
```bash
docker-compose up
```

### Step 3: Open Jupyter Lab
Open your browser and go to:
```
http://localhost:8888
```

### Step 4: Run the notebooks
1. Start with `kafka_spark.API.ipynb` to understand the APIs
2. Run `kafka_spark.example.ipynb` for the full pipeline demo

### Step 5: Stop all services
```bash
docker-compose down
```

## Key Concepts

### Apache Kafka
- **Producer**: Publishes stock price events to a Kafka topic
- **Topic**: `stock-prices` stores all incoming stock events
- **Consumer**: Reads events from the topic for processing
- **Broker**: Manages message storage and delivery

### Apache Spark Structured Streaming
- **Streaming DataFrame**: Continuously updated data from Kafka
- **Windowed Aggregations**: Compute moving averages over time windows
- **Price Alerts**: Trigger alerts when price moves beyond threshold

### Key Parameters
| Parameter | Value | Description |
|-----------|-------|-------------|
| Kafka Topic | stock-prices | Topic for stock events |
| Window Size | 5 events | Moving average window |
| Alert Threshold | 1.5% | Price movement alert threshold |
| Stocks | AAPL, GOOGL, MSFT, AMZN, TSLA | Simulated stocks |

## Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| kafka-python | 2.0.2 | Kafka producer/consumer |
| pyspark | 3.5.1 | Spark Structured Streaming |
| pandas | 2.1.0 | Data manipulation |
| numpy | 1.24.0 | Numerical computing |
| matplotlib | 3.7.0 | Visualization |
| seaborn | 0.12.2 | Statistical visualization |
| findspark | 2.0.1 | Spark initialization |
