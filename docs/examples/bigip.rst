1: Discover BIG-IPs running in a Cloud Provider
-------------

The following is an example of how to discover information about a BIG-IP, including IP addresses, running in a cloud provider.

::

    $ export F5_CLI_PROVIDER_ACCESS_KEY=<aws_access_key_id>
    $ export F5_CLI_PROVIDER_SECRET_KEY=<aws_secret_access_key>
    $ export F5_CLI_PROVIDER_REGION_NAME=<region>
    $ f5 bigip discover --provider aws --provider-tag "MyTagKey:value1"
    Discovering all BIG-IPs in aws with tag MyTagKey:value1
    {
        "id": "i-0e331f5ca76ad231d",
        ...
    }


2: Configure authentication to a BIG-IP
-------------

The following is an example of how to configure authentication for a BIG-IP. Any commands that interact with a BIG-IP require that authentication to that BIG-IP is already configured.

::

    $ f5 bigip configure-auth --host 54.224.182.104 --user myuser
    Password:
    Configuring BIG-IP Auth to 54.224.182.104 as myuser with ******


3: Install an Automation Toolchain package
-------------

The following is an example of how to install the Declarative Onboarding package onto a BIG-IP

::

    $ f5 bigip toolchain package install --component do
    Toolchain component package do installed


4: Install an Automation Toolchain service
-------------

The following is an example of how to configure a new service using AS3

::

    $ f5 bigip toolchain service --component as3 --declaration as3_decl.json create
    Toolchain component service create: {
        "declaration": {
            ...
        }
    }