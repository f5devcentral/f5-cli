""" This file provides the 'config' implementation of the CLI. """

import os

import json
import click_repl
import click

from f5cli import docs
from f5cli.constants import F5_CLI_DIR, F5_CONFIG_FILE, FORMATS
from f5cli.cli import PASS_CONTEXT, AliasedGroup

HELP = docs.get_docs()


# group: configure
@click.group('configure',
             help=HELP['CONFIG_CLI_HELP'],
             cls=AliasedGroup)
def cli():
    """ group """

@cli.command('output-format',
             help=HELP['FORMAT_HELP'])
@click.option('--output',
              default=FORMATS['DEFAULT'],
              help=HELP['OUTPUT_HELP'],
              show_default=True)
@PASS_CONTEXT
def output_format(ctx, output):
    """ command """
    ctx.log('Configure client')
    # Create configuration directory if not exists
    if not os.path.exists(F5_CLI_DIR):
        os.makedirs(F5_CLI_DIR)
    # Create/overwrite F5 cli configuration file
    config_content = {
        'output': output
    }
    with open(F5_CONFIG_FILE, 'w') as outfile:
        json.dump(config_content, outfile, indent=4, sort_keys=True)


click_repl.register_repl(cli)
