""" This file provides the 'bigip' implementation of the CLI. """

import os

import click_repl
import click
import json

from f5cloudcli import docs
from f5cloudcli.constants import F5_CLI_DIR,F5_CONFIG_FILE
from f5cloudcli.cli import PASS_CONTEXT, AliasedGroup

HELP = docs.get_docs()

# group: bigip
@click.group('config',
             help=HELP['CONFIG_CLI_HELP'],
             cls=AliasedGroup)
def cli():
    """ group """

@cli.command('format',
             help=HELP['FORMAT_HELP'])
@click.option('--output',
              default='json',
              help=HELP['OUTPUT_HELP'],
              show_default=True)
@PASS_CONTEXT
def format(ctx, output):
    """ command """
    ctx.log('Configure client')
    # Create configuration directory if not exists
    if not os.path.exists(F5_CLI_DIR):
        os.makedirs(F5_CLI_DIR)
    else:
        # Create/overwrite F5 cli configuration file
        config_content = {
            'output': output
        }
        with open(F5_CONFIG_FILE, 'w') as outfile:
            json.dump(config_content, outfile, indent=4, sort_keys=True)

click_repl.register_repl(cli)
