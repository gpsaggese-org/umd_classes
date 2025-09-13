#
# Configure the Docker container environment for development.
# It corresponds to the script `dev_scripts/setXYZ.sh` outside of the
# container.
#

set -e

echo "CSFY_USE_HELPERS_AS_NESTED_MODULE=$CSFY_USE_HELPERS_AS_NESTED_MODULE"

SCRIPT_PATH="devops/docker_run/docker_setenv.sh"
echo "##> $SCRIPT_PATH"

# - Source `utils.sh`.
# NOTE: we can't use $0 to find the path since we are sourcing this file.

SOURCE_PATH="${CSFY_HELPERS_ROOT_PATH}/dev_scripts_helpers/thin_client/thin_client_utils.sh"
echo "> source $SOURCE_PATH ..."
if [[ ! -f $SOURCE_PATH ]]; then
    echo -e "ERROR: Can't find $SOURCE_PATH"
    kill -INT $$
fi
source $SOURCE_PATH

# - Activate venv.
activate_docker_venv

# Check that the required environment vars are defined and non-empty.
dassert_var_defined "CSFY_USE_HELPERS_AS_NESTED_MODULE"
dassert_var_defined "CSFY_HOST_GIT_ROOT_PATH"
dassert_var_defined "CSFY_GIT_ROOT_PATH"
dassert_var_defined "CSFY_HELPERS_ROOT_PATH"

# Check that helpers_root path exists.
dassert_dir_exists $CSFY_HELPERS_ROOT_PATH

# - PATH
set_path .

# - Git.
set_up_docker_git

# - PYTHONPATH
set_pythonpath $CSFY_HELPERS_ROOT_PATH

# - Configure environment.
echo "# Configure env"
export PYTHONDONTWRITEBYTECODE=x
