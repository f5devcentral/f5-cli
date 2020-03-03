Frequently Asked Questions (FAQ)
================================

Does the CLI collect telemetry data?
````````````````````````````````````

F5 collects non-personal telemetry data to help improve the CLI. You can see an example of the payload that is sent below. To disable this feature, set the following environment variable ``F5_ALLOW_TELEMETRY='false'``.

.. code-block:: json

    {
        "installed": "true",
        "telemetryClientProperties": {
            "os": "Darwin"
        }
    }
