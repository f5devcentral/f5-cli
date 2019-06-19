import click
from click.testing import CliRunner

from ...global_test_imports import pytest, MagicMock, call, PropertyMock
from f5cloudcli.utils import clients

# Module under test
from f5cloudcli.commands.cmd_provider import cli


class TestCommandProvider(object):
    """ Test Class: command provider """
    @classmethod
    def setup_class(cls):
        """ Setup func """
        cls.runner = CliRunner()

    @classmethod
    def teardown_class(cls):
        """ Teardown func """
        pass

    def test_cmd_bigip_login_with_credentials(self, mocker):
        """ Log into a cloud
        Given
        - Cloud credentials

        When
        - User attempts to log into a cloud

        Then
        - Login is successful
        """
        mock_provider_client = mocker.patch('f5cloudcli.commands.cmd_provider.clients.get_provider_client')
        mock_provider_client.return_value.is_logged_in.return_value = True

        result = self.runner.invoke(cli, ['login', '--environment', 'azure'])
        assert result.output == "Login successful\n"

    def test_cmd_bigip_login_no_credentials(self, mocker):
        """ Log into a cloud
        Given
        - Cloud credentials

        When
        - User attempts to log into a cloud

        Then
        - Login is successful
        """
        mock_provider_client = mocker.patch('f5cloudcli.commands.cmd_provider.clients.get_provider_client')
        mock_provider_client.return_value.is_logged_in.return_value = False

        result = self.runner.invoke(cli, ['login', '--environment', 'azure'])
        assert result.output == "Login unsuccessful\n"
    