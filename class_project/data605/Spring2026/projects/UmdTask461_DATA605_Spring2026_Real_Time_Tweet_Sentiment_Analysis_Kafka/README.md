# Real-Time Tweet Sentiment Analysis using Apache Kafka and HuggingFace Transformers

## Author
- **Name**: Aashish Vinod
- **Course**: DATA605 Spring 2026
- **GitHub**: @aashishvinod
- **Project**: UmdTask461_DATA605_Spring2026_Real_Time_Tweet_Sentiment_Analysis_Kafka

## Project Overview

This project builds a real-time tweet sentiment analysis pipeline using Apache Kafka
for stream ingestion and a pre-trained HuggingFace transformer model
(cardiffnlp/twitter-roberta-base-sentiment) for sentiment classification.

Tweets from the Sentiment140 dataset (1.6M labeled tweets) are published to a Kafka
topic by a producer. A Kafka consumer reads the stream, runs each tweet through the
sentiment model, and classifies it as positive, negative, or neutral in real time.
Results are aggregated and visualized using Spark SQL, matplotlib, and a live
Streamlit dashboard.

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
  Streamlit Dashboard + Visualizations
```

## Description of Files

- `Dockerfile`
  - Docker image configuration with Python 3.11, Java, PyTorch, and HuggingFace

- `docker-compose.yml`
  - Orchestrates 3 containers: Zookeeper, Kafka broker, and JupyterLab

- `requirements.txt`
  - All pinned Python dependencies for the project

- `kafka_sentiment_utils.py`
  - Core utility functions: load_sentiment140(), preprocess_tweet(),
    create_tweet_event(), compute_sentiment_stats(), format_sentiment_summary()

- `kafka_sentiment.API.ipynb`
  - API reference notebook documenting each component individually:
    dataset loading, preprocessing, HuggingFace model, Kafka producer/consumer

- `kafka_sentiment.example.ipynb`
  - Full pipeline demo notebook running end-to-end sentiment analysis

- `dashboard.py`
  - Live Streamlit dashboard with real-time sentiment metrics, pie chart,
    and trend visualization

- `README.md`
  - This documentation file

- `docker_build.sh`
  - Script to build the Docker container image

- `docker_bash.sh`
  - Script to launch an interactive bash shell inside the container

- `docker_jupyter.sh`
  - Script to launch JupyterLab inside the container

- `docker_name.sh`
  - Configuration file defining Docker image naming variables

- `docker_clean.sh`
  - Script to remove Docker images for this project

- `docker_cmd.sh`
  - Script to execute arbitrary commands inside the container

- `docker_exec.sh`
  - Script to attach to a running container

- `docker_push.sh`
  - Script to push the Docker image to a registry

- `run_jupyter.sh`
  - Script to start JupyterLab server inside the container

- `utils.sh`
  - Bash utility library used by all docker_*.sh scripts

- `version.sh`
  - Script to report Python, pip, and Jupyter version information

- `bashrc`
  - Bash configuration file for the container environment

- `etc_sudoers`
  - Sudoers configuration for container permissions

- `copy_docker_files.py`
  - Python script for copying Docker configuration files

## Dataset

**Sentiment140**
- Source: Kaggle (https://www.kaggle.com/datasets/kazanova/sentiment140)
- Size: 1.6 million tweets
- Labels: 0 = negative, 4 = positive
- Access: Free download with Kaggle account
- Note: The dataset file is excluded from the repository via .gitignore due to
  its size (228MB). Download it from Kaggle and place it in the project folder
  before running.

## Model

**cardiffnlp/twitter-roberta-base-sentiment**
- Pre-trained RoBERTa model fine-tuned on approximately 58 million tweets
- Labels: LABEL_0 = negative, LABEL_1 = neutral, LABEL_2 = positive
- Source: HuggingFace Model Hub (free, no API key needed)
- Size: approximately 499MB (downloaded automatically on first run)

## How to Run

### Step 1: Download the dataset
Download `training.1600000.processed.noemoticon.csv` from Kaggle and place it
in this project directory.

### Step 2: Build the Docker image
```bash
> docker-compose build
```

### Step 3: Start all services
```bash
> docker-compose up -d
```

### Step 4: Verify all containers are running
```bash
> docker-compose ps
```
You should see Zookeeper, Kafka, and Jupyter all showing status "Up".

### Step 5: Open JupyterLab
Open your browser and go to:
```
http://localhost:8888
```

### Step 6: Run the notebooks
1. Open `kafka_sentiment.API.ipynb` and run all cells to understand each component
2. Open `kafka_sentiment.example.ipynb` and run all cells for the full pipeline demo

### Step 7: Run the Streamlit dashboard
In the JupyterLab terminal run:
```bash
> streamlit run /app/dashboard.py --server.port 8502 --server.address 0.0.0.0
```
Then open `http://localhost:8502` in your browser and click Run Pipeline.

### Step 8: Stop all services
```bash
> docker-compose down
```

## Workflows

- Build the container:
  ```bash
  > docker_build.sh
  ```

- Start JupyterLab:
  ```bash
  > docker_jupyter.sh
  # Go to localhost:8888
  ```

- Open a bash shell inside the container:
  ```bash
  > docker_bash.sh
  ```

- Check versions:
  ```bash
  > version.sh
  ```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| kafka-python | 2.0.2 | Kafka producer and consumer |
| transformers | 4.35.0 | HuggingFace sentiment model |
| torch | 2.1.0 | PyTorch backend for transformers |
| pyspark | 3.5.1 | Spark SQL and aggregations |
| pandas | 2.1.0 | Data manipulation |
| numpy | 1.26.0 | Numerical computing |
| matplotlib | 3.7.0 | Visualization |
| seaborn | 0.13.0 | Statistical visualization |
| wordcloud | 1.9.2 | Word cloud visualization |
| streamlit | 1.28.0 | Live dashboard |
| plotly | 6.7.0 | Interactive charts in dashboard |
| scikit-learn | 1.3.0 | Model evaluation metrics |
| findspark | 2.0.1 | PySpark initialization in Jupyter |
| tqdm | 4.66.1 | Progress bars |

## Results

From a full pipeline run on 500 tweets from Sentiment140:

| Metric | Value |
|--------|-------|
| Tweets produced | 500 |
| Tweets consumed | 500 |
| Positive | 184 (36.8%) |
| Negative | 168 (33.6%) |
| Neutral | 148 (29.6%) |
| Binary accuracy (RoBERTa) | 81.82% |
| DistilBERT accuracy (comparison) | 73.00% |
| Anomalies detected | 56 |
| Kafka throughput | up to 5732 tweets/sec |

## Architectural Decisions

### Why Apache Kafka?
Kafka was chosen as the message broker because it provides high-throughput,
fault-tolerant, and persistent message streaming. Unlike a simple queue, Kafka
retains all messages until the retention period expires, which allows multiple
consumers to read the same data independently. This is critical for a real-time
sentiment monitoring system where you may want to replay events for debugging.

### Why RoBERTa over other models?
The cardiffnlp/twitter-roberta-base-sentiment model was chosen because it is
specifically trained on 58 million tweets, making it well-suited for informal
Twitter language including abbreviations, hashtags, and slang. General-purpose
models trained on formal text tend to perform worse on tweets.

### Why Spark for aggregations?
PySpark was used for the aggregation layer because it provides a SQL interface
for querying large datasets and scales horizontally. While pandas would work for
500 tweets, Spark allows the same code to scale to millions of tweets without
modification.

### Why Streamlit for the dashboard?
Streamlit was chosen for the dashboard because it allows building interactive
web applications entirely in Python without requiring JavaScript or HTML knowledge.
The dashboard updates in real time as tweets are classified, providing the live
visualization required by the project description.

## Challenges and Solutions

### Challenge 1: Docker networking
When Kafka runs inside a Docker container, other containers cannot connect to it
using localhost:9092. The correct address is kafka:29092 using the internal Docker
network service name. This caused NoBrokersAvailable errors until the broker
address was corrected in the notebook configuration.

### Challenge 2: Kafka topic retention
Kafka retains all messages by default until the retention period expires. After
multiple test runs, the consumer was reading thousands of old messages from previous
runs. The solution was to delete and recreate the Kafka topic at the start of each
pipeline run to ensure only fresh tweets are processed.

### Challenge 3: Model label mapping
The cardiffnlp model returns LABEL_0, LABEL_1, and LABEL_2 instead of
human-readable labels. A mapping dictionary was created in kafka_sentiment_utils.py
to translate these to negative, neutral, and positive respectively.

### Challenge 4: Sentiment140 binary labels
The Sentiment140 dataset only has positive and negative labels (0 and 4). The
RoBERTa model also predicts neutral which the dataset does not have. Accuracy is
therefore measured only on positive and negative predictions, ignoring tweets
classified as neutral.
