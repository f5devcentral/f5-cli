""" This file provides the 'cloud_services' implementation of the CLI. """
#pylint: disable-msg=unused-import
import click
from click_repl import register_repl
from f5cloudcli.shared.util import getdoc
from f5cloudcli.cli import PASS_CONTEXT, AliasedGroup

DOC = getdoc()

@click.group('cloud_services',
             short_help='F5 Cloud Services',
             help=DOC['CLOUD_SERVICES_HELP'],
             no_args_is_help=True,
             cls=AliasedGroup)
@PASS_CONTEXT
def cli(ctx): # pylint: disable=unused-argument
    """ override """
    # pass

@cli.command('dns', help=DOC['DNS_HELP'])
@click.argument('action',
                required=True,
                type=click.Choice(['create', 'delete', 'update']),
                metavar='<ACTION>')
@click.argument('record_type',
                required=True,
                type=click.Choice(['a', 'aaaa', 'cname']),
                metavar='<RECORD_TYPE>')
@click.argument('members',
                required=False,
                metavar='<MEMBERS>')
@PASS_CONTEXT
def dns(ctx, action, record_type, members):
    """ override """
    ctx.log('%s DNS %s %s with members %s', action, record_type, members)

register_repl(cli)
