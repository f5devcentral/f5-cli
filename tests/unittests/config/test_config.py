""" Test config """

import copy
import click

from f5cli.config import AuthConfigurationClient
from f5cli import constants

from ...global_test_imports import pytest

# TEST CONSTANTS
TYPICAL_AUTH_CONTENTS = [
    {
        'name': 'cs1',
        'authentication-type': constants.AUTHENTICATION_PROVIDERS['CLOUD_SERVICES'],
        'default': True
    },
    {
        'name': 'bigip1',
        'authentication-type': constants.AUTHENTICATION_PROVIDERS['BIGIP'],
        'default': False
    },
    {
        'name': 'cs2',
        'authentication-type': constants.AUTHENTICATION_PROVIDERS['CLOUD_SERVICES'],
        'default': False
    },
    {
        'name': 'bigip2',
        'authentication-type': constants.AUTHENTICATION_PROVIDERS['BIGIP'],
        'default': True
    },
    {
        'name': 'bigip3',
        'host': '123',
        'user': 'user1',
        'password': 'password1',
        'authentication-type': constants.AUTHENTICATION_PROVIDERS['BIGIP'],
        'default': False
    }
]


class TestAuthConfigurationClient(object):
    """ Test Class: configure client """

    @staticmethod
    @pytest.fixture
    def yaml_load_fixture_core(mocker):
        """ PyTest fixture returning mocked json load() """
        mock_yaml_load = mocker.patch('f5cli.config.core.yaml.load')
        return mock_yaml_load

    @staticmethod
    @pytest.fixture
    def yaml_load_fixture_auth(mocker):
        """ PyTest fixture returning mocked json load() """
        mock_yaml_load = mocker.patch('f5cli.config.auth.yaml.load')
        return mock_yaml_load

    @staticmethod
    @pytest.fixture
    def os_path_exists_fixture(mocker):
        """ PyTest fixture returning mocked os.path.exists object """
        mock_exists = mocker.patch('f5cli.config.core.os.path.exists')
        mock_exists.return_value = True
        return mock_exists

    @staticmethod
    @pytest.fixture
    def os_path_isfile_fixture(mocker):
        """ PyTest fixture returning mocked os.path.isfile object """
        mock_isfile = mocker.patch('f5cli.config.core.os.path.isfile')
        mock_isfile.return_value = True
        return mock_isfile

    @staticmethod
    def test_read_exist_auth(mocker,
                             yaml_load_fixture_auth,
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
        client = AuthConfigurationClient()
        yaml_load_fixture_auth.return_value = [
            {'username': 'me@home.com',
             'authentication-type': 'cloud-services',
             'password': 'pass123',
             'default': True
             }]

        with mocker.patch('f5cli.config.auth.open', new_callable=mocker.mock_open()):
            result = client.read_auth('cloud-services')
        assert result == yaml_load_fixture_auth.return_value[0]
        yaml_load_fixture_auth.assert_called_once()

    @staticmethod
    def test_read_nonexist_auth(os_path_exists_fixture,  # pylint: disable=unused-argument
                                os_path_isfile_fixture):  # pylint: disable=unused-argument
        """ Attempt to read an Auth file that does not exist
        Given
        - Auth file does not exist

        When
        - read_auth() is invoked

        Then
        - Exception is thrown
        """
        client = AuthConfigurationClient()
        mock_path_is_file = os_path_isfile_fixture
        mock_path_is_file.return_value = False

        with pytest.raises(click.exceptions.ClickException) as error:
            client.read_auth('temp')
        assert error.value.args[0] == "Command failed. " \
                                      "You must configure a default authentication for temp!"

    @staticmethod
    def test_read_auth_without_key(mocker,
                                   yaml_load_fixture_auth,
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
        client = AuthConfigurationClient()

        group_name = 'CLOUD_SERVICES'
        yaml_load_fixture_auth.return_value = [
            {'name': 'temp', 'username': 'me@home.com', 'type': 'BIGIP', 'password': 'pass123'}
        ]

        with pytest.raises(click.exceptions.ClickException) as error:
            with mocker.patch('f5cli.config.auth.open', new_callable=mocker.mock_open()):
                client.read_auth(group_name)
        assert error.value.args[0] == f"Command failed. You must configure a default " \
                                      f"authentication for {group_name}!"

    @staticmethod
    def test_write_exist_config_directory(mocker,
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
        client = AuthConfigurationClient(auth={'name': 'blah'})
        mock_path_isfile = os_path_isfile_fixture
        mock_path_isfile.return_value = False
        mock_yaml_safe_dump = mocker.patch("f5cli.config.core.yaml.safe_dump")
        with mocker.patch('f5cli.config.core.open', new_callable=mocker.mock_open()):
            client.store_auth('create')
        mock_yaml_safe_dump.assert_called_once()

    @staticmethod
    def test_write_to_existing_auth_file(mocker,
                                         yaml_load_fixture_auth,
                                         os_path_exists_fixture,  # pylint: disable=unused-argument
                                         os_path_isfile_fixture):  # pylint: disable=unused-argument
        """ Write credentials to an existing Auth file
        Given
        - Config directory exists
        - Auth file exists with contents
        - Create action is invoked

        When
        - store_auth('create') is invoked

        Then
        - The existing Auth file is read
        - The Auth file is overwritten, containing merged credentials
        """
        bigip_auth = {
            'name': 'bigip_auth',
            'username': 'root',
            'password': '123',
            'host': '1.2.3.4',
            'type': 'BIGIP',
            'default': 'true'
        }
        client = AuthConfigurationClient(auth=bigip_auth)
        cloud_services_auth = {'name': 'cloud_services_auth',
                               'username': 'me@home.com',
                               'password': '123',
                               'type': 'CLOUD_SERVICES',
                               'default': 'true'}
        yaml_load_fixture_auth.return_value = [cloud_services_auth]

        mock_yaml_safe_dump = mocker.patch("f5cli.config.core.yaml.safe_dump")
        with mocker.patch('f5cli.config.core.open', new_callable=mocker.mock_open()):
            client.store_auth('create')
        mock_yaml_safe_dump.assert_called_once()
        mock_yaml_dump_wrote = mock_yaml_safe_dump.call_args_list[0][0][0]
        assert mock_yaml_dump_wrote[0] == cloud_services_auth
        assert mock_yaml_dump_wrote[1] == bigip_auth

    @staticmethod
    def test_write_nonexist_config_directory(mocker,
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

        mock_make_dir = mocker.patch("f5cli.config.core.os.makedirs")
        auth = {
            'name': 'blah',
            'username': 'me@home.com',
            'password': '1234'
        }
        client = AuthConfigurationClient(
            auth=auth
        )

        mock_yaml_safe_dump = mocker.patch("f5cli.config.core.yaml.safe_dump")
        with mocker.patch('f5cli.config.core.open', new_callable=mocker.mock_open()):
            client.store_auth('create')
        mock_yaml_safe_dump.assert_called_once()
        mock_make_dir.assert_called_once()
        assert mock_yaml_safe_dump.call_args_list[0][0][0][0] == auth

    @staticmethod
    def test_create_pre_existing_account(mocker,
                                         yaml_load_fixture_auth,
                                         os_path_exists_fixture,  # pylint: disable=unused-argument
                                         os_path_isfile_fixture):  # pylint: disable=unused-argument
        """ Attempt to perform crate auth account when an auth
            account of the same name has already been configured
            Given
            - Auth file containing multiple accounts

            When
            - store_auth('create') is invoked with auth details

            Then
            - store_auth raises an exception when trying to create a pre-existing account
        """
        new_account = {
            'name': 'cs1'
        }
        copy_typical_auth_contents = copy.deepcopy(TYPICAL_AUTH_CONTENTS)
        yaml_load_fixture_auth.return_value = copy_typical_auth_contents
        client = AuthConfigurationClient(auth=new_account)
        with pytest.raises(click.exceptions.ClickException) as error:
            with mocker.patch('f5cli.config.core.open', new_callable=mocker.mock_open()):
                client.store_auth('create')
        assert error.value.args[0] == f"Create command failed. " \
                                      f"A account of cs1 name already exists."

    @staticmethod
    def test_update_no_auth_file(mocker,
                                 yaml_load_fixture_auth,
                                 os_path_exists_fixture,  # pylint: disable=unused-argument
                                 os_path_isfile_fixture):  # pylint: disable=unused-argument
        """ Attempt to perform update auth account when no auth accounts have been configured yet
            Given
            - No Auth file

            When
            - store_auth('update') is invoked with auth details

            Then
            - store_auth raises an exception
        """
        new_account = {
            'name': 'bigip4'
        }
        yaml_load_fixture_auth.return_value = None
        client = AuthConfigurationClient(auth=new_account)
        with pytest.raises(click.exceptions.ClickException) as error:
            with mocker.patch('f5cli.config.auth.open', new_callable=mocker.mock_open()):
                client.store_auth('update')
            assert error.value.args[0] == f"Update command failed. " \
                                          f"No accounts have been configured yet"

    @staticmethod
    def test_update_non_existing_account(mocker,
                                         yaml_load_fixture_auth,
                                         os_path_exists_fixture,  # pylint: disable=unused-argument
                                         os_path_isfile_fixture):  # pylint: disable=unused-argument
        """ Update non-existing account
            Given
            - Auth file containing multiple accounts

            When
            - store_auth('update') is invoked with auth details

            Then
            - store_auth raises an exception when trying to update a non existing account
        """
        new_account = {
            'name': 'bigip4'
        }
        copy_typical_auth_contents = copy.deepcopy(TYPICAL_AUTH_CONTENTS)
        yaml_load_fixture_auth.return_value = copy_typical_auth_contents
        client = AuthConfigurationClient(auth=new_account)
        with pytest.raises(click.exceptions.ClickException) as error:
            with mocker.patch('f5cli.config.auth.open', new_callable=mocker.mock_open()):
                client.store_auth('update')
        assert error.value.args[0] == f"Update command failed." \
                                      f" A account of bigip4 name does not exist."

    @staticmethod
    def test_update_existing_account(mocker,
                                     yaml_load_fixture_auth,
                                     os_path_exists_fixture,  # pylint: disable=unused-argument
                                     os_path_isfile_fixture):  # pylint: disable=unused-argument
        """ Update an existing account
            Given
            - Auth file contains multiple accounts
            - The account name to the updated exists in the auth file

            When
            - store_auth('update')

            Then
            - Auth file is updated with the new account and the default
              account for the specific authentication provider is updated
        """

        new_account = {
            'name': 'bigip3',
            'host': 'host2',
            'default': True
        }

        mock_yaml_safe_dump = mocker.patch("f5cli.config.core.yaml.safe_dump")
        copy_typical_auth_contents = copy.deepcopy(TYPICAL_AUTH_CONTENTS)
        yaml_load_fixture_auth.return_value = copy_typical_auth_contents
        client = AuthConfigurationClient(auth=new_account)
        with mocker.patch('f5cli.config.core.open', new_callable=mocker.mock_open()):
            client.store_auth('update')
        mock_yaml_safe_dump.assert_called_once()
        mock_yaml_dump_wrote = mock_yaml_safe_dump.call_args_list[0][0][0]
        assert not mock_yaml_dump_wrote[3].get('default')
        returned_account = mock_yaml_dump_wrote[4]
        expected_result = TYPICAL_AUTH_CONTENTS[4]
        assert returned_account.get('host') == new_account.get('host')
        assert returned_account.get('default') == new_account.get('default')
        assert returned_account.get('user') == expected_result.get('user')
        assert returned_account.get('password') == expected_result.get('password')
        assert returned_account.get('type') == expected_result.get('type')

    @staticmethod
    def test_delete_non_default(mocker,
                                yaml_load_fixture_auth,
                                os_path_exists_fixture,  # pylint: disable=unused-argument
                                os_path_isfile_fixture):  # pylint: disable=unused-argument
        """ Delete a account that is not configured as a default account
            Given
            - Auth file contains multiple accounts
            - The account name to be deleted exists in the auth file and is not a default account

            When
            - delete_auth(account_name) is called

            Then
            - Auth file is updated
        """

        mock_yaml_safe_dump = mocker.patch("f5cli.config.core.yaml.safe_dump")
        copy_typical_auth_contents = copy.deepcopy(TYPICAL_AUTH_CONTENTS)
        yaml_load_fixture_auth.return_value = copy_typical_auth_contents
        client = AuthConfigurationClient()
        with mocker.patch('f5cli.config.core.open', new_callable=mocker.mock_open()):
            client.delete_auth('bigip3')
        mock_yaml_safe_dump.assert_called_once()
        mock_yaml_dump_wrote = mock_yaml_safe_dump.call_args_list[0][0][0]
        assert mock_yaml_dump_wrote[3].get('default')
        assert len(mock_yaml_dump_wrote) == 4

    @staticmethod
    def test_deleting_default_account(mocker,
                                      yaml_load_fixture_auth,
                                      os_path_exists_fixture,  # pylint: disable=unused-argument
                                      os_path_isfile_fixture):  # pylint: disable=unused-argument
        """ Delete a account that is configiured as a default account
            Given
            - Auth file contains multiple accounts
            - The account name to be deleted exists in the auth file and is a default account

            When
            - delete_auth(account_name) is called

            Then
            - The next available account of the same authentication provider
              is updated to be the new default account and the specified account is removed
        """

        mock_yaml_safe_dump = mocker.patch("f5cli.config.core.yaml.safe_dump")
        copy_typical_auth_contents = copy.deepcopy(TYPICAL_AUTH_CONTENTS)
        yaml_load_fixture_auth.return_value = copy_typical_auth_contents
        client = AuthConfigurationClient()
        with mocker.patch('f5cli.config.core.open', new_callable=mocker.mock_open()):
            client.delete_auth('bigip2')
        mock_yaml_safe_dump.assert_called_once()
        mock_yaml_dump_wrote = mock_yaml_safe_dump.call_args_list[0][0][0]
        assert mock_yaml_dump_wrote[1].get('default')
        assert mock_yaml_dump_wrote[3].get('name') == 'bigip3'

    @staticmethod
    def test_deleting_non_exist_account(mocker,
                                        yaml_load_fixture_auth,
                                        os_path_exists_fixture,  # pylint: disable=unused-argument
                                        os_path_isfile_fixture):  # pylint: disable=unused-argument
        """ Delete a account that is hasn't been configured
            Given
            - Auth file contains multiple accounts
            - The account name to be deleted that does not exist in the auth file

            When
            - delete_auth(account_name) is called

            Then
            - an exception should be thrown
        """

        copy_typical_auth_contents = copy.deepcopy(TYPICAL_AUTH_CONTENTS)
        yaml_load_fixture_auth.return_value = copy_typical_auth_contents
        client = AuthConfigurationClient()
        with pytest.raises(click.exceptions.ClickException) as error:
            with mocker.patch('f5cli.config.auth.open', new_callable=mocker.mock_open()):
                client.delete_auth('blah')
            assert error.value.args[0] == f"Delete command failed. No account named blah found"

    @staticmethod
    def test_list_accounts(mocker,
                           yaml_load_fixture_auth,
                           os_path_exists_fixture,  # pylint: disable=unused-argument
                           os_path_isfile_fixture):  # pylint: disable=unused-argument
        """ List all accounts that have been configured
            Given
            - Auth file contains multiple accounts

            When
            - list_auth is called

            Then
            - All the configured account credentials are listed
        """

        copy_typical_auth_contents = copy.deepcopy(TYPICAL_AUTH_CONTENTS)
        yaml_load_fixture_auth.return_value = copy_typical_auth_contents
        client = AuthConfigurationClient()
        with mocker.patch('f5cli.config.core.open', new_callable=mocker.mock_open()):
            result = client.list_auth()
        assert len(result) == 5
        for index in range(0, 4):
            assert result[index].get('name') \
                   == TYPICAL_AUTH_CONTENTS[index].get('name')
