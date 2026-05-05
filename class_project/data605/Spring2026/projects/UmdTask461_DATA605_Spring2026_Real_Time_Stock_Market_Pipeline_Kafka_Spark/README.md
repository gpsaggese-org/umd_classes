# Real-Time Stock Market Pipeline using Apache Kafka and Spark Structured Streaming

## Author
- **Name**: Aashish Vinod
- **Course**: DATA605 Spring 2026
- **GitHub Issue**: [#461](https://github.com/gpsaggese/gpsaggese.github.io/issues/461)
- **PR**: [#478](https://github.com/gpsaggese/gpsaggese.github.io/pull/478)

---

## Project Overview

This project builds a **real-time stock market data pipeline** that demonstrates how
Apache Kafka and Apache Spark Structured Streaming can be used together to ingest,
process, and analyze streaming financial data.

A Kafka producer simulates live stock price events for 5 major stocks (AAPL, GOOGL,
MSFT, AMZN, TSLA) and publishes them to a Kafka topic. A Spark Structured Streaming
consumer reads from the topic, computes windowed aggregations such as moving averages,
and generates price alerts when stocks move beyond a threshold. Everything runs
fully locally inside Docker containers.

---

## Architecture

```
Stock Price Simulator (Python)
        |
        v
  Kafka Producer
  (kafka-python)
        |
        v
   Kafka Topic: stock-prices
   (3 partitions, replication factor 1)
        |
        v
Spark Structured Streaming Consumer
(PySpark 3.5.1 + spark-sql-kafka connector)
        |
        v
  Windowed Aggregations
  - Moving Average (MA5, MA10)
  - Price Alerts (threshold: 1.0%)
  - Throughput Analysis
        |
        v
  Results + Visualizations
  (matplotlib, seaborn)
```

---

## Project Structure

```
UmdTask461_DATA605_Spring2026_Real_Time_Stock_Market_Pipeline_Kafka_Spark/
├── Dockerfile                    # Docker image: Python 3.11 + Java + PySpark + Jupyter
├── docker-compose.yml            # Multi-container: Zookeeper + Kafka + Jupyter
├── requirements.txt              # Python dependencies with pinned versions
├── kafka_spark_utils.py          # Core utility functions for the pipeline
├── kafka_spark.API.ipynb         # API reference notebook (how each component works)
├── kafka_spark.example.ipynb     # Full end-to-end pipeline demo notebook
└── README.md                     # This file
```

---

## Key Concepts

### Apache Kafka
Apache Kafka is a distributed event streaming platform. In this project:
- **Producer**: Simulates stock price events and publishes to the `stock-prices` topic
- **Topic**: `stock-prices` with 3 partitions for parallel processing
- **Consumer**: Reads events from the topic for downstream processing
- **Broker**: Runs inside Docker via `confluentinc/cp-kafka:7.4.0`
- **Zookeeper**: Manages Kafka broker metadata

### Apache Spark Structured Streaming
Spark Structured Streaming is a scalable, fault-tolerant stream processing engine. In this project:
- **Streaming DataFrame**: Continuously reads new events from Kafka
- **Schema**: Parses JSON events into typed columns (symbol, price, volume, timestamp)
- **Windowed Aggregations**: Groups events into 30-second windows with 10-second slides
- **Watermarking**: Handles late-arriving data with a 10-second watermark

### Moving Averages
Moving averages smooth out price fluctuations to reveal trends:
- **MA5**: Average of the last 5 price events per stock
- **MA10**: Average of the last 10 price events per stock
- When price crosses above MA5/MA10: potential uptrend signal
- When price crosses below MA5/MA10: potential downtrend signal

### Price Alerts
Alerts are triggered when a stock price moves beyond 1.0% from its base price:
- **UP alert**: price rose more than 1% above base
- **DOWN alert**: price fell more than 1% below base

---

## Prerequisites
- Docker Desktop installed and running (minimum 8GB RAM allocated)
- Docker Compose v2+
- Git Bash (Windows) or Terminal (Mac/Linux)

---

## How to Run

### Step 1: Clone and navigate to project folder
```bash
git clone https://github.com/aashishvinod/gpsaggese.github.io.git
cd class_project/data605/Spring2026/projects/UmdTask461_DATA605_Spring2026_Real_Time_Stock_Market_Pipeline_Kafka_Spark
```

### Step 2: Build Docker image
```bash
docker-compose build
```
Expected output: `Image ...jupyter Built`

### Step 3: Start all services
```bash
docker-compose up -d
```
Expected output: 3 containers started (zookeeper, kafka, jupyter)

### Step 4: Verify containers are running
```bash
docker-compose ps
```
All 3 services should show `Up` status.

### Step 5: Open Jupyter Lab
Open your browser and navigate to:
```
http://localhost:8888
```

### Step 6: Run the notebooks
1. Open `kafka_spark.API.ipynb` — run all cells to understand each API component
2. Open `kafka_spark.example.ipynb` — run all cells for the full pipeline demo

### Step 7: Stop all services
```bash
docker-compose down
```

---

## Results

### Pipeline Performance
| Metric | Value |
|--------|-------|
| Events produced | 200 |
| Events consumed | 205 |
| Producer throughput | ~7,650 events/sec |
| Consumer latency | ~8 seconds for 205 events |
| Price alerts triggered | 88 (42.9% alert rate) |

### Moving Average Results (sample run)
| Stock | Last Price | MA5 | MA10 |
|-------|-----------|-----|------|
| AAPL | $174.08 | $173.21 | $174.27 |
| GOOGL | $142.21 | $140.61 | $140.41 |
| MSFT | $374.33 | $375.77 | $378.52 |
| AMZN | $185.55 | $183.97 | $185.27 |
| TSLA | $253.96 | $250.64 | $249.40 |

### Price Alerts by Symbol (sample run)
| Stock | Alerts |
|-------|--------|
| AAPL | 20 |
| MSFT | 20 |
| AMZN | 18 |
| TSLA | 18 |
| GOOGL | 12 |

---

## Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| kafka-python | 2.0.2 | Kafka producer/consumer client |
| pyspark | 3.5.1 | Spark Structured Streaming engine |
| pandas | 2.1.0 | DataFrame operations and analysis |
| numpy | 1.26.0 | Numerical computing |
| matplotlib | 3.7.0 | Plotting and visualization |
| seaborn | 0.13.0 | Statistical visualization |
| yfinance | 0.2.28 | Real stock data (optional extension) |
| findspark | 2.0.1 | Spark session initialization helper |

---

## Design Decisions

### Why Kafka over direct streaming?
Kafka provides **fault tolerance** and **replay capability**. If the consumer crashes,
it can resume from its last committed offset. Direct streaming has no such guarantee.

### Why windowed aggregations over simple aggregations?
Windowed aggregations (30s window, 10s slide) give a **continuously updated view**
of recent price trends, which is more useful for real-time trading signals than
a static average over all historical data.

### Why Docker?
Docker ensures the pipeline runs identically on any machine regardless of OS or
installed software. The `docker-compose.yml` spins up Zookeeper, Kafka, and Jupyter
in a single command with all networking configured automatically.

### Trade-offs
- **Simplicity vs Realism**: Stock prices are simulated with ±2% random walks. Real
  production systems would use websocket feeds from brokers like Alpaca or Polygon.
- **Local vs Distributed**: Everything runs on one machine. In production, Kafka would
  have multiple brokers and Spark would run on a cluster (YARN/Kubernetes).
- **Python Kafka vs Spark Kafka source**: We use both kafka-python (for producer/consumer
  demos) and the Spark-Kafka connector (for structured streaming). Each has its use case.
