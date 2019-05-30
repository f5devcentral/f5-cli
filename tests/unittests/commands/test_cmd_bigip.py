import sys
sys.path.append("../../../../")
import click
from click.testing import CliRunner

from ...global_test_imports import pytest, MagicMock, call, PropertyMock
from f5cloudsdk.bigip import ManagementClient
from f5cloudsdk.provider.azure import ProviderClient
from f5cloudsdk.provider.azure.virtual_machines import OperationClient
from f5cloudcli.config import ConfigClient
from f5cloudcli.utils import clients, core

# Module under test
from f5cloudcli.commands.cmd_bigip import cli


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

    def test_cmd_bigip_login(self, mocker):
        """ Test: log into a BIGIP

        Assertions
        ----------
        - ManagementClient object is created
        - ConfigClient is created to write credentials
        - Host information is represented in output
        """
        mock_management_client = mocker.patch.object(ManagementClient, "_login_using_credentials")

        mock_config_client = mocker.patch.object(ConfigClient, "__init__")
        mock_config_client.return_value = None
        mock_config_client_write = mocker.patch.object(ConfigClient, "write_client")

        result = self.runner.invoke(cli, ['login', '--host', 'TEST HOST',
                                         '--user', 'TEST USER', '--password', 'TEST PASSWORD'])
        mock_management_client.assert_called_once()
        mock_config_client_write.assert_called_once()
        assert result.output == "Logging in to BIG-IP TEST HOST as TEST USER with ******\n"

    def test_cmd_discover_azure_resources(self, mocker):
        """ Test: discover azure resources

        Assertions
        ----------
        - Azure resources are retrieved
        """
        mock_clients = mocker.patch.object(clients, "get_provider_client")
        m = MagicMock()
        m.list.return_value = "TEST LIST"
        type(mock_clients.return_value).virtual_machines = PropertyMock(return_value=m)
        result = self.runner.invoke(cli, ['discover', '--provider', 'azure',
                                          '--provider-tag', 'test_key:test_value'])
        assert result.output == "Discovering all BIG-IPs in azure with tag test_key:test_value\nTEST LIST\n"
        
 