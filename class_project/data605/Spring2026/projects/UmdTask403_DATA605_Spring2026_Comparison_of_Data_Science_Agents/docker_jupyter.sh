#!/bin/bash
# """
# Execute Jupyter Lab in a Docker container.
#
# This script launches a Docker container running Jupyter Lab with
# configurable port, directory mounting, and vim bindings. It passes
# command-line options to the run_jupyter.sh script inside the container.
#
# Usage:
# > docker_jupyter.sh [options]
# """

# Exit immediately if any command exits with a non-zero status.
set -e

# Import the utility functions.
GIT_ROOT=$(git rev-parse --show-toplevel)
source $GIT_ROOT/class_project/project_template/utils.sh

# Parse command-line options and set Jupyter configuration variables.
parse_docker_jupyter_args "$@"

# Load Docker configuration variables for this script.
get_docker_vars_script ${BASH_SOURCE[0]}
source $DOCKER_NAME
print_docker_vars

# List available Docker images and inspect architecture.
run "docker image ls $FULL_IMAGE_NAME"
# The manifest probe hits docker.io and fails noisily when the user isn't
# logged in to that namespace (which is fine — we only build locally).
# Silence stderr so the demo output stays clean.
(docker manifest inspect $FULL_IMAGE_NAME 2>/dev/null | grep arch) || true

# Run the Docker container with Jupyter Lab.
# The parent template only mounts $GIT_ROOT at /git_root inside the container,
# so the in-container path to run_jupyter.sh is /git_root/<project-rel-dir>/.
# `get_run_jupyter_cmd` (defined in the template's utils.sh) builds it.
CMD=$(get_run_jupyter_cmd "${BASH_SOURCE[0]}" "$OLD_CMD_OPTS")
CONTAINER_NAME=$IMAGE_NAME

# Defensively remove any leftover container from a prior run that was killed
# without --rm cleanup (e.g. `docker stop` rather than Ctrl-C). Without this,
# a re-run of this script trips on a name collision and aborts.
docker rm -f $CONTAINER_NAME >/dev/null 2>&1 || true
DOCKER_CMD=$(get_docker_jupyter_command)
DOCKER_CMD_OPTS=$(get_docker_jupyter_options $CONTAINER_NAME $JUPYTER_HOST_PORT "$TARGET_DIR" $JUPYTER_USE_VIM)
run "$DOCKER_CMD $DOCKER_CMD_OPTS $FULL_IMAGE_NAME $CMD"
