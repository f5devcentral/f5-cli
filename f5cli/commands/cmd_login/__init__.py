""" Login command """

# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches

import click_repl
import click
from f5sdk.exceptions import DeviceReadyError, HTTPError, InvalidAuthError
from f5sdk.cs import ManagementClient as CSManagementClient
from f5sdk.bigip import ManagementClient as BigipManagementClient

from f5cli import docs, constants
from f5cli.config import AuthConfigurationClient
from f5cli.cli import PASS_CONTEXT, AliasedGroup

HELP = docs.get_docs()
BIGIP_AUTH_ACCOUNT_NAME = "login_bigip"
CS_AUTH_ACCOUNT_NAME = "login_cs"


# group: login
@click.group('login',
             help=HELP['LOGIN_HELP'],
             cls=AliasedGroup,
             invoke_without_command=True)
@click.option('--authentication-provider',
              required=True,
              type=click.Choice(constants.AUTHENTICATION_PROVIDERS.values()),
              metavar='<AUTHENTICATION_PROVIDER>')
@click.option('--host',
              required=False,
              metavar='<HOST>')
@click.option('--port',
              required=False,
              default=constants.DEFAULT_BIGIP_PORT,
              metavar='<PORT>')
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
def cli(ctx,
        authentication_provider,
        host,
        port,
        api_endpoint,
        user,
        password):
    """ command """

    if authentication_provider == \
            constants.AUTHENTICATION_PROVIDERS.get(constants.BIGIP_GROUP_NAME):
        if host is None:
            host = click.prompt("Host", type=str)
        auth_info = {
            'name': BIGIP_AUTH_ACCOUNT_NAME,
            'authentication-type': authentication_provider,
            'default': True,
            'host': host,
            'port': port
        }
    else:
        auth_info = {
            'name': CS_AUTH_ACCOUNT_NAME,
            'authentication-type': authentication_provider,
            'default': True
        }
        if api_endpoint is not None:
            auth_info['api_endpoint'] = api_endpoint

    if user is None:
        user = click.prompt("User", type=str)
    auth_info['user'] = user
    if password is None:
        password = click.prompt("Password", type=str, hide_input=True)
    auth_info['password'] = password

    # Validate credentials
    if authentication_provider == \
            constants.AUTHENTICATION_PROVIDERS.get(constants.BIGIP_GROUP_NAME):
        try:
            management_kwargs = dict(
                port=auth_info['port'],
                user=auth_info['user'],
                password=auth_info['password']
            )
            BigipManagementClient(auth_info['host'], **management_kwargs)
        except DeviceReadyError:
            raise click.ClickException(f"Device is not ready.") from None
        except InvalidAuthError:
            raise click.ClickException(f"Failed to login to BIG-IP, please provide valid"
                                       " credentials.") from None
        except HTTPError as error:
            raise click.ClickException(f"HTTP Error: {error}") from None
    else:
        try:
            CSManagementClient(user=auth_info['user'],
                               password=auth_info['password'],
                               api_endpoint=auth_info.pop('api_endpoint', None))
        except InvalidAuthError:
            raise click.ClickException(f"Failed to login to Cloud Services, please provide valid"
                                       " credentials.") from None
        except HTTPError as error:
            raise click.ClickException(f"HTTP Error: {error}") from None
    # Store credentials in auth file
    auth_client = AuthConfigurationClient(auth=auth_info)
    try:
        auth_client.store_auth('create')
    except click.ClickException:
        auth_client.store_auth('update')

    ctx.log('Logged in successfully')


click_repl.register_repl(cli)
