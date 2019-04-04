# F5 Cloud CLI

## Table of Contents
- [Introduction](#introduction)
- [Quick Start](#quick-start)
- [Developer Setup](#developer-setup)
- [Artifacts](#artifacts)


## Quick Start

Note: Published on artifactory pypi repo.

```bash
pip3 install f5-cloud-cli --extra-index-url https://***REMOVED***/artifactory/api/pypi/f5-cloud-solutions-pypi/simple
f5 --help
```

Note: Alternatively install from local repo (any branch)

```bash
pip3 install .
```

## Developer Setup

### Installation

This is still a work in progress (no venv, etc.), however below are the current steps.

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

- Code coverage report: https://cloudsolutions.pages.***REMOVED***/f5-cloud-cli/coverage/
