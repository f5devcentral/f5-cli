""" This file provides the base implementation of the CLI. """
import os
import sys
import click
from f5cloudcli.shared.util import getdoc

DOC = getdoc()

CONTEXT_SETTINGS = dict(auto_envvar_prefix='F5CloudCli')

class Context():
    """ Context class for click. """

    def __init__(self):
        self.verbose = False
        self.home = os.getcwd()

    def log(self, msg, *args): # pylint: disable=no-self-use
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)

class AliasedGroup(click.Group):
    """ Alias group class for click. """

    def get_command(self, ctx, cmd_name):
        ret = click.Group.get_command(self, ctx, cmd_name)
        if ret is not None:
            return ret
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        if len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))

PASS_CONTEXT = click.make_pass_decorator(Context, ensure=True)
CMD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          'commands'))

class F5CloudCLI(click.MultiCommand):
    """ Base click class for the CLI. """

    def list_commands(self, ctx):
        ret = []
        for filename in os.listdir(CMD_FOLDER):
            if filename.endswith('.py') and \
               filename.startswith('cmd_'):
                ret.append(filename[4:-3])
        ret.sort()
        return ret

    def get_command(self, ctx, cmd_name):
        try:
            if sys.version_info[0] == 2:
                cmd_name = cmd_name.encode('ascii', 'replace')
            mod = __import__('f5cloudcli.commands.cmd_' + cmd_name,
                             None, None, ['cli'])
        except ImportError as error:
            print(error)
            return
        return mod.cli


@click.command(cls=F5CloudCLI,
               context_settings=CONTEXT_SETTINGS,
               help=DOC[('CLI_HELP')],
               no_args_is_help=True)
@click.version_option('0.9.0')
@click.option('--verbose',
              is_flag=True,
              help=DOC[('VERBOSE_HELP')])
@PASS_CONTEXT
def cli(ctx='', verbose='', home='', prog_name=''): # pylint: disable=unused-argument
    """ override """
    ctx.verbose = verbose
    if home is not None:
        ctx.home = home

if __name__ == '__main__':
    cli(prog_name='f5')
