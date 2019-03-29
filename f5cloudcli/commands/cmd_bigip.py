import click
from f5cloudcli.cli import pass_context

class AliasedGroup(click.Group):

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))

@click.group('bigip', short_help='BIG-IP', cls=AliasedGroup)
@pass_context
def cli(ctx):
    pass

@cli.command()
@click.option('--user', help='Username for the BIG-IP', required=True, prompt=True)
@click.option('--password', help='Password for the BIG-IP', required=True, prompt=True)
@pass_context
def login(ctx, user, password):
    ctx.log('Logging in to BIG-IP as %s using %s', user, password)

@cli.command()
@click.option('--cloud', help='Public cloud environment where the tagged BIG-IPs are running', required=True, prompt=True)
@click.option('--tag', help='Tag (key/value pair) for discovery', required=True, prompt=True)
@pass_context
def discover(ctx, cloud, tag):
    ctx.log('Discovering all BIG-IPs in %s with tag %s', cloud, tag)
