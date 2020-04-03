""" Test Beacon command """

import json

from f5sdk.cs import ManagementClient
from f5sdk.cs.beacon.insights import InsightsClient

from f5cli.config import AuthConfigurationClient
from f5cli.commands.cmd_cs import cli

from ...global_test_imports import pytest, CliRunner

# Test Constants
MOCK_CONFIG_CLIENT_READ_AUTH_RETURN_VALUE = {
    'user': 'test_user',
    'password': 'test_password'
}


class TestCommandBeacon(object):
    """ Test Class: command beacon """

    @classmethod
    def setup_class(cls):
        """ Setup func """
        cls.runner = CliRunner()

    @classmethod
    def teardown_class(cls):
        """ Teardown func """

    @staticmethod
    @pytest.fixture
    def config_client_read_auth_fixture(mocker):
        """ PyTest fixture mocking AuthConfigurationClient's read_auth method """
        mock_config_client_read_auth = mocker.patch.object(
            AuthConfigurationClient, "read_auth")
        mock_config_client_read_auth.return_value = MOCK_CONFIG_CLIENT_READ_AUTH_RETURN_VALUE
        return mock_config_client_read_auth

    @staticmethod
    @pytest.fixture
    def mgmt_client_fixture(mocker):
        """ PyTest fixture returning mocked Cloud Services Management Client """
        mock_management_client = mocker.patch.object(ManagementClient, '__init__')
        mock_management_client.return_value = None
        return mock_management_client

    @pytest.mark.usefixtures("config_client_read_auth_fixture")
    @pytest.mark.usefixtures("mgmt_client_fixture")
    def test_cmd_beacon_insights_list(self, mocker):
        """ List all configured beacon insights

        Given
        - The Insights Client returns a successful response

        When
        - User executes a 'list'

        Then
        - The 'list' command returns a successful response
        """

        mock_response = {
            'foo': 'bar'
        }
        mocker.patch.object(
            InsightsClient, "list", return_value=mock_response)

        result = self.runner.invoke(cli, ['beacon', 'insights', 'list'])
        assert result.output == json.dumps(mock_response, indent=4, sort_keys=True) + '\n'

    @pytest.mark.usefixtures("config_client_read_auth_fixture")
    @pytest.mark.usefixtures("mgmt_client_fixture")
    def test_cmd_beacon_insights_create(self, mocker):
        """ Creating a beacon insight

        Given
        - The Insights Client returns a successful response

        When
        - User executes a 'create' with a declaration

        Then
        - The 'create' command returns a successful response
          and creates an insight
        """

        mock_response = {
            'title': 'foo',
            'description': 'blah'
        }
        mocker.patch.object(
            InsightsClient, "create", return_value=mock_response)

        result = self.runner.invoke(cli, ['beacon', 'insights', 'create',
                                          '--declaration', './test/fake_declaration.json'])
        assert result.output == json.dumps(mock_response, indent=4, sort_keys=True) + '\n'

    @pytest.mark.usefixtures("config_client_read_auth_fixture")
    @pytest.mark.usefixtures("mgmt_client_fixture")
    def test_cmd_beacon_insights_update(self, mocker):
        """ Updating a beacon insight

        Given
        - The Insights Client returns a successful response

        When
        - User executes a 'update' with a declaration with the same title

        Then
        - The 'update' command returns a successful response
          and updates the specified insight
        """
        mock_response = {
            'title': 'foo',
            'description': 'blah2'
        }
        mocker.patch.object(
            InsightsClient, "create", return_value=mock_response)

        result = self.runner.invoke(cli, ['beacon', 'insights', 'update',
                                          '--declaration', './test/fake_declaration.json'])
        assert result.output == json.dumps(mock_response, indent=4, sort_keys=True) + '\n'

    @pytest.mark.usefixtures("config_client_read_auth_fixture")
    @pytest.mark.usefixtures("mgmt_client_fixture")
    def test_cmd_beacon_insights_delete(self, mocker):
        """ Deleting a beacon insight

        Given
        - The Insights Client returns a successful response

        When
        - User executes a 'delete' with the title of the insight to be deleted

        Then
        - The 'delete' command returns a successful response
          and delete the specified insight
        """

        mocker.patch.object(
            InsightsClient, "delete", return_value={})

        result = self.runner.invoke(cli, ['beacon', 'insights', 'delete', '--title', 'foo'])
        assert result.output == json.dumps(
            {'message': 'Insight deleted successfully'},
            indent=4, sort_keys=True) + '\n'

    @pytest.mark.usefixtures("config_client_read_auth_fixture")
    @pytest.mark.usefixtures("mgmt_client_fixture")
    def test_cmd_beacon_insights_show(self, mocker):
        """ Show a beacon insight

        Given
        - The Insights Client returns a successful response

        When
        - User executes a 'show' with a title of the insight

        Then
        - The 'show' command returns requested insight
        """

        mock_response = {
            'title': 'foo',
            'description': 'blah'
        }
        mocker.patch.object(
            InsightsClient, "show", return_value=mock_response)

        result = self.runner.invoke(cli, ['beacon', 'insights', 'show', '--title', 'foo'])
        assert result.output == json.dumps(mock_response, indent=4, sort_keys=True) + '\n'
