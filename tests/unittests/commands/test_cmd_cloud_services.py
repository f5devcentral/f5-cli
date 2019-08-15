from click.testing import CliRunner

from f5cloudsdk.cloud_services import ManagementClient
from f5cloudcli.config import ConfigClient

# Module under test
from f5cloudcli.commands.cmd_cloud_services import cli
from f5cloudcli import constants


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
        result = self.runner.invoke(
            cli, ['dns', 'create', 'a', 'test_members'])
        expected_output = "create DNS a with members test_members\nError: Command not implemented\n"
        assert result.output == expected_output
        assert result.exception

    def test_cmd_cloud_services_configure_auth(self, mocker):
        """ Configure authentication to F5 Cloud Services

        Given
        - Cloud Services is available, and end-user has an account

        When
        - User configures Cloud Services authentication with user/password credentials

        Then
        - Credentials are passed to the ConfigClient
        - The ConfigClient is instructured to save the credentials
        """
        mock_config_client = mocker.patch.object(ConfigClient, "__init__")
        mock_config_client.return_value = None
        mock_config_client_store_auth = mocker.patch.object(
            ConfigClient, "store_auth")

        test_user = 'TEST USER'
        test_password = 'TEST PASSWORD'
        result = self.runner.invoke(cli, ['configure-auth', '--user', test_user,
                                          '--password', test_password])
        mock_config_client_store_auth.assert_called_once()
        mock_config_client_args = mock_config_client.call_args_list[0][1]
        assert mock_config_client_args['group_name'] == constants.CLOUD_SERVICES_GROUP_NAME
        assert mock_config_client_args['auth'] == {
            'username': test_user,
            'password': test_password
        }
        assert result.output == f"Logging in to F5 Cloud Services as {test_user} with ******\n"
