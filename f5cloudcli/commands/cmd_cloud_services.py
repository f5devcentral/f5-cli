""" This file provides the 'cloud_services' implementation of the CLI. """
#pylint: disable-msg=unused-import
import click
from f5cloudcli.shared.util import getdoc
from f5cloudcli.cli import PASS_CONTEXT, AliasedGroup

DOC = getdoc()

@click.group('cloud_services', short_help='F5 Cloud Services',
             help=DOC['CLOUD_SERVICES_HELP'], cls=AliasedGroup)
@PASS_CONTEXT
def cli(ctx): # pylint: disable=unused-argument
    """ override """
    # pass

@cli.command('dns', help=DOC['DNS_HELP'])
@click.argument('item', required=True, type=click.Choice(['record']))
@click.argument('action', required=True, type=click.Choice(['create', 'delete', 'update']))
@click.argument('itype', required=True, type=click.Choice(['a', 'aaaa', 'cname']))
@click.argument('members', required=False)
@PASS_CONTEXT
def dns(ctx, item, action, itype, members):
    """ override """
    ctx.log('%s DNS %s %s with members %s', action, itype, item, members)
