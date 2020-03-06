.. _troubleshooting:

Troubleshooting
===============
Below are Troubleshooting steps that can be used while working with the F5 CLI.


Enable Debugging
----------------

Debugging can be enabled by setting the following environment variable prior to using the SDK.

::

    export F5_SDK_LOG_LEVEL='DEBUG'


Ignore HTTPS warnings
---------------------

To ignore HTTPS warnings while the SDK is making HTTP requests, configure the following setting.

::

    f5 config set-defaults --disable-ssl-warnings true

.. WARNING::
    This is not recommended for production use, please configure the BIG-IP with a valid certificate.

|

.. include:: /_static/reuse/feedback.rst