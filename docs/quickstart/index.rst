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

Usage
-----

This example shows how to configure authentication with an existing BIG-IP system, and query the BIG-IP to determine whether or not the AS3 Toolchain component is already installed.

::

    $ f5 bigip configure-auth --host 54.224.182.104 --user myuser
    Password:
    Configuring BIG-IP Auth to 54.224.182.104 as myuser with ******

    $ f5 bigip toolchain package verify --component as3
    Toolchain component package installed: False