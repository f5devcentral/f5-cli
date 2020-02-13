"""Below are examples of using the CLI to manage authentication and
   global configuration settings.

    1. Create an authentication account
    -----------------------------------------------
    The following are examples of how to create an authentication config for a
    authentication provider. Any commands that interact with BIG-IP or CLOUD SERVICES
    require that authentication to that BIG-IP is already configured. ::

    $ f5 config auth create --authentication-provider bigip
        --name bigip-1 --host 192.0.2.10 --user myuser

    $ f5 config auth create --authentication-provider bigip --name bigip-2
        --host 192.0.2.11 --user myuser --password mypassword --set-default

    $ f5 config auth create --authentication-provider cloud-services
        --name cs-1 --user myuser@f5.com --password blah


    2. Update an authentication account
    ---------------------------------------
    The following are examples of how to update a authentication authentication accounts ::

        $ f5 config auth update --name bigip-1 --user aws --password mypassword --set-default

        $ f5 config auth update --name cs-1 --user myuserr@f5.com --password mypassword


    3. Delete an authentication account
    ------------------------------------------
    The following is an example of how to delete an authentication config auth ::

        $ f5 config auth delete --name bigip-1

    4. List all authentication accounts
    ------------------------------------------
    The following is an example of how to list all the authentication authentication accounts ::

        $ f5 config auth list

    5. Toggling a default authentication account
    ------------------------------------------
    The following is an example of how to set default authentication config auth ::

        $ f5 config auth update --name cs-1 --set-default

    6. Setting global config
    ------------------------------------------
    The following is an example of how to set the global output format setting ::

        $ f5 config output-format --output json


"""

import os

import yaml
import click_repl
import click

from f5cli import docs, constants
from f5cli.constants import F5_CLI_DIR, F5_CONFIG_FILE, FORMATS
from f5cli.cli import PASS_CONTEXT, AliasedGroup
from f5cli.config import ConfigClient

HELP = docs.get_docs()


# group: config
@click.group('config',
             help=HELP['CONFIG_HELP'],
             cls=AliasedGroup)
def cli():
    """ group """


@cli.command('output-format',
             help=HELP['FORMAT_HELP'])
@click.option('--output',
              default=FORMATS['DEFAULT'],
              help=HELP['OUTPUT_HELP'],
              show_default=True)
@PASS_CONTEXT
def output_format(ctx, output):
    """ command """
    ctx.log('Configure client')
    # Create configuration directory if not exists
    if not os.path.exists(F5_CLI_DIR):
        os.makedirs(F5_CLI_DIR)
    # Create/overwrite F5 cli configuration file
    config_content = {
        'output': output
    }
    with open(F5_CONFIG_FILE, 'w') as outfile:
        yaml.safe_dump(config_content, outfile, indent=4, sort_keys=True)


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
              metavar='<PORT>')
@click.option('--set-default',
              required=False,
              default=False,
              is_flag=True,
              metavar='<SET_DEFAULT>')
@click.option('--api-endpoint',
              required=False,
              metavar='<CLOUD_SERVICES_API_ENDPOINT>')
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
            constants.AUTHENTICATION_PROVIDERS.get(constants.CLOUD_SERVICES_GROUP_NAME):
        if api_endpoint is not None:
            auth_info['api_endpoint'] = api_endpoint
    else:
        if host is not None:
            auth_info['host'] = host
            auth_info['port'] = constants.DEFAULT_BIGIP_PORT
        if port is not None:
            auth_info['port'] = port

    config_client = ConfigClient(auth=auth_info)
    config_client.store_auth('create')

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
              metavar='<CLOUD_SERVICES_API_ENDPOINT>')
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
    config_client = ConfigClient(auth=auth_info)
    config_client.store_auth('update')

    ctx.log('Authentication updated successfully')


@auth.command('delete',
              help=HELP['DELETE_AUTH_HELP'])
@click.option('--name',
              required=True,
              metavar='<NAME>')
@PASS_CONTEXT
def auth_delete(ctx, name):
    """ command """

    config_client = ConfigClient()
    config_client.delete_auth(name)

    ctx.log(f"Successfully deleted auth: {name} contents")


@auth.command('list',
              help=HELP['LIST_AUTH_HELP'])
@PASS_CONTEXT
def auth_list(ctx):
    """ command """

    ctx.log(ConfigClient().list_auth())


click_repl.register_repl(cli)
