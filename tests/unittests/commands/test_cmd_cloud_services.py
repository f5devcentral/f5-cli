import pytest
from click.testing import CliRunner

from f5cloudcli.config import ConfigClient

# Module under test
from f5cloudcli.commands.cmd_cloud_services import cli
from f5cloudcli import constants

# Test Constants
TEST_USER = 'TEST USER'
TEST_PASSWORD = 'TEST PASSWORD'


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
            'api-endpoint': test_api_endpoint
        }
        assert result.output == f"Configuring F5 Cloud Services Auth for {TEST_USER} with ******\n"
