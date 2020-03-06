BIG-IP Examples
===============

Below are examples of using the CLI to interact with a BIG-IP.


Install package and post a declaration in one step
--------------------------------------------------
This example will send a declaration to AS3 and install the package if it is not already installed:

::

    $ f5 bigip extension service create --component as3 --declaration as3.json --install-component 

    { 
        "declaration":  
      {        ...    } 
    } 



Install or upgrade an extension package
---------------------------------------
The following are the examples of how to install, uninstall, upgrade, and verify the AS3 package on a BIG-IP.  ::

Install
```````
::

    $ f5 bigip extension package install --component as3   
    { 
        "message": "Extension component package 'as3' successfully installed version '3.17.0'" 
    } 

The example below shows how to install a specific version:
::

    $ f5 bigip extension package install --component as3 --version 3.17.0
    { 
        "message": "Extension component package 'as3' successfully installed version '3.17.0'" 
    } 

This example installs the latest version available online:

::

    $ f5 bigip extension package install --component as3 --use-latest-metadata
    {
        "message": "Extension component package 'as3' successfully installed version 'x.x.x"
    }

By default, the F5 CLI uses a local metadata file to query package components (AS3, DO, TS, etc) information to perform an action. This local metadata file can become out of date with the latest version published. The example above checks for the latest version of a published component by using the flag ``--use-latest-metadata`` to fetch the latest metadata online.




Verify
``````
This example verifies that the package is installed on the BIG-IP and shows you the latest version available online.

::

    $ f5 bigip extension package verify --component as3
    {
        "installed": true,
        "installed_version": "3.17.0",
        "latest_version": "3.17.1"
    }


Upgrade
```````
This example shows you how to upgrade to a specific version.

::

    $ f5 bigip extension package upgrade --component as3 --version 3.17.1
    {
        "message": "Successfully upgraded extension component package 'as3' to version '3.17.1'"
    }

.. note:: To revert, uninstall and reinstall the desired version.


Uninstall
`````````

::

    $ f5 bigip extension package uninstall --component as3
    {
        "message": "Successfully uninstalled extension component package 'as3' version '3.17.1'"
    }



Post a declaration
------------------
The following is an example of how to configure a new service using AS3:

::

    $ f5 bigip extension service create --component as3 --declaration as3_decl.json 
    {
        "declaration": {
            ...
        }
    }


|

.. include:: /_static/reuse/feedback.rst