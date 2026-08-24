"""
Run the notebooks in research/Implement_MonteCarlo_Tree_Search_and_Alpha_Zero/
inside Docker using docker_cmd.sh.

Import as:

import research.Implement_MonteCarlo_Tree_Search_and_Alpha_Zero.test.test_docker_template as rimtsaazttdt
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
    Run all Docker tests for
    research/Implement_MonteCarlo_Tree_Search_and_Alpha_Zero/.
    """

    _test_file = __file__

    @pytest.mark.slow
    def test1(self) -> None:
        """
        Test that mcts.example.ipynb runs without error inside Docker.
        """
        # Prepare inputs.
        notebook_name = "mcts.example.ipynb"
        # Run test.
        self.helper(notebook_name)

    @pytest.mark.slow
    def test2(self) -> None:
        """
        Test that mcts.API.ipynb runs without error inside Docker.
        """
        # Prepare inputs.
        notebook_name = "mcts.API.ipynb"
        # Run test.
        self.helper(notebook_name)
