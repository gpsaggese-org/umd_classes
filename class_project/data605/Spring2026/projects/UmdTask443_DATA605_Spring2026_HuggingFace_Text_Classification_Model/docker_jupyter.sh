#!/bin/bash

#   JUPYTER_PORT=8889 ./docker_jupyter.sh
# http://localhost:8888/lab
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/docker_utils.sh"
load_docker_vars

CONTAINER_NAME="${IMAGE_NAME}_jupyter"

# -p maps host:container port; -d runs detached so the terminal stays free.
OPTS=$(base_run_opts "$CONTAINER_NAME" "-d -p ${JUPYTER_PORT}:8888")

echo "🔬  Starting Jupyter Lab on http://localhost:${JUPYTER_PORT}/lab"
echo "    (container: $CONTAINER_NAME)"
echo ""

run "docker run $OPTS $FULL_IMAGE_NAME /bin/bash run_jupyter.sh"

echo ""
echo "✅  Jupyter is running. Open: http://localhost:${JUPYTER_PORT}/lab"
echo "    Stop with: docker stop $CONTAINER_NAME"
