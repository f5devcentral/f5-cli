""" Cloud services command """

import click_repl
import click

from f5sdk.cs import ManagementClient
from f5sdk.cs.accounts import AccountClient
from f5sdk.cs.subscriptions import SubscriptionClient
from f5sdk.cs.beacon.insights import InsightsClient
from f5sdk.cs.beacon.declare import DeclareClient
from f5sdk.cs.beacon.token import TokenClient

from f5cli import docs
from f5cli.cli import PASS_CONTEXT, AliasedGroup
from f5cli.config import AuthConfigurationClient
from f5cli.utils import core as utils_core
from f5cli import constants

HELP = docs.get_docs()


def get_mgmt_client():
    """ Get Management Client """

    auth_client = AuthConfigurationClient()
    auth = auth_client.read_auth(constants.AUTHENTICATION_PROVIDERS['CS'])

    management_kwargs = dict(
        user=auth['user'],
        password=auth['password'],
        api_endpoint=auth.pop('api_endpoint', None)
    )
    return ManagementClient(**management_kwargs)


# group: cs
@click.group('cs',
             help=HELP['CS_HELP'],
             cls=AliasedGroup)
def cli():
    """ group """


@cli.command('account',
             help=HELP['CS_ACCOUNT_HELP'])
@click.argument('action',
                required=True,
                type=click.Choice(['show-user']))
@PASS_CONTEXT
def account(ctx, action):
    """ command """

    account_client = AccountClient(get_mgmt_client())
    if action == 'show-user':
        ctx.log(account_client.show_user())
    else:
        raise click.ClickException(f"Action {action} not implemented for command")


@cli.command('subscription',
             help=HELP['CS_SUBSCRIPTION_HELP'])
@click.argument('action',
                required=True,
                type=click.Choice(['list', 'show', 'update']))
@click.option('--subscription-id')
@click.option('--declaration')
@click.option('--account-id-filter')
@PASS_CONTEXT
def subscription(ctx, action, subscription_id, declaration, account_id_filter):
    """ command """

    # 'update' requires declaration
    if action == 'update' and declaration is None:
        raise click.ClickException(
            'The --declaration option is required'
        )
    # 'show' and 'update require subscription id
    if action in ['show', 'update'] and subscription_id is None:
        raise click.ClickException(
            'The --subscription-id option is required'
        )

    subscription_client = SubscriptionClient(get_mgmt_client())
    if action == 'list':
        kwargs = {}
        if account_id_filter:
            kwargs['query_parameters'] = {
                'account_id': account_id_filter
            }
        ctx.log(subscription_client.list(**kwargs))
    elif action == 'show':
        ctx.log(subscription_client.show(name=subscription_id))
    elif action == 'update':
        ctx.log(subscription_client.update(
            name=subscription_id,
            config_file=utils_core.convert_to_absolute(declaration)
        ))
    else:
        raise click.ClickException(f"Action {action} not implemented for 'subscription' command")


@cli.group('beacon',
           help=HELP['CS_BEACON_HELP'])
def beacon():
    """ group """


@beacon.group('insights',
              help=HELP['CS_BEACON_INSIGHTS_HELP'])
def insights():
    """ group """


@insights.command('list',
                  help=HELP['CS_BEACON_INSIGHTS_LIST_HELP'])
@PASS_CONTEXT
def insights_list(ctx):
    """ command """
    insights_client = InsightsClient(get_mgmt_client())
    ctx.log(insights_client.list())


@insights.command('create',
                  help=HELP['CS_BEACON_INSIGHTS_CREATE_HELP'])
@click.option('--declaration',
              required=True,
              metavar='<DECLARATION>')
@PASS_CONTEXT
def insights_create(ctx, declaration):
    """ command """

    insights_client = InsightsClient(get_mgmt_client())
    ctx.log(insights_client.create(config_file=utils_core.convert_to_absolute(declaration)))


@insights.command('update',
                  help=HELP['CS_BEACON_INSIGHTS_UPDATE_HELP'])
@click.option('--declaration',
              required=True,
              metavar='<DECLARATION>')
@PASS_CONTEXT
def insights_update(ctx, declaration):
    """ command """

    insights_client = InsightsClient(get_mgmt_client())
    ctx.log(insights_client.create(config_file=utils_core.convert_to_absolute(declaration)))


@insights.command('show',
                  help=HELP['CS_BEACON_INSIGHTS_SHOW_HELP'])
@click.option('--name',
              required=True,
              metavar='<NAME>')
@PASS_CONTEXT
def insight_show(ctx, name):
    """ command """

    insights_client = InsightsClient(get_mgmt_client())
    ctx.log(insights_client.show(name=name))


@insights.command('delete',
                  help=HELP['CS_BEACON_INSIGHTS_DELETE_HELP'])
@click.option('--name',
              required=True,
              metavar='<NAME>')
@click.option('--auto-approve',
              default=False,
              is_flag=True,
              metavar='<AUTO-APPROVE>')
@PASS_CONTEXT
def insight_delete(ctx, name, auto_approve):
    """ command """
    approval_confirmation_map = {
        'delete': 'Insight named %s will be deleted' % name
    }
    utils_core.verify_approval('delete', approval_confirmation_map, auto_approve)
    insights_client = InsightsClient(get_mgmt_client())
    result = insights_client.delete(name=name, config={})
    if result == {}:
        ctx.log('Insight deleted successfully')
    else:
        ctx.log(result)


@beacon.group('declare',
              help=HELP['CS_BEACON_DECLARE_HELP'])
def declare():
    """ group """


@declare.command('show',
                 help=HELP['CS_BEACON_DECLARE_SHOW_HELP'])
@PASS_CONTEXT
def declare_show(ctx):
    """ command """

    client = DeclareClient(get_mgmt_client())
    ctx.log(client.create(config={'action': 'get'}))


@declare.command('create',
                 help=HELP['CS_BEACON_DECLARE_CREATE_HELP'])
@click.option('--declaration',
              required=True,
              metavar='<DECLARATION>')
@PASS_CONTEXT
def declare_create(ctx, declaration):
    """ command """

    client = DeclareClient(get_mgmt_client())
    ctx.log(client.create(config_file=utils_core.convert_to_absolute(declaration)))


@beacon.group('token',
              help=HELP['CS_BEACON_TOKEN_HELP'])
def token():
    """ group """


@token.command('list',
               help=HELP['CS_BEACON_TOKEN_LIST_HELP'])
@PASS_CONTEXT
def token_list(ctx):
    """ command """
    token_client = TokenClient(get_mgmt_client())
    ctx.log(token_client.list())


@token.command('create',
               help=HELP['CS_BEACON_TOKEN_CREATE_HELP'])
@click.option('--declaration',
              required=True,
              metavar='<DECLARATION>')
@PASS_CONTEXT
def token_create(ctx, declaration):
    """ command """

    token_client = TokenClient(get_mgmt_client())
    ctx.log(token_client.create(config_file=utils_core.convert_to_absolute(declaration)))


@token.command('show',
               help=HELP['CS_BEACON_TOKEN_SHOW_HELP'])
@click.option('--name',
              required=True,
              metavar='<NAME>')
@PASS_CONTEXT
def token_show(ctx, name):
    """ command """

    token_client = TokenClient(get_mgmt_client())
    ctx.log(token_client.show(name=name))


@token.command('delete',
               help=HELP['CS_BEACON_TOKEN_DELETE_HELP'])
@click.option('--name',
              required=True,
              metavar='<NAME>')
@click.option('--auto-approve',
              default=False,
              is_flag=True,
              metavar='<AUTO-APPROVE>')
@PASS_CONTEXT
def token_delete(ctx, name, auto_approve):
    """ command """
    approval_confirmation_map = {
        'delete': 'Token named %s will be deleted' % name
    }
    utils_core.verify_approval('delete', approval_confirmation_map, auto_approve)
    token_client = TokenClient(get_mgmt_client())
    result = token_client.delete(name=name, config={})
    if result == {}:
        ctx.log('Token deleted successfully')
    else:
        ctx.log(result)


click_repl.register_repl(cli)
