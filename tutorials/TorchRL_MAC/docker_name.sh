#!/bin/bash
# """
# Docker image naming configuration.
#
# This file defines the repository name, image name, and full image name
# variables used by all docker_*.sh scripts in the project template.
# """

REPO_NAME=""
IMAGE_NAME=torchrl_mac
FULL_IMAGE_NAME=${IMAGE_TAG:-torchrl_mac:latest}
