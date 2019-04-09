""" This file provides the 'bigip' implementation of the CLI. """
import click

from click_repl import register_repl

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
@click.argument('private-key',
                required=True,
                type=click.Path('sshkey'),
                metavar='<SSH_KEY>')
@PASS_CONTEXT
def login(ctx, host, user, private_key):
    """ override """
    ctx.log('Logging in to BIG-IP %s as %s with %s', host, user, private_key)

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
                type=click.Choice(['install', 'upgrade', 'verify', 'remove', 'create']),
                metavar='<ACTION>')
@click.argument('version',
                required=False)
@click.argument('declaration',
                required=False,
                type=click.File('decl'),
                metavar='<DECLARATION>')
@click.argument('template',
                required=False,
                type=click.File('tmpl'),
                metavar='<TEMPLATE>')
@PASS_CONTEXT
def toolchain(ctx, component, context, action, version, declaration, template):
    """ override """
    #pylint: disable-msg=too-many-arguments
    ctx.log('%sing %s %s %s %s', action, component, context, version, declaration, template)

register_repl(cli)
