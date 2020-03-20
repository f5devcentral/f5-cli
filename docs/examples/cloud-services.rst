Cloud Services Examples
=======================

Below are examples of using the CLI to interact with F5 Cloud Services.

List information for the current user
-------------------------------------
The following is an example of how to list information for the currently authenticated user:

::

    f5 cloud-services account show-user

Response:
::

        {
            "primary_account_id": "a-123",
            ...
        }

List F5 Cloud Services subscriptions (with filter)
--------------------------------------------------
The following is an example of how to list subscriptions with an account id filter:

::

    f5 cloud-services subscription list --account-id-filter a-123

Response:
::

        [
            {
                "subscription_id": "s-123",
                ...
            }
        ]


Update an F5 Cloud Services subscription
----------------------------------------
The following is an example of how to update an F5 Cloud Services subscription, such as a DNS Load Balancer:

::

    f5 cloud-services subscription update --subscription-id s-123 --declaration decl.json

Response:
::

        {
            "subscription_id": "s-123",
            ...
        }

Get configuration of an F5 Cloud Services subscription
------------------------------------------------------
The following is an example of how to display or show the configuration of an existing F5 Cloud Services subscription, such as a DNS Load Balancer:

::

    f5 cloud-services subscription show --subscription-id s-123

Response:
::

    {
        "subscription_id": "s-123",
        ...
    }

|

.. include:: /_static/reuse/feedback.rst