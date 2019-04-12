""" This file provides the 'bigip' implementation of the CLI. """
import click

from click_repl import register_repl
from f5cloudsdk.bigip import ManagementClient
from f5cloudsdk.bigip.toolchain import ToolChainClient

from f5cloudcli.config import ConfigClient
from f5cloudcli.shared.util import getdoc
from f5cloudcli.cli import PASS_CONTEXT, AliasedGroup

DOC = getdoc()

@click.group('bigip',
             short_help='BIG-IP',
             help=DOC["BIGIP_HELP"],
             cls=AliasedGroup,
             chain=True,
             no_args_is_help=True)
@PASS_CONTEXT
def cli(ctx): # pylint: disable=unused-argument
    """ override """
    # pass

@cli.command('login', help=DOC["BIGIP_LOGIN_HELP"])
@click.argument('host',
                required=True,
                metavar='<HOST>')
@click.argument('user',
                required=True,
                metavar='<USERNAME>')
@click.password_option('--password',
                       help=DOC['BIGIP_PASSWORD_HELP'],
                       required=False,
                       prompt=True,
                       confirmation_prompt=False,
                       metavar='<BIGIP_PASSWORD>')
@PASS_CONTEXT
def login(ctx, host, user, password):
    """ override """
    ctx.log('Logging in to BIG-IP %s as %s with %s', host, user, password)
    client = ManagementClient(host, user=user, password=password)
    ctx.client = client
    # write config state to disk
    config_client = ConfigClient(client=client)
    config_client.write_client()

@cli.command('discover', help=DOC['DISCOVER_HELP'])
@click.argument('provider',
                required=True,
                type=click.Choice(['aws', 'azure', 'gcp']),
                metavar='<PROVIDER>')
@click.argument('tag',
                required=True,
                metavar='<TAG>')
@PASS_CONTEXT
def discover(ctx, provider, tag):
    """ override """
    ctx.log('Discovering all BIG-IPs in %s with tag %s', provider, tag)

@cli.command('toolchain', help=DOC['TOOLCHAIN_HELP'])
@click.argument('component',
                required=True,
                type=click.Choice(['do', 'as3', 'ts', 'failover']),
                metavar='<COMPONENT>')
@click.argument('context', required=True,
                type=click.Choice(['package', 'service']),
                metavar='<CONTEXT>')
@click.argument('action',
                required=True,
                type=click.Choice(['install', 'uninstall', 'upgrade', 'verify', 'remove']),
                metavar='<ACTION>')
@click.option('--version',
              required=False)
@click.option('--declaration',
              required=False,
              metavar='<DECLARATION>')
@click.option('--template',
              required=False,
              metavar='<TEMPLATE>')
@PASS_CONTEXT
def toolchain(ctx, component, context, action, version, declaration, template):
    """ override """
    #pylint: disable-msg=too-many-arguments
    ctx.log('%s %s %s %s %s %s', action, component, context, version, declaration, template)

    client = ctx.client if hasattr(ctx, 'client') else ConfigClient().read_client()

    kwargs = {}
    if version:
        kwargs['version'] = version
    toolchain_client = ToolChainClient(client, component, **kwargs)

    if action == 'verify':
        installed = toolchain_client.package.is_installed()
        ctx.log('Toolchain component package installed: %s', (installed))
    elif action == 'install':
        toolchain_client.package.install()
        ctx.log('Toolchain component package installed')
    elif action == 'uninstall':
        toolchain_client.package.uninstall()
        ctx.log('Toolchain component package uninstalled')
    else:
        raise click.ClickException('Action not implemented')


register_repl(cli)
