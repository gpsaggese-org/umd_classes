"""
Run BambooAI notebooks inside Docker using docker_cmd.sh.

Import as:

import tutorials.BambooAI.test.test_docker_all as ttdall
"""

import logging
import os

import pytest

import helpers.hdocker_tests as hdoctest

_LOG = logging.getLogger(__name__)


# #############################################################################
# Test_docker
# #############################################################################


class Test_docker(hdoctest.DockerTestCase):
    """
    Run Docker tests for BambooAI notebooks.
    """

    _test_file = __file__

    @pytest.mark.slow
    def test1(self) -> None:
        """
        Test that template.example.ipynb runs without error inside Docker.
        """
        # Prepare inputs.
        notebook_name = "template.example.ipynb"
        # Run test.
        self._helper(notebook_name)

    @pytest.mark.slow
    def test2(self) -> None:
        """
        Test that template.API.ipynb runs without error inside Docker.
        """
        # Prepare inputs.
        notebook_name = "template.API.ipynb"
        # Run test.
        self._helper(notebook_name)

    @pytest.mark.slow
    @pytest.mark.skipif(
        os.getenv("BAMBOOAI_RUN_LLM_NOTEBOOKS") != "1",
        reason="bambooai.API.ipynb executes interactive LLM cells.",
    )
    def test3(self) -> None:
        """
        Test that bambooai.API.ipynb runs without error inside Docker.
        """
        # Prepare inputs.
        notebook_name = "bambooai.API.ipynb"
        # Run test.
        self._helper(notebook_name)
