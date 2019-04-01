import click
from f5cloudcli.cli import pass_context, AliasedGroup

@click.group('bigip', short_help='BIG-IP', cls=AliasedGroup)
@pass_context
def cli(ctx):
    pass

@cli.command()
@click.option('--user', help='Username for the BIG-IP', required=True, prompt=True)
@click.password_option('--password', help='Password for the BIG-IP', required=True, prompt=True)
@pass_context
def login(ctx, user, password):
    ctx.log('Logging in to BIG-IP as %s', user)

@cli.command()
@click.option('--cloud', help='Public cloud environment where the tagged BIG-IPs are running', required=True, prompt=True)
@click.option('--tag', help='Tag (key/value pair) for discovery', required=True, prompt=True)
@pass_context
def discover(ctx, cloud, tag):
    ctx.log('Discovering all BIG-IPs in %s with tag %s', cloud, tag)
