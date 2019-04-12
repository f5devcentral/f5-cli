""" This file provides the 'bigip' implementation of the CLI. """
import os
import pickle
import click

from click_repl import register_repl
from f5cloudsdk.bigip import ManagementClient
from f5cloudsdk.bigip.toolchain import ToolChainClient

from f5cloudcli.shared.util import getdoc
from f5cloudcli.cli import PASS_CONTEXT, AliasedGroup
import f5cloudcli.constants as constants

DOC = getdoc()

class Config():
    """ A class used to pass BIG-IP authentication
    tokens between CLI functions.

    It will store the object returned by the
    ManagementClient class.

    It will retrieve the management client object from storage.

    If a management client object is not present, it will return an error.

    Attributes
    ----------
    client : obj
        the BIG-IP management client object

    Methods
    -------
    write_client()
        Write management client object storage
    read_client()
        Read management client object from storage
    """

    def __init__(self, **kwargs):
        """Class initialization

        Parameters
        ----------
        **kwargs:
            optional keyword arguments

        Keyword Arguments
        -----------------
        client_obj : str
            the client object returned from bigip login

        Returns
        -------
        None
        """

        self.client_obj = kwargs.pop('client', '')

    def write_client(self):
        """ used by bigip login to write fresh token to local storage """

        tmp_file = '%s' % constants.TMP_DIR
        filename = tmp_file + '/auth.json'
        client_obj = self.client_obj

        with open(filename, 'wb') as file:
            pickle.dump(client_obj, file)
        return str(filename)

    @staticmethod
    def read_client():
        """ used by cli commands to check if there is an
        existing token
        """

        tmp_file = '%s' % constants.TMP_DIR
        filename = tmp_file + '/auth.json'
        exists = os.path.isfile(filename)

        if exists:
            with open(filename, 'rb') as file:
                client_obj = pickle.load(file)
            return client_obj

        raise Exception('Command failed. You must login to BIG-IP!')

@click.group('bigip',
             short_help='BIG-IP',
             help=DOC["BIGIP_HELP"],
             cls=AliasedGroup,
             chain=True,
             no_args_is_help=True)
@PASS_CONTEXT
def cli(ctx): # pylint: disable=unused-argument
    """ override """
    # pass

@cli.command('login', help=DOC["BIGIP_LOGIN_HELP"])
@click.argument('host',
                required=True,
                metavar='<HOST>')
@click.argument('user',
                required=True,
                metavar='<USERNAME>')
@click.password_option('--password',
                       help=DOC['BIGIP_PASSWORD_HELP'],
                       required=False,
                       prompt=True,
                       confirmation_prompt=False,
                       metavar='<BIGIP_PASSWORD>')
@PASS_CONTEXT
def login(ctx, host, user, password):
    """ override """
    ctx.log('Logging in to BIG-IP %s as %s with %s', host, user, password)
    client = ManagementClient(host, user=user, password=password)
    ctx.obj = client
    Config(client=client).write_client()

@cli.command('discover', help=DOC['DISCOVER_HELP'])
@click.argument('provider',
                required=True,
                type=click.Choice(['aws', 'azure', 'gcp']),
                metavar='<PROVIDER>')
@click.argument('tag',
                required=True,
                metavar='<TAG>')
@PASS_CONTEXT
def discover(ctx, provider, tag):
    """ override """
    ctx.log('Discovering all BIG-IPs in %s with tag %s', provider, tag)

@cli.command('toolchain', help=DOC['TOOLCHAIN_HELP'])
@click.argument('component',
                required=True,
                type=click.Choice(['do', 'as3', 'ts', 'failover']),
                metavar='<COMPONENT>')
@click.argument('context', required=True,
                type=click.Choice(['package', 'service']),
                metavar='<CONTEXT>')
@click.argument('action',
                required=True,
                type=click.Choice(['install', 'upgrade', 'verify', 'remove', 'create']),
                metavar='<ACTION>')
@click.option('--version',
              type=click.Choice(['latest', 'lts']),
              default='latest',
              required=False)
@click.option('--declaration',
              required=False,
              metavar='<DECLARATION>')
@click.option('--template',
              required=False,
              metavar='<TEMPLATE>')
@PASS_CONTEXT
def toolchain(ctx, component, context, action, version, declaration, template):
    """ override """
    #pylint: disable-msg=too-many-arguments
    ctx.log('%s %s %s %s %s %s', action, component, context, version, declaration, template)

    client = ctx.obj if hasattr(ctx, 'obj') else Config().read_client()

    installer = ToolChainClient(client, component)
    installer.package.install()
    ctx.log('Success!')

register_repl(cli)
