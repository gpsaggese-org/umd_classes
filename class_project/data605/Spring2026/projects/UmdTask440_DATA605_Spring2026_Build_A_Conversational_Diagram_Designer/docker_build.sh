#!/bin/bash
# Build the Docker image for the CDD project.
set -e
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
IMAGE_NAME="cdd_project"
echo "Building Docker image '$IMAGE_NAME'..."
docker build -t $IMAGE_NAME "$SCRIPT_DIR"
echo "Docker image '$IMAGE_NAME' built successfully."
