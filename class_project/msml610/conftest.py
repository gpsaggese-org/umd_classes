"""
Prevent pytest from collecting tests in this directory.
"""


def pytest_ignore_collect(_path, _config):
    """
    Skip test collection in this directory.
    """
    return True
