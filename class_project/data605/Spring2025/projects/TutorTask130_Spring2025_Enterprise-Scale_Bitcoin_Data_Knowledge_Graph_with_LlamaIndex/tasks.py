import logging
import os
from typing import Any

import helpers.repo_config_utils as hrecouti

# Expose the pytest targets.
# Extract with:
# > i print_tasks --as-code
from helpers.lib_tasks import (  # This is not an invoke target.
    parse_command_line,
    set_default_params,
)

# A lib contains dependencies that exist only in a Docker environment. Skipping the import
# if needed in order not to break other invoke targets.
try:
    from oms.lib_tasks_binance import (  # isort: skip # noqa: F401  # pylint: disable=unused-import
        binance_display_open_positions,
        binance_flatten_account,
        binance_log_open_positions,
        binance_log_total_balance,
    )
except ImportError:
    pass
# Collect imports that fails due to the `helpers` image is not being updated. See CmTask4892 for details.
try:
    from helpers.lib_tasks import (  # isort: skip # noqa: F401  # pylint: disable=unused-import
        copy_ecs_task_definition_image_url,
        docker_release_multi_build_dev_image,
        docker_tag_push_multi_build_local_image_as_dev,
        release_dags_to_airflow,
        integrate_file,
        lint_check_if_it_was_run,
    )
except ImportError:
    pass
try:
    from helpers.lib_tasks_gh import (  # isort: skip # noqa: F401  # pylint: disable=unused-import
        gh_publish_buildmeister_dashboard_to_s3,
    )
except ImportError:
    pass
# # TODO(gp): This is due to the coupling between code in linter container and
# #  the code being linted.
# try:
#     from helpers.lib_tasks import (  # isort: skip # noqa: F401  # pylint: disable=unused-import
#         docker_update_prod_task_definition,
#     )
# except ImportError as e:
#     #print(e)
#     pass


_LOG = logging.getLogger(__name__)


# #############################################################################
# Setup.
# #############################################################################


# TODO(gp): Move it to lib_tasks.
ECR_BASE_PATH = os.environ["CSFY_ECR_BASE_PATH"]


def _run_qa_tests(ctx: Any, stage: str, version: str) -> bool:
    """
    Run QA tests to verify that the invoke tasks are working properly.

    This is used when qualifying a docker image before releasing.
    """
    _ = ctx
    # The QA tests are in `qa_test_dir` and are marked with `qa_test_tag`.
    qa_test_dir = "test"
    # qa_test_dir = "test/test_tasks.py::TestExecuteTasks1::test_docker_bash"
    qa_test_tag = "qa and not superslow"
    cmd = f'pytest -m "{qa_test_tag}" {qa_test_dir} --image_stage {stage}'
    if version:
        cmd = f"{cmd} --image_version {version}"
    ctx.run(cmd)
    return True


default_params = {
    # TODO(Nikola): Remove prefix after everything is cleaned.
    #   Currently there are a lot dependencies on prefix.
    "CSFY_ECR_BASE_PATH": ECR_BASE_PATH,
    # When testing a change to the build system in a branch you can use a different
    # image, e.g., `XYZ_tmp` to not interfere with the prod system.
    # "BASE_IMAGE": "amp_tmp",
    "BASE_IMAGE": hrecouti.get_repo_config().get_docker_base_image_name(),
    "QA_TEST_FUNCTION": _run_qa_tests,
}


set_default_params(default_params)
parse_command_line()
