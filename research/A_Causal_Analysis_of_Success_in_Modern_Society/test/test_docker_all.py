"""
Run each notebook in research/A_Causal_Analysis_of_Success_in_Modern_Society/ inside Docker using docker_cmd.sh.

Import as:

import research.A_Causal_Analysis_of_Success_in_Modern_Society.test.test_docker_all as racaosimstda
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
    Run all Docker tests for research/A_Causal_Analysis_of_Success_in_Modern_Society/.
    """

    _test_file = __file__

    @pytest.mark.slow
    def test1(self) -> None:
        """
        Test that causal_success.example.ipynb runs without error inside Docker.
        """
        # Prepare inputs.
        notebook_name = "causal_success.example.ipynb"
        # Run test.
        self._helper(notebook_name)

    @pytest.mark.slow
    def test2(self) -> None:
        """
        Test that causal_success.API.ipynb runs without error inside Docker.
        """
        # Prepare inputs.
        notebook_name = "causal_success.API.ipynb"
        # Run test.
        self._helper(notebook_name)
