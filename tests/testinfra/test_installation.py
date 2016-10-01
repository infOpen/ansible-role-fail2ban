"""
Role tests
"""
import pytest

# To run all the tests on given docker images:
pytestmark = pytest.mark.docker_images(
    'infopen/ubuntu-trusty-ssh:0.1.0',
#    'infopen/ubuntu-xenial-ssh-py27:0.2.0'
)


def test_packages(Package):
    """
    Test package install
    """

    assert Package('fail2ban').is_installed
