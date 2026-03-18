"""
Run each notebook in tutorials/FilterPy/ inside Docker using docker_cmd.sh.

Import as:

import tutorials.FilterPy.test.test_docker_all as tftdal
"""

import logging
import os

import pytest

import helpers.hdbg as hdbg
import helpers.hsystem as hsystem
import helpers.hunit_test as hunitest

_LOG = logging.getLogger(__name__)


# #############################################################################
# Test_docker_build
# #############################################################################


class Test_docker_build(hunitest.TestCase):
    """
    Test that docker_build.sh builds the Docker image successfully.
    """

    @pytest.mark.slow
    def test1(self) -> None:
        """
        Test that docker_build.sh runs without error.
        """
        # Prepare inputs.
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        docker_build_script = os.path.join(script_dir, "docker_build.sh")
        # Run test.
        cmd = f"cd {script_dir} && bash {docker_build_script}"
        hsystem.system(cmd)


# #############################################################################
# Test_docker_run_notebooks
# #############################################################################


class Test_docker_run_notebooks(hunitest.TestCase):
    """
    Run each notebook in tutorials/FilterPy/ via docker_cmd.sh.
    """

    def _helper(self, notebook_name: str) -> None:
        """
        Run a single notebook inside Docker and assert it completes
        successfully.

        :param notebook_name: name of the notebook file relative to the
            tutorials/FilterPy/ directory (e.g., filterpy.example.ipynb)
        """
        # Prepare inputs.
        test_dir = os.path.dirname(os.path.abspath(__file__))
        script_dir = os.path.dirname(test_dir)
        docker_cmd_script = os.path.join(script_dir, "docker_cmd.sh")
        notebook_path = os.path.join(script_dir, notebook_name)
        hdbg.dassert_file_exists(notebook_path)
        # Run test.
        # cd into script_dir so docker_cmd.sh mounts the right directory.
        # Inside the container the notebooks are at /data/<notebook_name>.
        cmd = (
            f"cd {script_dir} && "
            f"bash {docker_cmd_script} "
            f"'jupyter nbconvert --execute --to html "
            f"--ExecutePreprocessor.timeout=-1 /data/{notebook_name}'"
        )
        hsystem.system(cmd)

    @pytest.mark.slow
    def test1(self) -> None:
        """
        Test that filterpy.example.ipynb runs without error inside Docker.
        """
        # Prepare inputs.
        notebook_name = "filterpy.example.ipynb"
        # Run test.
        self._helper(notebook_name)

    @pytest.mark.slow
    def test2(self) -> None:
        """
        Test that filterpy.api.ipynb runs without error inside Docker.
        """
        # Prepare inputs.
        notebook_name = "filterpy.api.ipynb"
        # Run test.
        self._helper(notebook_name)
