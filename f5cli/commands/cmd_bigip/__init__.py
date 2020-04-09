""" BIG-IP command """

# pylint: disable=too-many-arguments

import click_repl
import click

from f5sdk.bigip import ManagementClient

from f5cli import docs, constants
from f5cli.commands.cmd_bigip.extension_operations import ExtensionOperationsClient, COMPONENTS
from f5cli.config import AuthConfigurationClient
from f5cli.cli import PASS_CONTEXT, AliasedGroup
from f5cli.commands.cmd_bigip.extension_operations import check_install
from f5cli.utils.core import verify_approval

HELP = docs.get_docs()


# group: bigip
@click.group('bigip',
             help=HELP['BIGIP_HELP'],
             cls=AliasedGroup)
def cli():
    """ group """


# group: extension - as3, do, ts, cf
@cli.group('extension',
           help=HELP['BIGIP_EXTENSION_HELP']
           )
def extension():
    """ group """


@extension.command('as3',
                   help=HELP['BIGIP_EXTENSION_AS3_HELP']
                   )
@click.argument('action',
                required=True,
                type=click.Choice(COMPONENTS['as3']['actions']))
@click.option('--version',
              required=False
              )
@click.option('--declaration',
              required=False
              )
@click.option('--package-url',
              required=False,
              type=click.STRING
              )
@click.option('--auto-approve',
              default=False,
              is_flag=True,
              metavar='<AUTO-APPROVE>')
@PASS_CONTEXT
def command_as3(ctx, action, version, declaration, package_url, auto_approve):
    """ command """

    approval_confirmation_map = {
        'delete': 'AS3 declaration will be removed',
        'uninstall': 'AS3 package will be uninstalled'
    }
    verify_approval(action, approval_confirmation_map, auto_approve)
    extension_operations_client = ExtensionOperationsClient(
        get_mgmt_client(),
        'as3',
        version,
        package_url)
    extension_operations_client.install_component_if_required(check_install(action))
    output = process_extension_component_command(
        extension_operations_client,
        COMPONENTS['as3']['actions'],
        action,
        declaration=declaration
    )
    ctx.log(output)


@extension.command('do',
                   help=HELP['BIGIP_EXTENSION_DO_HELP']
                   )
@click.argument('action',
                required=True,
                type=click.Choice(COMPONENTS['do']['actions']))
@click.option('--version',
              required=False)
@click.option('--declaration',
              required=False)
@click.option('--package-url',
              required=False,
              type=click.STRING)
@click.option('--auto-approve',
              default=False,
              is_flag=True,
              metavar='<AUTO-APPROVE>')
@PASS_CONTEXT
def command_do(ctx, action, version, declaration, package_url, auto_approve):
    """ command """
    approval_confirmation_map = {
        'uninstall': 'DO package will be uninstalled'
    }
    verify_approval(action, approval_confirmation_map, auto_approve)
    extension_operations_client = ExtensionOperationsClient(
        get_mgmt_client(),
        'do',
        version,
        package_url
    )
    extension_operations_client.install_component_if_required(check_install(action))
    output = process_extension_component_command(
        extension_operations_client,
        COMPONENTS['do']['actions'],
        action,
        declaration=declaration
    )
    ctx.log(output)


@extension.command('ts',
                   help=HELP['BIGIP_EXTENSION_TS_HELP']
                   )
@click.argument('action',
                required=True,
                type=click.Choice(COMPONENTS['ts']['actions']))
@click.option('--version',
              required=False)
@click.option('--declaration',
              required=False)
@click.option('--package-url',
              required=False,
              type=click.STRING)
@click.option('--auto-approve',
              default=False,
              is_flag=True,
              metavar='<AUTO-APPROVE>')
@PASS_CONTEXT
def command_ts(ctx, action, version, declaration, package_url, auto_approve):
    """ command """
    approval_confirmation_map = {
        'uninstall': 'TS package will be uninstalled'
    }
    verify_approval(action, approval_confirmation_map, auto_approve)
    extension_operations_client = ExtensionOperationsClient(
        get_mgmt_client(),
        'ts',
        version,
        package_url
    )
    extension_operations_client.install_component_if_required(check_install(action))
    output = process_extension_component_command(
        extension_operations_client,
        COMPONENTS['ts']['actions'],
        action,
        declaration=declaration
    )
    ctx.log(output)


@extension.command('cf',
                   help=HELP['BIGIP_EXTENSION_CF_HELP']
                   )
@click.argument('action',
                required=True,
                type=click.Choice(COMPONENTS['cf']['actions']))
@click.option('--version',
              required=False)
@click.option('--declaration',
              required=False)
@click.option('--package-url',
              required=False,
              type=click.STRING)
@click.option('--auto-approve',
              default=False,
              is_flag=True,
              metavar='<AUTO-APPROVE>')
@PASS_CONTEXT
def command_cf(ctx, action, version, declaration, package_url, auto_approve):
    """ command """
    approval_confirmation_map = {
        'uninstall': 'CF package will be uninstalled',
        'reset': 'CF service will be reset'
    }
    verify_approval(action, approval_confirmation_map, auto_approve)
    extension_operations_client = ExtensionOperationsClient(
        get_mgmt_client(),
        'cf',
        version,
        package_url
    )
    extension_operations_client.install_component_if_required(check_install(action))
    output = process_extension_component_command(
        extension_operations_client,
        COMPONENTS['cf']['actions'],
        action,
        declaration=declaration
    )
    ctx.log(output)


def get_mgmt_client():
    """ Get Management Client """

    auth_client = AuthConfigurationClient()
    auth = auth_client.read_auth(constants.AUTHENTICATION_PROVIDERS['BIGIP'])

    management_kwargs = dict(
        port=auth['port'],
        user=auth['user'],
        password=auth['password']
    )
    return ManagementClient(auth['host'], **management_kwargs)


def process_extension_component_command(client, allowed_actions, action, **kwargs):
    """ Process extension component actions """

    declaration = kwargs.pop('declaration', None)

    if action not in allowed_actions:
        raise click.ClickException('Action \'{}\' not implemented'.format(action))

    try:
        actions_switch = {
            'verify': client.verify_package,
            'install': client.install_package,
            'uninstall': client.uninstall_package,
            'upgrade': client.upgrade_package,
            'list-versions': client.list_package_versions,
            'show': client.show_service,
            'create': client.create_service,
            'delete': client.delete_service,
            'show-info': client.show_info_service,
            'show-failover': client.show_failover_service,
            'trigger-failover': client.trigger_failover_service,
            'show-inspect': client.show_inspect_service,
            'reset': client.reset_service,
        }
        action_to_perform = actions_switch.get(action, lambda: None)
        # process any optional function arguments
        args = []
        if action in ['create', 'trigger-failover', 'reset']:
            args.append(declaration)
        return action_to_perform(*args)
    except Exception as error:
        raise click.ClickException(error)


click_repl.register_repl(cli)
