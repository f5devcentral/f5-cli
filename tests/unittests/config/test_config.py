import click
from click.testing import CliRunner

from ...global_test_imports import pytest, MagicMock, call, PropertyMock

# Module under test
from f5cloudcli.config import ConfigClient


class TestConfigClient(object):
    """ Test Class: configure client """
    def test_read_exist_config(self, mocker):
        """ Read an existing config
        Given
        - Config file exists

        When
        - read_client() is invoked

        Then
        - A client object is returned
        """
        mock_client_object = MagicMock()
        mock_path_exist = mocker.patch("f5cloudcli.config.os.path.exists")
        mock_path_exist.return_value = True
        client = ConfigClient(client=mock_client_object)
        mock_path_is_file = mocker.patch("f5cloudcli.config.os.path.isfile")
        mock_path_is_file.return_value = True
        mock_pickle_load = mocker.patch("f5cloudcli.config.pickle.load")
        mock_pickle_load.return_value = mock_client_object
        with mocker.patch('f5cloudcli.config.open', new_callable=mocker.mock_open()) as m:
            result = client.read_client()
        assert result == mock_client_object
        mock_pickle_load.assert_called_once()

    def test_read_nonexist_config(self, mocker):
        """ Read a nonexisting config
        Given
        - Config file does not exist

        When
        - read_client() is invoked

        Then
        - Exception is thrown
        """
        mock_client_object = MagicMock()
        mock_path_exist = mocker.patch("f5cloudcli.config.os.path.exists")
        mock_path_exist.return_value = True
        client = ConfigClient(client=mock_client_object)
        mock_path_is_file = mocker.patch("f5cloudcli.config.os.path.isfile")
        mock_path_is_file.return_value = False
        with pytest.raises(click.exceptions.ClickException) as e:
            result = client.read_client()
        assert e.value.args[0] == "Command failed. You must login to BIG-IP!"

    def test_write_exist_config_directory(self, mocker):
        """ Write ConfigClient object to a config file in an existing directory
        Given
        - Config directory exist
        When
        - write_client() is invoked

        Then
        - A client object is written
        - Config file path is returned
        """
        mock_client_object = MagicMock()
        mock_path_exist = mocker.patch("f5cloudcli.config.os.path.exists")
        mock_path_exist.return_value = True
        client = ConfigClient(client=mock_client_object)
        mock_pickle_dump = mocker.patch("f5cloudcli.config.pickle.dump")
        with mocker.patch('f5cloudcli.config.open', new_callable=mocker.mock_open()) as m:
            result = client.write_client()
        mock_pickle_dump.assert_called_once()
        assert 'f5_cloud_cli/auth.file' in result

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
        client = ConfigClient(client=mock_client_object)
        mock_pickle_dump = mocker.patch("f5cloudcli.config.pickle.dump")
        with mocker.patch('f5cloudcli.config.open', new_callable=mocker.mock_open()) as m:
            result = client.write_client()
        mock_pickle_dump.assert_called_once()
        assert 'f5_cloud_cli/auth.file' in result
        mock_make_dir.assert_called_once()
