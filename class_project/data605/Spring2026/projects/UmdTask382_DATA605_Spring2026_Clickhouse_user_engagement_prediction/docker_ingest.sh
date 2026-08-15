#!/usr/bin/env bash
set -euo pipefail

# - starts ClickHouse
# - creates DB/tables/materialized view
# - ingests data/2019-Oct.csv using clickhouse-client (fast)
# - prints row counts

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

CLICKHOUSE_USER="${CLICKHOUSE_USER:-default}"
CLICKHOUSE_PASSWORD="${CLICKHOUSE_PASSWORD:-password}"
CLICKHOUSE_DB="${CLICKHOUSE_DB:-ecomm}"

DATA_FILE="${DATA_FILE:-data/2019-Oct.csv}"

if [[ ! -f "$DATA_FILE" ]]; then
  echo "ERROR: data file not found: $DATA_FILE" >&2
  exit 1
fi

echo "Starting ClickHouse container..."
docker compose up -d clickhouse

echo "Creating schema (raw + typed + MV)..."
docker compose exec -T clickhouse clickhouse-client \
  --user "$CLICKHOUSE_USER" --password "$CLICKHOUSE_PASSWORD" \
  --multiquery \
  --query "
CREATE DATABASE IF NOT EXISTS ${CLICKHOUSE_DB};
USE ${CLICKHOUSE_DB};

DROP TABLE IF EXISTS events_raw;
CREATE TABLE events_raw
(
  event_time String,
  event_type LowCardinality(String),
  product_id UInt64,
  category_id UInt64,
  category_code Nullable(String),
  brand Nullable(String),
  price Float32,
  user_id UInt64,
  user_session String
)
ENGINE = MergeTree
ORDER BY (user_session);

DROP TABLE IF EXISTS events_typed;
CREATE TABLE events_typed
(
  event_time_dt DateTime64(0, 'UTC'),
  event_date Date,
  event_type LowCardinality(String),
  product_id UInt64,
  category_id UInt64,
  category_code Nullable(String),
  brand Nullable(String),
  price Float32,
  user_id UInt64,
  user_session String
)
ENGINE = MergeTree
PARTITION BY event_date
ORDER BY (user_session, event_time_dt);

DROP VIEW IF EXISTS mv_events_raw_to_typed;
CREATE MATERIALIZED VIEW mv_events_raw_to_typed
TO events_typed
AS
SELECT
  parseDateTimeBestEffortOrNull(replaceAll(event_time, ' UTC', '')) AS event_time_dt,
  toDate(parseDateTimeBestEffortOrNull(replaceAll(event_time, ' UTC', ''))) AS event_date,
  event_type,
  product_id,
  category_id,
  nullIf(category_code, '') AS category_code,
  nullIf(brand, '') AS brand,
  price,
  user_id,
  user_session
FROM events_raw
WHERE event_time_dt IS NOT NULL;
"

echo "Ingesting $DATA_FILE into ${CLICKHOUSE_DB}.events_raw ..."
docker compose exec -T clickhouse clickhouse-client \
  --user "$CLICKHOUSE_USER" --password "$CLICKHOUSE_PASSWORD" \
  --query "INSERT INTO ${CLICKHOUSE_DB}.events_raw FORMAT CSVWithNames" \
  < "$DATA_FILE"

echo "Counts after ingest:"
docker compose exec -T clickhouse clickhouse-client \
  --user "$CLICKHOUSE_USER" --password "$CLICKHOUSE_PASSWORD" \
  --query "SELECT count() AS events_raw_rows FROM ${CLICKHOUSE_DB}.events_raw"

docker compose exec -T clickhouse clickhouse-client \
  --user "$CLICKHOUSE_USER" --password "$CLICKHOUSE_PASSWORD" \
  --query "SELECT count() AS events_typed_rows FROM ${CLICKHOUSE_DB}.events_typed"

echo "Done ingesting. Next: run notebooks/clickhouse.API.ipynb (fast) and notebooks/clickhouse.example.ipynb."