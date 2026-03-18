#"""
#Run all tests in tutorials/FilterPy/test/ inside the Docker container using
#docker_cmd.sh.
#
#Import as:
#
#import tutorials.FilterPy.test.test_docker as tftdo
#"""
#
#import logging
#import os
#
#import pytest
#
#import helpers.hdocker_tests as hdtests
#import helpers.hsystem as hsystem
#import helpers.hunit_test as hunitest
#
#_LOG = logging.getLogger(__name__)
#
#
#
#
## #############################################################################
## Test_docker_run_all_tests
## #############################################################################
#
#
#class Test_docker_run_all_tests(hunitest.TestCase):
#    """
#    Run all tests in tutorials/FilterPy/test/ via docker_cmd.sh.
#    """
#
#    @pytest.mark.slow
#    def test1(self) -> None:
#        """
#        Test that all docker test files in the test directory pass inside the
#        container.
#        """
#        # Prepare inputs.
#        test_dir = os.path.dirname(os.path.abspath(__file__))
#        script_dir = os.path.dirname(test_dir)
#        docker_cmd_script = os.path.join(script_dir, "docker_cmd.sh")
#        # Run test.
#        rc = hdtests.run_all_tests(
#            test_dir, docker_cmd_script=docker_cmd_script
#        )
#        # Check output.
#        self.assertEqual(rc, 0)
