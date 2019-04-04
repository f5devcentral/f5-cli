""" This file provides the 'bigip' implementation of the CLI. """
import click
from f5cloudcli.cli import PASS_CONTEXT, AliasedGroup

@click.group('bigip', short_help='BIG-IP', cls=AliasedGroup)
@PASS_CONTEXT
def cli(ctx): # pylint: disable=unused-argument
    """ Click cli function """
    # pass

USER_HELP= 'Username for logging into the BIG-IP'
SSH_KEY_HELP= 'SSH key for logging into the BIG-IP'
@cli.command()
@click.option('--user', help=USER_HELP, required=True, prompt=False)
@click.argument('private-key', required=False, type=click.File('sshkey'))
@PASS_CONTEXT
def login(ctx, user, private_key):
    """ Click cli command """
    ctx.log('Logging in to BIG-IP as %s', user)

CLOUD_HELP = 'Public cloud environment where the tagged BIG-IPs are running'
TAG_HELP = 'Tag (key/value pair) for discovery'
@cli.command()
@click.option('--provider', help=CLOUD_HELP, required=True, prompt=True, type=click.Choice(['aws', 'azure', 'gcp']))
@click.option('--tag', help=TAG_HELP, required=True, prompt=True)
@PASS_CONTEXT
def discover(ctx, provider, tag):
    """ Click cli command """
    ctx.log('Discovering all BIG-IPs in %s with tag %s', provider, tag)

TOOLCHAIN_HELP = 'Use this command to install, upgrade, and verify Automation Toolchain packages and services'
@cli.command(help=TOOLCHAIN_HELP)
@click.argument('component', required=False, type=click.Choice(['do', 'as3', 'ts', 'failover']))
@click.argument('context', required=False, type=click.Choice(['package', 'service']))
@click.argument('action', required=False, type=click.Choice(['install', 'upgrade', 'verify', 'remove', 'create']))
@click.option('-v', '--version', required=False, prompt=False)
@click.argument('declaration', required=False, type=click.File('decl'))
@PASS_CONTEXT
def toolchain(ctx, component, context, action, version, declaration):
    """ Click cli command """
    ctx.log('%s %s %s %s %s', action, component, context, version, declaration)
