#!/usr/bin/env bash
set -euo pipefail

VERSION="${1:-1.0.0}"
export IMAGE="noesis_platform:local-${USER}-${VERSION}"
echo "Using IMAGE=${IMAGE}"

COMPOSE_BASE="devops/compose/tmp.docker-compose.yml"
COMPOSE_OVERRIDE="devops/compose/docker-compose.noesis.yml"
ENV_FILE="devops/env/default.env"

[[ -f ${COMPOSE_BASE} ]] || { echo "Error:  ${COMPOSE_BASE} missing"; exit 1; }

COMPOSE_FLAGS=(
  --env-file "${ENV_FILE}"
  -f "${COMPOSE_BASE}"
  -f "${COMPOSE_OVERRIDE}"
)

cleanup() {
  echo -e "Stopping noesis containers…"
  docker compose "${COMPOSE_FLAGS[@]}" \
      down noesis_api \
      2>/dev/null || true
}
trap cleanup INT TERM

# Start container.
docker compose "${COMPOSE_FLAGS[@]}" \
    up -d noesis_api

# Show status.
docker compose "${COMPOSE_FLAGS[@]}" \
    ps noesis_api

# Show API logs.
docker compose "${COMPOSE_FLAGS[@]}" \
    logs -f --tail=20 noesis_api
