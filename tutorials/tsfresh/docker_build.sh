#!/bin/bash
# """
# Build the Docker container image for the tsfresh tutorial.
# """

# Exit immediately if any command exits with a non-zero status.
set -e

# Import the utility functions from the project template.
GIT_ROOT=$(git rev-parse --show-toplevel)
source $GIT_ROOT/class_project/project_template/utils.sh

# Parse default args (-h, -v) and enable set -x if -v is passed.
# Shift processed option flags so remaining args are passed to the build.
parse_default_args "$@"
shift $((OPTIND-1))

# Load Docker configuration variables for this script.
get_docker_vars_script ${BASH_SOURCE[0]}
source $DOCKER_NAME
print_docker_vars

export DOCKER_BUILDKIT=1
export DOCKER_BUILD_MULTI_ARCH=0

# Build the container image.
# Pass extra arguments (e.g., --no-cache) via command line after -v.
build_container_image "$@"
