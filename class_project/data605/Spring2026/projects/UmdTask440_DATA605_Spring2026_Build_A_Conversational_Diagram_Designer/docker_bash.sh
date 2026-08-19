#!/bin/bash
# Open a bash shell inside the Docker container.
set -e
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
IMAGE_NAME="cdd_project"
docker run --rm -it \
    -p 8888:8888 -p 8000:8000 \
    -v "$SCRIPT_DIR":/app \
    --env-file "$SCRIPT_DIR/.env" \
    $IMAGE_NAME /bin/bash
