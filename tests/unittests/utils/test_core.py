"""Test: utils.core """

import os
import sys
import json
import click

from f5cli.constants import FORMATS, ENV_VARS
from f5cli.utils import core as core_utils

from ...global_test_imports import pytest

sys.path.append(os.getcwd())


def test_convert_absolute_path(mocker):
    """ Test absolute path """
    mock_getcwd = mocker.patch("f5cli.utils.core.os.getcwd")
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
        "os.environ",
        {
            ENV_VARS['OUTPUT_FORMAT']: FORMATS['JSON']
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
            "my_key": "my_first_value"
        },
        {
            "my_key": "my_first_value"
        }
    ]

    When
    - data is requested as table format

    Then
    - data is returned in table format
    """

    mocker.patch.dict(
        "os.environ",
        {
            ENV_VARS['OUTPUT_FORMAT']: FORMATS['TABLE']
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


def test_format_output_as_table_dict(mocker):
    """ Format output using table format
    Given
    - data as dictionary
    {
        "my_key": "my_first_value"
    }

    When
    - data is requested as table format

    Then
    - data is returned in table format
    """

    mocker.patch.dict(
        "os.environ",
        {
            ENV_VARS['OUTPUT_FORMAT']: FORMATS['TABLE']
        }
    )

    data = {
        'my_key': 'my_first_value'
    }

    expected_result = (
        "my_key        \t\t\n"
        "--------------\t\t\n"
        "my_first_value\t\t"
    )
    assert core_utils.format_output(data) == expected_result


def test_invalid_format_output(mocker):
    """ Invalid format output environment variable value
    Given
    - ENV_VARS['OUTPUT_FORMAT'] contains invalid value

    When
    - data is requested to be formatted

    Then
    - 'ClickException' error is raised
    """

    mocker.patch.dict(
        "os.environ",
        {
            ENV_VARS['OUTPUT_FORMAT']: 'foo'
        }
    )

    with pytest.raises(click.exceptions.ClickException) as error:
        core_utils.format_output({'foo': 'bar'})
    assert error.value.args[0] == "Unsupported format foo"
