"""
Run each notebook in msml610/tutorials/L09_multi_armed_bandits/ inside Docker
using docker_cmd.sh.

Import as:

import msml610.tutorials.L09_multi_armed_bandits.test.test_docker_all as mtl09mabdal
"""

import logging
import os

import pytest

import helpers.hdocker_tests as hdoctest
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
        # Run test.
        hdoctest.run_docker_build(script_dir)


# #############################################################################
# Test_docker_cmd
# #############################################################################


class Test_docker_cmd(hunitest.TestCase):
    """
    Test that docker_cmd.sh can run arbitrary shell commands inside Docker.
    """

    @pytest.mark.slow
    def test1(self) -> None:
        """
        Test that docker_cmd.sh 'ls /data' runs without error.
        """
        # Prepare inputs.
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Run test.
        hdoctest.run_docker_cmd(script_dir)


# #############################################################################
# Test_docker_run_notebooks
# #############################################################################


class Test_docker_run_notebooks(hunitest.TestCase):
    """
    Run each notebook in msml610/tutorials/L09_multi_armed_bandits/ via
    docker_cmd.sh.
    """

    def _helper(self, notebook_name: str) -> None:
        """
        Run a single notebook inside Docker and assert it completes
        successfully.

        :param notebook_name: name of the notebook file relative to the
            L09_multi_armed_bandits/ directory
        """
        # Prepare inputs.
        test_dir = os.path.dirname(os.path.abspath(__file__))
        script_dir = os.path.dirname(test_dir)
        # Run test.
        hdoctest.run_notebook_in_docker(notebook_name, script_dir)

    @pytest.mark.slow
    def test1(self) -> None:
        """
        Test that L09_03_multi_armed_bandits.ipynb runs without error.
        """
        # Prepare inputs.
        notebook_name = "L09_03_multi_armed_bandits.ipynb"
        # Run test.
        self._helper(notebook_name)
