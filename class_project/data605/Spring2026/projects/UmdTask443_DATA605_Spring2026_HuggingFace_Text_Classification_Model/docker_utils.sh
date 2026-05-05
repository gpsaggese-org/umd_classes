#!/bin/bash
# docker_utils.sh — shared helpers sourced by all docker_*.sh scripts.

#   - run()              : echo + execute a command
#   - load_docker_vars() : source docker_name.sh and print the resolved names
#   - base_run_opts()    : common `docker run` flags used by every script

run() {
    echo "+ $*"
    eval "$*"
}

# Source docker_name.sh (always relative to the script calling this file).
load_docker_vars() {
    local script_dir
    script_dir="$(cd "$(dirname "${BASH_SOURCE[1]}")" && pwd)"
    # shellcheck source=docker_name.sh
    source "$script_dir/docker_name.sh"
    echo "──────────────────────────────────────────"
    echo "  REPO       : $REPO_NAME"
    echo "  IMAGE      : $IMAGE_NAME"
    echo "  FULL IMAGE : $FULL_IMAGE_NAME"
    echo "  HF VOLUME  : $HF_CACHE_VOLUME"
    echo "──────────────────────────────────────────"
}

base_run_opts() {
    local container_name="$1"
    local extra="${2:-}"
    echo "--rm \
 --name $container_name \
 -v \"$(pwd):/app\" \
 -v \"$HF_CACHE_VOLUME:/hf_cache\" \
 $extra"
}
