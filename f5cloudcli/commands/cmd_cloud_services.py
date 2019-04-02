""" This file provides the 'cloud_services' implementation of the CLI. """
import click
from f5cloudcli.cli import PASS_CONTEXT, AliasedGroup

@click.group('cloud_services', short_help='F5 Cloud Services (!!placeholder!!)', cls=AliasedGroup)
@PASS_CONTEXT
def cli(ctx): # pylint: disable=unused-argument
    """ F5 Cloud Services CLI sub-command """
    # pass
