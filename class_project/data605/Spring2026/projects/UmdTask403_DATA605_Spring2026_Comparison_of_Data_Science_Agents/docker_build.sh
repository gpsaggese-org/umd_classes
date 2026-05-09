#!/bin/bash
# """
# Build a Docker container image for the project.
#
# This script sets up the build environment with error handling and command
# tracing, loads Docker configuration from docker_name.sh, and builds the
# Docker image using the build_container_image utility function. It supports
# both single-architecture and multi-architecture builds via the
# DOCKER_BUILD_MULTI_ARCH environment variable.
# """

# Exit immediately if any command exits with a non-zero status.
set -e

# Import the utility functions.
GIT_ROOT=$(git rev-parse --show-toplevel)
source $GIT_ROOT/class_project/project_template/utils.sh

# Parse default args (-h, -v) and enable set -x if -v is passed.
# Shift processed option flags so remaining args are passed to the build.
parse_default_args "$@"
shift $((OPTIND-1))

# Load Docker configuration variables (REPO_NAME, IMAGE_NAME, FULL_IMAGE_NAME).
get_docker_vars_script ${BASH_SOURCE[0]}
source $DOCKER_NAME
print_docker_vars

# Configure Docker build settings.
# Enable BuildKit for improved build performance and features.
export DOCKER_BUILDKIT=1
#export DOCKER_BUILDKIT=0

# Configure single-architecture build (set to 1 for multi-arch build).
#export DOCKER_BUILD_MULTI_ARCH=1
export DOCKER_BUILD_MULTI_ARCH=0

# Local override of the parent template's `build_container_image` to skip the
# `cp -Lr . ../tmp.build` staging step. That step predates BuildKit's
# .dockerignore handling and is now a 10+ min tax on a project with a large
# gitignored `results/` tree. BuildKit honors `.dockerignore` directly on the
# project root, so we just `docker build .` in place.
build_container_image() {
    echo "# ${FUNCNAME[0]} (local override) ..."
    FULL_IMAGE_NAME=$REPO_NAME/$IMAGE_NAME
    echo "FULL_IMAGE_NAME=$FULL_IMAGE_NAME"
    echo "DOCKER_BUILDKIT=$DOCKER_BUILDKIT"
    echo "DOCKER_BUILD_MULTI_ARCH=$DOCKER_BUILD_MULTI_ARCH"
    if [[ $DOCKER_BUILD_MULTI_ARCH == 1 ]]; then
        echo "Multi-arch builds still use the parent template's pipeline."
        # Fall back to the parent implementation.
        unset -f build_container_image
        build_container_image "$@"
        return $?
    fi
    OPTS="--progress plain $@"
    docker build $OPTS -t $FULL_IMAGE_NAME . 2>&1 | tee docker_build.log
    local rc=${PIPESTATUS[0]}
    if [[ $rc -ne 0 ]]; then
        echo "*****************************"
        echo "FAILED (docker build rc=$rc)"
        echo "*****************************"
        return $rc
    fi
    if [ -f docker_build.version.log ]; then
        rm docker_build.version.log
    fi
    docker run --rm -v "$(pwd):/data" $FULL_IMAGE_NAME bash -c "/data/version.sh" 2>&1 | tee docker_build.version.log
    docker image ls $FULL_IMAGE_NAME
    echo "*****************************"
    echo "SUCCESS"
    echo "*****************************"
}

# Build the container image.
# Pass extra arguments (e.g., --no-cache) via command line after -v.
build_container_image "$@"
