from click.testing import CliRunner

from ...global_test_imports import MagicMock, call, PropertyMock
from f5cloudsdk.bigip import ManagementClient
from f5cloudcli.config import ConfigClient
from f5cloudcli.utils import clients

# Module under test
from f5cloudcli.commands.cmd_bigip import cli, toolchain
from f5cloudcli import constants

MOCK_CONFIG_CLIENT_READ_AUTH_RETURN_VALUE = {
    'host': '1.2.3.4',
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

    def test_cmd_bigip_configure_auth(self, mocker):
        """ Configure authentication to a BIGIP
        Given
        - BIG IP is up

        When
        - User to configure auth with a BIGIP

        Then
        - Credentials are passed to the ConfigClient
        - The ConfigClient is instructured to save the credentials
        """
        mock_config_client = mocker.patch.object(ConfigClient, "__init__")
        mock_config_client.return_value = None
        mock_config_client_store_auth = mocker.patch.object(
            ConfigClient, "store_auth")

        test_host = 'TEST HOST'
        test_user = 'TEST USER'
        test_password = 'TEST PASSWORD'
        result = self.runner.invoke(cli, ['configure-auth', '--host', test_host,
                                          '--user', test_user, '--password', test_password])
        mock_config_client_store_auth.assert_called_once()
        mock_config_client_args = mock_config_client.call_args_list[0][1]
        assert mock_config_client_args['group_name'] == constants.BIGIP_GROUP_NAME
        assert mock_config_client_args['auth'] == {
            'host': test_host,
            'username': test_user,
            'password': test_password
        }
        assert result.output == "Logging in to BIG-IP TEST HOST as TEST USER with ******\n"

    def test_cmd_discover_azure_resources(self, mocker):
        """ Discover azure resources
        Given
        - Cloud provider is Azure
        - BIG-IP is up
        - 2 VMs are tagged by "test_key/test_value" tag
        - Output format is JSON

        When
        - User attempts to discover resources with tag test_key/test_value

        Then
        - Azure resources are retrieved
        """
        mock_clients = mocker.patch.object(clients, "get_provider_client")
        m = MagicMock()
        m.list.return_value = [{"id": "a1", "name": "f5bigip1"},
                               {"id": "b2", "name": "f5bigip2"}]
        type(mock_clients.return_value).virtual_machines = PropertyMock(
            return_value=m)
        result = self.runner.invoke(cli, ['discover', '--provider', 'azure',
                                          '--provider-tag', 'test_key:test_value'])
        assert result.output == "Discovering all BIG-IPs in azure with tag test_key:test_value\n{\n    \"id\": \"a1\",\n    \"name\": \"f5bigip1\"\n},\n{\n    \"id\": \"b2\",\n    \"name\": \"f5bigip2\"\n}\n"

    def test_cmd_package_verify_existing_toolchain_component(self, mocker):
        """ Command package verify an existing toolchain component
        Given
        - BIG-IP is up
        - 'do' toolchain component is installed
        When
        - User attempts to verify status of the install 'do' toolchain component
        Then
        - Installed 'do' toolchain component message is logged
        """
        mock_config_client = mocker.patch.object(ConfigClient, "__init__")
        mock_config_client.return_value = None
        mock_config_client_read_auth = mocker.patch.object(
            ConfigClient, "read_auth")
        mock_config_client_read_auth.return_value = MOCK_CONFIG_CLIENT_READ_AUTH_RETURN_VALUE

        mock_management_client = mocker.patch.object(ManagementClient)

        mock_toolchain_client = mocker.patch(
            "f5cloudcli.commands.cmd_bigip.ToolChainClient")

        m = MagicMock()
        m.is_installed.return_value = True
        type(mock_toolchain_client.return_value).package = PropertyMock(
            return_value=m)

        result = self.runner.invoke(
            toolchain, ['package', 'verify', '--component', 'do', '--version', '1.3.0'])
        mock_management_client.assert_called_once()
        assert result.output == "Toolchain component package installed: True\n"

    def test_cmd_package_verify_nonexist_toolchain_component(self, mocker):
        """ Command package verify a non-existing package
        Given
        - BIG-IP is up
        - 'do' component is not installed
        When
        - User attempts to verify status of the install 'do' component
        Then
        - Non existing 'do' component message is logged
        """
        mock_config_client = mocker.patch.object(ConfigClient, "__init__")
        mock_config_client.return_value = None
        mocker.patch.object(ConfigClient, "read_client")

        mock_toolchain_client = mocker.patch(
            "f5cloudcli.commands.cmd_bigip.ToolChainClient")

        m = MagicMock()
        m.is_installed.return_value = False
        type(mock_toolchain_client.return_value).package = PropertyMock(
            return_value=m)

        result = self.runner.invoke(
            toolchain, ['package', 'verify', '--component', 'do', '--version', '1.3.0'])
        assert result.output == "Toolchain component package installed: False\n"

    def test_cmd_package_install_existing_toolchain_component(self, mocker):
        """ Command package install an existing package
        Given
        - BIG-IP is up
        - 'do' component is installed
        When
        - User attempts to install 'do' component
        Then
        - Already installed 'do' component message is logged
        """
        mock_config_client = mocker.patch.object(ConfigClient, "__init__")
        mock_config_client.return_value = None
        mocker.patch.object(ConfigClient, "read_client")

        mock_toolchain_client = mocker.patch(
            "f5cloudcli.commands.cmd_bigip.ToolChainClient")

        m = MagicMock()
        m.is_installed.return_value = True
        type(mock_toolchain_client.return_value).package = PropertyMock(
            return_value=m)

        result = self.runner.invoke(
            toolchain, ['package', 'install', '--component', 'do', '--version', '1.3.0'])
        assert result.output == "Toolchain component package do is already installed\n"

    def test_cmd_package_install_non_existing_toolchain_component(self, mocker):
        """ Command package install a non-existing package
        Given
        - BIG-IP is up
        - 'do' component is not installed
        When
        - User attempts to install 'do' component
        Then
        -  Successfully installed 'do' component message is logged
        """
        mock_config_client = mocker.patch.object(ConfigClient, "__init__")
        mock_config_client.return_value = None
        mocker.patch.object(ConfigClient, "read_client")

        mock_toolchain_client = mocker.patch(
            "f5cloudcli.commands.cmd_bigip.ToolChainClient")

        m = MagicMock()
        m.is_installed.return_value = False
        m.install.return_value = None
        type(mock_toolchain_client.return_value).package = PropertyMock(
            return_value=m)

        result = self.runner.invoke(
            toolchain, ['package', 'install', '--component', 'do', '--version', '1.3.0'])
        assert result.output == "Toolchain component package do installed\n"

    def test_cmd_package_uninstall_existing_toolchain_component(self, mocker):
        """ Command package uninstall an existing package
        Given
        - BIG-IP is up
        - 'do' component is installed
        When
        - User attempts to uninstall 'do' component
        Then
        - Uninstalled 'do' component message is logged
        """
        mock_config_client = mocker.patch.object(ConfigClient, "__init__")
        mock_config_client.return_value = None
        mocker.patch.object(ConfigClient, "read_client")

        mock_toolchain_client = mocker.patch(
            "f5cloudcli.commands.cmd_bigip.ToolChainClient")

        m = MagicMock()
        m.is_installed.return_value = True
        m.uninstall.return_value = None
        type(mock_toolchain_client.return_value).package = PropertyMock(
            return_value=m)

        result = self.runner.invoke(
            toolchain, ['package', 'uninstall', '--component', 'do', '--version', '1.3.0'])
        assert result.output == "Toolchain component package do uninstalled\n"

    def test_cmd_package_uninstall_non_existing_toolchain_component(self, mocker):
        """ Command package uninstall a non-existing package
        Given
        - BIG-IP is up
        - 'do' component is not installed
        When
        - User attempts to uninstall 'do' component
        Then
        -  Already uninstalled 'do' component message is logged
        """
        mock_config_client = mocker.patch.object(ConfigClient, "__init__")
        mock_config_client.return_value = None
        mocker.patch.object(ConfigClient, "read_client")

        mock_toolchain_client = mocker.patch(
            "f5cloudcli.commands.cmd_bigip.ToolChainClient")

        m = MagicMock()
        m.is_installed.return_value = False
        type(mock_toolchain_client.return_value).package = PropertyMock(
            return_value=m)

        result = self.runner.invoke(
            toolchain, ['package', 'uninstall', '--component', 'do', '--version', '1.3.0'])
        assert result.output == "Toolchain component package do is already uninstalled\n"

    def test_cmd_package_unsupported_action(self, mocker):
        """ Unsupported command package action
        Given
        - BIG-IP is up
        - 'do' component is not installed
        When
        - User attempts to perform 'upgrade' action on 'do' component
        Then
        -  Non-implemented action exception is thrown
        """
        mock_config_client = mocker.patch.object(ConfigClient, "__init__")
        mock_config_client.return_value = None
        mocker.patch.object(ConfigClient, "read_client")

        mock_toolchain_client = mocker.patch(
            "f5cloudcli.commands.cmd_bigip.ToolChainClient")

        m = MagicMock()
        m.is_installed.return_value = False
        type(mock_toolchain_client.return_value).package = PropertyMock(
            return_value=m)
        result = self.runner.invoke(
            toolchain, ['package', 'upgrade', '--component', 'do'])
        assert result.exception
        assert result.output == "Error: Action upgrade not implemented\n"

    def test_cmd_service_show_installed_component(self, mocker):
        """ Command service show an already installed component
        Given
        - BIG-IP is up
        - 'do' component is installed
        When
        - User attempts to show the status of 'do' component
        Then
        -  Current status message of 'do' component is logged
        """
        mock_config_client = mocker.patch.object(ConfigClient, "__init__")
        mock_config_client.return_value = None
        mocker.patch.object(ConfigClient, "read_client")

        mock_toolchain_client = mocker.patch(
            "f5cloudcli.commands.cmd_bigip.ToolChainClient")

        mock_package = MagicMock()
        mock_package.is_installed.return_value = True
        type(mock_toolchain_client.return_value).package = PropertyMock(
            return_value=mock_package)
        mock_service = MagicMock()
        mock_service.show.return_value = "Test DO status"
        type(mock_toolchain_client.return_value).service = PropertyMock(
            return_value=mock_service)

        result = self.runner.invoke(
            toolchain, ['service', 'show', '--component', 'do', '--version', '1.3.0'])
        assert result.output == "Toolchain component service show: Test DO status\n"

    def test_cmd_service_show_non_installed_component(self, mocker):
        """ Command service show status of a non-installed component
        Given
        - BIG-IP is up
        - 'do' component is not installed
        When
        - User attempts to show the status of 'do' component
        Then
        - 'do' component is installed
        - 'do' component is available
        -  Current status message of 'do' component is logged
        """
        mock_config_client = mocker.patch.object(ConfigClient, "__init__")
        mock_config_client.return_value = None
        mocker.patch.object(ConfigClient, "read_client")

        mock_toolchain_client = mocker.patch(
            "f5cloudcli.commands.cmd_bigip.ToolChainClient")

        mock_package = MagicMock()
        mock_package.is_installed.return_value = False
        mock_package.install.return_value = None
        type(mock_toolchain_client.return_value).package = PropertyMock(
            return_value=mock_package)
        mock_service = MagicMock()
        mock_service.show.return_value = "Test DO status"
        mock_service.is_available.return_value = None
        type(mock_toolchain_client.return_value).service = PropertyMock(
            return_value=mock_service)

        result = self.runner.invoke(toolchain, [
                                    'service', 'show', '--component', 'do', '--version', '1.3.0', '--install-component'])
        assert result.output == "Installing toolchain component package\nChecking toolchain component service is available\nToolchain component service show: Test DO status\n"

    def test_cmd_service_create_declaration_installed_component(self, mocker):
        """ Command service create declaration of an installed component
        Given
        - BIG-IP is up
        - 'do' component is installed
        When
        - User attempts to create a 'do' declaration
        Then
        -  result status of create action is logged
        """
        mock_config_client = mocker.patch.object(ConfigClient, "__init__")
        mock_config_client.return_value = None
        mocker.patch.object(ConfigClient, "read_client")

        mock_toolchain_client = mocker.patch(
            "f5cloudcli.commands.cmd_bigip.ToolChainClient")

        mock_package = MagicMock()
        mock_package.is_installed.return_value = True
        type(mock_toolchain_client.return_value).package = PropertyMock(
            return_value=mock_package)
        mock_service = MagicMock()
        mock_service.create.return_value = "Test DO create status"
        type(mock_toolchain_client.return_value).service = PropertyMock(
            return_value=mock_service)

        mock_utils_core_convert = mocker.patch(
            "f5cloudcli.commands.cmd_bigip.utils_core.convert_to_absolute")
        mock_utils_core_convert.return_value = "fake location"

        result = self.runner.invoke(toolchain, ['service', 'create', '--component', 'do',
                                                '--declaration', './test/fake_declaration.json'])
        assert result.output == "Toolchain component service create: Test DO create status\n"
        mock_utils_core_convert.assert_has_calls(
            [call('./test/fake_declaration.json')])

    def test_cmd_service_delete_installed_component(self, mocker):
        """ Command service delete of an already installed component
        Given
        - BIG-IP is up
        - 'do' component is installed
        When
        - User attempts to delete a 'do' service
        Then
        -  deleted status of 'do' service is logged
        """
        mock_config_client = mocker.patch.object(ConfigClient, "__init__")
        mock_config_client.return_value = None
        mocker.patch.object(ConfigClient, "read_client")

        mock_toolchain_client = mocker.patch(
            "f5cloudcli.commands.cmd_bigip.ToolChainClient")

        mock_package = MagicMock()
        mock_package.is_installed.return_value = True
        type(mock_toolchain_client.return_value).package = PropertyMock(
            return_value=mock_package)
        mock_service = MagicMock()
        mock_service.delete.return_value = "Test DO delete status"
        type(mock_toolchain_client.return_value).service = PropertyMock(
            return_value=mock_service)

        result = self.runner.invoke(
            toolchain, ['service', 'delete', '--component', 'do'])
        assert result.output == "Toolchain component service delete: Test DO delete status\n"

    def test_cmd_service_unsupported_action(self, mocker):
        """ Unsupported command service action
        Given
        - BIG-IP is up
        - 'do' component is installed
        When
        - User attempts to perform 'remove' action on 'do' component
        Then
        -  Non-implemented action exception is thrown
        """
        mock_config_client = mocker.patch.object(ConfigClient, "__init__")
        mock_config_client.return_value = None
        mocker.patch.object(ConfigClient, "read_client")

        mock_toolchain_client = mocker.patch(
            "f5cloudcli.commands.cmd_bigip.ToolChainClient")

        m = MagicMock()
        m.is_installed.return_value = False
        type(mock_toolchain_client.return_value).package = PropertyMock(
            return_value=m)
        result = self.runner.invoke(
            toolchain, ['service', 'remove', '--component', 'do'])
        assert "invalid choice: remove" in result.output
        assert result.exception
