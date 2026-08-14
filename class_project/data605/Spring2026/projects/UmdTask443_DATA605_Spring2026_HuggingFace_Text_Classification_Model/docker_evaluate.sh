#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/docker_utils.sh"
load_docker_vars

CONTAINER_NAME="${IMAGE_NAME}_evaluate"
OPTS=$(base_run_opts "$CONTAINER_NAME")

echo "Running evaluation..."
echo "    Results will be saved to ./results/ on your host."
echo ""

run "docker run $OPTS $FULL_IMAGE_NAME python project_files/scripts/evaluate_model.py $*"

echo ""
echo "  Evaluation complete. Check ./results/ for outputs."