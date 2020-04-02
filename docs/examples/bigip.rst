BIG-IP Examples
===============

Below are examples of using the CLI to interact with a BIG-IP system.


Install package and post a declaration in one step
--------------------------------------------------
This example will send a declaration to AS3 and install the package if it is not already installed:

::

    f5 bigip extension as3 create --declaration as3.json

Response:
::

    { 
        "declaration":  
      {        ...    } 
    } 



Install or upgrade an extension package
---------------------------------------
The following are examples of how to install, uninstall, upgrade, and verify the AS3 package on a BIG-IP system.

Install
```````
::

    f5 bigip extension as3 install

Response:
::

    { 
        "message": "Extension component package 'as3' successfully installed version '3.17.0'" 
    } 


|

The example below shows how to install a specific version:

::

    f5 bigip extension as3 install --version 3.17.0

Response:

::

    { 
        "message": "Extension component package 'as3' successfully installed version '3.17.0'" 
    } 


|


Verify
``````
This example verifies that the package is installed on the BIG-IP and shows you the latest version available online.

::

    f5 bigip extension as3 verify

Response:

::

    {
        "installed": true,
        "installed_version": "3.17.0",
        "latest_version": "3.17.1"
    }


Upgrade
```````
This example shows you how to upgrade to a specific version.

::

    f5 bigip extension as3 upgrade --version 3.17.1

Response:

::

    {
        "message": "Successfully upgraded extension component package 'as3' to version '3.17.1'"
    }


.. note:: To revert, uninstall and then reinstall the desired version.


Uninstall
`````````

::

    f5 bigip extension as3 uninstall

Response:

::

    {
        "message": "Successfully uninstalled extension component package 'as3' version '3.17.1'"
    }



Post a declaration
------------------
The following is an example of how to configure a new service using AS3:

::

    f5 bigip extension as3 create --declaration as3_decl.json

Response:

::

    {
        "declaration": {
            ...
        }
    }


|

.. include:: /_static/reuse/feedback.rst