""" This file provides the 'bigip' implementation of the CLI. """
import click
from f5cloudcli.cli import PASS_CONTEXT, AliasedGroup

@click.group('bigip', short_help='BIG-IP', cls=AliasedGroup)
@PASS_CONTEXT
def cli(ctx): # pylint: disable=unused-argument
    """ Click cli function """
    # pass

@cli.command()
@click.option('--user', help='Username for the BIG-IP', required=True, prompt=True)
@click.password_option('--password', help='Password for the BIG-IP', required=True, prompt=True)
@PASS_CONTEXT
def login(ctx, user, password):
    """ Click cli command """
    ctx.log('Logging in to BIG-IP as %s', user, password)

CLOUD_HELP = 'Public cloud environment where the tagged BIG-IPs are running'
@cli.command()
@click.option('--cloud', help=CLOUD_HELP, required=True, prompt=True)
@click.option('--tag', help='Tag (key/value pair) for discovery', required=True, prompt=True)
@PASS_CONTEXT
def discover(ctx, cloud, tag):
    """ Click cli command """
    ctx.log('Discovering all BIG-IPs in %s with tag %s', cloud, tag)
