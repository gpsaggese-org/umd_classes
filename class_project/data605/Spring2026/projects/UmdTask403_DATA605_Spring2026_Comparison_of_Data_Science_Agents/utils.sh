#!/bin/bash
# """
# Utility functions for Docker container management.
# """

get_docker_bash_command() {
    # """
    # Return the base docker run command for an interactive bash shell.
    #
    # :return: docker run command string with --rm and -ti flags
    # """
    echo "docker run --rm -ti"
}


get_docker_cmd_command() {
    # """
    # Return the base docker run command for executing a non-interactive command.
    #
    # :return: docker run command string with --rm and -i flags
    # """
    echo "docker run --rm -i"
}


_print_default_help() {
    # """
    # Print usage information and available default options for docker scripts.
    # """
    echo "Usage: $(basename $0) [options]"
    echo ""
    echo "Options:"
    echo "  -h    Print this help message and exit"
    echo "  -v    Enable verbose output (set -x)"
}


parse_default_args() {
    # """
    # Parse default command-line arguments for docker scripts.
    #
    # Sets VERBOSE variable in the caller's scope and enables set -x when -v
    # is passed.  Prints help and exits when -h is passed.
    # Updates OPTIND so the caller can shift away processed arguments.
    #
    # :param @: command-line arguments forwarded from the calling script
    # """
    VERBOSE=0
    while getopts "hv" flag; do
        case "${flag}" in
            h) _print_default_help; exit 0;;
            v) VERBOSE=1;;
            *) _print_default_help; exit 1;;
        esac
    done
    enable_verbose_mode
}


_print_docker_jupyter_help() {
    # """
    # Print usage information and available options for docker_jupyter.sh.
    # """
    echo "Usage: $(basename $0) [options]"
    echo ""
    echo "Launch Jupyter Lab inside a Docker container."
    echo ""
    echo "Options:"
    echo "  -h          Print this help message and exit"
    echo "  -p PORT     Host port to forward to Jupyter Lab (default: 8888)"
    echo "  -d DIR      Directory to mount as /data inside the container (default: git root)"
    echo "  -u          Enable vim keybindings in Jupyter Lab"
    echo "  -v          Enable verbose output (set -x)"
}


parse_docker_jupyter_args() {
    # """
    # Parse command-line arguments for docker_jupyter.sh.
    #
    # Sets JUPYTER_HOST_PORT, JUPYTER_USE_VIM, TARGET_DIR, VERBOSE, and
    # OLD_CMD_OPTS in the caller's scope.  Enables set -x when -v is passed.
    # Prints help and exits when -h is passed.
    #
    # :param @: command-line arguments forwarded from the calling script
    # """
    # Set defaults.
    JUPYTER_HOST_PORT=8888
    JUPYTER_USE_VIM=0
    TARGET_DIR=$GIT_ROOT
    VERBOSE=0
    # Save original args to pass through to run_jupyter.sh.
    OLD_CMD_OPTS="$*"
    # Parse options.
    while getopts "hp:d:uv" flag; do
        case "${flag}" in
            h) _print_docker_jupyter_help; exit 0;;
            p) JUPYTER_HOST_PORT=${OPTARG};;  # Port for Jupyter Lab.
            u) JUPYTER_USE_VIM=1;;            # Enable vim bindings.
            d) TARGET_DIR=${OPTARG};;         # Directory to mount as /data.
            v) VERBOSE=1;;                    # Enable verbose output.
            *) _print_docker_jupyter_help; exit 1;;
        esac
    done
    # Enable command tracing if verbose mode is requested.
    enable_verbose_mode
}


enable_verbose_mode() {
    # """
    # Enable shell command tracing (set -x) when VERBOSE is set to 1.
    #
    # Reads the VERBOSE variable set by parse_docker_jupyter_args.
    # Call this after parsing args to activate tracing for the rest of the script.
    # """
    if [[ $VERBOSE == 1 ]]; then
        set -x
    fi
}


# #############################################################################
# Jupyter configuration
# #############################################################################


configure_jupyter_vim_keybindings() {
    # """
    # Configure JupyterLab vim keybindings based on JUPYTER_USE_VIM env var.
    #
    # Reads JUPYTER_USE_VIM; if 1, verifies jupyterlab_vim is installed and
    # writes enabled settings; otherwise writes disabled settings.
    # """
    mkdir -p ~/.jupyter/lab/user-settings/@axlair/jupyterlab_vim
    if [[ $JUPYTER_USE_VIM == 1 ]]; then
        # Check that jupyterlab_vim is installed before trying to enable it.
        if ! pip show jupyterlab_vim > /dev/null 2>&1; then
            echo "ERROR: jupyterlab_vim is not installed but vim bindings were requested."
            echo "Install it with: pip install jupyterlab_vim"
            exit 1
        fi
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
}


configure_jupyter_notifications() {
    # """
    # Disable JupyterLab news fetching and update checks.
    # """
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
}


get_jupyter_args() {
    # """
    # Print the standard Jupyter Lab command-line arguments.
    #
    # :return: space-separated Jupyter Lab args for port 8888 with no browser,
    #   allow root, and no authentication
    # """
    echo "--port=8888 --no-browser --ip=0.0.0.0 --allow-root --ServerApp.token='' --ServerApp.password=''"
}


get_docker_jupyter_command() {
    # """
    # Return the base docker run command for running Jupyter Lab interactively.
    #
    # :return: docker run command string with --rm and -ti flags
    # """
    echo "docker run --rm -ti"
}


get_docker_common_options() {
    # """
    # Return docker run options common to all container types.
    #
    # Includes volume mounts for the current directory and git root, plus
    # environment variables for PYTHONPATH and host OS name.
    #
    # :return: docker run options string with volume mounts and env vars
    # """
    echo "-v $(pwd):/curr_dir \
    -v $GIT_ROOT:/git_root \
    -e PYTHONPATH=/git_root:/git_root/helpers_root \
    -e CSFY_HOST_OS_NAME=$(uname -s) \
    -e CSFY_HOST_NAME=$(uname -n)"
}


get_docker_jupyter_options() {
    # """
    # Return docker run options for a Jupyter Lab container.
    #
    # :param container_name: Name for the Docker container
    # :param host_port: Host port to forward to container port 8888
    # :param target_dir: Optional directory to mount as /data (empty to skip)
    # :param jupyter_use_vim: 0 or 1 to enable vim bindings
    # :return: docker run options string
    # """
    local container_name=$1
    local host_port=$2
    local target_dir=$3
    local jupyter_use_vim=$4
    local target_dir_opt=""
    if [[ -n $target_dir ]]; then
        target_dir_opt="-v $target_dir:/data"
    fi
    # Run as the current user when user is saggese.
    if [[ "$(whoami)" == "saggese" ]]; then
        echo "Overwriting jupyter_use_vim since user='saggese'"
        jupyter_use_vim=1
    fi
    echo "--name $container_name \
    -p $host_port:8888 \
    $target_dir_opt \
    $(get_docker_common_options) \
    -e JUPYTER_USE_VIM=$jupyter_use_vim"
}


get_docker_bash_options() {
    # """
    # Return docker run options for a Docker container.
    #
    # :param container_name: Name for the Docker container
    # :param port: Port number to forward (optional, skipped if empty)
    # :param extra_opts: Additional docker run options (optional)
    # :return: docker run options string with name, volume mounts, and env vars
    # """
    local container_name=$1
    local port=$2
    local extra_opts=$3
    local port_opt=""
    if [[ -n $port ]]; then
        port_opt="-p $port:$port"
    fi
    echo "--name $container_name \
    $port_opt \
    $extra_opts \
    $(get_docker_common_options)"
}


get_docker_vars_script() {
    # """
    # Load Docker variables from docker_name.sh script.
    #
    # :param script_path: Path to the script to determine the Docker configuration directory
    # :return: Sources REPO_NAME, IMAGE_NAME, and FULL_IMAGE_NAME variables
    # """
    local script_path=$1
    # Find the name of the container.
    SCRIPT_DIR=$(dirname $script_path)
    DOCKER_NAME="$SCRIPT_DIR/docker_name.sh"
    if [[ ! -e $SCRIPT_DIR ]]; then
        echo "Can't find $DOCKER_NAME"
        exit -1
    fi;
    source $DOCKER_NAME
}


print_docker_vars() {
    # """
    # Print current Docker variables to stdout.
    # """
    echo "REPO_NAME=$REPO_NAME"
    echo "IMAGE_NAME=$IMAGE_NAME"
    echo "FULL_IMAGE_NAME=$FULL_IMAGE_NAME"
}


run() {
    # """
    # Execute a command with echo output.
    #
    # :param cmd: Command string to execute
    # :return: Exit status of the executed command
    # """
    cmd="$*"
    echo "> $cmd"
    eval "$cmd"
}


build_container_image() {
    # """
    # Build a Docker container image.
    #
    # Supports both single-architecture and multi-architecture builds.
    # Creates temporary build directory, copies files, and builds the image.
    #
    # :param @: Additional options to pass to docker build/buildx build
    # """
    echo "# ${FUNCNAME[0]} ..."
    FULL_IMAGE_NAME=$REPO_NAME/$IMAGE_NAME
    echo "FULL_IMAGE_NAME=$FULL_IMAGE_NAME"
    # Prepare build area.
    #tar -czh . | docker build $OPTS -t $IMAGE_NAME -
    DIR="../tmp.build"
    if [[ -d $DIR ]]; then
        rm -rf $DIR
    fi;
    cp -Lr . $DIR || true
    # Build container.
    echo "DOCKER_BUILDKIT=$DOCKER_BUILDKIT"
    echo "DOCKER_BUILD_MULTI_ARCH=$DOCKER_BUILD_MULTI_ARCH"
    if [[ $DOCKER_BUILD_MULTI_ARCH != 1 ]]; then
        # Build for a single architecture.
        echo "Building for current architecture..."
        OPTS="--progress plain $@"
        (cd $DIR; docker build $OPTS -t $FULL_IMAGE_NAME . 2>&1 | tee ../docker_build.log; exit ${PIPESTATUS[0]})
    else
        # Build for multiple architectures.
        echo "Building for multiple architectures..."
        OPTS="$@"
        export DOCKER_CLI_EXPERIMENTAL=enabled
        # Create a new builder.
        #docker buildx rm --all-inactive --force
        #docker buildx create --name mybuilder
        #docker buildx use mybuilder
        # Use the default builder.
        docker buildx use multiarch
        docker buildx inspect --bootstrap
        # Note that one needs to push to the repo since otherwise it is not
        # possible to keep multiple.
        (cd $DIR; docker buildx build --push --platform linux/arm64,linux/amd64 $OPTS --tag $FULL_IMAGE_NAME . 2>&1 | tee ../docker_build.log; exit ${PIPESTATUS[0]})
        # Report the status.
        docker buildx imagetools inspect $FULL_IMAGE_NAME
    fi;
    # Report build version.
    if [ -f docker_build.version.log ]; then
      rm docker_build.version.log
    fi
    (cd $DIR; docker run --rm -it -v $(pwd):/data $FULL_IMAGE_NAME bash -c "/data/version.sh") 2>&1 | tee docker_build.version.log
    #
    docker image ls $REPO_NAME/$IMAGE_NAME
    rm -rf $DIR
    echo "*****************************"
    echo "SUCCESS"
    echo "*****************************"
}


remove_container_image() {
    # """
    # Remove Docker container image(s) matching the current configuration.
    # """
    echo "# ${FUNCNAME[0]} ..."
    FULL_IMAGE_NAME=$REPO_NAME/$IMAGE_NAME
    echo "FULL_IMAGE_NAME=$FULL_IMAGE_NAME"
    docker image ls | grep $FULL_IMAGE_NAME
    docker image ls | grep $FULL_IMAGE_NAME | awk '{print $1}' | xargs -n 1 -t docker image rm -f
    docker image ls
    echo "${FUNCNAME[0]} ... done"
}


push_container_image() {
    # """
    # Push Docker container image to registry.
    #
    # Authenticates using credentials from ~/.docker/passwd.$REPO_NAME.txt.
    # """
    echo "# ${FUNCNAME[0]} ..."
    FULL_IMAGE_NAME=$REPO_NAME/$IMAGE_NAME
    echo "FULL_IMAGE_NAME=$FULL_IMAGE_NAME"
    docker login --username $REPO_NAME --password-stdin <~/.docker/passwd.$REPO_NAME.txt
    docker images $FULL_IMAGE_NAME
    docker push $FULL_IMAGE_NAME
    echo "${FUNCNAME[0]} ... done"
}


pull_container_image() {
    # """
    # Pull Docker container image from registry.
    # """
    echo "# ${FUNCNAME[0]} ..."
    FULL_IMAGE_NAME=$REPO_NAME/$IMAGE_NAME
    echo "FULL_IMAGE_NAME=$FULL_IMAGE_NAME"
    docker pull $FULL_IMAGE_NAME
    echo "${FUNCNAME[0]} ... done"
}


kill_container() {
    # """
    # Kill and remove Docker container(s) matching the current configuration.
    # """
    echo "# ${FUNCNAME[0]} ..."
    FULL_IMAGE_NAME=$REPO_NAME/$IMAGE_NAME
    echo "FULL_IMAGE_NAME=$FULL_IMAGE_NAME"
    docker container ls
    #
    CONTAINER_ID=$(docker container ls -a | grep $FULL_IMAGE_NAME | awk '{print $1}')
    echo "CONTAINER_ID=$CONTAINER_ID"
    if [[ ! -z $CONTAINER_ID ]]; then
        docker container rm -f $CONTAINER_ID
        docker container ls
    fi;
    echo "${FUNCNAME[0]} ... done"
}


exec_container() {
    # """
    # Execute bash shell in running Docker container.
    #
    # Opens an interactive bash session in the first container matching the
    # current configuration.
    # """
    echo "# ${FUNCNAME[0]} ..."
    FULL_IMAGE_NAME=$REPO_NAME/$IMAGE_NAME
    echo "FULL_IMAGE_NAME=$FULL_IMAGE_NAME"
    docker container ls
    #
    CONTAINER_ID=$(docker container ls -a | grep $FULL_IMAGE_NAME | awk '{print $1}')
    echo "CONTAINER_ID=$CONTAINER_ID"
    docker exec -it $CONTAINER_ID bash
    echo "${FUNCNAME[0]} ... done"
}
