#!/bin/bash
# Remove the project Docker image
#   ./docker_clean.sh --volumes # also removes the HF cache named volume
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/docker_utils.sh"
load_docker_vars

run "docker image rm -f $FULL_IMAGE_NAME" || true

if [[ "$1" == "--volumes" ]]; then
    echo "Also removing named volume: $HF_CACHE_VOLUME"
    run "docker volume rm $HF_CACHE_VOLUME" || true
fi

echo ""
run "docker ps -a"
echo "  Cleanup complete. Run './docker_build.sh' to rebuild."
