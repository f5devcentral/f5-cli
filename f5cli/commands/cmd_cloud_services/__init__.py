"""Below are examples of using the CLI to interact with F5 Cloud Services.

    1. Update an F5 Cloud Services subscription
    -------------------------------------------
    The following is an example of how to update an F5 Cloud Services subscription,
    such as a DNS Load Balancer. ::

        $ f5 cloud-services subscription update --subscription-id s-123 --declaration decl.json
        {
            "subscription_id": "s-123",
            ...
        }

    2. Get configuration of an F5 Cloud Services subscription
    ---------------------------------------------------------
    The following is an example of how to display or show the configuration of an existing
    F5 Cloud Services subscription, such as a DNS Load Balancer. ::

        $ f5 cloud-services subscription show --subscription-id s-123
        {
            "subscription_id": "s-123",
            ...
        }

"""

import click_repl
import click
from f5sdk.cloud_services import ManagementClient
from f5sdk.cloud_services.subscriptions import SubscriptionClient

from f5cli import docs
from f5cli.cli import PASS_CONTEXT, AliasedGroup
from f5cli.config import ConfigClient
from f5cli.utils import core as utils_core
from f5cli import constants

HELP = docs.get_docs()


# group: cloud-services
@click.group('cloud-services',
             help=HELP['CLOUD_SERVICES_HELP'],
             cls=AliasedGroup)
def cli():
    """ group """


@cli.command('subscription',
             help=HELP['CLOUD_SERVICES_SUBSCRIPTION_HELP'])
@click.argument('action',
                required=True,
                type=click.Choice(['show', 'update']))
@click.option('--subscription-id', required=True, metavar='<CLOUD_SERVICES_SUBSCRIPTION_ID>')
@click.option('--declaration',
              required=False,
              metavar='<SUBSCRIPTION_DECLARATION>',
              help='required if performing an update')
@PASS_CONTEXT
def subscription(ctx, action, subscription_id, declaration):
    """ Performs actions against a F5 Cloud Services subscription

    Parameters
    ----------
    action : str
        which action to perform
    subscription_id : str
        which subscription to perform the requested action on
    declaration : str
        file name or path to file of declaration to send to F5 Cloud Services

    Returns
    -------
    str
        the response for the requested action against the F5 Cloud Services subscription
    """
    # Additional option validation
    if action == 'update' and declaration is None:
        raise click.ClickException(
            'The --declaration option is required when updating a Cloud Services subscription'
        )

    auth = ConfigClient().read_auth(
        constants.AUTHENTICATION_PROVIDERS[constants.CLOUD_SERVICES_GROUP_NAME])
    mgmt_client = ManagementClient(user=auth['user'], password=auth['password'],
                                   api_endpoint=auth.pop('api_endpoint', None))

    subscription_client = SubscriptionClient(mgmt_client)
    if action == 'show':
        ctx.log(subscription_client.show(name=subscription_id))
    elif action == 'update':
        ctx.log(subscription_client.update(
            name=subscription_id,
            config_file=utils_core.convert_to_absolute(declaration)
        ))
    else:
        raise click.ClickException(f"Action {action} not implemented for 'subscription' command")


@cli.command('dns',
             help=HELP['CLOUD_SERVICES_DNS_HELP'], )
@click.argument('action',
                required=True,
                type=click.Choice(['create', 'delete', 'update']),
                metavar='<ACTION>')
@click.argument('record_type',
                required=True,
                type=click.Choice(['a', 'aaaa', 'cname']),
                metavar='<RECORD_TYPE>')
@click.argument('members',
                required=True,
                metavar='<MEMBERS>')
@PASS_CONTEXT
def dns(ctx, action, record_type, members):
    """ command """

    raise click.ClickException('Command not implemented')


click_repl.register_repl(cli)
