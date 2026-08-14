#!/bin/bash

REPO_NAME=data605_class_project
IMAGE_NAME=huggingface_text_classifier
FULL_IMAGE_NAME=$REPO_NAME/$IMAGE_NAME

# Named volume for HuggingFace model downloads (shared across all containers).
HF_CACHE_VOLUME=hf_cache

# Default Jupyter port (override with JUPYTER_PORT env var if needed).
JUPYTER_PORT=${JUPYTER_PORT:-8888}
