Quick Start
===========

Prerequisites and Requirements
------------------------------

The following are prerequisites for using the F5 CLI:

- Python 3.7+. For installation instructions, see `python download documentation <https://www.python.org/downloads/>`_.
- A Python virtual environment, for details see `python venv documentation <https://docs.python.org/3/tutorial/venv.html>`_.
- Optional: Ignore untrusted TLS certificate warnings during HTTPS requests to BIG-IP.  See the :ref:`troubleshooting` section for more details.

Installation
------------

::

    pip install f5-cli


Quick Start
-----------

This example shows how to configure authentication with an existing BIG-IP system, and query the BIG-IP to determine whether AS3 is already installed. If it is not already installed, it will install and send a declaration.

::

    f5 login --authentication-provider bigip --host 192.0.2.10 --user myuser

    Password: <type your password here> 

Response:

::

    { 
        "message": "Logged in successfully" 
    } 

|

Verify command:

::

    f5 bigip extension as3 verify

Response:

::

    { 
        "installed": false, 
        "installed_version": "", 
        "latest_version": "3.17.1" 
    } 


If you have an AS3 declaration in a local file (as3.json), install the AS3 extension and post a declaration to it all at once:  

::

    f5 bigip extension as3 create --declaration as3.json

Response:

::

    { 
        "declaration":  
      {        ...    } 
    } 



Getting Help
------------

The F5 CLI includes a `help` option, which will display relevant help information, and can be used to provide help information for each command.

The CLI will provide help information for any sub-commands, as well as relevant options. For example, providing the `help` option without specifying any commands will show you information on the available commands:

::

    f5 --help 

Response:

::

    Usage: f5 [OPTIONS] COMMAND [ARGS]...

    Welcome to the F5 command line interface.

    Options:
    --version  Show the version and exit.
    --help     Show this message and exit.

    Commands:
    login           Login to BIG-IP, F5 Cloud Services, etc.
    bigip           Manage BIG-IP
    cs              Manage F5 Cloud Services
    config          Configure CLI authentication and configuration


The CLI will also provide help information for any commands, for example, how to use the ``f5 bigip extension`` command:

::

    f5 bigip extension --help 

Response:

::

    Usage: f5 bigip extension [OPTIONS] COMMAND [ARGS]...

    Manage extensions, such as AS3, DO, TS and CF

    Options:
    --help  Show this message and exit.

    Commands:
    as3  Manage AS3, perform installation and service operations
    cf   Manage CF, perform installation and service operations
    do   Manage DO, perform installation and service operations
    ts   Manage TS, perform installation and service operations

|

.. include:: /_static/reuse/feedback.rst