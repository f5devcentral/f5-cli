""" Test BIG-IP command """

import json

from f5sdk.bigip import ManagementClient

from f5cli.config import AuthConfigurationClient
from f5cli.commands.cmd_bigip import cli

from ...global_test_imports import MagicMock, call, PropertyMock, pytest, CliRunner

MOCK_CONFIG_CLIENT_READ_AUTH_RETURN_VALUE = {
    'host': '1.2.3.4',
    'port': '1234',
    'type': 'BIGIP',
    'user': 'test_user',
    'password': 'test_password'
}

MOCK_IS_INSTALLED_RETURN_VALUE = {
    'installed': True,
    'installed_version': '1.10.0',
    'latest_version': '1.10.0'
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
    def do_extension_client_fixture(mocker):
        """Test fixture """
        mock_extension_client = mocker.patch(
            "f5sdk.bigip.extension.DOClient")

        mock = MagicMock()
        mock.is_installed.return_value = MOCK_IS_INSTALLED_RETURN_VALUE
        type(mock_extension_client.return_value).package = PropertyMock(return_value=mock)
        return mock_extension_client

    @staticmethod
    @pytest.fixture
    def as3_extension_client_fixture(mocker):
        """Test fixture """
        mock_extension_client = mocker.patch(
            "f5sdk.bigip.extension.AS3Client")

        mock = MagicMock()
        mock.is_installed.return_value = {
            'installed': True
        }
        type(mock_extension_client.return_value).package = PropertyMock(return_value=mock)
        return mock_extension_client

    @staticmethod
    @pytest.fixture
    def cf_extension_client_fixture(mocker):
        """Test fixture """
        mock_extension_client = mocker.patch(
            "f5sdk.bigip.extension.CFClient")

        mock = MagicMock()
        mock.is_installed.return_value = MOCK_IS_INSTALLED_RETURN_VALUE
        type(mock_extension_client.return_value).package = PropertyMock(return_value=mock)
        return mock_extension_client

    @staticmethod
    @pytest.fixture
    def config_client_read_auth_fixture(mocker):
        """ PyTest fixture mocking AuthConfigurationClient's read_auth method """
        mock_config_client_read_auth = mocker.patch.object(
            AuthConfigurationClient, "read_auth")
        mock_config_client_read_auth.return_value = MOCK_CONFIG_CLIENT_READ_AUTH_RETURN_VALUE

    @staticmethod
    @pytest.fixture
    def config_client_fixture(mocker):
        """ PyTest fixture returning mocked AuthConfigurationClient """
        mock_config_client = mocker.patch.object(AuthConfigurationClient, "__init__")
        mock_config_client.return_value = None
        return mock_config_client

    @staticmethod
    @pytest.fixture
    def mgmt_client_fixture(mocker):
        """ PyTest fixture returning mocked BigIP Management Client """
        mock_management_client = mocker.patch.object(ManagementClient, '__init__')
        mock_management_client.return_value = None
        return mock_management_client

    # pylint: disable=unused-argument
    def test_cmd_package_verify_existing_extension_component(self,
                                                             mocker,
                                                             mgmt_client_fixture,
                                                             config_client_read_auth_fixture):
        """ Command package verify an existing extension component
        Given
        - BIG-IP is up
        - 'do' extension component is installed
        When
        - User attempts to verify status of the install 'do' extension component
        Then
        - Installed version information 'do' extension component is logged
        """
        mock_extension_client = mocker.patch(
            "f5sdk.bigip.extension.DOClient")
        mock = MagicMock()
        mock.is_installed.return_value = MOCK_IS_INSTALLED_RETURN_VALUE
        type(mock_extension_client.return_value).package = PropertyMock(return_value=mock)
        result = self.runner.invoke(
            cli, ['extension', 'do', 'verify', '--version', '1.10.0'])
        assert result.output == json.dumps(
            MOCK_IS_INSTALLED_RETURN_VALUE,
            indent=4,
            sort_keys=True
        ) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_package_verify_nonexist_extension_component(self,
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
        - Installed version information 'do' extension component is logged
        """
        mock_extension_client = mocker.patch(
            "f5sdk.bigip.extension.DOClient")

        mock_is_installed_return_value = {
            'installed': False,
            'installed_version': '',
            'latest_version': '1.10.0'
        }

        mock = MagicMock()
        mock.is_installed.return_value = mock_is_installed_return_value
        type(mock_extension_client.return_value).package = PropertyMock(return_value=mock)

        result = self.runner.invoke(
            cli, ['extension', 'do', 'verify', '--version', '1.10.0'])
        assert result.output == json.dumps(
            mock_is_installed_return_value, indent=4, sort_keys=True
        ) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_package_install_existing_extension_component(self,
                                                              mocker,
                                                              config_client_read_auth_fixture,
                                                              mgmt_client_fixture):
        """ Command package install an existing package
        Given
        - BIG-IP is up
        - 'do' component is installed
        When
        - User attempts to install 'do' component
        Then
        - Already installed 'do' component message is logged
        """
        mock_extension_client = mocker.patch(
            "f5sdk.bigip.extension.DOClient")
        mock = MagicMock()
        mock.is_installed.return_value = {
            'installed': True,
            'installed_version': '1.10.0',
            'latest_version': '1.10.0'
        }
        type(mock_extension_client.return_value).package = PropertyMock(return_value=mock)
        result = self.runner.invoke(
            cli, ['extension', 'do', 'install', '--version', '1.10.0'])
        assert result.output == json.dumps(
            {"message": "Extension component package 'do' version '1.10.0' is already installed"},
            indent=4,
            sort_keys=True
        ) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_package_install_non_existing_extension_component(self,
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
        mock_extension_client = mocker.patch(
            "f5sdk.bigip.extension.DOClient")
        mock = MagicMock()
        mock.is_installed.return_value = {
            'installed': False,
            'installed_version': '',
            'latest_version': '1.10.0'
        }
        mock.install.return_value = {'version': '1.10.0'}
        type(mock_extension_client.return_value).package = PropertyMock(return_value=mock)

        result = self.runner.invoke(
            cli, ['extension', 'do', 'install', '--version', '1.10.0'])
        assert result.output == json.dumps(
            {"message": "Extension component package 'do' successfully installed version '1.10.0'"},
            indent=4,
            sort_keys=True
        ) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_package_uninstall_existing_extension_component(self,
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
        mock_extension_client = mocker.patch(
            "f5sdk.bigip.extension.DOClient")
        mock = MagicMock()
        mock.is_installed.return_value = {
            'installed': True,
            'installed_version': '1.10.0',
        }
        mock.uninstall.return_value = None
        type(mock_extension_client.return_value).package = PropertyMock(
            return_value=mock
        )

        result = self.runner.invoke(
            cli, ['extension', 'do', 'uninstall', '--version', '1.10.0', '--auto-approve'])
        assert result.output == json.dumps(
            {
                "message": "Extension component package 'do' successfully uninstalled"
            },
            indent=4,
            sort_keys=True
        ) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_package_uninstall_non_existing_extension_component(self,
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
        mock_extension_client = mocker.patch(
            "f5sdk.bigip.extension.DOClient")
        mock = MagicMock()
        mock.is_installed.return_value = {
            'installed': False,
            'installed_version': ''
        }
        type(mock_extension_client.return_value).package = PropertyMock(return_value=mock)

        result = self.runner.invoke(
            cli, ['extension', 'do', 'uninstall', '--version', '1.10.0', '--auto-approve'])
        assert result.output == json.dumps(
            {"message": "Extension component package 'do' is already uninstalled"},
            indent=4,
            sort_keys=True
        ) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_package_install_optional_package_url_https(self,
                                                            mocker,
                                                            config_client_read_auth_fixture,
                                                            mgmt_client_fixture,
                                                            as3_extension_client_fixture):
        """ Command package install optional package-url https
        Given
        - BIG-IP is up
        - 'as3' component is not installed
        When
        - User attempts to install package 'as3' --package-url with https:// specify
        Then
        - Successfully installed 'as3' component message is logged
        """
        mock_package = MagicMock()
        mock_package.is_installed.return_value = {
            'installed': False
        }
        mock_response = {
            "message": "Extension component package 'as3' successfully installed version '3.17.1'"
        }
        remote_rpm = 'https://myhost/f5-appsvcs-3.17.1-1.noarch.rpm'
        mock_package.install(package_url=remote_rpm)
        mock_package.install.return_value = {'version': '3.17.1'}
        mock_extension_client = as3_extension_client_fixture
        type(mock_extension_client.return_value).package = PropertyMock(
            return_value=mock_package)

        result = self.runner.invoke(cli, ['extension', 'as3', 'install', '--package-url',
                                          remote_rpm])

        assert result.output == json.dumps(mock_response, indent=4, sort_keys=True) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_package_install_optional_package_url_file(self,
                                                           mocker,
                                                           config_client_read_auth_fixture,
                                                           mgmt_client_fixture,
                                                           as3_extension_client_fixture):
        """ Command package install optional package-url file
        Given
        - BIG-IP is up
        - 'as3' component is not installed
        When
        - User attempts to install package 'as3' --package-url with file:// specify
        Then
        - Successfully installed 'as3' component message is logged
        """
        mock_package = MagicMock()
        mock_package.is_installed.return_value = {
            'installed': False
        }
        mock_response = {
            "message": "Extension component package 'as3' successfully installed version '3.17.1'"
        }
        local_rpm = 'file:///downloads/f5-appsvcs-3.17.1-1.noarch.rpm'
        mock_package.install(package_url=local_rpm)
        mock_package.install.return_value = {'version': '3.17.1'}
        mock_extension_client = as3_extension_client_fixture
        type(mock_extension_client.return_value).package = PropertyMock(
            return_value=mock_package)

        result = self.runner.invoke(cli, ['extension', 'as3', 'install', '--package-url',
                                          local_rpm])

        assert result.output == json.dumps(mock_response, indent=4, sort_keys=True) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_package_upgrade_existing_extension_component(self,
                                                              mocker,
                                                              config_client_read_auth_fixture,
                                                              mgmt_client_fixture):
        """ Command package upgrade to a latest version
        Given
        - BIG-IP is up
        - 'do' component is installed
        When
        - User attempts to upgrade 'do' component
        Then
        - Upgraded 'do' component message is logged
        """
        mock_extension_client = mocker.patch(
            "f5sdk.bigip.extension.DOClient")
        mock = MagicMock()
        mock.is_installed.return_value = {
            'installed': True,
            'installed_version': '1.8.0',
            'latest_version': '1.10.0'
        }
        type(mock_extension_client.return_value).package = PropertyMock(return_value=mock)

        mock_extension_client = mocker.patch(
            "f5sdk.bigip.extension.DOClient")
        mock = MagicMock()
        mock.is_installed.return_value = {
            'installed': False,
            'installed_version': ''
        }
        mock.uninstall.return_value = None
        type(mock_extension_client.return_value).package = PropertyMock(return_value=mock)

        mock_extension_client = mocker.patch(
            "f5sdk.bigip.extension.DOClient")
        mock = MagicMock()
        mock.is_installed.return_value = {
            'installed': True,
            'installed_version': '1.8.0',
            'latest_version': '1.10.0'
        }
        mock.install.return_value = None
        type(mock_extension_client.return_value).package = PropertyMock(return_value=mock)

        result = self.runner.invoke(
            cli, ['extension', 'do', 'upgrade'])
        assert result.output == json.dumps(
            {"message": "Successfully upgraded extension component package 'do' to "
                        "version '1.10.0'"},
            indent=4,
            sort_keys=True
        ) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_package_upgrade_existing_extension_component_ver(self,
                                                                  mocker,
                                                                  config_client_read_auth_fixture,
                                                                  mgmt_client_fixture):
        """ Command package upgrade to a specific version
        Given
        - BIG-IP is up
        - 'do' component is installed
        When
        - User attempts to upgrade 'do' component --version 1.9.0
        Then
        - Upgraded 'do' component message is logged
        """
        mock_extension_client = mocker.patch(
            "f5sdk.bigip.extension.DOClient")
        mock = MagicMock()
        mock.is_installed.return_value = {
            'installed': True,
            'installed_version': '1.8.0',
            'latest_version': '1.10.0'
        }
        type(mock_extension_client.return_value).package = PropertyMock(return_value=mock)

        mock_extension_client = mocker.patch(
            "f5sdk.bigip.extension.DOClient")
        mock = MagicMock()
        mock.is_installed.return_value = {
            'installed': False,
            'installed_version': ''
        }
        mock.uninstall.return_value = None
        type(mock_extension_client.return_value).package = PropertyMock(return_value=mock)

        mock_extension_client = mocker.patch(
            "f5sdk.bigip.extension.DOClient")
        mock = MagicMock()
        mock.is_installed.return_value = {
            'installed': True,
            'installed_version': '1.9.0',
            'latest_version': '1.10.0'
        }
        mock.install.return_value = None
        type(mock_extension_client.return_value).package = PropertyMock(return_value=mock)

        result = self.runner.invoke(
            cli, ['extension', 'do', 'upgrade', '--version', '1.9.0'])

        assert result.exit_code == 0, result.exception
        assert result.output == json.dumps(
            {"message": "Successfully upgraded extension component package 'do' to "
                        "version '1.9.0'"},
            indent=4,
            sort_keys=True
        ) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_package_upgrade_installed_vers_equals_latest_vers(self,
                                                                   mocker,
                                                                   config_client_read_auth_fixture,
                                                                   mgmt_client_fixture):
        """ Command package upgrade to a version already latest
        Given
        - BIG-IP is up
        - 'do' component is installed
        When
        - User attempts to upgrade to a version already installed
        Then
        - Upgraded 'do' component message is logged
        """
        mock_extension_client = mocker.patch(
            "f5sdk.bigip.extension.DOClient")

        mock = MagicMock()
        mock.is_installed.return_value = {
            'installed': True,
            'installed_version': '1.10.0',
            'latest_version': '1.10.0'
        }
        type(mock_extension_client.return_value).package = PropertyMock(
            return_value=mock
        )

        result = self.runner.invoke(
            cli, ['extension', 'do', 'upgrade'])
        assert result.output == json.dumps(
            {"message": "Extension component package 'do' version '1.10.0' "
                        "is already installed"},
            indent=4,
            sort_keys=True
        ) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_package_upgrade_uninstalled_extension_component(self,
                                                                 mocker,
                                                                 config_client_read_auth_fixture,
                                                                 mgmt_client_fixture):
        """ Command package upgrade uninstalled extension component
        Given
        - BIG-IP is up
        - 'do' component is not installed
        When
        - User attempts to upgrade 'do' component
        Then
        - Already uninstalled 'do', re-run install message is logged
        """
        mock_extension_client = mocker.patch(
            "f5sdk.bigip.extension.DOClient")
        mock = MagicMock()
        mock.is_installed.return_value = {
            'installed': False,
            'installed_version': '',
            'latest_version': '1.10.0'
        }
        type(mock_extension_client.return_value).package = PropertyMock(return_value=mock)

        result = self.runner.invoke(
            cli, ['extension', 'do', 'upgrade'])
        assert result.output == json.dumps(
            {"message": "Extension component package 'do' is uninstalled, re-run install command"},
            indent=4,
            sort_keys=True
        ) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_service_show_installed_component(self,
                                                  mocker,
                                                  config_client_read_auth_fixture,
                                                  mgmt_client_fixture,
                                                  do_extension_client_fixture):
        """ Command service show an already installed component
        Given
        - BIG-IP is up
        - 'do' component is installed
        When
        - User attempts to show the status of 'do' component
        Then
        -  Current status message of 'do' component is logged
        """

        mock_extension_client = mocker.patch(
            "f5sdk.bigip.extension.DOClient")

        show_response = {
            'foo': 'bar'
        }

        mock_service = MagicMock()
        mock_service.show.return_value = show_response
        type(mock_extension_client.return_value).service = PropertyMock(
            return_value=mock_service)

        result = self.runner.invoke(
            cli, ['extension', 'do', 'show', '--version', '1.3.0'])
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
        mock_extension_client = mocker.patch(
            "f5sdk.bigip.extension.DOClient"
        )

        is_installed_response = {
            'installed': False
        }
        show_response = {
            'foo': 'bar'
        }

        mock_package = MagicMock()
        mock_package.is_installed.return_value = is_installed_response
        mock_package.install.return_value = None
        type(mock_extension_client.return_value).package = PropertyMock(
            return_value=mock_package)

        mock_service = MagicMock()
        mock_service.show.return_value = show_response
        mock_service.is_available.return_value = None
        type(mock_extension_client.return_value).service = PropertyMock(
            return_value=mock_service)

        result = self.runner.invoke(
            cli,
            ['extension', 'do', 'show', '--version', '1.3.0']
        )
        assert result.exit_code == 0, result.exception
        assert result.output == json.dumps(show_response, indent=4, sort_keys=True) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_list_versions_component(self,
                                         mocker,
                                         config_client_read_auth_fixture,
                                         mgmt_client_fixture):
        """ Command package list-versions
        Given
        - BIG-IP is up
        When
        - User attempts to list available package versions of 'do'
        Then
        - all available packages will be listed
        """
        mock_extension_client = mocker.patch(
            "f5sdk.bigip.extension.DOClient"
        )

        list_response = [
            'foo',
            'bar'
        ]

        mock_package = MagicMock()
        mock_package.list_versions.return_value = list_response
        type(mock_extension_client.return_value).package = PropertyMock(
            return_value=mock_package)

        result = self.runner.invoke(
            cli,
            ['extension', 'do', 'list-versions']
        )
        assert result.output == json.dumps(list_response, indent=4, sort_keys=True) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_service_create_declaration_non_installed_component(self,
                                                                    mocker,
                                                                    config_client_read_auth_fixture,
                                                                    mgmt_client_fixture,
                                                                    as3_extension_client_fixture):
        """ Command service create declaration of an installed component
        Given
        - BIG-IP is up
        - 'as3' component is not installed
        When
        - User attempts to create a 'as3' declaration
        Then
        -  result status of create action is logged
        """
        mock_package = MagicMock()
        mock_package.is_installed.return_value = {
            'installed': False
        }

        mock_service = MagicMock()
        create_response = {
            'foo': 'bar'
        }
        mock_service.create.return_value = create_response
        mock_extension_client = as3_extension_client_fixture
        type(mock_extension_client.return_value).service = PropertyMock(
            return_value=mock_service)

        mock_utils_core_convert = mocker.patch(
            "f5cli.utils.core.convert_to_absolute")
        mock_utils_core_convert.return_value = "fake location"

        result = self.runner.invoke(cli, ['extension', 'as3', 'create',
                                          '--declaration', './test/fake_declaration.json'])

        assert result.output == json.dumps(create_response, indent=4, sort_keys=True) + '\n'
        mock_utils_core_convert.assert_has_calls(
            [call('./test/fake_declaration.json')])

    # pylint: disable=unused-argument
    def test_cmd_service_create_declaration_installed_component(self,
                                                                mocker,
                                                                config_client_read_auth_fixture,
                                                                mgmt_client_fixture,
                                                                do_extension_client_fixture):
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
        mock_extension_client = do_extension_client_fixture
        type(mock_extension_client.return_value).service = PropertyMock(
            return_value=mock_service)

        mock_utils_core_convert = mocker.patch(
            "f5cli.utils.core.convert_to_absolute")
        mock_utils_core_convert.return_value = "fake location"

        result = self.runner.invoke(cli, ['extension', 'do', 'create',
                                          '--declaration', './test/fake_declaration.json'])

        assert result.output == json.dumps(create_response, indent=4, sort_keys=True) + '\n'
        mock_utils_core_convert.assert_has_calls(
            [call('./test/fake_declaration.json')])

    # pylint: disable=unused-argument
    def test_cmd_service_show_failover_cf_component(self,
                                                    mocker,
                                                    config_client_read_auth_fixture,
                                                    mgmt_client_fixture,
                                                    cf_extension_client_fixture):
        """ Command service show failover (/GET trigger) from CF extension
        Given
        - 'cf' component is installed
        When
        - User attempts to show-failover
        Then
        -  result status of show-failover
        """
        mock_service = MagicMock()

        show_failover_response = {
            'foo': 'bar'
        }

        mock_service.show_trigger.return_value = show_failover_response
        mock_extension_client = cf_extension_client_fixture
        type(mock_extension_client.return_value).service = PropertyMock(
            return_value=mock_service)

        result = self.runner.invoke(cli, ['extension', 'cf', 'show-failover'])

        assert result.output == json.dumps(show_failover_response, indent=4, sort_keys=True) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_service_show_info_cf_component(self,
                                                mocker,
                                                config_client_read_auth_fixture,
                                                mgmt_client_fixture,
                                                cf_extension_client_fixture):
        """ Command service show-info of CF extension component
        Given
        - BIG-IP is up
        - 'cf' component is installed
        When
        - User attempts to show-info
        Then
        -  result status of show-info
        """
        mock_service = MagicMock()

        show_info_response = {
            'foo': 'bar'
        }

        mock_service.show_info.return_value = show_info_response
        mock_extension_client = cf_extension_client_fixture
        type(mock_extension_client.return_value).service = PropertyMock(
            return_value=mock_service)

        result = self.runner.invoke(cli, ['extension', 'cf', 'show-info'])

        assert result.output == json.dumps(show_info_response, indent=4, sort_keys=True) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_service_show_inspect_cf_component(self,
                                                   mocker,
                                                   config_client_read_auth_fixture,
                                                   mgmt_client_fixture,
                                                   cf_extension_client_fixture):
        """ Command service show-inspect of CF extension component
        Given
        - BIG-IP is up
        - 'cf' component is installed
        When
        - User attempts to show-inspect
        Then
        -  result status of show-inspect
        """
        mock_service = MagicMock()

        show_inspect_response = {
            'foo': 'bar'
        }

        mock_service.show_inspect.return_value = show_inspect_response
        mock_extension_client = cf_extension_client_fixture
        type(mock_extension_client.return_value).service = PropertyMock(
            return_value=mock_service)

        result = self.runner.invoke(cli, ['extension', 'cf', 'show-inspect'])

        assert result.output == json.dumps(show_inspect_response, indent=4, sort_keys=True) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_service_reset_cf_component(self,
                                            mocker,
                                            config_client_read_auth_fixture,
                                            mgmt_client_fixture,
                                            cf_extension_client_fixture):
        """ Command service reset of CF extension component
        Given
        - BIG-IP is up
        - 'cf' component is installed
        When
        - User attempts to reset
        Then
        -  result status of reset
        """
        mock_service = MagicMock()

        reset_response = {
            'foo': 'bar'
        }

        mock_service.reset.return_value = reset_response
        mock_extension_client = cf_extension_client_fixture
        type(mock_extension_client.return_value).service = PropertyMock(
            return_value=mock_service)

        result = self.runner.invoke(cli, ['extension', 'cf', 'reset', '--auto-approve'])

        assert result.output == json.dumps(reset_response, indent=4, sort_keys=True) + '\n'

    # pylint: disable=unused-argument
    def test_cmd_service_trigger_cf_component(self,
                                              mocker,
                                              config_client_read_auth_fixture,
                                              mgmt_client_fixture,
                                              cf_extension_client_fixture):
        """ Command service trigger failover of CF extension component
        Given
        - BIG-IP is up
        - 'cf' component is installed
        When
        - User attempts to trigger
        Then
        -  result status of trigger
        """
        mock_service = MagicMock()

        trigger_response = {
            'foo': 'bar'
        }

        mock_service.trigger.return_value = trigger_response
        mock_extension_client = cf_extension_client_fixture
        type(mock_extension_client.return_value).service = PropertyMock(
            return_value=mock_service)

        result = self.runner.invoke(cli, ['extension', 'cf', 'trigger-failover'])

        assert result.output == json.dumps(trigger_response, indent=4, sort_keys=True) + '\n'

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
            cli, ['extension', 'as3', 'remove'])
        assert "invalid choice: remove" in result.output
        assert result.exception
