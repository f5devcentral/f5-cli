""" Test Config command """
import json

from f5cli.config import ConfigClient
from f5cli.commands.cmd_config import cli

from ...global_test_imports import pytest, CliRunner

# Test Constants
TEST_USER = 'TEST USER'
TEST_PASSWORD = 'TEST PASSWORD'
SUBSCRIPTION_ID = 's-123'

MOCK_CONFIG_CLIENT_READ_AUTH_RETURN_VALUE = {
    'user': 'test_user',
    'password': 'test_password'
}


class TestCommandConfig(object):
    """ Test Class: command config """

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
        """ PyTest fixture mocking ConfigClient's read_auth method """
        mock_config_client_read_auth = mocker.patch.object(
            ConfigClient, "read_auth")
        mock_config_client_read_auth.return_value = MOCK_CONFIG_CLIENT_READ_AUTH_RETURN_VALUE

    @staticmethod
    @pytest.fixture
    def config_client_store_auth_fixture(mocker):
        """ PyTest fixture mocking ConfigClient's store_auth method """
        mock_config_client_store_auth = mocker.patch.object(
            ConfigClient, "store_auth")
        return mock_config_client_store_auth

    @staticmethod
    @pytest.fixture
    def config_client_delete_auth_fixture(mocker):
        """ PyTest fixture mocking ConfigClient's store_auth method """
        mock_config_client_delete_auth = mocker.patch.object(
            ConfigClient, "delete_auth")
        return mock_config_client_delete_auth

    @staticmethod
    @pytest.fixture
    def config_client_list_auth_fixture(mocker):
        """ PyTest fixture mocking ConfigClient's store_auth method """
        mock_config_client_list_auth = mocker.patch.object(
            ConfigClient, "list_auth")
        return mock_config_client_list_auth

    @staticmethod
    @pytest.fixture
    def config_client_fixture(mocker):
        """ PyTest fixture returning mocked ConfigClient """
        mock_config_client = mocker.patch.object(ConfigClient, "__init__")
        mock_config_client.return_value = None
        return mock_config_client

    # Helper methods
    @staticmethod
    def _assert_two_dicts(dict1, dict2):
        assert len(dict1.keys()) == len(dict2.keys())
        for key in dict1.keys():
            assert key in dict2.keys()
            assert dict2.get(key) == dict1.get(key)

    def test_cmd_configure_auth_bigip(self, mocker, config_client_fixture):
        """ Configure authentication to a BIGIP
        Given
        - BIG IP is up

        When
        - User to configure auth with a BIGIP

        Then
        - Credentials are passed to the ConfigClient
        - The ConfigClient is instructed to save the credentials
        """
        mock_config_client = config_client_fixture
        mock_config_client_store_auth = mocker.patch.object(
            ConfigClient, "store_auth")

        test_host = 'TEST HOST'
        test_user = 'TEST USER'
        test_password = 'TEST PASSWORD'
        result = self.runner.invoke(cli, [
            'auth',
            'create',
            '--authentication-provider', 'bigip',
            '--name', 'test1',
            '--host', test_host,
            '--user', test_user,
            '--password', test_password
        ])
        mock_config_client_store_auth.assert_called_with('create')
        mock_config_client_args = mock_config_client.call_args_list[0][1]
        expected_result = {
            'authentication-type': 'bigip',
            'default': False,
            'name': 'test1',
            'host': test_host,
            'port': 443,
            'user': test_user,
            'password': test_password
        }
        self._assert_two_dicts(mock_config_client_args['auth'], expected_result)
        assert result.output == json.dumps(
            {'message': 'Authentication configured successfully'},
            indent=4,
            sort_keys=True
        ) + '\n'

    def test_cmd_configure_auth_bigip_with_port(self, mocker, config_client_fixture):
        """ Configure authentication to a BIGIP with port
        Given
        - BIG IP is up

        When
        - User to configure auth with a BIGIP against a specific port

        Then
        - Credentials as well as the host and port information is passed to the ConfigClient
        - The ConfigClient is instructed to save the credentials
        """
        mock_config_client = config_client_fixture
        mock_config_client_store_auth = mocker.patch.object(
            ConfigClient, "store_auth")

        test_host = 'TEST HOST'
        test_user = 'TEST USER'
        test_port = 'TEST PORT'
        test_password = 'TEST PASSWORD'
        result = self.runner.invoke(cli, [
            'auth',
            'create',
            '--authentication-provider', 'bigip',
            '--name', 'test1',
            '--host', test_host,
            '--user', test_user,
            '--port', test_port,
            '--password', test_password
        ])
        mock_config_client_store_auth.assert_called_with('create')
        mock_config_client_args = mock_config_client.call_args_list[0][1]
        expected_result = {
            'authentication-type': 'bigip',
            'default': False,
            'name': 'test1',
            'host': test_host,
            'user': test_user,
            'port': test_port,
            'password': test_password
        }
        self._assert_two_dicts(mock_config_client_args['auth'], expected_result)
        assert result.output == json.dumps(
            {'message': 'Authentication configured successfully'},
            indent=4,
            sort_keys=True
        ) + '\n'

    def test_cmd_configure_auth_cloud_services(self,
                                               config_client_fixture,
                                               config_client_store_auth_fixture):
        """ Configure authentication to F5 Cloud Services

        Given
        - Cloud Services is available, and end-user has an account

        When
        - User configures Cloud Services authentication with user/password credentials

        Then
        - Credentials are passed to the ConfigClient
        - The ConfigClient is instructed to save the credentials
        """
        mock_config_client = config_client_fixture
        mock_config_client_store_auth = config_client_store_auth_fixture

        result = self.runner.invoke(cli, [
            'auth',
            'create',
            '--authentication-provider', 'cloud-services',
            '--name', 'test1',
            '--user', TEST_USER,
            '--password', TEST_PASSWORD])

        mock_config_client_store_auth.assert_called_once()
        mock_config_client_args = mock_config_client.call_args_list[0][1]
        expected_result = {
            'authentication-type': 'cloud-services',
            'default': False,
            'name': 'test1',
            'user': TEST_USER,
            'password': TEST_PASSWORD
        }
        self._assert_two_dicts(mock_config_client_args['auth'], expected_result)
        assert result.output == json.dumps(
            {'message': 'Authentication configured successfully'},
            indent=4,
            sort_keys=True
        ) + '\n'

    def test_cmd_configure_auth_with_custom_api(self,
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
        - The ConfigClient is instructed to save the credentials and API endpoint
        """
        mock_config_client = config_client_fixture
        mock_config_client_store_auth = config_client_store_auth_fixture

        test_api_endpoint = 'my-f5.api.com'
        result = self.runner.invoke(cli, [
            'auth',
            'create',
            '--authentication-provider', 'cloud-services',
            '--name', 'test1',
            '--user', TEST_USER,
            '--password', TEST_PASSWORD,
            '--api-endpoint', test_api_endpoint,
            '--set-default'])

        mock_config_client_store_auth.assert_called_once()
        mock_config_client_args = mock_config_client.call_args_list[0][1]
        expected_result = {
            'authentication-type': 'cloud-services',
            'name': 'test1',
            'default': True,
            'user': TEST_USER,
            'password': TEST_PASSWORD,
            'api_endpoint': test_api_endpoint
        }
        self._assert_two_dicts(mock_config_client_args['auth'], expected_result)
        assert result.output == json.dumps(
            {'message': 'Authentication configured successfully'},
            indent=4,
            sort_keys=True
        ) + '\n'

    def test_cmd_update_auth_bigip_with_password_prompt(self,
                                                        config_client_fixture,
                                                        config_client_store_auth_fixture):
        """ Update an auth account

        Given
        - User has a BIGIP auth account configured

        When
        - User updates the auth account with a new user name

        Then
        - User is prompted to supply a password
        - The credentials are then stored
        """
        mock_config_client = config_client_fixture
        mock_config_client_store_auth = config_client_store_auth_fixture

        result = self.runner.invoke(cli, [
            'auth',
            'update',
            '--authentication-provider', 'cloud-services',
            '--name', 'test1',
            '--user', TEST_USER,
            '--set-default'], input='blah')

        mock_config_client_store_auth.assert_called_once()
        mock_config_client_args = mock_config_client.call_args_list[0][1]
        expected_result = {
            'authentication-type': 'cloud-services',
            'name': 'test1',
            'default': True,
            'host': None,
            'user': TEST_USER,
            'port': None,
            'password': 'blah',
            'api-endpoint': None
        }
        self._assert_two_dicts(mock_config_client_args['auth'], expected_result)
        assert json.dumps(
            {'message': 'Authentication updated successfully'},
            indent=4,
            sort_keys=True
        ) + '\n' in result.output

    def test_cmd_delete_auth(self, config_client_delete_auth_fixture):
        """ Delete an auth account

        Given
        - Account has been configured

        When
        - User deletes the auth account

        Then
        - Credentials are removed from the credential store

        """
        mock_config_client_delete_auth = config_client_delete_auth_fixture

        result = self.runner.invoke(cli, [
            'auth',
            'delete',
            '--name', 'test1'])

        mock_config_client_delete_auth.assert_called_with('test1')
        assert json.dumps(
            {'message': 'Successfully deleted auth: test1 contents'},
            indent=4,
            sort_keys=True
        ) + '\n' in result.output

    def test_cmd_list_auth(self,
                           config_client_list_auth_fixture):
        """ List all auth accounts

        Given
        - Multiple auth accounts are configured

        When
        - User sends list command

        Then
        - All the stored auth accounts are listed

        """
        mock_config_client_list_auth = config_client_list_auth_fixture
        self.runner.invoke(cli, ['auth', 'list'])
        mock_config_client_list_auth.assert_called_once()

    def test_cmd_configure_output_format_cli_dir_not_exist(self, mocker):
        """ Configure output format
        Given
        - BIG IP is up
        - F5_CLI_DIR not exists

        When
        - User attempts to configure output format as JSON_FORMAT

        Then
        - F5_CLI_DIR is created
        - JSON_FORMAT is written into F5_CONFIG_FILE
        """
        mock_path_exist = mocker.patch("os.path.exists")
        mock_path_exist.return_value = False
        mock_make_dir = mocker.patch("os.makedirs")
        mocker.patch("f5cli.cli.Context.log")
        with mocker.patch('f5cli.commands.cmd_config.open', new_callable=mocker.mock_open()):
            mock_yaml_dump = mocker.patch("yaml.safe_dump")
            self.runner.invoke(cli, ['output-format', '--output', 'json'])
            mock_yaml_dump.assert_called_once()
            mock_make_dir.assert_called_once()

    def test_cmd_configure_output_format_cli_dir_exist(self, mocker):
        """ Configure output format
        Given
        - BIG IP is up
        - F5_CLI_DIR exists

        When
        - User attempts to configure output format as JSON_FORMAT

        Then
        - JSON_FORMAT is written into F5_CONFIG_FILE
        """
        mock_path_exist = mocker.patch("os.path.exists")
        mock_path_exist.return_value = True
        mocker.patch("f5cli.cli.Context.log")
        with mocker.patch('f5cli.commands.cmd_config.open', new_callable=mocker.mock_open()):
            mock_yaml_dump = mocker.patch("yaml.safe_dump")
            self.runner.invoke(cli, ['output-format', '--output', 'json'])
            mock_yaml_dump.assert_called_once()
