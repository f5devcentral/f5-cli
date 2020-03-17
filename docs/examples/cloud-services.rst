Cloud Services Examples
=======================

Below are examples of using the CLI to interact with F5 Cloud Services.

Update an F5 Cloud Services subscription
----------------------------------------
The following is an example of how to update an F5 Cloud Services subscription, such as a DNS Load Balancer:

::

    f5 cloud-services subscription update --subscription-id s-123 --declaration decl.json
        {
            "subscription_id": "s-123",
            ...
        }

Get configuration of an F5 Cloud Services subscription
------------------------------------------------------
The following is an example of how to display or show the configuration of an existing F5 Cloud Services subscription, such as a DNS Load Balancer:

::

    f5 cloud-services subscription show --subscription-id s-123
    {
        "subscription_id": "s-123",
        ...
    }

|

.. include:: /_static/reuse/feedback.rst