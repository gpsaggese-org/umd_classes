#!/bin/bash
# Run inference with the fine-tuned model inside Docker.
#   ./docker_predict.sh --text "Apple reports record iPhone sales"
#   ./docker_predict.sh --file /app/articles.txt   # file must be inside ./
#   ./docker_predict.sh                            # interactive mode
#
# Note: run ./docker_train.sh first so the model checkpoint exists.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/docker_utils.sh"
load_docker_vars

CONTAINER_NAME="${IMAGE_NAME}_predict"

# Only allocate a TTY for interactive mode (no args).
# When --text or --file is passed it runs non-interactively
if [[ $# -eq 0 ]]; then
    EXTRA="-it"
else
    EXTRA=""
fi

OPTS=$(base_run_opts "$CONTAINER_NAME" "$EXTRA")

run "docker run $OPTS $FULL_IMAGE_NAME python project_files/scripts/predict.py $*"