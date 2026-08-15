# Understanding Project Steps & Tutorial Draft

### The project pipeline:
CSV / Twitter API
      ↓
tweet_producer.py
      ↓
Kafka topic: "tweets"
      ↓
Faust consumer / stream processor
      ↓
Sentiment model
      ↓
Output: positive / negative / neutral
      ↓
Dashboard or database

## Setting up Kafka Tweet Streaming:
1. docker-compose.yml: This file starts Kafka using Docker.
- Zookeeper manages Kafka broker metadata. Older Kafka setups use it to coordinate brokers.
- The Kafka broker is the actual message server.
- The port 9092 is exposed on the local computer at localhost:9092.
    - KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092 tells Kafka that clients should connect through localhost:9092.
- KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1 is used because this is a single-node local Kafka setup (this replication would be higher in production).

2. requirements.txt
- faust-streaming: Used for real-time stream processing from Kafka.
- kafka-python: Used in tweet_producer.py to send tweets into Kafka.
- transformers, torch: Used for Hugging Face sentiment analysis models.
- streamlit: (could be used) for building the dashboard.
- pandas, numpy, matplotlib, seaborn: (could be used) for batch analysis, evaluation, and visualization.
3. tweet_producer.py:
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
    - {
    "sentiment": "0",
    "id": "1467810369",
    "date": "...",
    "user": "username",
    "text": "tweet text here"
    }
    - Sentiment labels are as follows:
        - 0 = negative
        - 2 = neutral
        - 4 = positive
- Tweets are sent to Kafka via the producer send() function with the Kafka topic names "tweets".
- time.sleep(0.1) simulates real-time streaming by waiting 0.1 seconds between tweets.


## Create topics:
** Note: Example using kafka container name umdtask425_data605_spring2026_faust-kafka-1

`docker exec -it umdtask425_data605_spring2026_faust-kafka-1 kafka-topics   --create   --topi
c tweets   --bootstrap-server localhost:9092   --partitions 1   --replication-factor 1`

## Check if they exist
`docker exec -it umdtask425_data605_spring2026_faust-kafka-1 kafka-topics \
--list \
--bootstrap-server localhost:9092`

## Run the producer and verify Kafka is receiving messages
1. python tweet_producer.py
2. `docker exec -it umdtask425_data605_spring2026_faust-kafka-1 kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic tweets \
  --from-beginning`

## Run the Faust App
** Note: Kafka is installed on Python3.11, and the latest stable Python release is 3.14 as of April 2026. 
In a new terminal, run the following:
1. Create Python3.11 conda environment: `conda create -n faust311 python=3.11 -y`
2. Activate the conda environment: `conda activate faust311`
3. Upgrade pip: `pip install --upgrade pip`
4. Install Faust and sentiment analysis dependencies: `pip install faust-streaming kafka-python transformers torch "aiokafka<0.11"`
5. Run the Faust App: `faust -A faust_app worker -l info`

## Produce tweets
In a new terminal, navigate to the project root directory, and run the following:
1. Create a new Python virtual environment: `python3 -m venv .venv`
2. Activate the virtual environment: `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the tweets producer script: `python tweet_producer.py` 

## Observe Output
1. The docker container will show the produced tweets with simulated streaming.
2. The faust app terminal will show the Sentiment Result including the start of the tweet content, original sentiment, predicted sentiment, and confidence.