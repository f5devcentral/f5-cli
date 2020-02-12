"""Below are examples of using the CLI to interact with a BIG-IP.

    1. Discover BIG-IPs running in a Cloud Provider
    -----------------------------------------------
    The following is an example of how to discover information about a BIG-IP,
    including IP addresses, running in a cloud provider. ::

        $ export F5_CLI_PROVIDER_ACCESS_KEY=<aws_access_key_id>
        $ export F5_CLI_PROVIDER_SECRET_KEY=<aws_secret_access_key>
        $ export F5_CLI_PROVIDER_REGION_NAME=<region>
        $ f5 bigip discover --provider aws --provider-tag "MyTagKey:value1"
        {
            "id": "i-0e331f5ca76ad231d",
            ...
        }

    2. Configure authentication to a BIG-IP
    ---------------------------------------
    The following is an example of how to configure authentication for a BIG-IP. Any commands
    that interact with a BIG-IP require that authentication to that BIG-IP is already configured. ::

        $ f5 bigip configure-auth --host 54.224.182.104 --port 443 --user myuser
        Password:
        {
            "message": "Authentication configured successfully"
        }


    3. Install or upgrade an Automation Toolchain package
    ------------------------------------------
    The following are the examples of how to install, uninstall, upgrade, and verify the Declarative
    Onboarding package onto a BIG-IP.  ::
        $ f5 bigip extension package install --component do
        {
            "message": "Extension component package 'do' successfully installed version '1.10.0'"
        }

        $ f5 bigip extension package verify --component do
        {
            "installed": true,
            "installed_version": "1.10.0",
            "latest_version": "1.10.0"
        }

        $ f5 bigip extension package uninstall --component do
        {
           "message": "Successfully uninstalled extension component package 'do' version '1.10.0'"
        }

        $ f5 bigip extension package upgrade --component do --version 1.9.0
        {
            "message": "Successfully upgraded extension component package 'do' to version '1.9.0'"
        }


    4. Install an Automation Toolchain service
    ------------------------------------------
    The following is an example of how to configure a new service using AS3 ::

        $ f5 bigip extension service --component as3 --declaration as3_decl.json create
        {
            "declaration": {
                ...
            }
        }


"""

# pylint: disable=too-many-arguments

from f5sdk.bigip import ManagementClient
from f5sdk.bigip.extension import ExtensionClient

import click_repl
import click

from f5cli import docs, constants
from f5cli.utils import clients
from f5cli.utils import core as utils_core
from f5cli.commands.cmd_bigip import extension_operations
from f5cli.config import ConfigClient
from f5cli.cli import PASS_CONTEXT, AliasedGroup

HELP = docs.get_docs()


# group: bigip
@click.group('bigip',
             help=HELP['BIGIP_HELP'],
             cls=AliasedGroup)
def cli():
    """ group """

@cli.command('configure-auth',
             help=HELP['BIGIP_CONFIGURE_AUTH_HELP'])
@click.option('--host',
              required=True,
              metavar='<HOST>')
@click.option('--port',
              required=False,
              metavar='<PORT>')
@click.option('--user', **constants.CLI_OPTIONS_USER_AUTH)
@click.password_option('--password',
                       **constants.CLI_OPTIONS_PASSWORD_AUTH,
                       metavar='<BIGIP_PASSWORD>')
@PASS_CONTEXT
def configure_auth(ctx, host, port, user, password):
    """ command """

    config_client = ConfigClient(
        group_name=constants.BIGIP_GROUP_NAME,
        auth={
            'username': user,
            'password': password,
            'host': host,
            'port': port
        })
    config_client.store_auth()

    ctx.log('Authentication configured successfully')

@cli.command('discover',
             help=HELP['BIGIP_DISCOVER_HELP'])
@click.option('--provider',
              required=True,
              type=click.Choice(['aws', 'azure', 'gcp']),
              metavar='<PROVIDER>')
@click.option('--provider-tag',
              required=True,
              metavar='<PROVIDER TAG>')
@PASS_CONTEXT
def discover(ctx, provider, provider_tag):
    """ command """

    # get provider client
    provider_client = clients.get_provider_client(provider)
    # list virtual machines
    virtual_machines = provider_client.virtual_machines.list(filter_tag=provider_tag)

    ctx.log(virtual_machines)


# group: extension - package, service
EXTENSION_COMPONENTS = ['do', 'as3', 'ts', 'cf']
@cli.group('extension',
           help=HELP['BIGIP_EXTENSION_HELP'])
def extension():
    """ group """

@extension.command('package',
                   help=HELP['BIGIP_EXTENSION_PACKAGE_HELP'])
@click.argument('action',
                required=True,
                type=click.Choice(['install', 'uninstall', 'upgrade', 'verify']))
@click.option('--component',
              required=True,
              type=click.Choice(EXTENSION_COMPONENTS))
@click.option('--version',
              required=False)
@click.option('--use-latest-metadata', is_flag=True)
@PASS_CONTEXT
def package(ctx, action, component, version, use_latest_metadata):
    """ command """
    auth = ConfigClient().read_auth(constants.BIGIP_GROUP_NAME)
    management_kwargs = dict(port=auth['port'], user=auth['username'], password=auth['password'])
    client = ManagementClient(auth['host'], **management_kwargs)

    kwargs = {}
    if version:
        kwargs['version'] = version
    if use_latest_metadata:
        kwargs['use_latest_metadata'] = use_latest_metadata
    extension_client = ExtensionClient(client, component, **kwargs)

    if action == 'verify':
        ctx.log(extension_operations.verify_package(client, component, **kwargs))
    elif action == 'install':
        ctx.log(extension_operations.install_package(client, component, **kwargs))
    elif action == 'uninstall':
        ctx.log(extension_operations.uninstall_package(client, component, **kwargs))
    elif action == 'upgrade':
        ctx.log(extension_operations.upgrade_package(client, component, version))
    else:
        raise click.ClickException('Action {} not implemented'.format(action))

@extension.command('service',
                   help=HELP['BIGIP_EXTENSION_SERVICE_HELP'])
@click.argument('action',
                required=True,
                type=click.Choice(['create', 'delete', 'show']))
@click.option('--component',
              required=True,
              type=click.Choice(EXTENSION_COMPONENTS))
@click.option('--version',
              required=False)
@click.option('--declaration',
              required=False)
@click.option('--install-component',
              required=False,
              is_flag=True)
@PASS_CONTEXT
def service(ctx, action, component, version, declaration, install_component):
    """ command """
    auth = ConfigClient().read_auth(constants.BIGIP_GROUP_NAME)
    management_kwargs = dict(port=auth['port'], user=auth['username'], password=auth['password'])
    client = ManagementClient(auth['host'], **management_kwargs)
    kwargs = {}
    if version:
        kwargs['version'] = version
    extension_client = ExtensionClient(client, component, **kwargs)

    # intent based - support install in 'service' sub-command
    # install extension component if requested (and not installed)
    installed = extension_client.package.is_installed()['installed']
    if install_component and not installed:
        extension_client.package.install()
        extension_client.service.is_available()

    if action == 'show':
        ctx.log(extension_client.service.show())
    elif action == 'create':
        if not installed:
            ctx.log("Package is not installed, run command "
                    "'f5 bigip extension package install --component %s'" % component)
        else:
            ctx.log(extension_client.service.create(
                config_file=utils_core.convert_to_absolute(declaration)))
    elif action == 'delete':
        ctx.log(extension_client.service.delete())
    else:
        raise click.ClickException('Action not implemented')


click_repl.register_repl(cli)
