""" This file provides the 'bigip' implementation of the CLI. """
import click
import f5cloudcli.shared.help as helpfile
from f5cloudcli.cli import PASS_CONTEXT, AliasedGroup

@click.group('bigip', short_help='BIG-IP', cls=AliasedGroup, chain=True)
@PASS_CONTEXT
def cli(ctx): # pylint: disable=unused-argument
    """ Click cli function """

@cli.command('login', help=helpfile.BIGIP_LOGIN_HELP)
@click.option('--host', help=helpfile.HOST_HELP, required=True, prompt=False)
@click.option('--user', help=helpfile.USER_HELP, required=True, prompt=False)
@click.option('--private-key', help=helpfile.SSH_KEY_HELP, required=True,
              type=click.Path('sshkey'), prompt=False)
@PASS_CONTEXT
def login(ctx, host, user, private_key):
    """ Click cli command """
    ctx.log('Logging in to BIG-IP %s as %s with %s', host, user, private_key)

@cli.command('discover', help=helpfile.DISCOVER_HELP)
@click.option('--provider', help=helpfile.CLOUD_HELP, required=True,
              prompt=True, type=click.Choice(['aws', 'azure', 'gcp']))
@click.option('--tag', help=helpfile.TAG_HELP, required=True, prompt=True)
@PASS_CONTEXT
def discover(ctx, provider, tag):
    """ Click cli command """
    ctx.log('Discovering all BIG-IPs in %s with tag %s', provider, tag)

@cli.command('toolchain', help=helpfile.TOOLCHAIN_HELP)
@click.argument('component', required=False, type=click.Choice(['do', 'as3', 'ts', 'failover']))
@click.argument('context', required=False, type=click.Choice(['package', 'service']))
@click.argument('action', required=False,
                type=click.Choice(['install', 'upgrade', 'verify', 'remove', 'create']))
@click.option('--version', help='Package version', required=False, prompt=False)
@click.option('--declaration', required=False, type=click.File('decl'))
@PASS_CONTEXT
def toolchain(ctx, component, context, action, version, declaration):
    #pylint: disable-msg=too-many-arguments
    """ Click cli command """
    ctx.log('%sing %s %s %s %s', action, component, context, version, declaration)
