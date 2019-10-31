""" Test Provider command """

import json

from f5cloudcli.commands.cmd_provider import cli

from ...global_test_imports import CliRunner


class TestCommandProvider(object):
    """ Test Class: command provider """
    @classmethod
    def setup_class(cls):
        """ Setup func """
        cls.runner = CliRunner()

    @classmethod
    def teardown_class(cls):
        """ Teardown func """

    def test_cmd_bigip_login_with_credentials(self, mocker):
        """ Log into a cloud
        Given
        - Cloud credentials

        When
        - User attempts to log into a cloud

        Then
        - Login is successful
        """
        mock_provider_client = mocker.patch(
            'f5cloudcli.commands.cmd_provider.clients.get_provider_client'
        )
        mock_provider_client.return_value.is_logged_in.return_value = True

        result = self.runner.invoke(cli, ['login', '--environment', 'azure'])
        assert result.output == json.dumps(
            {'message': 'Login successful'}, indent=4, sort_keys=True
        ) + '\n'

    def test_cmd_bigip_login_no_credentials(self, mocker):
        """ Log into a cloud
        Given
        - Cloud credentials

        When
        - User attempts to log into a cloud

        Then
        - Login is successful
        """
        mock_provider_client = mocker.patch(
            'f5cloudcli.commands.cmd_provider.clients.get_provider_client'
        )
        mock_provider_client.return_value.is_logged_in.return_value = False

        result = self.runner.invoke(cli, ['login', '--environment', 'azure'])
        assert result.output == json.dumps(
            {'message': 'Login unsuccessful'}, indent=4, sort_keys=True
        ) + '\n'
