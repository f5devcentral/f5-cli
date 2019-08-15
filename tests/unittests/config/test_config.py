import click

from ...global_test_imports import pytest, MagicMock

# Module under test
from f5cloudcli.config import ConfigClient


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

    '''
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
    '''

    def test_write_nonexist_config_directory(self, mocker):
        """ Write ConfigClient object to a config file in a non-exist directory
        Given
        - Config directory does not exist
        When
        - write_client() is invoked

        Then
        - Config directory is created
        - A client object is written
        - Config file path is returned
        """
        mock_client_object = MagicMock()
        mock_path_exist = mocker.patch("f5cloudcli.config.os.path.exists")
        mock_path_exist.return_value = False
        mock_make_dir = mocker.patch("f5cloudcli.config.os.makedirs")
        client = ConfigClient()
        mock_pickle_dump = mocker.patch("f5cloudcli.config.pickle.dump")
        with mocker.patch('f5cloudcli.config.open', new_callable=mocker.mock_open()):
            result = client.write_client()
        mock_pickle_dump.assert_called_once()
        assert 'f5_cloud_cli/auth.file' in result
        mock_make_dir.assert_called_once()
