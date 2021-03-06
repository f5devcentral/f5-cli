Configuring the CLI
===================

Where is stateful configuration stored?
---------------------------------------

The F5 CLI stores configuration settings and credentials in the user's home directory inside a folder called :code:`.f5_cli`.  There are a number of files in this folder. Below you can see a description for each of these files and an example of information typically found in each one.

:code:`auth.yaml` - Authentication information such as credentials used by the CLI

.. code-block:: yaml

    - name: bigip1
      host: 192.0.2.10
      authentication-type: bigip
      password: mypassword1
      port: 443
      username: myuser1
      default: true
    - name: bigip2
      host: 192.0.2.11
      authentication-type: bigip
      password: mypassword2
      port: 443
      username: myuser2
      default: false
    - name: cs1
      password: mypassword3
      authentication-type: cs
      username: myuser1@f5.com
      default: true

:code:`config.yaml` - Configuration settings used by the CLI

.. code-block:: yaml

    output: json

.. NOTE:: Typically changing configuration settings in these files is done using the F5 CLI directly, however for advanced use cases it may be a requirement to change the settings directly in these files.

|

.. include:: /_static/reuse/feedback.rst