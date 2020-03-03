""" This file provides the base implementation of the CLI. """

import os
import sys

import click

from f5cli import constants
from f5cli import docs
from f5cli.utils.core import format_output
from f5cli.config.telemetry import TelemetryClient

DOC = docs.get_docs()

CONTEXT_SETTINGS = dict(auto_envvar_prefix='f5cli')
CMD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'commands'))


class Context():
    """ Context class for click. """

    def __init__(self):
        self.verbose = False
        self.home = os.getcwd()

    @staticmethod
    def log(msg, *args):
        """Logs a message"""

        # if args are provided, assume string formatting is required
        if args:
            msg %= args

        click.echo(format_output(msg), file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


PASS_CONTEXT = click.make_pass_decorator(Context, ensure=True)


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


class CLI(click.MultiCommand):
    """ Base click class for the CLI. """

    def list_commands(self, ctx):
        ret = []
        for _dir in os.listdir(CMD_FOLDER):
            if os.path.isdir(os.path.join(CMD_FOLDER, _dir)) and _dir.startswith('cmd_'):
                cmd = _dir[4:]
                cmd = cmd.replace('_', '-')  # multi-word commands: foo_bar -> foo-bar
                ret.append(cmd)
        return ret

    def get_command(self, ctx, cmd_name):
        try:
            if sys.version_info[0] == 2:
                cmd_name = cmd_name.encode('ascii', 'replace')
            cmd_name = cmd_name.replace('-', '_')
            mod = __import__('f5cli.commands.cmd_' + cmd_name, None, None, ['cli'])
        except ImportError as error:
            ctx.log(error)
        return mod.cli


@click.command(cls=CLI,
               context_settings=CONTEXT_SETTINGS,
               help=DOC[('CLI_HELP')])
@click.version_option(constants.VERSION)
@click.option('--verbose',
              is_flag=True,
              help=DOC[('VERBOSE_HELP')])
@click.option('--output',
              help=DOC['OUTPUT_FORMAT_HELP'])
@PASS_CONTEXT
def cli(ctx='', output='', verbose='', home='', prog_name=''):  # pylint: disable=unused-argument
    """ main cli """

    if ctx.verbose:
        ctx.verbose = verbose
    if home is not None:
        ctx.home = home
    if output:
        os.environ[constants.ENV_VARS['OUTPUT_FORMAT']] = output

    telemetry_client = TelemetryClient(context=ctx)
    telemetry_client.report()


if __name__ == '__main__':
    cli(prog_name='f5')
