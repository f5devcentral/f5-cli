""" Test BIG-IP command """

import json

from f5sdk.bigip import ManagementClient

from f5cli.config import ConfigClient
from f5cli.utils import clients
from f5cli.commands.cmd_bigip import cli, toolchain
from f5cli import constants

from ...global_test_imports import MagicMock, call, PropertyMock, pytest, CliRunner

MOCK_CONFIG_CLIENT_READ_AUTH_RETURN_VALUE = {
    'host': '1.2.3.4',
    'port': '1234',
    'username': 'test_user',
    'password': 'test_password'
}

MOCK_IS_INSTALLED_RETURN_VALUE = {
    'installed': True,
    'installed_version': '1.3.0',
    'latest_version': '1.3.0'
}

# pylint: disable=too-many-public-methods


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
    def toolchain_client_fixture(mocker):
        """Test fixture """
        mock_toolchain_client = mocker.patch(
            "f5cli.commands.cmd_bigip.ToolChainClient")

        mock = MagicMock()
        mock.is_installed.return_value = MOCK_IS_INSTALLED_RETURN_VALUE
        type(mock_toolchain_client.return_value).package = PropertyMock(return_value=mock)
        return mock_toolchain_client

    @staticmethod
    @pytest.fixture
    def config_client_read_auth_fixture(mocker):
        """ PyTest fixture mocking ConfigClient's read_auth method """
        mock_config_client_read_auth = mocker.patch.object(
            ConfigClient, "read_auth")
        mock_config_client_read_auth.return_value = MOCK_CONFIG_CLIENT_READ_AUTH_RETURN_VALUE

    @staticmethod
    @pytest.fixture
    def config_client_fixture(mocker):
        """ PyTest fixture returning mocked ConfigClient """
        mock_config_client = mocker.patch.object(ConfigClient, "__init__")
        mock_config_client.return_value = None
        return mock_config_client

    @staticmethod
    @pytest.fixture
    def mgmt_client_fixture(mocker):
        """ PyTest fixture returning mocked BigIP Management Client """
        mock_management_client = mocker.patch.object(ManagementClient, '__init__')
        mock_management_client.return_value = None
        return mock_management_client

    def test_cmd_bigip_configure_auth(self, mocker, config_client_fixture):
        """ Configure authentication to a BIGIP
        Given
        - BIG IP is up

        When
        - User to configure auth with a BIGIP

        Then
        - Credentials are passed to the ConfigClient
        - The ConfigClient is instructured to save the credentials
        """
        mock_config_client = config_client_fixture
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
            'port': None,
            'username': test_user,
            'password': test_password
        }
        assert result.output == json.dumps(
            {'message': 'Authentication configured successfully'},
            indent=4,
            sort_keys=True
        ) + '\n'

    def test_cmd_bigip_configure_auth_with_port(self, mocker, config_client_fixture):
        """ Configure authentication to a BIGIP
        Given
        - BIG IP is up

        When
        - User to configure auth with a BIGIP against a specific port

        Then
        - Credentials as well as the host and port information is passed to the ConfigClient
        - The ConfigClient is instructured to save the credentials
        """
        mock_config_client = config_client_fixture
        mock_config_client_store_auth = mocker.patch.object(
            ConfigClient, "store_auth")

        test_host = 'TEST HOST'
        test_user = 'TEST USER'
        test_port = 'TEST PORT'
        test_password = 'TEST PASSWORD'
        result = self.runner.invoke(
            cli,
            ['configure-auth', '--host', test_host, '--port', test_port,
             '--user', test_user, '--password', test_password]
        )
        mock_config_client_store_auth.assert_called_once()
        mock_config_client_args = mock_config_client.call_args_list[0][1]
        assert mock_config_client_args['group_name'] == constants.BIGIP_GROUP_NAME
        assert mock_config_client_args['auth'] == {
            'host': test_host,
            'port': test_port,
            'username': test_user,
            'password': test_password
        }
        assert result.output == json.dumps(
            {'message': 'Authentication configured successfully'},
            indent=4,
            sort_keys=True
        ) + '\n'

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

        virtual_machines = [
            {
                "id": "a1",
                "name": "f5bigip1"
            },
            {
                "id": "b2",
                "name": "f5bigip2"
            }
        ]

        mock_clients = mocker.patch.object(clients, "get_provider_client")
        mock_list = MagicMock()
        mock_list.list.return_value = virtual_machines
        type(mock_clients.return_value).virtual_machines = PropertyMock(
            return_value=mock_list)

        result = self.runner.invoke(
            cli,
            ['discover', '--provider', 'azure', '--provider-tag', 'test_key:test_value']
        )
        assert result.output == json.dumps(virtual_machines, indent=4, sort_keys=True) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_package_verify_existing_toolchain_component(self,
                                                             mocker,
                                                             mgmt_client_fixture,
                                                             config_client_read_auth_fixture,
                                                             toolchain_client_fixture):
        """ Command package verify an existing toolchain component
        Given
        - BIG-IP is up
        - 'do' toolchain component is installed
        When
        - User attempts to verify status of the install 'do' toolchain component
        Then
        - Installed version information 'do' toolchain component is logged
        """
        mock_management_client = mgmt_client_fixture

        result = self.runner.invoke(
            toolchain, ['package', 'verify', '--component', 'do', '--version', '1.3.0'])
        mock_management_client.assert_called_once()
        assert result.output == json.dumps(
            MOCK_IS_INSTALLED_RETURN_VALUE,
            indent=4,
            sort_keys=True
        ) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_package_verify_nonexist_toolchain_component(self,
                                                             mocker,
                                                             config_client_read_auth_fixture,
                                                             mgmt_client_fixture):
        """ Command package verify a non-existing package
        Given
        - BIG-IP is up
        - 'do' component is not installed
        When
        - User attempts to verify status of the install 'do' component
        Then
        - Installed version information 'do' toolchain component is logged
        """
        mock_toolchain_client = mocker.patch(
            "f5cli.commands.cmd_bigip.ToolChainClient")

        mock_is_installed_return_value = {
            'installed': False,
            'installed_version': '',
            'latest_version': '1.3.0'
        }

        mock = MagicMock()
        mock.is_installed.return_value = mock_is_installed_return_value
        type(mock_toolchain_client.return_value).package = PropertyMock(return_value=mock)

        result = self.runner.invoke(
            toolchain, ['package', 'verify', '--component', 'do', '--version', '1.3.0'])
        assert result.output == json.dumps(
            mock_is_installed_return_value, indent=4, sort_keys=True
        ) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_package_install_existing_toolchain_component(self,
                                                              mocker,
                                                              config_client_read_auth_fixture,
                                                              mgmt_client_fixture,
                                                              toolchain_client_fixture):
        """ Command package install an existing package
        Given
        - BIG-IP is up
        - 'do' component is installed
        When
        - User attempts to install 'do' component
        Then
        - Already installed 'do' component message is logged
        """
        result = self.runner.invoke(
            toolchain, ['package', 'install', '--component', 'do', '--version', '1.3.0'])
        assert result.output == json.dumps(
            {'message': 'Toolchain component package do version 1.3.0 is already installed'},
            indent=4,
            sort_keys=True
        ) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_package_install_non_existing_toolchain_component(self,
                                                                  mocker,
                                                                  config_client_read_auth_fixture,
                                                                  mgmt_client_fixture):
        """ Command package install a non-existing package
        Given
        - BIG-IP is up
        - 'do' component is not installed
        When
        - User attempts to install 'do' component
        Then
        -  Successfully installed 'do' component message is logged
        """
        mock_toolchain_client = mocker.patch(
            "f5cli.commands.cmd_bigip.ToolChainClient")

        mock = MagicMock()
        mock.is_installed.return_value = {
            'installed': False,
            'installed_version': '',
            'latest_version': '1.3.0'
        }
        mock.install.return_value = None
        type(mock_toolchain_client.return_value).package = PropertyMock(return_value=mock)

        result = self.runner.invoke(
            toolchain, ['package', 'install', '--component', 'do', '--version', '1.3.0'])
        assert result.output == json.dumps(
            {'message': 'Toolchain component package do installed'},
            indent=4,
            sort_keys=True
        ) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_package_uninstall_existing_toolchain_component(self,
                                                                mocker,
                                                                config_client_read_auth_fixture,
                                                                mgmt_client_fixture):
        """ Command package uninstall an existing package
        Given
        - BIG-IP is up
        - 'do' component is installed
        When
        - User attempts to uninstall 'do' component
        Then
        - Uninstalled 'do' component message is logged
        """
        mock_toolchain_client = mocker.patch(
            "f5cli.commands.cmd_bigip.ToolChainClient")

        mock = MagicMock()
        mock.is_installed.return_value = {'installed': True}
        mock.uninstall.return_value = None
        type(mock_toolchain_client.return_value).package = PropertyMock(
            return_value=mock
        )

        result = self.runner.invoke(
            toolchain, ['package', 'uninstall', '--component', 'do', '--version', '1.3.0'])
        assert result.output == json.dumps(
            {'message': 'Toolchain component package do uninstalled'},
            indent=4,
            sort_keys=True
        ) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_package_uninstall_non_existing_toolchain_component(self,
                                                                    mocker,
                                                                    config_client_read_auth_fixture,
                                                                    mgmt_client_fixture):
        """ Command package uninstall a non-existing package
        Given
        - BIG-IP is up
        - 'do' component is not installed
        When
        - User attempts to uninstall 'do' component
        Then
        -  Already uninstalled 'do' component message is logged
        """
        mock_toolchain_client = mocker.patch(
            "f5cli.commands.cmd_bigip.ToolChainClient")

        mock = MagicMock()
        mock.is_installed.return_value = {'installed': False}
        type(mock_toolchain_client.return_value).package = PropertyMock(return_value=mock)

        result = self.runner.invoke(
            toolchain, ['package', 'uninstall', '--component', 'do', '--version', '1.3.0'])
        assert result.output == json.dumps(
            {'message': 'Toolchain component package do is already uninstalled'},
            indent=4,
            sort_keys=True
        ) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_package_unsupported_action(self,
                                            mocker,
                                            config_client_read_auth_fixture,
                                            mgmt_client_fixture):
        """ Unsupported command package action
        Given
        - BIG-IP is up
        - 'do' component is not installed
        When
        - User attempts to perform 'upgrade' action on 'do' component
        Then
        -  Non-implemented action exception is thrown
        """
        mock_toolchain_client = mocker.patch(
            "f5cli.commands.cmd_bigip.ToolChainClient")

        mock = MagicMock()
        mock.is_installed.return_value = {'installed': False}
        type(mock_toolchain_client.return_value).package = PropertyMock(return_value=mock)

        result = self.runner.invoke(
            toolchain, ['package', 'upgrade', '--component', 'do'])
        assert result.exception
        assert result.output == "Error: Action upgrade not implemented\n"

    # pylint: disable=unused-argument
    def test_cmd_service_show_installed_component(self,
                                                  mocker,
                                                  config_client_read_auth_fixture,
                                                  mgmt_client_fixture,
                                                  toolchain_client_fixture):
        """ Command service show an already installed component
        Given
        - BIG-IP is up
        - 'do' component is installed
        When
        - User attempts to show the status of 'do' component
        Then
        -  Current status message of 'do' component is logged
        """

        mock_toolchain_client = mocker.patch(
            "f5cli.commands.cmd_bigip.ToolChainClient")

        show_response = {
            'foo': 'bar'
        }

        mock_service = MagicMock()
        mock_service.show.return_value = show_response
        type(mock_toolchain_client.return_value).service = PropertyMock(
            return_value=mock_service)

        result = self.runner.invoke(
            toolchain, ['service', 'show', '--component', 'do', '--version', '1.3.0'])
        assert result.output == json.dumps(show_response, indent=4, sort_keys=True) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_service_show_non_installed_component(self,
                                                      mocker,
                                                      config_client_read_auth_fixture,
                                                      mgmt_client_fixture):
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
        mock_toolchain_client = mocker.patch(
            "f5cli.commands.cmd_bigip.ToolChainClient")

        is_installed_response = {
            'installed': False
        }
        show_response = {
            'foo': 'bar'
        }

        mock_package = MagicMock()
        mock_package.is_installed.return_value = is_installed_response
        mock_package.install.return_value = None
        type(mock_toolchain_client.return_value).package = PropertyMock(
            return_value=mock_package)
        mock_service = MagicMock()
        mock_service.show.return_value = show_response
        mock_service.is_available.return_value = None
        type(mock_toolchain_client.return_value).service = PropertyMock(
            return_value=mock_service)

        result = self.runner.invoke(
            toolchain,
            ['service', 'show', '--component', 'do', '--version', '1.3.0', '--install-component']
        )
        assert result.output == json.dumps(show_response, indent=4, sort_keys=True) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_service_create_declaration_installed_component(self,
                                                                mocker,
                                                                config_client_read_auth_fixture,
                                                                mgmt_client_fixture,
                                                                toolchain_client_fixture):
        """ Command service create declaration of an installed component
        Given
        - BIG-IP is up
        - 'do' component is installed
        When
        - User attempts to create a 'do' declaration
        Then
        -  result status of create action is logged
        """
        mock_service = MagicMock()

        create_response = {
            'foo': 'bar'
        }

        mock_service.create.return_value = create_response
        mock_toolchain_client = toolchain_client_fixture
        type(mock_toolchain_client.return_value).service = PropertyMock(
            return_value=mock_service)

        mock_utils_core_convert = mocker.patch(
            "f5cli.commands.cmd_bigip.utils_core.convert_to_absolute")
        mock_utils_core_convert.return_value = "fake location"

        result = self.runner.invoke(toolchain, ['service', 'create', '--component', 'do',
                                                '--declaration', './test/fake_declaration.json'])

        assert result.output == json.dumps(create_response, indent=4, sort_keys=True) + '\n'
        mock_utils_core_convert.assert_has_calls(
            [call('./test/fake_declaration.json')])

    # pylint: disable=unused-argument
    def test_cmd_service_delete_installed_component(self,
                                                    mocker,
                                                    config_client_read_auth_fixture,
                                                    mgmt_client_fixture,
                                                    toolchain_client_fixture):
        """ Command service delete of an already installed component
        Given
        - BIG-IP is up
        - 'do' component is installed
        When
        - User attempts to delete a 'do' service
        Then
        -  deleted status of 'do' service is logged
        """
        mock_toolchain_client = toolchain_client_fixture

        delete_response = {
            'foo': 'bar'
        }

        mock_service = MagicMock()
        mock_service.delete.return_value = delete_response
        type(mock_toolchain_client.return_value).service = PropertyMock(
            return_value=mock_service)

        result = self.runner.invoke(
            toolchain, ['service', 'delete', '--component', 'do'])
        assert result.output == json.dumps(delete_response, indent=4, sort_keys=True) + '\n'

    def test_cmd_service_unsupported_action(self):
        """ Unsupported command service action
        Given
        - BIG-IP is up
        - 'do' component is installed
        When
        - User attempts to perform 'remove' action on 'do' component
        Then
        -  Non-implemented action exception is thrown
        """

        result = self.runner.invoke(
            toolchain, ['service', 'remove', '--component', 'do'])
        assert "invalid choice: remove" in result.output
        assert result.exception
