#!/bin/bash
# """
# Kill and remove a running Docker container.
#
# This script terminates a running Docker container matching the project
# configuration and removes it.
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

# Kill and remove the container.
kill_container
