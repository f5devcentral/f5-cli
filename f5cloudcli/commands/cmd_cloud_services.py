import click
from f5cloudcli.cli import pass_context, AliasedGroup

@click.group('cloud_services', short_help='F5 Cloud Services (!!placeholder!!)', cls=AliasedGroup)
@pass_context
def cli(ctx):
    """Cloud Services CLI sub-command"""
    pass