""" This file provides the 'provider' implementation of the CLI. """
import click
import f5cloudcli.shared.help as helpfile
from f5cloudcli.cli import PASS_CONTEXT, AliasedGroup

@click.group('provider', short_help='Provider', cls=AliasedGroup)
@PASS_CONTEXT
def cli(ctx): # pylint: disable=unused-argument
    """ Provider sub-command """
    # pass

@cli.command('login', help=helpfile.PROVIDER_LOGIN_HELP)
@click.argument('environment')
@click.option('--user', help=helpfile.USER_HELP, required=True, prompt=True)
@click.password_option('--password', help=helpfile.PASSWORD_HELP, required=True, prompt=True)
@PASS_CONTEXT
def login(ctx, environment, user, password):
    """ Click cli command """
    ctx.log('Logging into %s as %s with %s', environment, user, password)
