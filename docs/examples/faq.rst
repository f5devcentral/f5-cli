Frequently Asked Questions (FAQ)
================================


**Does the F5 CLI collect telemetry data?**
	
F5 collects non-personal telemetry data to help improve the CLI. You can see an example of the payload that is sent below. To disable this feature, set the following environment variable ``F5_ALLOW_TELEMETRY='false'``.

.. code-block:: json

    {
        "installed": "true",
        "telemetryClientProperties": {
            "os": "Darwin"
        }
    }


-----------------------------------------


**How do I report issues, feature requests, and get help with F5 CLI?**

You can use GitHub issues to submit feature requests or problems with F5 CLI, including documentation issues.


-----------------------------------------


**Do you verify vulnerabilities for third party libraries used in SDK?**

As part of our automated release process we do verify dependency vulnerabilities for third party libraries used in SDK.
