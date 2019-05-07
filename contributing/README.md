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

## Standard options

- ```--help, -h```
  - purpose: standard help relative to current command
- ```--verbose, -v```
  - purpose: increased logging
  - alternate options: --debug, --log-level debug
- ```--output, -o```
  - purpose: output format
  - alternate options: --output-format