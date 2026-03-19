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


parse_docker_jupyter_args() {
    # """
    # Parse command-line arguments for docker_jupyter.sh.
    #
    # Sets JUPYTER_HOST_PORT, JUPYTER_USE_VIM, TARGET_DIR, VERBOSE, and
    # OLD_CMD_OPTS in the caller's scope.  Enables set -x when -v is passed.
    #
    # :param @: command-line arguments forwarded from the calling script
    # """
    # Set defaults.
    JUPYTER_HOST_PORT=8888
    JUPYTER_USE_VIM=0
    TARGET_DIR=.
    VERBOSE=0
    # Save original args to pass through to run_jupyter.sh.
    OLD_CMD_OPTS="$*"
    # Parse options.
    while getopts p:d:uv flag
    do
        case "${flag}" in
            p) JUPYTER_HOST_PORT=${OPTARG};;  # Port for Jupyter Lab.
            u) JUPYTER_USE_VIM=1;;            # Enable vim bindings.
            d) TARGET_DIR=${OPTARG};;         # Directory to mount as /data.
            v) VERBOSE=1;;                    # Enable verbose output.
        esac
    done
    # Enable command tracing if verbose mode is requested.
    if [[ $VERBOSE == 1 ]]; then
        set -x
    fi
}


get_docker_jupyter_command() {
    # """
    # Return the base docker run command for running Jupyter Lab interactively.
    #
    # :return: docker run command string with --rm and -ti flags
    # """
    echo "docker run --rm -ti"
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
    echo "--name $container_name \
    -p $host_port:8888 \
    $target_dir_opt \
    -v $(pwd):/curr_dir \
    -v $GIT_ROOT:/git_root \
    -e PYTHONPATH=/git_root:/git_root/helpers_root \
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
    -v $(pwd):/data \
    -v $GIT_ROOT:/git_root \
    -e PYTHONPATH=/git_root:/git_root/helpers_root \
    -e CSFY_HOST_OS_NAME=$(uname -s)"
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
