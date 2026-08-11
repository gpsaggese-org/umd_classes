"""
Run each notebook in tutorials/fastapi/ inside Docker using docker_cmd.sh.

Import as:

import tutorials.fastapi.test.test_docker_fastapi as tfattdofa
"""

import logging

import pytest

import helpers.hdocker_tests as hdoctest

_LOG = logging.getLogger(__name__)


# #############################################################################
# Test_docker
# #############################################################################


class Test_docker(hdoctest.DockerTestCase):
    """
    Run all Docker tests for tutorials/fastapi/.
    """

    _test_file = __file__

    @pytest.mark.slow
    def test1(self) -> None:
        """
        Test that fastapi.API.ipynb runs without error inside Docker.
        """
        # Prepare inputs.
        notebook_name = "fastapi.API.ipynb"
        # Run test.
        self._helper(notebook_name)

    @pytest.mark.slow
    def test2(self) -> None:
        """
        Test that fastapi.example.ipynb runs without error inside Docker.
        """
        # Prepare inputs.
        notebook_name = "fastapi.example.ipynb"
        # Run test.
        self._helper(notebook_name)
