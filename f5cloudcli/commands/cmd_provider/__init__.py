""" This file provides the 'provider' implementation of the CLI. """

import click_repl
import click

from f5cloudcli import docs
from f5cloudcli.utils import clients
from f5cloudcli.cli import PASS_CONTEXT, AliasedGroup

HELP = docs.get_docs()

@click.group('provider',
             help=HELP['PROVIDER_HELP'],
             cls=AliasedGroup)
def cli():
    """ group """

@cli.command('login',
             help=HELP['PROVIDER_LOGIN_HELP'])
@click.option('--environment',
              required=True,
              type=click.Choice(['aws', 'azure', 'gcp']))
@PASS_CONTEXT
def login(ctx, environment):
    """ command """
    provider_client = clients.get_provider_client(environment)
    if provider_client.is_logged_in():
        ctx.log('Login successful')
    else:
        ctx.log('Login unsuccessful')

click_repl.register_repl(cli)
