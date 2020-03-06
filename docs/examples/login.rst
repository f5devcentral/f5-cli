Login examples
==============

Below are examples of using the CLI for logging into an authentication provider by setting the provided credentials as default. This is a convenience function as it is an abstraction for config auth 'create' or 'update' scenario.

Log into BIG-IP provider
------------------------
The following is an example of configuring a quick default auth account for BIG-IP. ::

    $ f5 login --authentication-provider bigip --host 192.0.2.1 --user admin --password admin


Log into F5 Cloud services provider
-----------------------------------
The following is an example of configuring a quick default auth account for Cloud Services. ::

    $ f5 login --authentication-provider cloud-services --user admin@f5.com --password admin

|

.. include:: /_static/reuse/feedback.rst