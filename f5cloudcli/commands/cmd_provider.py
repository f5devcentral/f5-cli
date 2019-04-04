""" This file provides the 'provider' implementation of the CLI. """
import click
from f5cloudcli.cli import PASS_CONTEXT, AliasedGroup

@click.group('provider', short_help='Provider', cls=AliasedGroup)
@PASS_CONTEXT
def cli(ctx): # pylint: disable=unused-argument
    """ Provider sub-command """
    # pass

LOGIN_HELP = 'Use this command to log into the cloud provider'
USER_HELP = 'Username for logging into the provider'
PASSWORD_HELP = 'Password for logging into the provider'
@cli.command(help=LOGIN_HELP)
@click.argument('environment')
@click.option('--user', help=USER_HELP, required=True, prompt=True)
@click.password_option('--password', help=PASSWORD_HELP, required=True, prompt=True)
@PASS_CONTEXT
def login(ctx, environment, user, password):
    """ Click cli command """
    ctx.log('Logging into %s as %s with %s', environment, user, password)
