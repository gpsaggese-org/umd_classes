#!/usr/bin/env bash

set -e

IMAGE_NAME="sdv-privacy-classification"

echo "Running Docker image: ${IMAGE_NAME}"
docker run --rm ${IMAGE_NAME}
