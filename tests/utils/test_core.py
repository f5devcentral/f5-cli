"""Test: utils.core """

import os
import sys

from f5cloudcli.utils import core as core_utils

sys.path.append(os.getcwd()) # TODO: fix this import process

def test_multiply():
    """ Test case """
    assert core_utils.multiply(2, 5) == 10
