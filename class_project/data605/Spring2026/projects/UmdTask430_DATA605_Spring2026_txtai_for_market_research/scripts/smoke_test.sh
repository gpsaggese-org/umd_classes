#!/usr/bin/env bash
# End-to-end smoke test:
#   1. assume `docker-compose up -d` is already running (api + storage tiers)
#   2. ingest one ticker with --limit 1
#   3. backfill the txtai index from chunks
#   4. POST one query to /research and assert the answer is non-empty
#
# Usage:
#   > ./scripts/smoke_test.sh
#   > TICKER=MSFT ./scripts/smoke_test.sh

set -euo pipefail

TICKER="${TICKER:-AAPL}"
API_URL="${API_URL:-http://localhost:8000}"
QUERY="${QUERY:-What are the key risks discussed in the latest 10-K?}"

echo "[smoke] ensuring docker-compose stack is up..."
docker-compose ps --services --filter status=running | grep -q api \
  || (echo "[smoke] api service is not running. Start it with 'docker-compose up -d'." >&2; exit 1)

echo "[smoke] ingesting one filing for ${TICKER}..."
docker-compose exec -T api python -m scripts.run_sec_collector \
  --ticker "${TICKER}" \
  --filing-types 10-K \
  --limit 1

echo "[smoke] backfilling txtai index from chunks..."
docker-compose exec -T api python -m scripts.backfill_txtai_from_chunks --from-scratch

echo "[smoke] hitting ${API_URL}/research..."
RESPONSE=$(curl -sS -X POST "${API_URL}/research" \
  -H 'Content-Type: application/json' \
  -d "{\"query\": \"${QUERY}\"}")

echo "${RESPONSE}" | head -c 800
echo ""

# Pull the answer field via python (no jq dependency).
ANSWER=$(printf '%s' "${RESPONSE}" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("answer",""))')

if [ -z "${ANSWER}" ]; then
  echo "[smoke] FAIL: empty answer returned" >&2
  exit 1
fi

echo "[smoke] OK — answer length=${#ANSWER}"
