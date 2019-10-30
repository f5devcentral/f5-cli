"""Test: utils.core """

import os
import sys
import json

from f5cloudcli.constants import FORMATS, FORMATS_ENV_VAR
from f5cloudcli.utils import core as core_utils

sys.path.append(os.getcwd())


def test_convert_absolute_path(mocker):
    """ Test absolute path """
    mock_getcwd = mocker.patch("f5cloudcli.utils.core.os.getcwd")
    mock_getcwd.return_value = "/test/current/directory"
    result = core_utils.convert_to_absolute("fake.txt")
    assert result == "/test/current/directory/fake.txt"


def test_format_output_as_default():
    """ Format output using default format (JSON)
    Given
    - data as list of dictionary
    [
        {
            "foo": "bar"
        },
        {
            "foo": "baz"
        }
    ]

    When
    - data is requested as default format

    Then
    - data is returned in pretty JSON format
    """

    data = [
        {
            'foo': 'bar'
        },
        {
            'foo': 'baz'
        }
    ]

    expected_result = json.dumps(data, indent=4, sort_keys=True)
    assert core_utils.format_output(data) == expected_result


def test_format_output_as_json(mocker):
    """ Format output using JSON format
    Given
    - data as list of dictionary
    [
        {
            "foo": "bar"
        },
        {
            "foo": "baz"
        }
    ]

    When
    - data is requested as json format

    Then
    - data is returned in pretty JSON format
    """

    mocker.patch.dict(
        "f5cloudcli.utils.clients.os.environ",
        {
            FORMATS_ENV_VAR: FORMATS['JSON']
        }
    )

    data = [
        {
            'foo': 'bar'
        },
        {
            'foo': 'baz'
        }
    ]

    expected_result = json.dumps(data, indent=4, sort_keys=True)
    assert core_utils.format_output(data) == expected_result


def test_format_output_as_table(mocker):
    """ Format output using table format
    Given
    - data as list of dictionary
    [
        {
            "foo": "bar"
        },
        {
            "foo": "baz"
        }
    ]

    When
    - data is requested as table format

    Then
    - data is returned in table format
    """

    mocker.patch.dict(
        "f5cloudcli.utils.clients.os.environ",
        {
            FORMATS_ENV_VAR: FORMATS['TABLE']
        }
    )

    data = [
        {
            'my_key': 'my_first_value'
        },
        {
            'my_key': 'my_second_value'
        }
    ]

    expected_result = (
        "my_key        \t\t\n"
        "--------------\t\t\n"
        "my_first_value\t\t\n"
        "my_second_value\t\t"
    )
    assert core_utils.format_output(data) == expected_result
