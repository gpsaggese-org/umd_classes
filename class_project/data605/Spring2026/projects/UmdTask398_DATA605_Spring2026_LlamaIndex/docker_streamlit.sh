#!/bin/bash
# """
# Execute Streamlit in a Docker container.
#
# This script launches a Docker container running the Streamlit app with
# the correct port exposed (8501).
# """

# Exit immediately if any command exits with a non-zero status.
set -e

# Import the utility functions.
GIT_ROOT=$(git rev-parse --show-toplevel)
source $GIT_ROOT/class_project/project_template/utils.sh

parse_default_args "$@"

# Load Docker configuration variables for this script.
get_docker_vars_script ${BASH_SOURCE[0]}
source $DOCKER_NAME
print_docker_vars

# List available Docker images.
run "docker image ls $FULL_IMAGE_NAME"

# Configure and run the Docker container with Streamlit.
CONTAINER_NAME="${IMAGE_NAME}_streamlit"
DOCKER_CMD=$(get_docker_bash_command)
PORT="8501"
DOCKER_RUN_OPTS=""
DOCKER_CMD_OPTS=$(get_docker_bash_options $CONTAINER_NAME $PORT "$DOCKER_RUN_OPTS")

# Run Streamlit on 0.0.0.0 so it's accessible outside the container
run "$DOCKER_CMD $DOCKER_CMD_OPTS -v \$(pwd):/curr_dir -w /curr_dir $FULL_IMAGE_NAME streamlit run app.py --server.port $PORT --server.address 0.0.0.0"