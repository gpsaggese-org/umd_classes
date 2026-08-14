## ClickHouse (Beginner-Friendly) — Session Purchase Prediction

This project uses **ClickHouse** (a fast, column-oriented OLAP database) to ingest and analyze an e-commerce event log, then builds a **training table** that a Python notebook uses to train ML models to predict whether a session will eventually contain a purchase.

**Dataset**: https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store

### What is ClickHouse?

- **OLAP vs OLTP**: ClickHouse is built for analytics (large scans + aggregations), not frequent row-by-row updates.
- **Column-oriented**: It reads only the columns your query needs, which is why group-bys and filters can be very fast.
- **MergeTree engine**: Most tables here use `MergeTree`, where performance depends heavily on how you choose:
  - **`PARTITION BY`** (how data is split into parts, usually time-based)
  - **`ORDER BY`** (how data is sorted on disk; this is key for fast filtering)
- **Materialized Views (MV)**: An MV can turn “raw” ingests into a clean/typed table automatically, acting like a lightweight pipeline.

### Project flow (what happens where)

- **ClickHouse does**: ingestion, typing/cleaning, OLAP analytics, labeling, feature engineering, and building a stable training table.
- **Python does**: model training (Logistic Regression + XGBoost), evaluation, and writing predictions back to ClickHouse for dashboards.

### Repository quickstart (recommended order)

1) **Start containers**

```bash
docker compose up -d
```

2) **Ingest the dataset into ClickHouse (fast, reproducible)**

```bash
./docker_ingest.sh
```

What `docker_ingest.sh` creates:
- **Database**: `ecomm` (configurable)
- **Raw table**: `events_raw` (keeps `event_time` as a string)
- **Typed table**: `events_typed` (parses timestamps + adds `event_date`)
- **Materialized view**: `mv_events_raw_to_typed` (raw → typed pipeline)

3) **Run the notebooks**

- **Notebook A (ClickHouse-first / feature engineering)**: `notebooks/clickhouse.API.ipynb`
  - Verifies ingestion, runs OLAP analytics, builds labels + features, and produces the training table `training_sessions_n5`.
- **Notebook B (ML)**: `notebooks/clickhouse.example.ipynb`
  - Trains models on `training_sessions_n5`, evaluates them, and writes predictions back to ClickHouse.

### Configuration (environment variables)

The Python notebooks connect using `clickhouse_utils.py`. You can override defaults using:

- **`CLICKHOUSE_HOST`** (default: `clickhouse`)
- **`CLICKHOUSE_PORT`** (default: `9000`)
- **`CLICKHOUSE_USER`** (default: `default`)
- **`CLICKHOUSE_PASSWORD`** (default: empty string in Python; `docker_ingest.sh` defaults to `password`)
- **`CLICKHOUSE_DB`** (default: `ecomm`)

If you are running everything via Docker Compose as provided, the defaults should work.

### Tables you should know

- **`events_raw`**: raw CSV rows; minimal parsing; quick to ingest.
- **`events_typed`**: cleaned/typed events with `event_time_dt` and `event_date`.
- **`session_outcomes`**: one row per `user_session` with the label `has_purchase_in_session`.
- **`training_sessions_n5`**: one row per session with features computed from the **first N events** (N=5 by default).
- **`session_purchase_predictions`**: model scores written back from the ML notebook.

### Common beginner questions

- **Why not ingest the CSV with pandas?**
  - The dataset is large; ingesting directly with ClickHouse is faster, more reproducible, and keeps notebooks lightweight.
- **Why do we need `events_typed`?**
  - Analytics is much easier and faster when timestamps are real `DateTime` and data is partitioned/sorted for common queries.

