#!/bin/bash
# The current directory is mounted at /app so all code changes are live.
#   ./docker_bash.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/docker_utils.sh"
load_docker_vars

CONTAINER_NAME="${IMAGE_NAME}_bash"
OPTS=$(base_run_opts "$CONTAINER_NAME" "-it")

run "docker run $OPTS $FULL_IMAGE_NAME /bin/bash"
