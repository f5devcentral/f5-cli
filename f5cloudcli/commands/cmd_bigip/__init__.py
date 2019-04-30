""" This file provides the 'bigip' implementation of the CLI. """

import os

from f5cloudsdk.bigip import ManagementClient
from f5cloudsdk.bigip.toolchain import ToolChainClient

import click_repl
import click

from f5cloudcli import docs
from f5cloudcli.utils import clients
from f5cloudcli.config import ConfigClient
from f5cloudcli.cli import PASS_CONTEXT, AliasedGroup

HELP = docs.get_docs()

# group: bigip
@click.group('bigip',
             help=HELP['BIGIP_HELP'],
             cls=AliasedGroup)
def cli():
    """ group """

@cli.command('login',
             help=HELP['BIGIP_LOGIN_HELP'])
@click.option('--host',
              required=True,
              metavar='<HOST>')
@click.option('--user',
              required=True,
              metavar='<USERNAME>')
@click.password_option('--password',
                       required=False,
                       prompt=True,
                       confirmation_prompt=False,
                       metavar='<BIGIP_PASSWORD>')
@PASS_CONTEXT
def login(ctx, host, user, password):
    """ command """
    ctx.log('Logging in to BIG-IP %s as %s with ******', host, user)
    client = ManagementClient(host, user=user, password=password)
    # delete sensitive attributes
    delattr(client, 'user')
    delattr(client, 'password')
    ctx.client = client
    # write config state to disk
    config_client = ConfigClient(client=client)
    config_client.write_client()

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
    ctx.log('Discovering all BIG-IPs in %s with tag %s', provider, provider_tag)

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
    ctx.log('%s %s %s', component, version, action)

    client = ctx.client if hasattr(ctx, 'client') else ConfigClient().read_client()

    kwargs = {}
    if version:
        kwargs['version'] = version
    toolchain_client = ToolChainClient(client, component, **kwargs)

    installed = toolchain_client.package.is_installed()
    if action == 'verify':
        ctx.log('Toolchain component package installed: %s', (installed))
    elif action == 'install':
        if not installed:
            toolchain_client.package.install()
            ctx.log('Toolchain component package installed')
        else:
            ctx.log('Toolchain component is already installed')
    elif action == 'uninstall':
        if not installed:
            ctx.log('Toolchain component package is already uninstalled')
        else:
            toolchain_client.package.uninstall()
            ctx.log('Toolchain component package uninstalled')
    else:
        raise click.ClickException('Action not implemented')

@toolchain.command('service',
                   help=HELP['BIGIP_TOOLCHAIN_SERVICE_HELP'])
@click.argument('action',
                required=True,
                type=click.Choice(['create', 'delete', 'verify']))
@click.option('--component',
              required=True,
              type=click.Choice(TOOLCHAIN_COMPONENTS))
@click.option('--version',
              required=False)
@PASS_CONTEXT
def service(ctx, action, component, version):
    """ command """
    ctx.log('%s %s %s', component, version, action)
    raise click.ClickException('Command not implemented')

click_repl.register_repl(cli)
