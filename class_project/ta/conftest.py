"""
Disable all tests under class_project/ta/.

Import as:

import class_project.ta.conftest as cptaconf
"""


def pytest_ignore_collect(collection_path, config):
    """
    Skip test collection in this directory.
    """
    return True
