"""
Run each notebook in the FastText project inside Docker.

Import as:
import class_project.data605.Spring2026.projects.UmdTask458_DATA605_Spring2026_FastText_text_classification.test.test_docker_all as tftdal
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
    Run all Docker tests for the FastText text classification project.
    """

    _test_file = __file__

    @pytest.mark.slow
    def test1(self) -> None:
        """
        Test that fasttext.example.ipynb runs without error inside Docker.
        """
        notebook_name = "fasttext.example.ipynb"
        self._helper(notebook_name)

    @pytest.mark.slow
    def test2(self) -> None:
        """
        Test that fasttext.API.ipynb runs without error inside Docker.
        """
        notebook_name = "fasttext.API.ipynb"
        self._helper(notebook_name)