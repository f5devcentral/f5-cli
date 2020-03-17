F5 CLI
======

Welcome to the F5 CLI User Guide. To provide feedback on this documentation, you can file a `GitHub Issue <https://github.com/f5devcentral/f5-cli/issues>`_.

Introduction
------------

The F5 CLI provides a command-line interface (CLI) to various F5 products and services. It focuses primarily on facilitating the consumption of our most popular APIs and services, currently including BIG-IP (via Automation Tool Chain) and F5 Cloud Services.

Similar to popular cloud shells (AWS CLI, Azure CLI, Google glcoud), it is built on a python client library. For those looking to write custom automation scripts or workloads, you may choose to leverage the same python library it is built on: 

https://github.com/f5devcentral/f5-sdk-python  

Benefits: 

- Quickly access and consume F5’s APIs and Services with familiar remote CLI UX
- Configurable settings 
- Include common actions in Continuous Deployment (CD) pipelines 
- Prototyping

    - Test calls that may be used in more complex custom integrations using the underlying SDK
    - Supports discovery activities/querying of command-line results (for example, “list accounts” to find the desired account which will be used as an input to final automation)

- Support quick one-off automation activities (for example, leveraging a bash loop to create/delete large lists of objects)   


Use the following links, the navigation on the left, and/or the Next and Previous buttons to explore the documentation.

User Guide Index
----------------

.. toctree::
   :maxdepth: 2
   :includehidden:
   :glob:

   examples/quickstart
   examples/index
   configuration/index
   examples/faq
   examples/troubleshooting


.. include:: /_static/reuse/feedback.rst
