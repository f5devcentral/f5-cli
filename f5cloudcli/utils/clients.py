""" Core utility functions """

import os
import json
from f5cloudsdk import provider
import click

def get_env_vars(env_vars):
    """ Get environment variables """

    if not all(x in os.environ for x in env_vars):
        err_msg = 'Environment variables must exist: %s' % (env_vars)
        raise click.ClickException(err_msg)

    # return resolved environment variables
    return [os.environ[i] for i in env_vars]

# TODO: put this somewhere better...
def get_provider_client(_provider):
    """ Get provider client """

    if _provider not in ['aws', 'azure']:
        raise click.ClickException('Provider not implemented')

    # instantiate provider client
    if _provider == 'azure':
        env_vars = get_env_vars([
            'F5_CLI_PROVIDER_TENANT_ID',
            'F5_CLI_PROVIDER_CLIENT_ID',
            'F5_CLI_PROVIDER_SECRET',
            'F5_CLI_PROVIDER_SUBSCRIPTION_ID'
        ])
        return provider.azure.ProviderClient(
            tenant_id=env_vars[0],
            client_id=env_vars[1],
            secret=env_vars[2],
            subscription_id=env_vars[3]
        )
    if _provider == 'aws':
        env_vars = get_env_vars([
            'F5_CLI_PROVIDER_ACCESS_KEY',
            'F5_CLI_PROVIDER_SECRET_KEY',
            'F5_CLI_PROVIDER_REGION_NAME'
        ])
        return provider.aws.ProviderClient(
            access_key=env_vars[0], secret_key=env_vars[1], region_name=env_vars[2]
        )

def get_output_format(data, format):
    """ Get JSON in pretty format """
    formatted_data = data
    if len(data) > 0 and type(data[0]) is dict:
        if format == 'json':
            formatted_data = ',\n'.join(tuple([json.dumps(d, indent=4, sort_keys=True) for d in data]))
        elif format == 'table':
            # Get common keys
            common_keys = {key for key,val in data[0].items() if type(val) is str}
            for idx in range(1, len(data)):
                common_keys = common_keys.intersection(set(data[idx].keys()))
            # Construct output as table
            column_width = {val:len(data[0][val]) + 4 for val in common_keys}
            row_format = ''.join(['{:' + str(width) + '}\t\t' for _,width in column_width.items()])

            title = row_format.format(*column_width.keys())

            separator_column_width = ['-'*width for _,width in column_width.items()]
            separator = row_format.format(*separator_column_width)
            formatted_data = title + '\n' + separator

            # Construct each row data
            for d in data:
                row_data = [d[key] for key in common_keys]
                formatted_data += '\n' + row_format.format(*row_data)
    
    return formatted_data
