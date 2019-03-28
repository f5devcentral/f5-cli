import click
from f5cloudcli.cli import pass_context

@click.group('cloud_services', short_help='F5 Cloud Services')
@pass_context
def cli(ctx):
    """Cloud Services CLI sub-command"""
    pass

@cli.command()
@click.option('--destination', help='Toolchain destination BIG-IP', required=True)
@pass_context
def tool(ctx, destination):
    ctx.log('Toolchain destination BIG-IP... destination:%s', destination)

@cli.command()
@click.option('--destination', help='Configuration destination BIG-IP', required=True)
@pass_context
def configure(ctx, destination):
    ctx.log('Configuration destination BIG-IP... destination:%s', destination)
