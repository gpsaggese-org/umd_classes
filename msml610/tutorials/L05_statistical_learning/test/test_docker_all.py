"""
Run each notebook in msml610/tutorials/L05_statistical_learning/ inside Docker
using docker_cmd.sh.

Import as:

import msml610.tutorials.L05_statistical_learning.test.test_docker_all as mtl05tdal
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
    Run each notebook in msml610/tutorials/L05_statistical_learning/ via
    docker_cmd.sh.
    """

    def _helper(self, notebook_name: str) -> None:
        """
        Run a single notebook inside Docker and assert it completes
        successfully.

        :param notebook_name: name of the notebook file relative to the
            L05_statistical_learning/ directory
        """
        # Prepare inputs.
        test_dir = os.path.dirname(os.path.abspath(__file__))
        script_dir = os.path.dirname(test_dir)
        # Run test.
        hdoctest.run_notebook_in_docker(notebook_name, script_dir)

    @pytest.mark.slow
    def test1(self) -> None:
        """
        Test that L05_01_01_hoeffding_inequality.ipynb runs without error.
        """
        # Prepare inputs.
        notebook_name = "L05_01_01_hoeffding_inequality.ipynb"
        # Run test.
        self._helper(notebook_name)

    @pytest.mark.slow
    def test2(self) -> None:
        """
        Test that L05_01_02_bin_analogy_ml.ipynb runs without error.
        """
        # Prepare inputs.
        notebook_name = "L05_01_02_bin_analogy_ml.ipynb"
        # Run test.
        self._helper(notebook_name)

    @pytest.mark.slow
    def test3(self) -> None:
        """
        Test that L05_01_03_vc_dimension.ipynb runs without error.
        """
        # Prepare inputs.
        notebook_name = "L05_01_03_vc_dimension.ipynb"
        # Run test.
        self._helper(notebook_name)

    @pytest.mark.slow
    def test4(self) -> None:
        """
        Test that L05_01_04_growth_function.ipynb runs without error.
        """
        # Prepare inputs.
        notebook_name = "L05_01_04_growth_function.ipynb"
        # Run test.
        self._helper(notebook_name)

    @pytest.mark.slow
    def test5(self) -> None:
        """
        Test that L05_02_01_bias_variance.ipynb runs without error.
        """
        # Prepare inputs.
        notebook_name = "L05_02_01_bias_variance.ipynb"
        # Run test.
        self._helper(notebook_name)

    @pytest.mark.slow
    def test6(self) -> None:
        """
        Test that L05_02_02_overfitting.ipynb runs without error.
        """
        # Prepare inputs.
        notebook_name = "L05_02_02_overfitting.ipynb"
        # Run test.
        self._helper(notebook_name)
