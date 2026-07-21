#!/bin/bash
# """
# Build a Docker container image for the project.
# """

# Exit immediately if any command exits with a non-zero status.
set -e

# Import the utility functions.
GIT_ROOT=$(git rev-parse --show-toplevel)
source $GIT_ROOT/class_project/project_template/utils.sh

# Parse default args (-h, -v) and enable set -x if -v is passed.
parse_default_args "$@"
shift $((OPTIND-1))

# Load Docker configuration variables.
get_docker_vars_script ${BASH_SOURCE[0]}
source $DOCKER_NAME
print_docker_vars

# Configure Docker build settings.
export DOCKER_BUILDKIT=1
export DOCKER_BUILD_MULTI_ARCH=0

# Build the container image.
build_container_image "$@"