Cloud Services Examples
=======================

Below are examples of using the CLI to interact with F5 Cloud Services.

List information for the current user
-------------------------------------
The following is an example of how to list information for the currently authenticated user:

::

    f5 cs account show-user

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

    f5 cs subscription list --account-id-filter a-123

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

    f5 cs subscription update --subscription-id s-123 --declaration decl.json

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

    f5 cs subscription show --subscription-id s-123

Response:
::

    {
        "subscription_id": "s-123",
        ...
    }

Show the F5 Cloud Services Declaration
--------------------------------------
The following is an example of how to display or show the existing F5 Cloud Services Beacon Declaration, which contains things such as applications:

::

    f5 cs beacon declare show

Response:
::

    {
        "action": "get",
        "declaration": []
    }

Create or Update the F5 Cloud Services Declaration
--------------------------------------------------
The following is an example of how to create or update an application using the F5 Cloud Services Beacon Declarative API:

::

    f5 cs beacon declare create --declaration decl.json

Response:
::

    {
        "action": "deploy",
        "declaration": []
    }

Create a F5 Cloud Services Beacon insight
-----------------------------------------
The following is an example of how to create a F5 Cloud Services Beacon Insight:

::

    f5 cs beacon insight create --declaration example-insight.json

Response:
::

    {
        "title": "example-title",
        "description": "example-description",
        ...
    }

Update a F5 Cloud Services Beacon insight
-----------------------------------------
The following is an example of how to update a F5 Cloud Services Beacon Insight:

::

    f5 cs beacon insight update --declaration example-insight-2.json

Response:
::

    {
        "title": "example-title",
        "description": "example-description-2",
        ...
    }

Show a F5 Cloud Services Beacon insight
---------------------------------------
The following is an example of how to show a F5 Cloud Services Beacon Insight:

::

    f5 cs beacon insight show --title example-title

Response:
::

    {
        "title": "example-title",
        "description": "example-description-2",
        ...
    }

Delete a F5 Cloud Services Beacon insight
-----------------------------------------
The following is an example of how to delete a F5 Cloud Services Beacon Insight:

::

    f5 cs beacon insight delete --title example-title

Response:
::

    {
        "message": "Insight deleted successfully"
    }

List F5 Cloud Services Beacon insights
--------------------------------------
The following is an example of how to list F5 Cloud Services Beacon Insights:

::

    f5 cs beacon insight list

Response:
::

    "insights": [
        {
            "title": "insight-1",
            ...
        },
        {
            "title": "insight-2",
            ...
        }
    ]

Create a F5 Cloud Services Beacon token
---------------------------------------
The following is an example of how to create a F5 Cloud Services Beacon Token:

::

    f5 cs beacon token create --declaration example-token.json

Response:
::

    {
        "name": "example-name",
        ...
    }

Show a F5 Cloud Services Beacon token
-------------------------------------
The following is an example of how to show a F5 Cloud Services Beacon Token:

::

    f5 cs beacon token show --name example-name

Response:
::

    {
        "name": "example-name"
        ...
    }
Delete a F5 Cloud Services Beacon token
---------------------------------------
The following is an example of how to delete a F5 Cloud Services Beacon Token:

::

    f5 cs beacon token delete --name example-name

Response:
::

    {
        "message": "Token deleted successfully"
    }

List F5 Cloud Services Beacon tokens
------------------------------------
The following is an example of how to list F5 Cloud Services Beacon tokens:

::

    f5 cs beacon token list

Response:
::

    "tokens": [
        {
            "name": "token-1",
            ...
        },
        {
            "name": "token-2",
            ...
        }
    ]

|

.. include:: /_static/reuse/feedback.rst
