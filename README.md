[![Releases](https://img.shields.io/github/release/f5devcentral/f5-cli.svg)](https://github.com/f5devcentral/f5-cli/releases)
[![Issues](https://img.shields.io/github/issues/f5devcentral/f5-cli.svg)](https://github.com/f5devcentral/f5-cli/issues)

# Introduction

The F5 CLI provides a command-line interface (CLI) to various F5 products and services. It focuses primarily on facilitating consuming our most popular APIs and services, currently including BIG-IP (via Automation Tool Chain) and F5 Cloud Services. 

Similar to other popular cloud shells (for example, AWS CLI, Azure CLI, and Google gcloud), it is built on a python client library. For those looking to write custom automation scripts or workloads, one may choose to leverage the same python library it is built on (https://github.com/f5devcentral/f5-sdk-python).  

The F5 CLI is currently in early development and we want to hear from you! To provide feedback on CLI or this documentation, you can file a [GitHub Issue](https://github.com/F5Devcentral/f5-cli/issues).

Benefits: 

- Quickly access and consume F5’s APIs and Services with familiar remote CLI UX
- Configurable settings 
- Include common actions in Continuous Deployment (CD) pipelines 
- Prototyping  
    - Test calls that may be used in more complex custom integrations using the underlying SDK
    - Supports discovery activities/querying of command-line results (for example, “list accounts” to find the desired account which will be used as an input to final automation) 
- Support quick one-off automation activities (for example, leveraging a bash loop to create/delete large lists of objects)   

## Table of Contents

- [Quick Start](#quick-start)
- [User Documentation](#user-documentation)

## Quick Start

```bash
pip install f5-cli
f5 --help
```

## User Documentation

See the [documentation](https://clouddocs.f5.com/sdk/f5-cli/) for details on installation, usage and much more.

## Source Repository

See the source repository [here](https://github.com/f5devcentral/f5-cli).

## Filing Issues and Getting Help

If you come across a bug or other issue when using Cloud Failover, use [GitHub Issues](https://github.com/f5devcentral/f5-cli/issues) to submit an issue for our team.  You can also see the current known issues on that page, which are tagged with a Known Issue label.  

F5 Cloud Failover Extension is community-supported. For more information, see the [Support page](SUPPORT.md).

## Copyright

Copyright 2014-2020 F5 Networks Inc.

### F5 Networks Contributor License Agreement

Before you start contributing to any project sponsored by F5 Networks, Inc. (F5) on GitHub, you will need to sign a Contributor License Agreement (CLA).  

If you are signing as an individual, we recommend that you talk to your employer (if applicable) before signing the CLA since some employment agreements may have restrictions on your contributions to other projects. Otherwise by submitting a CLA you represent that you are legally entitled to grant the licenses recited therein.  

If your employer has rights to intellectual property that you create, such as your contributions, you represent that you have received permission to make contributions on behalf of that employer, that your employer has waived such rights for your contributions, or that your employer has executed a separate CLA with F5.

If you are signing on behalf of a company, you represent that you are legally entitled to grant the license recited therein. You represent further that each employee of the entity that submits contributions is authorized to submit such contributions on behalf of the entity pursuant to the CLA.