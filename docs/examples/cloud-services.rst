1: Configure authentication to F5 Cloud Services
-------------

The following is an example of how to configure authentication to F5 Cloud Services. Any commands that interact with F5 Cloud Services require that authentication to F5 Cloud Services already be configured.

::

    $ f5 cloud-services configure-auth --user user@us.com
    Password:
    Configuring F5 Cloud Services Auth for user@us.com with ******


2: Update an F5 Cloud Services subscription
-------------

The following is an example of how to update an F5 Cloud Services subscription, such as a DNS Load Balancer.

::

    $ f5 cloud-services subscription update --subscription-id s-123 --declaration decl.json
    Calling update against the s-123 subscription in F5 Cloud Services
    Cloud Services Subscription updated:
    {
        "subscription_id": "s-123",
        ...
    }


3: Get configuration of an F5 Cloud Services subscription
-------------

The following is an example of how to display or show the configuration of an existing F5 Cloud Services subscription, such as a DNS Load Balancer.

::

    $ f5 cloud-services subscription show --subscription-id s-123 
    Calling show against the s-123 subscription in F5 Cloud Services
    Cloud Services Subscription updated:
    {
        "subscription_id": "s-123",
        ...
    }