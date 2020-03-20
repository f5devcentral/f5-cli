""" Test Login command """
import json

from click import ClickException
from f5sdk.bigip import ManagementClient as BigipManagementClient
from f5sdk.cloud_services import ManagementClient as CSManagementClient
from f5sdk.exceptions import DeviceReadyError, InvalidAuthError
from f5cli.config import AuthConfigurationClient
from f5cli.commands.cmd_login import cli

from ...global_test_imports import pytest, CliRunner

# Test Constants
TEST_USER = 'TEST USER'
TEST_PASSWORD = 'TEST PASSWORD'
TEST_HOST = 'TEST HOST'
SUBSCRIPTION_ID = 's-123'

MOCK_CONFIG_CLIENT_READ_AUTH_RETURN_VALUE = {
    'user': 'test_user',
    'password': 'TEST_PASSWORD'
}


class TestCommandLogin(object):
    """ Test Class: command login """

    @classmethod
    def setup_class(cls):
        """ Setup func """
        cls.runner = CliRunner()

    @classmethod
    def teardown_class(cls):
        """ Teardown func """

    @staticmethod
    @pytest.fixture
    def config_client_store_auth_fixture(mocker):
        """ PyTest fixture mocking AuthConfigurationClient's store_auth method """
        mock_config_client_store_auth = mocker.patch.object(
            AuthConfigurationClient, "store_auth")
        return mock_config_client_store_auth

    @staticmethod
    @pytest.fixture
    def config_client_fixture(mocker):
        """ PyTest fixture returning mocked AuthConfigurationClient """
        mock_config_client = mocker.patch.object(AuthConfigurationClient, "__init__")
        mock_config_client.return_value = None
        return mock_config_client

    @staticmethod
    @pytest.fixture
    def bigip_mgmt_client_fixture(mocker):
        """ PyTest fixture returning mocked BigIP Management Client """
        mock_management_client = mocker.patch.object(BigipManagementClient, '__init__')
        mock_management_client.return_value = None
        return mock_management_client

    @staticmethod
    @pytest.fixture
    def cs_mgmt_client_fixture(mocker):
        """ PyTest fixture returning mocked BigIP Management Client """
        mock_management_client = mocker.patch.object(CSManagementClient, '__init__')
        mock_management_client.return_value = None
        return mock_management_client

    # Helper methods
    @staticmethod
    def _assert_two_dicts(dict1, dict2):
        assert len(dict1.keys()) == len(dict2.keys())
        for key in dict1.keys():
            assert key in dict2.keys()
            assert dict2.get(key) == dict1.get(key)

    # pylint: disable=unused-argument
    def test_cmd_login_bigip(self,
                             config_client_fixture,
                             config_client_store_auth_fixture,
                             bigip_mgmt_client_fixture):
        """ Log into a BIGIP with provided credentials
        Given
        - BIG IP is up

        When
        - User to log into a BIGIP with provided auth

        Then
        - Credentials are passed to the AuthConfigurationClient
        - The AuthConfigurationClient is instructed to save the credentials in temp
          auth account named login_bigip and is set as the default account
          for bigip
        """
        result = self.runner.invoke(cli, [
            '--authentication-provider', 'bigip',
            '--host', TEST_HOST,
            '--user', TEST_USER,
            '--password', TEST_PASSWORD
        ])
        config_client_store_auth_fixture.assert_called_with('create')
        mock_config_client_args = config_client_fixture.call_args_list[0][1]
        expected_result = {
            'authentication-type': 'bigip',
            'default': True,
            'name': 'login_bigip',
            'host': TEST_HOST,
            'port': 443,
            'user': TEST_USER,
            'password': TEST_PASSWORD
        }
        self._assert_two_dicts(mock_config_client_args['auth'], expected_result)
        assert result.output == json.dumps(
            {'message': 'Logged in successfully'},
            indent=4,
            sort_keys=True
        ) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_login_bigip_when_auth_account_exists(self,
                                                      config_client_fixture,
                                                      config_client_store_auth_fixture,
                                                      bigip_mgmt_client_fixture):
        """ Log into a BIGIP with provided credentials
        Given
        - BIG IP is up

        When
        - User to log into a BIGIP with provided auth
        - login_bigip authentication account already exists

        Then
        - Credentials are passed to the AuthConfigurationClient
        - The AuthConfigurationClient is instructed to save the credentials in temp
          auth account named login_bigip and is set as the default account
          for bigip
        """
        def test_side_effect(*args):
            if args[0] == 'create':
                raise ClickException("Account already exists")

        config_client_store_auth_fixture.side_effect = test_side_effect
        result = self.runner.invoke(cli, [
            '--authentication-provider', 'bigip',
            '--host', TEST_HOST,
            '--user', TEST_USER,
            '--password', TEST_PASSWORD
        ])
        config_client_store_auth_fixture.call_count = 2
        assert config_client_store_auth_fixture.call_args_list[0][0][0] == 'create'
        assert config_client_store_auth_fixture.call_args_list[1][0][0] == 'update'
        mock_config_client_args = config_client_fixture.call_args_list[0][1]
        expected_result = {
            'authentication-type': 'bigip',
            'default': True,
            'name': 'login_bigip',
            'host': TEST_HOST,
            'port': 443,
            'user': TEST_USER,
            'password': TEST_PASSWORD
        }
        self._assert_two_dicts(mock_config_client_args['auth'], expected_result)
        assert result.output == json.dumps(
            {'message': 'Logged in successfully'},
            indent=4,
            sort_keys=True
        ) + '\n'

    # pylint: disable=unused-argument
    def test_login_bigip_with_prompt(self,
                                     config_client_fixture,
                                     config_client_store_auth_fixture,
                                     bigip_mgmt_client_fixture):
        """ Login into bigip without providing expected information

        Given
        - BIG IP is up

        When
        - User to log into a BIGIP without providing auth

        Then
        - User is prompted to supply authentication-provider, user and password
        - Credentials are passed to the AuthConfigurationClient
        - The AuthConfigurationClient is instructed to save the credentials in temp
          auth account named login_bigip and is set as the default account
          for bigip
        """
        result = self.runner.invoke(cli, [
            '--authentication-provider', 'bigip',
            '--host', TEST_HOST,
            '--user', TEST_USER,
            '--password', TEST_PASSWORD
        ])

        config_client_store_auth_fixture.assert_called_with('create')
        mock_config_client_args = config_client_fixture.call_args_list[0][1]
        expected_result = {
            'authentication-type': 'bigip',
            'default': True,
            'name': 'login_bigip',
            'host': TEST_HOST,
            'port': 443,
            'user': TEST_USER,
            'password': TEST_PASSWORD
        }
        self._assert_two_dicts(mock_config_client_args['auth'], expected_result)
        assert 'Logged in successfully' in result.output

    # pylint: disable=unused-argument
    def test_login_bigip_incorrect_creds(self,
                                         config_client_fixture,
                                         config_client_store_auth_fixture,
                                         bigip_mgmt_client_fixture):
        """ Login into bigip incorrect credentials

        Given
        - BIG IP is up

        When
        - User to log into a BIGIP with wrong auth

        Then
        - The bigip management client will throw a HTTPError
        - Credentials are not passed to the AuthConfigurationClient
        - Unsuccessful login message is thrown
        """
        error = 'Failed to login to BIG-IP, please provide valid credentials.'
        bigip_mgmt_client_fixture.side_effect = InvalidAuthError(error)
        result = self.runner.invoke(cli, [
            '--authentication-provider', 'bigip',
            '--host', TEST_HOST,
            '--user', TEST_USER,
            '--password', TEST_PASSWORD
        ])

        config_client_store_auth_fixture.assert_not_called()
        assert result.output == f'Error: {error}\n'

    # pylint: disable=unused-argument
    def test_login_bigip_host_not_ready(self,
                                        config_client_fixture,
                                        config_client_store_auth_fixture,
                                        bigip_mgmt_client_fixture):
        """ Attempt to log into bigip when device is down

        Given
        - BIG IP is down

        When
        - User attempts to log into a BIGIP

        Then
        - The bigip management client will throw a DeviceReadyError
        - Credentials are not passed to the AuthConfigurationClient
        - Unsuccessful login message is thrown
        """

        bigip_mgmt_client_fixture.side_effect = DeviceReadyError('Not ready')
        result = self.runner.invoke(cli, [
            '--authentication-provider', 'bigip',
            '--host', TEST_HOST,
            '--user', TEST_USER,
            '--password', TEST_PASSWORD
        ])

        config_client_store_auth_fixture.assert_not_called()
        assert result.output == "Error: Device is not ready.\n"

    # pylint: disable=unused-argument
    def test_cmd_login_cloud_services(self,
                                      config_client_fixture,
                                      config_client_store_auth_fixture,
                                      cs_mgmt_client_fixture):
        """ Log into a cloud services with provided credentials
        Given
        - Cloud services is up

        When
        - User is to log into a cloud services with provided auth

        Then
        - Credentials are passed to the AuthConfigurationClient
        - The AuthConfigurationClient is instructed to save the credentials in temp
          auth account named login_cloud_services and is set as the default account
          for cloud-services provider
        """

        result = self.runner.invoke(cli, [
            '--authentication-provider', 'cloud-services',
            '--user', TEST_USER,
            '--password', TEST_PASSWORD
        ])
        config_client_store_auth_fixture.assert_called_with('create')
        mock_config_client_args = config_client_fixture.call_args_list[0][1]
        expected_result = {
            'authentication-type': 'cloud-services',
            'default': True,
            'name': 'login_cloud_services',
            'user': TEST_USER,
            'password': TEST_PASSWORD
        }
        self._assert_two_dicts(mock_config_client_args['auth'], expected_result)
        assert result.output == json.dumps(
            {'message': 'Logged in successfully'},
            indent=4,
            sort_keys=True
        ) + '\n'

    # pylint: disable=unused-argument
    def test_login_cloud_services_with_prompt(self,
                                              config_client_fixture,
                                              config_client_store_auth_fixture,
                                              cs_mgmt_client_fixture):
        """ Log into a cloud services with provided credentials
        Given
        - Cloud services is up

        When
        - User is to log into a cloud services with provided auth

        Then
        - Credentials are passed to the AuthConfigurationClient
        - The AuthConfigurationClient is instructed to save the credentials in temp
          auth account named login_cloud_services and is set as the default account
          for cloud-services provider
        """

        result = self.runner.invoke(cli, ['--authentication-provider', 'cloud-services'],
                                    input='TEST USER\nTEST PASSWORD\n')
        config_client_store_auth_fixture.assert_called_with('create')
        mock_config_client_args = config_client_fixture.call_args_list[0][1]
        expected_result = {
            'authentication-type': 'cloud-services',
            'default': True,
            'name': 'login_cloud_services',
            'user': TEST_USER,
            'password': TEST_PASSWORD
        }
        self._assert_two_dicts(mock_config_client_args['auth'], expected_result)
        assert 'Logged in successfully' in result.output

    # pylint: disable=unused-argument
    def test_login_cs_incorrect_creds(self,
                                      config_client_fixture,
                                      config_client_store_auth_fixture,
                                      cs_mgmt_client_fixture):
        """ Login into cloud-services incorrect credentials

        Given
        - Cloud services is up

        When
        - User attempts to log into cloud-services with incorrect creds

        Then
        - The cloud services management client will throw a HTTPError
        - Credentials are not passed to the AuthConfigurationClient
        - Unsuccessful login message is thrown
        """
        error = 'Failed to login to Cloud Services, please provide valid credentials.'
        cs_mgmt_client_fixture.side_effect = InvalidAuthError(error)
        result = self.runner.invoke(cli, [
            '--authentication-provider', 'cloud-services',
            '--host', TEST_HOST,
            '--user', TEST_USER,
            '--password', TEST_PASSWORD
        ])

        config_client_store_auth_fixture.assert_not_called()
        assert result.output == f'Error: {error}\n'
