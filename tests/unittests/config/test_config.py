import click

from ...global_test_imports import pytest

# Module under test
from f5cloudcli.config import ConfigClient
from f5cloudcli import constants


class TestConfigClient(object):
    """ Test Class: configure client """

    def test_read_exist_auth(self, mocker):
        """ Read an existing Auth file
        Given
        - Auth file exists

        When
        - read_auth() is invoked

        Then
        - The appropriate credentials are returned
        """
        mock_path_exist = mocker.patch("f5cloudcli.config.os.path.exists")
        mock_path_exist.return_value = True
        client = ConfigClient()
        mock_path_is_file = mocker.patch("f5cloudcli.config.os.path.isfile")
        mock_path_is_file.return_value = True
        mock_json_load = mocker.patch("f5cloudcli.config.json.load")

        group_name = 'CLOUD_SERVICES'
        mock_json_load.return_value = {
            group_name: {'username': 'me@home.com', 'password': 'pass123'}}
        with mocker.patch('f5cloudcli.config.open', new_callable=mocker.mock_open()):
            result = client.read_auth(group_name)
        assert result == mock_json_load.return_value[group_name]
        mock_json_load.assert_called_once()

    def test_read_nonexist_auth(self, mocker):
        """ Attempt to read an Auth file that does not exist
        Given
        - Auth file does not exist

        When
        - read_auth() is invoked

        Then
        - Exception is thrown
        """
        mock_path_exist = mocker.patch("f5cloudcli.config.os.path.exists")
        mock_path_exist.return_value = True
        client = ConfigClient()
        mock_path_is_file = mocker.patch("f5cloudcli.config.os.path.isfile")
        mock_path_is_file.return_value = False
        with pytest.raises(click.exceptions.ClickException) as error:
            client.read_auth('temp')
        assert error.value.args[0] == "Command failed. You must configure BIG-IP auth!"

    def test_write_exist_config_directory(self, mocker):
        """ Write credentials to Auth file in an existing directory
        Given
        - Config directory exist
        - Auth file does not exist

        When
        - store_auth() is invoked

        Then
        - The credentials are written to the Auth file
        """
        mock_path_exist = mocker.patch("f5cloudcli.config.os.path.exists")
        mock_path_exist.return_value = True
        client = ConfigClient()
        mock_path_isfile = mocker.patch("f5cloudcli.config.os.path.isfile")
        mock_path_isfile.return_value = False
        mock_json_dump = mocker.patch("f5cloudcli.config.json.dump")
        with mocker.patch('f5cloudcli.config.open', new_callable=mocker.mock_open()):
            client.store_auth()
            mock_json_dump.assert_called_once()

    def test_write_to_existing_auth_file(self, mocker):
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
        mock_path_exist = mocker.patch("f5cloudcli.config.os.path.exists")
        mock_path_exist.return_value = True
        bigip_auth = {
            'username': 'root',
            'password': '123',
            'host': '1.2.3.4'
        }
        client = ConfigClient(
            group_name=constants.BIGIP_GROUP_NAME,
            auth=bigip_auth)
        mock_path_isfile = mocker.patch("f5cloudcli.config.os.path.isfile")
        mock_path_isfile.return_value = True
        mock_json_load = mocker.patch("f5cloudcli.config.json.load")
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

    def test_write_nonexist_config_directory(self, mocker):
        """ Write Auth file into a non-exist directory
        Given
        - Config directory does not exist

        When
        - store_auth() is invoked

        Then
        - Config directory is created
        - Auth file is written to disk
        """

        mock_path_exist = mocker.patch("f5cloudcli.config.os.path.exists")
        mock_path_exist.return_value = False
        mock_make_dir = mocker.patch("f5cloudcli.config.os.makedirs")
        auth = {
            'username': 'me@home.com',
            'password': '1234'
        }
        client = ConfigClient(
            group_name=constants.CLOUD_SERVICES_GROUP_NAME,
            auth=auth
        )
        mock_path_is_file = mocker.patch("f5cloudcli.config.os.path.isfile")
        mock_path_is_file.return_value = False
        mock_json_dump = mocker.patch("f5cloudcli.config.json.dump")
        with mocker.patch('f5cloudcli.config.open', new_callable=mocker.mock_open()):
            client.store_auth()
        mock_json_dump.assert_called_once()
        mock_make_dir.assert_called_once()
        assert mock_json_dump.call_args_list[0][0][0][constants.CLOUD_SERVICES_GROUP_NAME] == auth
