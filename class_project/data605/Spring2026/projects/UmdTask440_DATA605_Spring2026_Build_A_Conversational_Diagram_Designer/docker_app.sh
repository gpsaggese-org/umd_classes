#!/bin/bash
# Launch the CDD web app (FastAPI backend + React frontend).
# Access at http://localhost:8000
set -e
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
IMAGE_NAME="cdd_project"
echo "Starting CDD app on http://localhost:8000 ..."
docker run --rm -it \
    -p 8000:8000 \
    -v "$SCRIPT_DIR":/app \
    --env-file "$SCRIPT_DIR/.env" \
    $IMAGE_NAME \
    uvicorn cdd_server:app --host 0.0.0.0 --port 8000
