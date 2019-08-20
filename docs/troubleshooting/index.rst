.. _troubleshooting:

Troubleshooting
===============
Below are Troubleshooting steps that can be used while working with the F5 Cloud CLI.

*Note:* Many of the Environment Variables mentioned below influence behavior within the F5 Cloud SDK, not with with F5 Cloud CLI directly.

Enable Debugging
----------------

Debugging can be enabled by setting the following environment variable prior to using the SDK.

::

    export F5_SDK_LOG_LEVEL='DEBUG'

Ignore HTTPS warnings
---------------------

To ignore HTTPS warnings while the SDK is making HTTP requests, set the following environment variable prior to using the SDK.

::

    export PYTHONWARNINGS="ignore:Unverified HTTPS request"

.. note::
    This is not recommended for production use, please configure the BIG-IP with a valid certificate.