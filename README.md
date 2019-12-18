# F5 CLI

## Table of Contents
- [Introduction](#introduction)
- [Quick Start](#quick-start)
- [Developer Setup](#developer-setup)
- [Artifacts](#artifacts)


## Quick Start

Pre-Release Note: Currently published in an artifactory repo.

```bash
pip3 install f5-cli --extra-index-url https://***REMOVED***/artifactory/api/pypi/f5-cloud-solutions-pypi/simple
f5 --help
```

## Developer Setup

### Installation

Note: A virtual environment should be created first.  See [python docs](https://docs.python.org/3/library/venv.html) for more details.

```bash
pip3 install -r requirements.txt
pip3 install .
f5 --help
```

### Testing

This project uses `Make` as a build automation tool... check out the Makefile for the full set of recipes.

- Run unit tests: ```make unit_test```
- Run linter: ```make lint```

## Artifacts

- Index: https://cloudsolutions.pages.***REMOVED***/f5-cli
- Code coverage report: https://cloudsolutions.pages.***REMOVED***/f5-cli/coverage/

## Supported Platforms

The CLI provides support for the following platforms.

- Linux (Ubuntu)
- Mac OS
- Windows

Pre-Release Note: This list is the intended goal, the project needs to include automated testing for each platform.