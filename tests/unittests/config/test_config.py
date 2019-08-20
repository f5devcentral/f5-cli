import click

from ...global_test_imports import pytest

# Module under test
from f5cloudcli.config import ConfigClient
from f5cloudcli import constants


class TestConfigClient(object):
    """ Test Class: configure client """

    @pytest.fixture
    def json_load_fixture(self, mocker):
        """ PyTest fixture returning mocked json load() """
        mock_json_load = mocker.patch('f5cloudcli.config.json.load')
        return mock_json_load

    @pytest.fixture
    def os_path_exists_fixture(self, mocker):
        """ PyTest fixture returning mocked os.path.exists object """
        mock_exists = mocker.patch('f5cloudcli.config.os.path.exists')
        mock_exists.return_value = True
        return mock_exists

    @pytest.fixture
    def os_path_isfile_fixture(self, mocker):
        """ PyTest fixture returning mocked os.path.isfile object """
        mock_isfile = mocker.patch('f5cloudcli.config.os.path.isfile')
        mock_isfile.return_value = True
        return mock_isfile

    def test_read_exist_auth(self,
                             mocker,
                             json_load_fixture,
                             os_path_exists_fixture,  # pylint: disable=unused-argument
                             os_path_isfile_fixture):  # pylint: disable=unused-argument
        """ Read an existing Auth file
        Given
        - Auth file exists

        When
        - read_auth() is invoked

        Then
        - The appropriate credentials are returned
        """

        client = ConfigClient()
        group_name = 'CLOUD_SERVICES'
        mock_json_load = json_load_fixture
        mock_json_load.return_value = {
            group_name: {'username': 'me@home.com', 'password': 'pass123'}
        }

        with mocker.patch('f5cloudcli.config.open', new_callable=mocker.mock_open()):
            result = client.read_auth(group_name)
        assert result == mock_json_load.return_value[group_name]
        mock_json_load.assert_called_once()

    def test_read_nonexist_auth(self,
                                os_path_exists_fixture,  # pylint: disable=unused-argument
                                os_path_isfile_fixture):  # pylint: disable=unused-argument
        """ Attempt to read an Auth file that does not exist
        Given
        - Auth file does not exist

        When
        - read_auth() is invoked

        Then
        - Exception is thrown
        """
        client = ConfigClient()
        mock_path_is_file = os_path_isfile_fixture
        mock_path_is_file.return_value = False

        with pytest.raises(click.exceptions.ClickException) as error:
            client.read_auth('temp')
        assert error.value.args[0] == "Command failed. You must configure authentication for temp!"

    def test_read_auth_without_key(self,
                                   mocker,
                                   json_load_fixture,
                                   os_path_exists_fixture,  # pylint: disable=unused-argument
                                   os_path_isfile_fixture):  # pylint: disable=unused-argument
        """ Attempt to read an Auth file that exists, but does not contain the required key
        Given
        - Auth file does exist
        - 'Group' key does not exist

        When
        - read_auth() is invoked

        Then
        - Exception is thrown
        """
        client = ConfigClient()
        mock_json_load = json_load_fixture

        group_name = 'CLOUD_SERVICES'
        mock_json_load.return_value = {
            group_name: {'username': 'me@home.com', 'password': 'pass123'}}

        with pytest.raises(click.exceptions.ClickException) as error:
            with mocker.patch('f5cloudcli.config.open', new_callable=mocker.mock_open()):
                client.read_auth('temp')
        assert error.value.args[0] == "Command failed. You must configure authentication for temp!"

    def test_write_exist_config_directory(self,
                                          mocker,
                                          os_path_exists_fixture,  # pylint: disable=unused-argument
                                          os_path_isfile_fixture):
        """ Write credentials to Auth file in an existing directory
        Given
        - Config directory exist
        - Auth file does not exist

        When
        - store_auth() is invoked

        Then
        - The credentials are written to the Auth file
        """
        client = ConfigClient()
        mock_path_isfile = os_path_isfile_fixture
        mock_path_isfile.return_value = False
        mock_json_dump = mocker.patch("f5cloudcli.config.json.dump")
        with mocker.patch('f5cloudcli.config.open', new_callable=mocker.mock_open()):
            client.store_auth()
            mock_json_dump.assert_called_once()

    def test_write_to_existing_auth_file(self,
                                         mocker,
                                         json_load_fixture,
                                         os_path_exists_fixture,  # pylint: disable=unused-argument
                                         os_path_isfile_fixture):  # pylint: disable=unused-argument
        """ Write credentials to an existing Auth file
        Given
        - Config directory exists
        - Auth file exists with contents

        When
        - store_auth() is invoked

        Then
        - The existing Auth file is read
        - The Auth file is overwritten, containing merged credentials
        """
        bigip_auth = {
            'username': 'root',
            'password': '123',
            'host': '1.2.3.4'
        }
        client = ConfigClient(
            group_name=constants.BIGIP_GROUP_NAME,
            auth=bigip_auth)
        mock_json_load = json_load_fixture
        cloud_services_auth = {'username': 'me@home.com', 'password': '123'}
        mock_json_load.return_value = {
            'CLOUD_SERVICES': cloud_services_auth
        }

        mock_json_dump = mocker.patch("f5cloudcli.config.json.dump")
        with mocker.patch('f5cloudcli.config.open', new_callable=mocker.mock_open()):
            client.store_auth()
            mock_json_dump.assert_called_once()
        mock_json_dump_wrote = mock_json_dump.call_args_list[0][0][0]
        assert mock_json_dump_wrote[constants.BIGIP_GROUP_NAME] == bigip_auth
        assert mock_json_dump_wrote[constants.CLOUD_SERVICES_GROUP_NAME] == cloud_services_auth

    def test_write_nonexist_config_directory(self,
                                             mocker,
                                             os_path_exists_fixture,
                                             os_path_isfile_fixture):
        """ Write Auth file into a non-exist directory
        Given
        - Config directory does not exist

        When
        - store_auth() is invoked

        Then
        - Config directory is created
        - Auth file is written to disk
        """

        mock_path_exist = os_path_exists_fixture
        mock_path_exist.return_value = False
        mock_path_is_file = os_path_isfile_fixture
        mock_path_is_file.return_value = False

        mock_make_dir = mocker.patch("f5cloudcli.config.os.makedirs")
        auth = {
            'username': 'me@home.com',
            'password': '1234'
        }
        client = ConfigClient(
            group_name=constants.CLOUD_SERVICES_GROUP_NAME,
            auth=auth
        )

        mock_json_dump = mocker.patch("f5cloudcli.config.json.dump")
        with mocker.patch('f5cloudcli.config.open', new_callable=mocker.mock_open()):
            client.store_auth()
        mock_json_dump.assert_called_once()
        mock_make_dir.assert_called_once()
        assert mock_json_dump.call_args_list[0][0][0][constants.CLOUD_SERVICES_GROUP_NAME] == auth
