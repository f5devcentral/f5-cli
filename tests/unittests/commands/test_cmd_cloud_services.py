import pytest
import click
import os

from click.testing import CliRunner

from f5cloudsdk.cloud_services import ManagementClient
from f5cloudsdk.cloud_services.subscription import SubscriptionClient
from f5cloudcli.config import ConfigClient

# Module under test
from f5cloudcli.commands.cmd_cloud_services import cli
from f5cloudcli import constants

# Test Constants
TEST_USER = 'TEST USER'
TEST_PASSWORD = 'TEST PASSWORD'
SUBSCRIPTION_ID = 's-123'

MOCK_CONFIG_CLIENT_READ_AUTH_RETURN_VALUE = {
    'username': 'test_user',
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
        pass

    @pytest.fixture
    def config_client_fixture(self, mocker):
        """ PyTest fixture returning mocked ConfigClient """
        mock_config_client = mocker.patch.object(ConfigClient, "__init__")
        mock_config_client.return_value = None
        return mock_config_client

    @pytest.fixture
    def config_client_store_auth_fixture(self, mocker):
        """ PyTest fixture mocking ConfigClient's store_auth method """
        mock_config_client_store_auth = mocker.patch.object(
            ConfigClient, "store_auth")
        return mock_config_client_store_auth

    @pytest.fixture
    def config_client_read_auth_fixture(self, mocker):
        """ PyTest fixture mocking ConfigClient's read_auth method """
        mock_config_client_read_auth = mocker.patch.object(
            ConfigClient, "read_auth")
        mock_config_client_read_auth.return_value = MOCK_CONFIG_CLIENT_READ_AUTH_RETURN_VALUE
        return mock_config_client_read_auth

    @pytest.fixture
    def mgmt_client_fixture(self, mocker):
        """ PyTest fixture returning mocked Cloud Services Management Client """
        mock_management_client = mocker.patch.object(ManagementClient, '__init__')
        mock_management_client.return_value = None
        return mock_management_client

    @pytest.fixture
    def subscription_client_fixture(self, mocker):
        """ PyTest fixture returning mocked Cloud Services Subscription Client """
        mock_subscription_client = mocker.patch.object(SubscriptionClient, '__init__')
        mock_subscription_client.return_value = None
        return mock_subscription_client

    def test_dns_service(self):
        """ Test DNS service
        Given
        - BIG IP is up

        When
        - User attempts to create a DNS

        Then
        - Exception is thrown
        """
        result = self.runner.invoke(
            cli, ['dns', 'create', 'a', 'test_members'])
        expected_output = "create DNS a with members test_members\nError: Command not implemented\n"
        assert result.output == expected_output
        assert result.exception

    def test_cmd_cloud_services_configure_auth(self,
                                               config_client_fixture,
                                               config_client_store_auth_fixture):
        """ Configure authentication to F5 Cloud Services

        Given
        - Cloud Services is available, and end-user has an account

        When
        - User configures Cloud Services authentication with user/password credentials

        Then
        - Credentials are passed to the ConfigClient
        - The ConfigClient is instructured to save the credentials
        """
        mock_config_client = config_client_fixture
        mock_config_client_store_auth = config_client_store_auth_fixture

        result = self.runner.invoke(cli, ['configure-auth', '--user', TEST_USER,
                                          '--password', TEST_PASSWORD])

        mock_config_client_store_auth.assert_called_once()
        mock_config_client_args = mock_config_client.call_args_list[0][1]
        assert mock_config_client_args['group_name'] == constants.CLOUD_SERVICES_GROUP_NAME
        assert mock_config_client_args['auth'] == {
            'username': TEST_USER,
            'password': TEST_PASSWORD
        }
        assert result.output == f"Configuring F5 Cloud Services Auth for {TEST_USER} with ******\n"

    def test_cmd_cloud_services_configure_auth_custom_api(self,
                                                          config_client_fixture,
                                                          config_client_store_auth_fixture):
        """ Configure authentication to F5 Cloud Services using a custom API endpoint

        Given
        - Cloud Services is available, and end-user has an account

        When
        - User configures Cloud Services authentication with user/password credentials
        - And a custom API endpoint is provided

        Then
        - Credentials are passed to the ConfigClient
        - The ConfigClient is instructured to save the credentials and API endpoint
        """
        mock_config_client = config_client_fixture
        mock_config_client_store_auth = config_client_store_auth_fixture

        test_api_endpoint = 'my-f5.api.com'
        result = self.runner.invoke(cli, ['configure-auth', '--user', TEST_USER,
                                          '--password', TEST_PASSWORD,
                                          '--api-endpoint', test_api_endpoint])
        mock_config_client_store_auth.assert_called_once()
        mock_config_client_args = mock_config_client.call_args_list[0][1]
        assert mock_config_client_args['group_name'] == constants.CLOUD_SERVICES_GROUP_NAME
        assert mock_config_client_args['auth'] == {
            'username': TEST_USER,
            'password': TEST_PASSWORD,
            'api_endpoint': test_api_endpoint
        }
        assert result.output == f"Configuring F5 Cloud Services Auth for {TEST_USER} with ******\n"

    def test_cmd_cloud_services_subscription_show(self,
                                                  mocker,
                                                  config_client_read_auth_fixture,  # pylint: disable=unused-argument
                                                  mgmt_client_fixture,  # pylint: disable=unused-argument
                                                  subscription_client_fixture):  # pylint: disable=unused-argument
        """ Execute a 'show' action against an F5 Cloud Services subscription

        Given
        - Cloud Services is available, and end-user has an account
        - The user has already configured authentication with Cloud Services

        When
        - User executes a 'show' against F5 Cloud Services

        Then
        - Authentication data is read from disk
        - A Management client is createddd
        - A Subscription client is created
        - The show command is executed
        """
        mock_subscription_client_show = mocker.patch.object(
            SubscriptionClient, "show")
        mock_subscription_client_show.return_value = {
            'subscription_id': SUBSCRIPTION_ID,
            'account_id': 'a-123'
        }
        click_echo = mocker.patch.object(click, 'echo')
        self.runner.invoke(cli, ['subscription', 'show',
                                 '--subscription-id', SUBSCRIPTION_ID])

        expected_response = '{"subscription_id": "s-123", "account_id": "a-123"}'
        assert click_echo.call_args[1]['message'] == expected_response

    def test_cmd_cloud_services_subscription_bad_action(self):
        """ Execute an unimplemented action for F5 Cloud Services subscription

        Given
        - Cloud Services is available, and end-user has an account
        - The user has already configured authentication with Cloud Services

        When
        - User executes a 'blahblah' command against F5 Cloud Services

        Then
        - The CLI responds that an unimplemented action was executed
        """
        bad_action = 'blahblah'

        result = self.runner.invoke(cli, ['subscription', bad_action])
        assert f"invalid choice: {bad_action}" in result.output
        assert result.exception

    def test_cmd_cloud_services_subscription_update_no_declaration(self):
        """ Execute 'update' without providing a declaration

        When
        - The User executes the 'update' action for a Cloud Services Subscription
        - A declaration is not provided in the 'update' action

        Then
        - The CLI responds that a declaration is required
        """

        result = self.runner.invoke(cli, ['subscription', 'update', '--subscription-id', 's'])
        assert result.exception
        assert result.output == 'Error: The --declaration option is required when updating a Cloud Services subscription\n'  # pylint: disable=line-too-long

    def test_cmd_cloud_services_subscription_update(self,
                                                    mocker,
                                                    config_client_read_auth_fixture,  # pylint: disable=unused-argument
                                                    mgmt_client_fixture,  # pylint: disable=unused-argument
                                                    subscription_client_fixture):  # pylint: disable=unused-argument
        """ Execute an 'update' action against a Cloud Services subscription

        Given
        - Cloud Services is available, and end-user has an account
        - The user has already configured authentication with Cloud Services
        - There is an existing F5 Cloud Services configuration

        When
        - The User executes the 'update' action for a Cloud Services Subscription
        - The User provides a valid declaration file

        Then
        - The CLI calls the F5 Cloud SDK to update Cloud Services
        """

        mock_subscription_client_update = mocker.patch.object(
            SubscriptionClient, "update")
        mock_subscription_client_update.return_value = {
            'subscription_id': SUBSCRIPTION_ID,
            'account_id': 'a-123'
        }

        declaration_file = 'decl.json'
        expected_config_file = os.path.join(os.getcwd(), declaration_file)
        result = self.runner.invoke(cli, ['subscription', 'update', '--subscription-id',
                                          SUBSCRIPTION_ID, '--declaration', 'decl.json'])
        assert "Cloud Services Subscription updated" in result.output
        assert mock_subscription_client_update.call_args[1]['config_file'] == expected_config_file
