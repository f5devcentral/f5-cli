""" Test Cloud Services command """

import json
import os


from f5sdk.cs import ManagementClient
from f5sdk.cs.accounts import AccountClient
from f5sdk.cs.subscriptions import SubscriptionClient

from f5cli.config import AuthConfigurationClient
from f5cli.commands.cmd_cs import cli

from ...global_test_imports import pytest, CliRunner

# Test Constants
TEST_USER = 'TEST USER'
TEST_PASSWORD = 'TEST PASSWORD'
SUBSCRIPTION_ID = 's-123'

MOCK_CONFIG_CLIENT_READ_AUTH_RETURN_VALUE = {
    'user': 'test_user',
    'password': 'test_password'
}


class TestCommandBigIp(object):
    """ Test Class: command bigip """
    @classmethod
    def setup_class(cls):
        """ Setup func """
        cls.runner = CliRunner()

    @classmethod
    def teardown_class(cls):
        """ Teardown func """

    @staticmethod
    @pytest.fixture
    def config_client_fixture(mocker):
        """ PyTest fixture returning mocked AuthConfigurationClient """
        mock_config_client = mocker.patch.object(AuthConfigurationClient, "__init__")
        mock_config_client.return_value = None
        return mock_config_client

    @staticmethod
    @pytest.fixture
    def config_client_store_auth_fixture(mocker):
        """ PyTest fixture mocking AuthConfigurationClient's store_auth method """
        mock_config_client_store_auth = mocker.patch.object(
            AuthConfigurationClient, "store_auth")
        return mock_config_client_store_auth

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
    def test_cmd_cs_account_show_user(self, mocker):
        """ Show currently authentication CS user

        Given
        - The Account Client returns a successful response

        When
        - User executes a 'show_user'

        Then
        - The show_user command returns a successful response
        """

        mock_response = {
            'foo': 'bar'
        }
        mocker.patch.object(
            AccountClient, "show_user", return_value=mock_response)

        result = self.runner.invoke(cli, ['account', 'show-user'])
        assert result.output == json.dumps(mock_response, indent=4, sort_keys=True) + '\n'

    @pytest.mark.usefixtures("config_client_read_auth_fixture")
    @pytest.mark.usefixtures("mgmt_client_fixture")
    def test_cmd_cs_subscription_list(self, mocker):
        """ List subscriptions

        Given
        - The Account Client returns a successful response

        When
        - User executes the 'show_user' commaned

        Then
        - The command returns a successful response
        """

        mock_response = {
            'foo': 'bar'
        }
        mocker.patch.object(
            SubscriptionClient,
            "list",
            return_value=mock_response
        )

        result = self.runner.invoke(cli, ['subscription', 'list'])
        assert result.output == json.dumps(mock_response, indent=4, sort_keys=True) + '\n'

    @pytest.mark.usefixtures("config_client_read_auth_fixture")
    @pytest.mark.usefixtures("mgmt_client_fixture")
    def test_cmd_cs_subscription_list_with_filter(self, mocker):
        """ List subscriptions (with account ID filter)

        Given
        - The Account Client returns a successful response

        When
        - User executes the 'show_user' commaned

        Then
        - The command returns a successful response
        - The subscription client is passed the account id filter
        """

        mock_response = {
            'foo': 'bar'
        }
        mock_subscription_client_list = mocker.patch.object(
            SubscriptionClient,
            "list",
            return_value=mock_response
        )

        result = self.runner.invoke(cli, ['subscription', 'list', '--account-id-filter', 'foo'])
        assert result.output == json.dumps(mock_response, indent=4, sort_keys=True) + '\n'
        _, kwargs = mock_subscription_client_list.call_args
        assert kwargs['query_parameters']['account_id'] == 'foo'

    @pytest.mark.usefixtures("config_client_read_auth_fixture")
    @pytest.mark.usefixtures("mgmt_client_fixture")
    def test_cmd_cs_subscription_show(self, mocker):
        """ Execute a 'show' action against an F5 Cloud Services subscription

        Given
        - The Subscription Client returns a successful response

        When
        - User executes the 'show' command

        Then
        - The command returns a successful response
        """

        mock_response = {
            'subscription_id': SUBSCRIPTION_ID,
            'account_id': 'a-123'
        }
        mocker.patch.object(
            SubscriptionClient,
            "show",
            return_value=mock_response
        )

        result = self.runner.invoke(cli, ['subscription', 'show',
                                          '--subscription-id', SUBSCRIPTION_ID])
        assert result.output == json.dumps(mock_response, indent=4, sort_keys=True) + '\n'

    @pytest.mark.usefixtures("config_client_read_auth_fixture")
    @pytest.mark.usefixtures("mgmt_client_fixture")
    def test_cmd_cs_subscription_bad_action(self):
        """ Execute an unimplemented action for F5 Cloud Services subscription

        Given
        - The CLI is available

        When
        - User executes a 'blahblah' command against F5 Cloud Services

        Then
        - The CLI responds that an unimplemented action was executed
        """
        bad_action = 'blahblah'

        result = self.runner.invoke(cli, ['subscription', bad_action])
        assert f"invalid choice: {bad_action}" in result.output
        assert result.exception

    @pytest.mark.usefixtures("config_client_read_auth_fixture")
    @pytest.mark.usefixtures("mgmt_client_fixture")
    def test_cmd_cs_subscription_update_no_declaration(self):
        """ Execute 'update' without providing a declaration

        Given
        - The CLI is available

        When
        - The User executes the 'update' action for a Cloud Services Subscription
        - A declaration is not provided in the 'update' action

        Then
        - The CLI responds that a declaration is required
        """

        result = self.runner.invoke(cli, ['subscription', 'update', '--subscription-id', 's'])
        assert result.exception

        expected_output = ("Error: The --declaration option is required\n")
        assert result.output == expected_output

    @pytest.mark.usefixtures("config_client_read_auth_fixture")
    @pytest.mark.usefixtures("mgmt_client_fixture")
    def test_cmd_cs_subscription_update(self, mocker):
        """ Execute an 'update' action against a Cloud Services subscription

        Given
        - The CLI exists

        When
        - The User executes the 'update' action for a Cloud Services Subscription
        - The User provides a valid declaration file

        Then
        - The CLI calls the F5 SDK to update Cloud Services
        """

        mock_update_return = {
            'subscription_id': SUBSCRIPTION_ID,
            'account_id': 'a-123'
        }

        mock_subscription_client_update = mocker.patch.object(
            SubscriptionClient,
            "update",
            return_value=mock_update_return
        )

        declaration_file = 'decl.json'
        expected_config_file = os.path.join(os.getcwd(), declaration_file)
        result = self.runner.invoke(cli, ['subscription', 'update', '--subscription-id',
                                          SUBSCRIPTION_ID, '--declaration', 'decl.json'])
        assert result.output == json.dumps(mock_update_return, indent=4, sort_keys=True) + '\n'
        assert mock_subscription_client_update.call_args[1]['config_file'] == expected_config_file
