""" Core utility functions """

import os

import click

from f5cloudsdk import provider
from f5cloudcli.constants import AWS_PROVIDER, AZURE_PROVIDER


def get_env_vars(env_vars):
    """ Get environment variables """

    if not all(x in os.environ for x in env_vars):
        err_msg = 'Environment variables must exist: %s' % (env_vars)
        raise click.ClickException(err_msg)

    # return resolved environment variables
    return [os.environ[i] for i in env_vars]


def get_provider_client(_provider):
    """ Get provider client """
    client = None
    # instantiate provider client
    if _provider == AZURE_PROVIDER:
        env_vars = get_env_vars([
            'F5_CLI_PROVIDER_TENANT_ID',
            'F5_CLI_PROVIDER_CLIENT_ID',
            'F5_CLI_PROVIDER_SECRET',
            'F5_CLI_PROVIDER_SUBSCRIPTION_ID'
        ])
        client = provider.azure.ProviderClient(
            tenant_id=env_vars[0],
            client_id=env_vars[1],
            secret=env_vars[2],
            subscription_id=env_vars[3]
        )
    elif _provider == AWS_PROVIDER:
        env_vars = get_env_vars([
            'F5_CLI_PROVIDER_ACCESS_KEY',
            'F5_CLI_PROVIDER_SECRET_KEY',
            'F5_CLI_PROVIDER_REGION_NAME'
        ])
        client = provider.aws.ProviderClient(
            access_key=env_vars[0],
            secret_key=env_vars[1],
            region_name=env_vars[2]
        )
    else:
        raise click.ClickException('Provider {} not implemented'.format(_provider))
    return client
