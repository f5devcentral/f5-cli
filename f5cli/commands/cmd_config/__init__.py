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

    6. Setting global config (output format, enable/disable CLI telemetry, etc.)
    ------------------------------------------
    The following is an example of how to configure global settings ::

        $ f5 config set-defaults --output json --allow-telemetry true


"""

import click_repl
import click

from f5cli import docs, constants
from f5cli.cli import PASS_CONTEXT, AliasedGroup
from f5cli.config import ConfigurationClient, AuthConfigurationClient

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
@PASS_CONTEXT
def set_defaults(ctx, output, allow_telemetry):
    """ command """
    # Process any changed defaults
    new_defaults = {}
    for i in [
            {'key': 'output', 'inputValue': output},
            {'key': 'allowTelemetry', 'inputValue': allow_telemetry}
    ]:
        if i['inputValue'] is not None:
            new_defaults[i['key']] = i['inputValue']
    # Create/update configuration file
    ctx.config_client.create_or_update(new_defaults)
    ctx.log('CLI defaults updated successfully')

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
    auth_client = AuthConfigurationClient(auth=auth_info)
    auth_client.store_auth('update')

    ctx.log('Authentication updated successfully')


@auth.command('delete',
              help=HELP['DELETE_AUTH_HELP'])
@click.option('--name',
              required=True,
              metavar='<NAME>')
@PASS_CONTEXT
def auth_delete(ctx, name):
    """ command """

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
