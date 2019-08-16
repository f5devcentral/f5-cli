""" This file provides the 'cloud-services' implementation of the CLI. """

from f5cloudsdk.cloud_services import ManagementClient

import click_repl
import click

from f5cloudcli import docs
from f5cloudcli.cli import PASS_CONTEXT, AliasedGroup
from f5cloudcli.config import ConfigClient
from f5cloudcli import constants

HELP = docs.get_docs()

# group: cloud-services
@click.group('cloud-services',
             help=HELP['CLOUD_SERVICES_HELP'],
             cls=AliasedGroup)
def cli():
    """ group """

@cli.command('configure-auth',
             help=HELP['CLOUD_SERVICES_CONFIGURE_AUTH_HELP'])
@click.option('--user', **constants.CLI_OPTIONS_USER_AUTH)
@click.password_option('--password',
                       **constants.CLI_OPTIONS_PASSWORD_AUTH,
                       metavar='<CLOUD_SERVICES_PASSWORD>')
@click.option('--api-endpoint', required=False, metavar='<CLOUD_SERVICES_API_ENDPOINT>')
@PASS_CONTEXT
def configure_auth(ctx, user, password, api_endpoint):
    """ command """
    ctx.log('Configuring F5 Cloud Services Auth for %s with ******', user)
    auth = {
        'username': user,
        'password': password
    }
    if api_endpoint is not None:
        auth['api-endpoint'] = api_endpoint

    config_client = ConfigClient(
        group_name=constants.CLOUD_SERVICES_GROUP_NAME,
        auth=auth)
    config_client.store_auth()

@cli.command('dns',
             help=HELP['CLOUD_SERVICES_DNS_HELP'],)
@click.argument('action',
                required=True,
                type=click.Choice(['create', 'delete', 'update']),
                metavar='<ACTION>')
@click.argument('record_type',
                required=True,
                type=click.Choice(['a', 'aaaa', 'cname']),
                metavar='<RECORD_TYPE>')
@click.argument('members',
                required=True,
                metavar='<MEMBERS>')
@PASS_CONTEXT
def dns(ctx, action, record_type, members):
    """ command """
    ctx.log('%s DNS %s with members %s', action, record_type, members)
    raise click.ClickException('Command not implemented')

click_repl.register_repl(cli)
