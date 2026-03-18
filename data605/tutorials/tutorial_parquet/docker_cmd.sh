#!/bin/bash
# """
# Execute a command in a Docker container.
#
# This script runs a specified command inside a new Docker container instance.
# The container is removed automatically after the command completes. The
# current directory is mounted to /data inside the container.
# """

# Exit immediately if any command exits with a non-zero status.
set -e
#set -x

# Capture the command to execute from command-line arguments.
CMD="$@"
echo "Executing: '$CMD'"

# Import the utility functions.
GIT_ROOT=$(git rev-parse --show-toplevel)
source $GIT_ROOT/class_project/project_template/utils.sh

# Load Docker configuration variables for this script.
get_docker_vars_script ${BASH_SOURCE[0]}
source $DOCKER_NAME
print_docker_vars

# List available Docker images matching the expected image name.
run "docker image ls $FULL_IMAGE_NAME"
#(docker manifest inspect $FULL_IMAGE_NAME | grep arch) || true

# Configure and run the Docker container with the specified command.
CONTAINER_NAME=$IMAGE_NAME
DOCKER_CMD=$(get_docker_cmd_command)
PORT=""
DOCKER_RUN_OPTS=""
DOCKER_CMD_OPTS=$(get_docker_bash_options $CONTAINER_NAME $PORT $DOCKER_RUN_OPTS)
run "$DOCKER_CMD $DOCKER_CMD_OPTS $FULL_IMAGE_NAME bash -c '$CMD'"
