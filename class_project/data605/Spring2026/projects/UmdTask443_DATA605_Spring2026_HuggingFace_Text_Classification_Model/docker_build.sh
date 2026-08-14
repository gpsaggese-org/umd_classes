#!/bin/bash
#   ./docker_build.sh --no-cache  # force full rebuild (re-installs all deps)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/docker_utils.sh"
load_docker_vars

# Enable BuildKit for faster, cached layer builds.
export DOCKER_BUILDKIT=1

# Pass any extra args (like --no-cache) straight through to docker build.
EXTRA_ARGS="$*"

run "docker build $EXTRA_ARGS -t $FULL_IMAGE_NAME $SCRIPT_DIR"

echo ""
echo "    Image built: $FULL_IMAGE_NAME"
echo "    Run './docker_bash.sh'    to open an interactive shell."
echo "    Run './docker_train.sh'   to start fine-tuning."
echo "    Run './docker_jupyter.sh' to launch Jupyter Lab."
