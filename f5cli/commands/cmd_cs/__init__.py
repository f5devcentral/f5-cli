""" Cloud services command """

import click_repl
import click
from f5sdk.cs import ManagementClient
from f5sdk.cs.accounts import AccountClient
from f5sdk.cs.subscriptions import SubscriptionClient
from f5sdk.cs.beacon.insights import InsightsClient

from f5cli import docs
from f5cli.cli import PASS_CONTEXT, AliasedGroup
from f5cli.config import AuthConfigurationClient
from f5cli.utils import core as utils_core
from f5cli import constants

HELP = docs.get_docs()


# group: cs
@click.group('cs',
             help=HELP['CS_HELP'],
             cls=AliasedGroup)
@PASS_CONTEXT
def cli(ctx):
    """ group """

    auth = AuthConfigurationClient().read_auth(
        constants.AUTHENTICATION_PROVIDERS[constants.CS_GROUP_NAME]
    )
    ctx.mgmt_client = ManagementClient(
        user=auth['user'],
        password=auth['password'],
        api_endpoint=auth.pop('api_endpoint', None)
    )


@cli.command('account',
             help=HELP['CS_ACCOUNT_HELP'])
@click.argument('action',
                required=True,
                type=click.Choice(['show-user']))
@PASS_CONTEXT
def account(ctx, action):
    """ Performs actions against F5 Cloud Services account(s)

    Parameters
    ----------
    action : str
        which action to perform

    Returns
    -------
    None
    """

    account_client = AccountClient(ctx.mgmt_client)
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
    """ Performs actions against F5 Cloud Services subscription

    Parameters
    ----------
    action : str
        which action to perform
    subscription_id : str
        which subscription to perform the requested action on
    declaration : str
        file name or path to file of declaration to send to F5 Cloud Services
    account_id_filter : str
        account ID to use as a filter, typically during a list call

    Returns
    -------
    None
    """

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

    subscription_client = SubscriptionClient(ctx.mgmt_client)
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
    insights_client = InsightsClient(ctx.mgmt_client)
    ctx.log(insights_client.list())


@insights.command('create',
                  help=HELP['CS_BEACON_INSIGHTS_CREATE_HELP'])
@click.option('--declaration',
              required=True,
              metavar='<DECLARATION>')
@PASS_CONTEXT
def insights_create(ctx, declaration):
    """ command """

    insights_client = InsightsClient(ctx.mgmt_client)
    ctx.log(insights_client.create(config=declaration))


@insights.command('update',
                  help=HELP['CS_BEACON_INSIGHTS_UPDATE_HELP'])
@click.option('--declaration',
              required=True,
              metavar='<DECLARATION>')
@PASS_CONTEXT
def insights_update(ctx, declaration):
    """ command """

    insights_client = InsightsClient(ctx.mgmt_client)
    ctx.log(insights_client.create(config=declaration))


@insights.command('show',
                  help=HELP['CS_BEACON_INSIGHTS_SHOW_HELP'])
@click.option('--title',
              required=True,
              metavar='<TITLE>')
@PASS_CONTEXT
def insight_show(ctx, title):
    """ command """

    insights_client = InsightsClient(ctx.mgmt_client)
    ctx.log(insights_client.show(name=title))


@insights.command('delete',
                  help=HELP['CS_BEACON_INSIGHTS_DELETE_HELP'])
@click.option('--title',
              required=True,
              metavar='<TITLE>')
@PASS_CONTEXT
def insight_delete(ctx, title):
    """ command """

    insights_client = InsightsClient(ctx.mgmt_client)
    insights_client.delete(name=title, config={})
    ctx.log('Insight deleted successfully')


click_repl.register_repl(cli)
