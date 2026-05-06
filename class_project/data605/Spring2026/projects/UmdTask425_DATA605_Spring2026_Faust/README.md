# Faust Tutorial

Real-time tweet sentiment analysis using Faust stream processing and Apache Kafka.

## Quick Start

- `cd` into the project folder
- Start Kafka: `docker compose up -d`
- Install dependencies: `pip install -r requirements.txt`
- Launch Jupyter: `./docker_jupyter.sh` (or `jupyter notebook` locally)

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

# Terminal 4 (optional) — Live dashboard
python3 -m streamlit run dashboard.py
```

## Project Files

| File | Purpose |
|---|---|
| `faust_utils.py` | Reusable helper functions for all notebooks |
| `faust.API.ipynb` | Faust API walkthrough |
| `faust.example.ipynb` | End-to-end sentiment analysis demo |
| `faust_app.py` | Faust stream processing worker |
| `tweet_producer.py` | Kafka producer that streams CSV tweets |
| `dashboard.py` | Streamlit live sentiment dashboard |
| `docker-compose.yml` | Kafka + Zookeeper setup |
