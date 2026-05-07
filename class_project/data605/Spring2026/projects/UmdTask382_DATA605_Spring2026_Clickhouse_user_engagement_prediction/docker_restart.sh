#!/usr/bin/env bash
set -euo pipefail

# One-command, linear run:
# - wipe volumes (ClickHouse + Grafana)
# - rebuild + start containers
# - wait for ClickHouse + Grafana readiness
# - create schema + ingest data (docker_ingest.sh)
# - execute notebooks (nbconvert)
# - print URLs

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

CLICKHOUSE_USER="${CLICKHOUSE_USER:-default}"
CLICKHOUSE_PASSWORD="${CLICKHOUSE_PASSWORD:-password}"
CLICKHOUSE_DB="${CLICKHOUSE_DB:-ecomm}"

echo "==> Hard reset (docker compose down -v)"
docker compose down -v

echo "==> Build + start containers"
docker compose up -d --build

echo "==> Waiting for ClickHouse to be ready..."
for i in {1..60}; do
  if docker compose exec -T clickhouse clickhouse-client \
    --user "${CLICKHOUSE_USER}" --password "${CLICKHOUSE_PASSWORD}" \
    --query "SELECT 1" >/dev/null 2>&1; then
    echo "ClickHouse is ready."
    break
  fi
  sleep 2
  if [[ $i -eq 60 ]]; then
    echo "ERROR: ClickHouse did not become ready in time" >&2
    exit 1
  fi
done

echo "==> Waiting for Grafana to be ready..."
for i in {1..60}; do
  if curl -sS "http://localhost:3000/api/health" | grep -q ok; then
    echo "Grafana is ready."
    break
  fi
  sleep 2
  if [[ $i -eq 60 ]]; then
    echo "ERROR: Grafana did not become ready in time" >&2
    exit 1
  fi
done

echo "==> Ingesting data via docker_ingest.sh (this can take a while)"
./docker_ingest.sh

# echo "==> Executing notebooks (nbconvert --execute)"
# docker compose exec -T notebook bash -lc \
#   "jupyter nbconvert --execute --to notebook --inplace notebooks/clickhouse.API.ipynb"

# docker compose exec -T notebook bash -lc \
#   "jupyter nbconvert --execute --to notebook --inplace notebooks/clickhouse.example.ipynb"

echo
echo "==> Done."
echo "Grafana: http://localhost:3000 (admin/admin)"
echo "Jupyter: http://localhost:8888 (check docker logs for token)"
echo

