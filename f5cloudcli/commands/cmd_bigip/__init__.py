# pylint: disable=line-too-long
"""Below are examples of using the Cloud CLI to interact with a BIG-IP.

    1. Discover BIG-IPs running in a Cloud Provider
    -----------------------------------------------
    The following is an example of how to discover information about a BIG-IP, including IP addresses, running in a cloud provider. ::

        $ export F5_CLI_PROVIDER_ACCESS_KEY=<aws_access_key_id>
        $ export F5_CLI_PROVIDER_SECRET_KEY=<aws_secret_access_key>
        $ export F5_CLI_PROVIDER_REGION_NAME=<region>
        $ f5 bigip discover --provider aws --provider-tag "MyTagKey:value1"
        Discovering all BIG-IPs in aws with tag MyTagKey:value1
        {
            "id": "i-0e331f5ca76ad231d",
            ...
        }

    2. Configure authentication to a BIG-IP
    ---------------------------------------
    The following is an example of how to configure authentication for a BIG-IP. Any commands that interact with a BIG-IP require that authentication to that BIG-IP is already configured. ::

        $ f5 bigip configure-auth --host 54.224.182.104 --port 443 --user myuser
        Password:
        Configuring BIG-IP Auth to 54.224.182.104 as myuser with ******


    3. Install an Automation Toolchain package
    ------------------------------------------
    The following is an example of how to install the Declarative Onboarding package onto a BIG-IP. ::

        $ f5 bigip toolchain package install --component do
        Toolchain component package do installed


    4. Install an Automation Toolchain service
    ------------------------------------------
    The following is an example of how to configure a new service using AS3 ::

        $ f5 bigip toolchain service --component as3 --declaration as3_decl.json create
        Toolchain component service create: {
            "declaration": {
                ...
            }
        }


"""
# pylint: enable=line-too-long

import os

from f5cloudsdk.bigip import ManagementClient
from f5cloudsdk.bigip.toolchain import ToolChainClient

import click_repl
import click

from f5cloudcli import docs, constants
from f5cloudcli.utils import clients
from f5cloudcli.utils import core as utils_core
from f5cloudcli.config import ConfigClient
from f5cloudcli.cli import PASS_CONTEXT, AliasedGroup

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
    ctx.log('Configuring BIG-IP Auth to %s as %s with ******', host, user)
    config_client = ConfigClient(
        group_name=constants.BIGIP_GROUP_NAME,
        auth={
            'username': user,
            'password': password,
            'host': host,
            'port': port
        })
    config_client.store_auth()

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

# group: toolchain - package, service
TOOLCHAIN_COMPONENTS = ['do', 'as3', 'ts', 'failover']
@cli.group('toolchain',
           help=HELP['BIGIP_TOOLCHAIN_HELP'])
def toolchain():
    """ group """

@toolchain.command('package',
                   help=HELP['BIGIP_TOOLCHAIN_PACKAGE_HELP'])
@click.argument('action',
                required=True,
                type=click.Choice(['install', 'uninstall', 'upgrade', 'verify']))
@click.option('--component',
              required=True,
              type=click.Choice(TOOLCHAIN_COMPONENTS))
@click.option('--version',
              required=False)
@PASS_CONTEXT
def package(ctx, action, component, version):
    """ command """
    auth = ConfigClient().read_auth(constants.BIGIP_GROUP_NAME)
    management_kwargs = dict(port=auth['port'], user=auth['username'], password=auth['password'])
    client = ManagementClient(auth['host'], **management_kwargs)

    kwargs = {}
    if version:
        kwargs['version'] = version
    toolchain_client = ToolChainClient(client, component, **kwargs)

    component_info = toolchain_client.package.is_installed()
    if action == 'verify':
        ctx.log(component_info)
    elif action == 'install':
        if not component_info['installed']:
            toolchain_client.package.install()
            ctx.log('Toolchain component package %s installed', component)
        else:
            ctx.log('Toolchain component package %s version %s is already installed',
                    component, component_info['installed_version'])
    elif action == 'uninstall':
        if not component_info['installed']:
            ctx.log('Toolchain component package %s is already uninstalled', component)
        else:
            toolchain_client.package.uninstall()
            ctx.log('Toolchain component package %s uninstalled', component)
    else:
        raise click.ClickException('Action {} not implemented'.format(action))

@toolchain.command('service',
                   help=HELP['BIGIP_TOOLCHAIN_SERVICE_HELP'])
@click.argument('action',
                required=True,
                type=click.Choice(['create', 'delete', 'show']))
@click.option('--component',
              required=True,
              type=click.Choice(TOOLCHAIN_COMPONENTS))
@click.option('--version',
              required=False)
@click.option('--declaration',
              required=False)
@click.option('--install-component',
              required=False,
              is_flag=True)
@PASS_CONTEXT
def service(ctx, action, component, version, declaration, install_component): # pylint: disable=too-many-arguments
    """ command """
    auth = ConfigClient().read_auth(constants.BIGIP_GROUP_NAME)
    management_kwargs = dict(port=auth['port'], user=auth['username'], password=auth['password'])
    client = ManagementClient(auth['host'], **management_kwargs)
    kwargs = {}
    if version:
        kwargs['version'] = version
    toolchain_client = ToolChainClient(client, component, **kwargs)

    # intent based - support install in 'service' sub-command
    # install toolchain component if requested (and not installed)
    installed = toolchain_client.package.is_installed()['installed']
    if install_component and not installed:
        ctx.log('Installing toolchain component package')
        toolchain_client.package.install()
        ctx.log('Checking toolchain component service is available')
        toolchain_client.service.is_available()

    if action == 'show':
        result = toolchain_client.service.show()
        ctx.log('Toolchain component service show: %s', (result))
    elif action == 'create':
        decl_location = utils_core.convert_to_absolute(declaration)
        result = toolchain_client.service.create(config_file=decl_location)
        ctx.log('Toolchain component service create: %s', (result))
    elif action == 'delete':
        result = toolchain_client.service.delete()
        ctx.log('Toolchain component service delete: %s', (result))
    else:
        raise click.ClickException('Action not implemented')

click_repl.register_repl(cli)
