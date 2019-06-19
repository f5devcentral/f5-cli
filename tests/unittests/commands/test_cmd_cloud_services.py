import click
from click.testing import CliRunner

from ...global_test_imports import pytest, MagicMock, call, PropertyMock

# Module under test
from f5cloudcli.commands.cmd_cloud_services import cli


class TestCommandBigIp(object):
    """ Test Class: command bigip """
    @classmethod
    def setup_class(cls):
        """ Setup func """
        cls.runner = CliRunner()

    @classmethod
    def teardown_class(cls):
        """ Teardown func """
        pass

    def test_dns_service(self, mocker):
        """ Test DNS service
        Given
        - BIG IP is up

        When
        - User attempts to create a DNS

        Then
        - Exception is thrown
        """
        result = self.runner.invoke(cli, ['dns', 'create', 'a', 'test_members'])
        assert result.output == "create DNS a with members test_members\nError: Command not implemented\n"
        assert result.exception
