# Real-time tweet sentiment analysis pipeline built using Apache Kafka, Faust stream processing, and transformer-based sentiment analysis

The goal of this project is to simulate a real-time streaming system where tweets are continuously ingested, processed, classified into sentiment categories, and visualized live on a dashboard.

## Project Pipeline
CSV → `tweet_producer.py` → Kafka topic: `tweets` → Faust stream processor → Sentiment model → Output: positive/negative/neutral → Dashboard

The tweets are first sent into a Kafka topic using a Kafka producer script. Faust then consumes the streaming data from Kafka and performs sentiment analysis using a Hugging Face transformer model. Finally, the processed results are displayed through a live dashboard.

## Pre-requisites
Before running this project, make sure the following tools are available:

### Software Requirements
- Mac or Linux OS (assumed)
- Python 3.12+
- Docker and Docker Compose
- Git
- pip or conda package manager
- Jupyter Notebook or JupyterLab

### Python Libraries
Python dependencies can be installed with:
```bash
pip install -r requirements.txt
```

### Architecture Used
1. Kafka
2. Faust
3. Transformers
4. Streamlit

## Quick Start

- Launch Docker
- From the repo root, navigate to the project folder with: `cd class_project/data605/Spring2026/projects/UmdTask425_DATA605_Spring2026_Faust/`
- Start Kafka: `docker compose up -d`
- Install dependencies: `pip install -r requirements.txt`
- Launch Jupyter: `./docker_jupyter.sh` (or `jupyter notebook` locally)
- In the notebook choose: Kernel → Change Kernel → Python if not already chosen by default.

Open the notebooks in this order:

1. **`faust.API.ipynb`** — Learn the five core Faust concepts (App, Record, Topic, Agent, Table) with runnable examples. No Kafka required.
2. **`faust.example.ipynb`** — Run the full sentiment analysis pipeline: load tweets, classify sentiment, evaluate accuracy, and visualize results.

## Running the Full Pipeline

Open three terminal windows in the project folder:

```bash
# Terminal 1 — Kafka
docker compose up -d

# Terminal 2 — Faust worker
python3 -m faust -A faust_app worker -l info

# Terminal 3 — Tweet producer
python3 tweet_producer.py

# Terminal 4 — Live dashboard for visualization
python3 -m streamlit run dashboard.py
```

The dashboard opens automatically in your browser and updates every 2 seconds with:
- **Sentiment counts** — total tweets processed, broken down by positive, negative, and neutral
- **Bar chart** — live sentiment distribution
- **Recent tweets table** — the last 50 processed tweets with predicted sentiment and confidence score

## Project Files

### Files and their Purpose

| File | Purpose |
|---|---|
| `faust_utils.py` | Core reusable utility module containing Kafka, Faust, sentiment analysis, data loading, and visualization helper functions |
| `faust.API.ipynb` | Faust API walkthrough |
| `faust.example.ipynb` | End-to-end sentiment analysis demo |
| `faust_app.py` | Faust stream processing worker |
| `tweet_producer.py` | Kafka producer that streams CSV tweets |
| `dashboard.py` | Streamlit live sentiment dashboard |
| `docker-compose.yml` | Kafka + Zookeeper setup |
| `requirements.txt` | Python dependencies for the project |

### Core File Explanations
#### Setting up Kafka Tweet Streaming:
1. `docker-compose.yml`: This file starts Kafka using Docker.
- Zookeeper manages Kafka broker metadata. Older Kafka setups use it to coordinate brokers.
- The Kafka broker is the actual message server.
- The port 9092 is exposed on the local computer at localhost:9092.
    - KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092 tells Kafka that clients should connect through localhost:9092.
- KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1 is used because this is a single-node local Kafka setup (this replication would be higher in production).

2. `requirements.txt`
- faust-streaming: Used for real-time stream processing from Kafka.
- kafka-python: Used in tweet_producer.py to send tweets into Kafka.
- transformers, torch: Used for Hugging Face sentiment analysis models.
- streamlit: (could be used) for building the dashboard.
- pandas, numpy, matplotlib, seaborn: (could be used) for batch analysis, evaluation, and visualization.

3. `tweet_producer.py`
- reads tweets from a CSV file and sends them one-by-one into Kafka.
- value_serializer convets each Python dictionary into JSON bytes because Kafka messages are sent as bytes.
- Reads the tweet dataset, where each rows has these fields:
    - sentiment
    - id
    - date
    - query
    - user
    - text
- Each Kafka message is a JSON object that looks like:
    ```
    {
    "sentiment": "0",
    "id": "1467810369",
    "date": "...",
    "user": "username",
    "text": "tweet text here"
    }
    ```
    - Sentiment labels are as follows:
        - 0 = negative
        - 2 = neutral
        - 4 = positive
- Tweets are sent to Kafka via the producer send() function with the Kafka topic names `tweets`.
- `time.sleep(0.1)` simulates real-time streaming by waiting 0.1 seconds between tweets.

#### Create topics:
```
docker exec -it <kafka_container_name> kafka-topics \
--create \
--topic tweets \
--bootstrap-server localhost:9092 \
--partitions 1 \
--replication-factor 1
```

#### Check if the topics exist
```
docker exec -it <kafka_container_name> kafka-topics \
--list \
--bootstrap-server localhost:9092
```
#### Run Producer and Verify Kafka is Receiving the Messages
1. Run tweet producer: `python tweet_producer.py`
2. 
```
docker exec -it <kafka_container_name> kafka-console-consumer \
--bootstrap-server localhost:9092 \
--topic tweets \
--from-beginning
``` 

#### Run the Faust App
Run the Faust App: `faust -A faust_app worker -l info`

#### Produce tweets and verify with Kafka
In a new terminal, run the tweets producer script: `python tweet_producer.py`

#### Sentiment Analysis
1. `faust_utils.py`
This module centralizes reusable helper functions used throughout the project.

| Function                   | Purpose                                                          |
| -------------------------- | ---------------------------------------------------------------- |
| `create_faust_app()`       | Create and configure a Faust stream processing application       |
| `load_tweets()`            | Load tweet data from the Sentiment140 CSV dataset                |
| `tweets_to_dataframe()`    | Convert tweet dictionaries into Pandas DataFrames                |
| `create_kafka_producer()`  | Create a Kafka producer for sending JSON messages                |
| `send_tweets_to_kafka()`   | Stream tweets into a Kafka topic with simulated real-time delays |
| `create_kafka_consumer()`  | Create a Kafka consumer for reading Kafka messages               |
| `poll_sentiment_results()` | Read processed sentiment messages from Kafka into a DataFrame    |
| `load_sentiment_model()`   | Load the Hugging Face transformer sentiment analysis model       |
| `analyze_sentiment()`      | Predict sentiment and confidence for a single text input         |
| `analyze_tweets_batch()`   | Run sentiment analysis across a batch of tweets                  |
| `sentiment_summary()`      | Compute counts of sentiment labels                               |
| `accuracy_score()`         | Calculate prediction accuracy against original labels            |


The sentiment model used is: `cardiffnlp/twitter-roberta-base-sentiment-latest` which predicts sentiments with the following tags:
- negative
- neutral
- positive

#### Observe Output
1. The docker container will show the produced tweets with simulated streaming.
2. The faust app terminal will show the Sentiment Result including the start of the tweet content, original sentiment, predicted sentiment, and confidence.

#### Optional: Running Inside Docker

### Step 1: Build Docker Image
```bash
docker build -t gpsaggese/umd_project_template .
```
Expected output: 
```
Successfully built <image_id>
Successfully tagged gpsaggese/umd_project_template:latest
```

### Step 2: Launch Jupyter Notebook  via Docker
```bash
bash docker_jupyter.sh
```
Then open: http://localhost:8888/lab

**Note:** When running notebooks inside Docker, Kafka cannot be reached via 
`localhost`. Change `localhost` to `host.docker.internal` in `faust_utils.py`:
```python
# Change this:
bootstrap_servers: str = "localhost:9092"
# To this:
bootstrap_servers: str = "host.docker.internal:9092"
