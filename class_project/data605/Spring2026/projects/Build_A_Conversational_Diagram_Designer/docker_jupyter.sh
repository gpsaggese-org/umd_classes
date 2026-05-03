#!/bin/bash
# Launch Jupyter notebook inside the Docker container.
set -e
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
IMAGE_NAME="cdd_project"
echo "Starting Jupyter notebook on http://localhost:8888 ..."
docker run --rm -it \
    -p 8888:8888 \
    -v "$SCRIPT_DIR":/app \
    --env-file "$SCRIPT_DIR/.env" \
    $IMAGE_NAME
