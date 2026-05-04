import csv 
import json 
import time 
from kafka import KafkaProducer 

# Connect to Kafka.
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Define the CSV file path.
csv_file = 'training.1600000.processed.noemoticon.csv'

def read_tweets(file_path):
    with open(file_path, encoding='latin-1') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            tweet = {
                'sentiment': row[0],
                'id': row[1],
                'date': row[2],
                'user': row[4],
                'text': row[5]
            }
            producer.send('tweets', tweet)
            print(f"Sent tweet {i}: {tweet['text'][:50]}")
            # simulate real-time stream by waiting 0.1 seconds
            time.sleep(0.1)
            # stop after 200 tweets for testing
            if i >= 200:
                break

if __name__ == '__main__':
    read_tweets(csv_file)
    print("done")
