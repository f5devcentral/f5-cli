Config Examples
===============

Below are examples of using the CLI to manage authentication and global configuration settings.

Create an authentication account
--------------------------------
The following are examples of how to create an authentication config for an authentication provider. Any commands that interact with BIG-IP or Cloud Services require that authentication to that BIG-IP is already configured.

::

    f5 config auth create --authentication-provider bigip
        --name bigip-1 --host 192.0.2.10 --user myuser

::

    f5 config auth create --authentication-provider bigip --name bigip-2
        --host 192.0.2.11 --user myuser --password mypassword --set-default

::

    f5 config auth create --authentication-provider cloud-services
        --name cs-1 --user myuser@f5.com --password blah


Update an authentication account
--------------------------------
The following are examples of how to update authentication accounts:

::

    f5 config auth update --name bigip-1 --user aws --password mypassword --set-default

::

    f5 config auth update --name cs-1 --user myuserr@f5.com --password mypassword


Delete an authentication account
--------------------------------
The following is an example of how to delete an authentication config auth: ::

    f5 config auth delete --name bigip-1



List all authentication accounts
--------------------------------
The following is an example of how to list all the authentication accounts: ::

    f5 config auth list


Toggle a default authentication account
---------------------------------------
The following is an example of how to set default authentication config auth: ::

    f5 config auth update --name cs-1 --set-default


Set global config
-----------------
The following is an example of how to set the global output format setting: ::

    # f5 config set-defaults --output json

Response:

::

    {
        "message": "CLI defaults updated successfully."
    }



Disable SSL Warnings through global config settings
---------------------------------------------------
The following is an example of how to disable SSL warnings: ::

    f5 config set-defaults --disable-ssl-warnings true



|

.. include:: /_static/reuse/feedback.rst