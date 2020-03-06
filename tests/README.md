# Introduction

This directory contains all of the tests for this project.  This documentation is designed to make clear things that would otherwise be unclear.

Tests reside inside the `tests` directory, but you know that... since you found this README.

## Unit

All unit tests are written using the [pytest](https://docs.pytest.org/en/latest/) framework, and run using `make test` during automated test.

Triggered: Every commit pushed to central repository.

Best practices:

- Create a separate folder for each top-level source package being tested.
- Keep mocking simple, use one of the following (in order of preference)
    - Use [mocker fixture](https://github.com/pytest-dev/pytest-mock)
    - Use [unittest.mock](https://docs.python.org/3/library/unittest.mock.html) - Available via `pytest-mock`
- Treat tests as a first class citizen: Use OOP principles, etc...
- Monitor and enforce coverage, but avoid writing tests simply to increase coverage when there is no other perceived value.
- With that being said, **enforce coverage** in automated test.


## Functional

Note: Currently functional tests simply consist of a terraform and ansible example deployment plan that makes use of the F5 CLI.

Triggered: If smart commit contains `smart:run_functional_tests` or if environment variable `RUN_FUNCTIONAL_TESTS` has a value of true.

Best Practices:

- Clean up after yourself - although it is a fairly safe assumption to make that this is a fresh environment consider if it were multi-use when writing tests
- Consider carefully before testing things in functional test that should or could be tested via unit test - those are run more frequently

### Environment

It is somewhat implied that running the functional tests requires a runtime (BIG-IP, container, etc.) to deploy the iLX extension, consumers, etc.  The current methodology is to deploy and subsequently teardown the runtime every time functional tests are run, with the understanding that functional tests will be run less frequently than unit tests.

To do automated environment creation this project makes use of `automation-sdk/deployment-tool`, please see that repository for more information.

#### Manual Environment Setup

Creating an environment manually using the same methodology as automated tests is entirely acceptable, in fact it is anticipated for development.  For more information, including usage, please see the `automation-sdk/deployment-tool` repository.