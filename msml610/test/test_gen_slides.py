"""
Test gen_slides.py script.

Import as:

import class_scripts.test.test_gen_slides as cltetegsl
"""

import logging

import pytest

import helpers.hsystem as hsystem
import helpers.hunit_test as hunitest

_LOG = logging.getLogger(__name__)


# #############################################################################
# Test_gen_slides1
# #############################################################################


class Test_gen_slides1(hunitest.TestCase):
    """
    Test gen_slides.py script invocation.
    """

    @pytest.mark.slow
    def test1(self) -> None:
        """
        Test running gen_slides.py for msml610 lesson 01.1.
        """
        # Run test.
        cmd = "gen_slides.py msml610 01.1"
        hsystem.system(cmd)
