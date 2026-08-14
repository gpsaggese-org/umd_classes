#!/usr/bin/env bash

set -e

IMAGE_NAME="sdv-privacy-classification"

echo "Building Docker image: ${IMAGE_NAME}"
docker build -t ${IMAGE_NAME} .

echo "Docker image built successfully."
