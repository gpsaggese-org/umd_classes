#!/bin/bash
# """
# Pull Docker container image from registry.
#
# This script downloads a Docker container image from the remote registry
# to the local system.
# """

# Exit immediately if any command exits with a non-zero status.
set -e

# Print each command to stdout before executing it.
set -x

# Import the utility functions.
GIT_ROOT=$(git rev-parse --show-toplevel)
source $GIT_ROOT/class_project/project_template/utils.sh

# Load Docker configuration variables for this script.
get_docker_vars_script ${BASH_SOURCE[0]}
source $DOCKER_NAME
print_docker_vars

# Pull the container image from the registry.
pull_container_image
