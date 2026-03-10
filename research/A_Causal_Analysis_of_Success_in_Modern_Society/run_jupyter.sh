#!/bin/bash -xe
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

mkdir -p ~/.jupyter/lab/user-settings/@axlair/jupyterlab_vim
if [[ $JUPYTER_USE_VIM == 1 ]]; then
    echo "Enabling vim."
    cat <<EOF > ~/.jupyter/lab/user-settings/\@axlair/jupyterlab_vim/plugin.jupyterlab-settings
{
    "enabled": true,
    "enabledInEditors": true,
    "extraKeybindings": []
}
EOF
else
    echo "Disabling vim."
    cat <<EOF > ~/.jupyter/lab/user-settings/\@axlair/jupyterlab_vim/plugin.jupyterlab-settings
{
    "enabled": false,
    "enabledInEditors": false,
    "extraKeybindings": []
}
EOF
fi;

mkdir -p ~/.jupyter/lab/user-settings/@jupyterlab/apputils-extension
cat <<EOF > ~/.jupyter/lab/user-settings/\@jupyterlab/apputils-extension/notification.jupyterlab-settings
{
    // Notifications
    // @jupyterlab/apputils-extension:notification
    // Notifications settings.

    // Fetch official Jupyter news
    // Whether to fetch news from the Jupyter news feed. If Always (`true`), it will make a request to a website.
    "fetchNews": "false",
    "checkForUpdates": false
}
EOF

# Initialize Jupyter Lab command with base configuration.
JUPYTER_ARGS=(
    "--port=8888"
    "--no-browser"
    "--ip=0.0.0.0"
    "--allow-root"
    "--ServerApp.token=''"
    "--ServerApp.password=''"
)

# Note: jupyterlab-vim extension can be disabled via JupyterLab settings if needed.

# Start Jupyter Lab with development-friendly settings.
jupyter lab "${JUPYTER_ARGS[@]}"

# Alternative: Use classic Jupyter Notebook instead of Jupyter Lab.
#jupyter-notebook \
#    --port=8888 \
#    --no-browser --ip=0.0.0.0 \
#    --allow-root \
#    --NotebookApp.token='' \
#    --NotebookApp.password=''
