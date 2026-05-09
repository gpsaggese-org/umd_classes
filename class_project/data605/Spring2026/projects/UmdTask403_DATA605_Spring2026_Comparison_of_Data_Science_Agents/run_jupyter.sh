#!/bin/bash
# """
# Launch Jupyter Lab server.
#
# This script starts Jupyter Lab on port 8888 with the following configuration:
# - No browser auto-launch (useful for Docker containers)
# - Accessible from any IP address (0.0.0.0)
# - Root user allowed (required for Docker environments)
# - No authentication token or password (for development convenience)
# - Vim keybindings can be enabled via JUPYTER_USE_VIM environment variable
# """

# Exit immediately if any command exits with a non-zero status.
set -e

# Print each command to stdout before executing it.
#set -x

# Import the utility functions from the project template.
# The host monorepo is mounted at /git_root by get_docker_common_options
# in the parent template's utils.sh; that's where the project lives at runtime.
GIT_ROOT=/git_root
source $GIT_ROOT/class_project/project_template/utils.sh

# Load Docker configuration variables for this script.
get_docker_vars_script ${BASH_SOURCE[0]}
source $DOCKER_NAME
print_docker_vars

# Defensive install: jupyterlab + ipykernel are declared in requirements.in
# but older Docker images may predate that change. Install on the fly into
# the project venv so the grader doesn't need a rebuild to launch Jupyter.
PYTHON_BIN="${PYTHON_BIN:-/app/.venv/bin/python}"
if ! "$PYTHON_BIN" -c "import jupyterlab" 2>/dev/null; then
    echo "[run_jupyter] jupyterlab missing, installing into project venv..."
    "$PYTHON_BIN" -m pip install --quiet jupyterlab ipykernel
fi

# Configure vim keybindings and notifications.
configure_jupyter_vim_keybindings
configure_jupyter_notifications

# Initialize Jupyter Lab command with base configuration.
JUPYTER_ARGS=$(get_jupyter_args)

# Serve from the host-mounted project tree (set by get_docker_vars_script as
# SCRIPT_DIR), not from /app. The image's /app copy of the project does not
# contain `results/` (it's gitignored and excluded by .dockerignore), so
# notebooks that read master_scorecard.csv only work when JupyterLab serves
# the host-mounted directory.
cd "$SCRIPT_DIR"

# Start Jupyter Lab with development-friendly settings.
run "jupyter lab $JUPYTER_ARGS"
