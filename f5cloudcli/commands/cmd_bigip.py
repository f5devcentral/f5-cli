import click
from f5cloudcli.cli import pass_context

@click.group('bigip', short_help='BIG-IP')
@pass_context
def cli(ctx):
    pass

@cli.command()
@click.option('--user', help='Username for the BIG-IP', required=True)
@click.option('--password', help='Password for the BIG-IP', required=True)
@pass_context
def login(ctx, user, password):
    ctx.log('Logging in to BIG-IP... user:%s password:%s', user, password)

@cli.command()
@click.option('--cloud', help='Public cloud environment where the tagged BIG-IPs are running', required=True)
@click.option('--tag', help='Tag (key/value pair) for discovery', required=True)
@pass_context
def discover(ctx, cloud, tag):
    ctx.log('Discovering BIG-IPs.. cloud:%s tag:%s', cloud, tag)
