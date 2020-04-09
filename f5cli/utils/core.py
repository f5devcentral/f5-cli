""" Core utility functions """

import os
import json
import yaml

import click

from f5cli.constants import FORMATS, ENV_VARS
from f5cli.config import ConfigurationClient


def convert_to_absolute(file):
    """Convert file to absolute path """
    if file is not None:
        return os.path.abspath(os.path.join(os.getcwd(), file))
    return None


def write_file(filename, content):
    """Write content to a file and set the correct file permission """
    with open(os.open(filename,
                      os.O_CREAT | os.O_WRONLY, 0o600), 'w') as file:
        yaml.safe_dump(content, file, default_flow_style=False, sort_keys=False)


def _get_output_format():
    """Get output format """

    config_client = ConfigurationClient()

    # format discovery priority is as follows:
    # 1) environment variable
    # 2) config file
    # 3) default format
    if ENV_VARS['OUTPUT_FORMAT'] in os.environ:
        output_format = os.environ[ENV_VARS['OUTPUT_FORMAT']]
    elif config_client.list().get('output', None):
        output_format = config_client.list().get('output', None)
    else:
        output_format = FORMATS['DEFAULT']

    return output_format


def _format_data_as_table(data):
    """Format data as a table """

    if isinstance(data, dict):
        data = [data]

    # Get common keys
    common_keys = {key for key, val in data[0].items() if isinstance(val, str)}
    for idx in range(1, len(data)):
        common_keys = common_keys.intersection(set(data[idx].keys()))
    common_keys = sorted(common_keys)
    # Construct output as table
    column_width = {val: len(data[0][val]) for val in common_keys}
    row_format = ''.join(['{:' + str(width) + '}\t\t' for _, width in column_width.items()])

    title = row_format.format(*column_width.keys())

    separator_column_width = ['-' * width for _, width in column_width.items()]
    separator = row_format.format(*separator_column_width)
    formatted_data = title + '\n' + separator

    # Construct each row data
    for entry in data:
        row_data = [entry[key] for key in common_keys]
        formatted_data += '\n' + row_format.format(*row_data)
    return formatted_data


def format_output(data):
    """ Get data in specified format

        Parameters
        ----------
        data : dict
            output data in a machine readable format
        Returns
        -------
        str
            data in specified format
            If output_format is TABLE, output will look like:
            id                                                      location
            ----------------------------------------                ----------
            624d58f0-6875-469a-ba12-d0f1390f7464                    westus
            17cd4583-f63b-4f38-a890-4bdee3d99e98                    westus

            If output_format is JSON, output will be pretty print JSON:
            {
                "id": "624d58f0-6875-469a-ba12-d0f1390f7464",
                "location": "westus",
                "name": "f5bigiq01",
                "privateIPAddress": "192.168.1.100",
                "publicIPAddress": "13.64.89.85",
                "tags": {
                    "application": "APP",
                    "cost": "COST",
                    "environment": "ENV",
                    "group": "GROUP",
                    "owner": "OWNER",
                    "test_cli": "f5"
                }
            },
            {
                "id": "17cd4583-f63b-4f38-a890-4bdee3d99e98",
                "location": "westus",
                "name": "f5vm",
                "privateIPAddress": "10.100.1.4",
                "publicIPAddress": "40.112.135.141",
                "tags": {
                    "application": "APP",
                    "cost": "COST",
                    "environment": "ENV",
                    "group": "GROUP",
                    "owner": "OWNER",
                    "test_cli": "f5"
                }
            }
    """
    output_format = _get_output_format()

    # it is typical that data is machine readable, however
    # if text is provided wrap it like so: {"message": "my message"}
    if not isinstance(data, (dict, list)):
        data = {'message': data}

    if output_format == FORMATS['JSON']:
        formatted_data = json.dumps(data, indent=4, sort_keys=True)
    elif output_format == FORMATS['TABLE']:
        formatted_data = _format_data_as_table(data)
    else:
        raise click.ClickException("Unsupported format {}".format(output_format))

    return formatted_data


def verify_approval(action, approval_confirmation_map, auto_approve):
    """ Verify approval for action in approval_confirmation_map """
    if action in approval_confirmation_map.keys() and not auto_approve:
        click.confirm('%s. Do you want to continue?' %
                      approval_confirmation_map[action],
                      abort=True)
