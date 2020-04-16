""" Config command """

import os

import click_repl
import click

from f5cli import docs, constants
from f5cli.cli import PASS_CONTEXT, AliasedGroup
from f5cli.config import ConfigurationClient, AuthConfigurationClient
from f5cli.utils.core import verify_approval

HELP = docs.get_docs()


# group: config
@click.group('config',
             help=HELP['CONFIG_HELP'],
             cls=AliasedGroup)
@PASS_CONTEXT
def cli(ctx):
    """ group """

    ctx.config_client = ConfigurationClient()


@cli.command('set-defaults',
             help=HELP['SET_DEFAULTS_HELP'])
@click.option('--output',
              help=HELP['OUTPUT_FORMAT_HELP'])
@click.option('--allow-telemetry',
              help=HELP['ALLOW_TELEMETRY_HELP'])
@click.option('--disable-ssl-warnings',
              help=HELP['SSL_WARNINGS'])
@click.option('--auto-approve',
              default=False,
              is_flag=True,
              metavar='<AUTO-APPROVE>')
@PASS_CONTEXT
def set_defaults(ctx, output, allow_telemetry, disable_ssl_warnings, auto_approve):
    """ command """
    # Process any changed defaults
    new_defaults = {}
    for i in [{'key': 'output', 'inputValue': output},
              {'key': 'allowTelemetry', 'inputValue': allow_telemetry},
              {'key': 'disableSSLWarnings', 'inputValue': disable_ssl_warnings}]:
        if i['inputValue'] is not None:
            new_defaults[i['key']] = i['inputValue']
    approval_confirmation_map = {'set-defaults': 'Defaults will be edited.'}
    verify_approval('set-defaults', approval_confirmation_map, auto_approve)
    # Create/update configuration file
    ctx.config_client.create_or_update(new_defaults)
    message = 'CLI defaults updated successfully.'
    if disable_ssl_warnings:
        os.environ[constants.ENV_VARS['DISABLE_SSL_WARNINGS']] = disable_ssl_warnings
        if disable_ssl_warnings == 'true':
            message += ' Warning: Insecure SSL warnings have been disabled'
    ctx.log(message)


@cli.command('list-defaults',
             help=HELP['LIST_DEFAULTS_HELP'])
@PASS_CONTEXT
def list_defaults(ctx):
    """ command """
    ctx.log(ctx.config_client.list())


@cli.group('auth',
           help=HELP['AUTH_HELP'])
def auth():
    """ group """


@auth.command('create',
              help=HELP['CONFIGURE_AUTH_HELP'])
@click.option('--authentication-provider',
              required=True,
              type=click.Choice(constants.AUTHENTICATION_PROVIDERS.values()),
              metavar='<AUTHENTICATION_PROVIDER>')
@click.option('--name',
              required=True,
              metavar='<NAME>')
@click.option('--host',
              required=False,
              metavar='<HOST>')
@click.option('--port',
              required=False,
              default=constants.DEFAULT_BIGIP_PORT,
              metavar='<PORT>')
@click.option('--set-default',
              required=False,
              default=False,
              is_flag=True,
              metavar='<SET_DEFAULT>')
@click.option('--api-endpoint',
              required=False,
              metavar='<CS_API_ENDPOINT>')
@click.option('--user',
              required=False,
              metavar='<USERNAME>')
@click.option('--password',
              required=False,
              metavar='<PASSWORD>')
@PASS_CONTEXT
def auth_create(ctx,  # pylint: disable=too-many-arguments
                authentication_provider,
                host,
                port,
                name,
                set_default,
                api_endpoint,
                user,
                password):
    """ command """
    auth_info = {
        'name': name,
        'authentication-type': authentication_provider,
        'default': set_default
    }
    if user:
        if password is None:
            password = click.prompt("Password", type=str, hide_input=True)
        auth_info.update({
            'user': user,
            'password': password})

    if authentication_provider == \
            constants.AUTHENTICATION_PROVIDERS.get(constants.CS_GROUP_NAME):
        if api_endpoint is not None:
            auth_info['api_endpoint'] = api_endpoint
    else:
        if host is not None:
            auth_info['host'] = host
        auth_info['port'] = port

    auth_client = AuthConfigurationClient(auth=auth_info)
    auth_client.store_auth('create')

    ctx.log('Authentication configured successfully')


@auth.command('update',
              help=HELP['UPDATE_AUTH_HELP'])
@click.option('--authentication-provider',
              required=False,
              type=click.Choice(constants.AUTHENTICATION_PROVIDERS.values()),
              metavar='<AUTHENTICATION_PROVIDER>')
@click.option('--name',
              required=True,
              metavar='<NAME>')
@click.option('--host',
              required=False,
              metavar='<HOST>')
@click.option('--port',
              required=False,
              metavar='<PORT>')
@click.option('--set-default',
              required=False,
              is_flag=True,
              metavar='<SET_DEFAULT>')
@click.option('--api-endpoint',
              required=False,
              metavar='<CS_API_ENDPOINT>')
@click.option('--user',
              required=False,
              metavar='<USERNAME>')
@click.option('--password',
              required=False,
              metavar='<PASSWORD>')
@PASS_CONTEXT
def auth_update(ctx,  # pylint: disable=too-many-arguments
                authentication_provider,
                host,
                port,
                name,
                set_default,
                api_endpoint,
                user,
                password):
    """ command """

    auth_info = {
        'name': name,
        'authentication-type': authentication_provider,
        'default': set_default,
        'host': host,
        'port': port,
        'api-endpoint': api_endpoint
    }

    if user:
        if password is None:
            password = click.prompt("Password", type=str, hide_input=True)
        auth_info.update({
            'user': user,
            'password': password})
    auth_client = AuthConfigurationClient(auth=auth_info)
    auth_client.store_auth('update')

    ctx.log('Authentication updated successfully')


@auth.command('delete',
              help=HELP['DELETE_AUTH_HELP'])
@click.option('--name',
              required=True,
              metavar='<NAME>')
@click.option('--auto-approve',
              default=False,
              is_flag=True,
              metavar='<AUTO-APPROVE>')
@PASS_CONTEXT
def auth_delete(ctx, name, auto_approve):
    """ command """
    approval_confirmation_map = {
        'delete': 'Auth contents named %s will be deleted.' % name
    }
    verify_approval('delete', approval_confirmation_map, auto_approve)
    auth_client = AuthConfigurationClient()
    auth_client.delete_auth(name)
    ctx.log(f"Successfully deleted auth: {name} contents")


@auth.command('list',
              help=HELP['LIST_AUTH_HELP'])
@PASS_CONTEXT
def auth_list(ctx):
    """ command """

    ctx.log(AuthConfigurationClient().list_auth())


click_repl.register_repl(cli)
