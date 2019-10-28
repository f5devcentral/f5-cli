"""Test: utils.core """

import os
import sys

from f5cloudcli.utils import core as core_utils

sys.path.append(os.getcwd())


def test_convert_absolute_path(mocker):
    """ Test absolute path """
    mock_getcwd = mocker.patch("f5cloudcli.utils.core.os.getcwd")
    mock_getcwd.return_value = "/test/current/directory"
    result = core_utils.convert_to_absolute("fake.txt")
    assert result == "/test/current/directory/fake.txt"
