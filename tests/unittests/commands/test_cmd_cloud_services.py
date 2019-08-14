from click.testing import CliRunner

from f5cloudsdk.cloud_services import ManagementClient
from f5cloudcli.config import ConfigClient

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

    def test_cmd_cloud_services_login(self, mocker):
        """ Log into Cloud Services
        Given
        - Cloud Services is available, and client has an account

        When
        - User attempts to login to Cloud Services with user/password credentials

        Then
        - ManagementClient object is created
        - ConfigClient is created to store credentials for further request
        - Connection attempt is logged as output
        """
        mock_management_client = mocker.patch.object(ManagementClient, "_login_using_credentials")

        mock_config_client = mocker.patch.object(ConfigClient, "__init__")
        mock_config_client.return_value = None
        mock_config_client_write = mocker.patch.object(ConfigClient, "write_client")

        test_user = 'TEST USER'
        result = self.runner.invoke(cli, ['login', '--user', test_user,
                                          '--password', 'TEST PASSWORD'])
        mock_management_client.assert_called_once()
        mock_config_client_write.assert_called_once()
        assert result.output == f"Logging in to F5 Cloud Services as {test_user} with ******\n"
