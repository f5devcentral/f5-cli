import click
from f5cloudcli.cli import pass_context

@click.group('cloud_services', short_help='F5 Cloud Services')
@pass_context
def cli(ctx):
    """Cloud Services CLI sub-command"""
    pass

@cli.command()
@click.option('--destination', help='Toolchain destination BIG-IP', required=True, prompt=True)
@click.option('--action', help='Toolchain action', required=True, prompt=True, type=click.Choice(['install', 'upgrade', 'remove', 'verify']), default='install')
@click.option('--component', help='Toolchain component', required=True, prompt=True, type=click.Choice(['DO', 'AS3', 'TS', 'Failover', 'all components']), default='all components')
@click.option('--version', help='Toolchain component version', required=True, prompt=True, type=click.Choice(['latest', 'LTS']), default='latest')
@pass_context
def tool(ctx, destination, action, component, version):
    ctx.log('Performing %s operation of %s %s on BIG-IP %s ...', action, component, version, destination)

@cli.command()
@click.option('--destination', help='Configuration destination BIG-IP', required=True, prompt=True)
@click.option('--declaration', help='Configuration declaration file', required=True, prompt=True)
@pass_context
def configure(ctx, destination, declaration):
    ctx.log('Configuring destination BIG-IP %s using declaration %s', destination, declaration)
