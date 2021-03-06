# Introduction

This contains useful information about contributing to this project.

## Style Guide

In short this is a set of rules to ensure users of the CLI find it intuitive and acts like they expect based on interaction with other industry CLI UX

- Be consistent with POSIX tools - cat, grep, awk, etc.
- Be consistent with successful existing CLI UX's (see Discovery for more details)
- Commands should follow a consistent pattern: " [ command (f5) ] [ sub-command (product) ] [ sub-command (feature) ] [ argument (required data) ] [ --options (change command behavior) ] "
- Commands should use consistent verbiage: " [ noun ] [ noun ] [ noun ] [ verb ] [ --options ] "
- Multi-word commands should use "-" as the separator: " f5 bigip cloud-services "
- All commands must support standard options
- Prefer long options over short, --output instead of -o.
- Make use of aliasing and auto complete, where possible
- For Leaf endpoints of a resource, the verb use does not have to conform to be CRUD operation and does not require a command subgroup. For examples, see cf extension CRUD operations.

## Standard options

- ```--help, -h```
  - purpose: standard help relative to current command
- ```--verbose, -v```
  - purpose: increased logging
  - alternate options: --debug, --log-level debug
- ```--output, -o```
  - purpose: output format
  - alternate options: --output-format

## State

This project maintains stateful configuration, in general below is the files that may exist.

- `~/.f5cli/` - root state directory (inside user's home directory)
    - `config.yaml`
        - Purpose: Any stateful configuration settings for the CLI, such as default output format, telemetry choice, etc.
    - `auth.yaml`
        - Purpose: Authentication tokens, etc. derived from `login` or `config auth` command(s)

## Authentication configuration

This flowchart describes the high-level decisions around authentication behavior.

![diagram](../docs/diagrams/auth_decision_tree.png)

### Creating a profile for authentication

`f5 config auth create --authentication-provider bigip --name bigip-2 --host 192.0.2.10 --user myuser --password mypassword --set-default`
