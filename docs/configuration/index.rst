Configuring the CLI
===================

Where is stateful configuration stored?
---------------------------------------

The F5 CLI stores configuration settings and credentials in the user's home directory inside a folder called :code:`.f5_cli`.  There are a number of files in this folder, below describes each of these files and provides an example of information typically found in each one.

:code:`auth.json` - Authentication information such as credentials used by the CLI

.. code-block:: json

    {
        "BIGIP": {
            "username": "user",
            "password": "password",
            "host": "192.0.2.10",
            "port": "443"
        },
        "CLOUD_SERVICES": {
            "username": "user",
            "password": "password"
        }
    }

:code:`config.json` - Configuration settings used by the CLI

.. code-block:: json

    {
        "output": "json"
    }

.. NOTE:: Typically changing configuration settings in these files is done using the F5 CLI directly, however for advanced use cases it may be a requirement to change the settings directly in these files.