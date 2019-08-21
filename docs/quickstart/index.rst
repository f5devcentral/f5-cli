.. _quickstart:

Prerequisites and Requirements
------------------------------

The following are prerequisites for using the F5 Cloud CLI:

- Python 3.7+. For installation instructions, see `python download docs <https://www.python.org/downloads/>`_.
- A Python virtual environment, for details see `python venv docs <https://docs.python.org/3/tutorial/venv.html>`_.
- Optional: Ignore untrusted TLS certificate warnings during HTTPS requests to BIG-IP.  See the :ref:`troubleshooting` section for more details.

Installation
------------

::

    pip install f5-cloud-cli --extra-index-url https://***REMOVED***/artifactory/api/pypi/f5-cloud-solutions-pypi/simple

Getting Help
------------

The F5 Cloud CLI includes a `--help` option, which will display relevant help information, and can be used to provide help information for each command.

The CLI will provide help information for any sub-commands, as well as relevant options. For example, providing the `--help` option without specifying any commands will provide information on the available commands:

::

    $ f5 --help
    Usage: f5 [OPTIONS] COMMAND [ARGS]...

    Welcome to the F5 Cloud command line interface.

    You can do all the things here.

    Options:
    --version      Show the version and exit.
    --verbose      Enables verbose mode
    --output TEXT  Specify output format. Allowed values: json, table.
                    [default: json]
    --help         Show this message and exit.

    Commands:
    bigip           Configure BIG-IP
    cloud-services  Configure F5 Cloud Services
    provider        Configure provider environment
    config          Configure client

The CLI will also provide help information for any commands, such as the describing how to use the `bigip toolchain service` command:

::

    $ f5 bigip toolchain service --help
    Usage: f5 bigip toolchain service [OPTIONS] [create|delete|show]

    Create, delete and verify Automation Toolchain services

    Options:
    --component [do|as3|ts|failover]
                                    [required]
    --version TEXT
    --declaration TEXT
    --install-component
    --help                          Show this message and exit.


Usage
-----

This example shows how to configure authentication with an existing BIG-IP system, and query the BIG-IP to determine whether or not the AS3 Toolchain component is already installed.

::

    $ f5 bigip configure-auth --host 54.224.182.104 --user myuser
    Password:
    Configuring BIG-IP Auth to 54.224.182.104 as myuser with ******

    $ f5 bigip toolchain package verify --component as3
    Toolchain component package installed: False