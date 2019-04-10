""" This file provides the 'provider' implementation of the CLI. """
import click
from click_repl import register_repl

from f5cloudcli.shared.util import getdoc
from f5cloudcli.cli import PASS_CONTEXT, AliasedGroup

DOC = getdoc()

@click.group('provider',
             short_help='Provider',
             help=DOC['PROVIDER_HELP'],
             no_args_is_help=True,
             cls=AliasedGroup)
@PASS_CONTEXT
def cli(ctx): # pylint: disable=unused-argument
    """ override """
    # pass

@cli.command('login', help=DOC['PROVIDER_LOGIN_HELP'])
@click.argument('environment',
                required=True,
                type=click.Choice(['aws', 'azure', 'gcp']),
                metavar='<ENVIRONMENT>')
@click.argument('user', required=True, metavar='<USERNAME>')
@click.password_option('--password',
                       help=DOC['PASSWORD_HELP'],
                       required=True,
                       prompt=True,
                       metavar='<PROVIDER_PASSWORD>')
@PASS_CONTEXT
def login(ctx, environment, user, password):
    """ override """
    ctx.log('Logging into %s as %s with %s', environment, user, password)

register_repl(cli)
