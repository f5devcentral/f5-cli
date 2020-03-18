"""Authentication Configuration module for the CLI """

import os
import yaml
import click

import f5cli.constants as constants
import f5cli.utils.core as utils


class AuthConfigurationClient:
    """ A class used to interact with stateful authentication information

    Note: The backend storage method is simply a YAML file in
    the F5 CLI home directory (auth.yaml)

    Attributes
    ----------

    Methods
    -------
    store_auth()
        See method documentation for more details
    read_auth()
        See method documentation for more details
    delete_auth()
        See method documentation for more details
    list_auth()
        See method documentation for more details
    """

    def __init__(self, **kwargs):
        """Class initialization

        Parameters
        ----------
        **kwargs:
            optional keyword arguments

        Keyword Arguments
        -----------------
        auth: list
            list of the required authentication credentials

        Returns
        -------
        None
        """
        self.auth = kwargs.pop('auth', '')
        # create config directory
        self._create_dir(constants.F5_CLI_DIR)

    @staticmethod
    def _create_dir(_dir):
        """Create directory (recursively)

        Parameters
        ----------
        _dir: str
            a string containing the directory to create

        Returns
        -------
        None
        """

        if not os.path.exists(_dir):
            os.makedirs(_dir)

    @staticmethod
    def _load_auth_contents():
        """Loads auth file and returns a list with the contents

        Parameters
        ----------
        None

        Returns
        -------
        list
            a list containing the authentication accounts from auth file
        """
        auth_contents = []
        if os.path.isfile(constants.F5_AUTH_FILE):
            with open(constants.F5_AUTH_FILE) as file:
                auth_contents = yaml.safe_load(file)
        return auth_contents

    @staticmethod
    def _dump_auth_content_to_file(auth_contents):
        """Dumps auth file and returns a list with the contents

        Parameters
        ----------
        auth_contents: list
            a list containing the authentication accounts to convert to auth file

        Returns
        -------
        None
        """
        try:
            utils.write_file(constants.F5_AUTH_FILE, auth_contents)
        except IOError as error:
            raise click.ClickException(
                f"Unable to open auth file. Error returned {error}.")

    @staticmethod
    def _get_default_auth_contents(authentication_provider, auth_contents):
        """Find the default account for a specific authentication provider

        Parameters
        ----------
        authentication_provider: str
            the type of authentication account to return
        auth_contents: list
            list containing authentication accounts

        Returns
        -------
        list
            a list containing the default authentication account
        """
        if auth_contents:
            for account in auth_contents:
                if account.get('default') and \
                        account.get('authentication-type') == authentication_provider:
                    return account
        return None

    @staticmethod
    def _set_default_auth_contents(account_name, auth_contents):
        """Sets the provided account name as the default account

        Parameters
        ----------
        account_name: str
            the name of the account that is to be set as the default
        auth_contents: list
            list containing authentication accounts

        Returns
        -------
        list
            a list containing the updated authentication accounts
        """
        new_default_account = {}
        auth_contents = auth_contents or []
        for account in auth_contents:
            if account.get('name') == account_name:
                account.update({'default': True})
                new_default_account = account
                break
        if new_default_account:
            for account in auth_contents:
                if account.get('name') != account_name and account.get('authentication-type') \
                        == new_default_account.get('authentication-type'):
                    account.update({'default': False})
        return auth_contents

    def store_auth(self, action):
        """ Persists the current authentication data to the configuration directory

        Parameters
        ----------
        action: str
            the action that invoked store_auth, could either be 'create' or 'update'

        Returns
        -------
        None
        """

        auth_contents = []
        try:
            auth_contents = self._load_auth_contents()
        except TypeError:
            pass
        if action == 'create':
            if not auth_contents:
                auth_contents = [self.auth]
            else:
                fetched_account = self._get_account(self.auth.get('name'), auth_contents)
                if fetched_account is not None:
                    raise click.ClickException(f"Create command failed. "f"A account of "
                                               f"{self.auth.get('name')} name already exists.")
                auth_contents.append(self.auth)
            # If this is the first account of that type to be configured, mark it as default
            if self.auth.get('default') or \
                    self._get_default_auth_contents(self.auth.get('authentication-type'),
                                                    auth_contents) is None:
                auth_contents = self._set_default_auth_contents(self.auth.get('name'),
                                                                auth_contents)
        else:
            if not auth_contents:
                raise click.ClickException(
                    f"Update command failed. No authentication accounts have been configured yet.")
            fetched_account = self._get_account(self.auth.get('name'), auth_contents)
            if not fetched_account:
                raise click.ClickException(f"Update command failed. A account of "
                                           f"{self.auth.get('name')} name does not exist.")
            for key in self.auth.keys():
                if self.auth.get(key) is not None:
                    fetched_account.update({key: self.auth.get(key)})
        # Set the newly created/updated account as default if specified
        if self.auth.get('default'):
            auth_contents = self._set_default_auth_contents(
                self.auth.get('name'), auth_contents)
        self._dump_auth_content_to_file(auth_contents)

    @staticmethod
    def _get_account(account_name, auth_contents):
        """ Used by the CLI commands to read the default persisted credentials,
            when the CLI commands need to generate a new ManagementClient

        Parameters
        ----------
        account_name: str
            name of the account to be fetched from auth_contents
        auth_contents: list
            list containing authentication accounts

        Returns
        -------
        dict
            the dict account details
        """
        for auth_account in auth_contents:
            if auth_account.get('name') == account_name:
                return auth_account
        return None

    def read_auth(self, group_name):
        """ Used by the CLI commands to read the default persisted credentials,
            when the CLI commands need to generate a new ManagementClient

        Parameters
        ----------
        group_name: str
            a string containing the CLI 'group' name to use as the credentials file key

        Returns
        -------
        list
            a list containing the default credentials for the provided CLI group name
        """

        err_msg = f"Command failed. You must configure a default authentication for {group_name}!"

        try:
            auth_contents = self._load_auth_contents()
        except Exception:
            raise click.ClickException(
                f"Command failed. Unable to read {constants.F5_AUTH_FILE} contents")

        account = self._get_default_auth_contents(group_name, auth_contents)
        if not account:
            raise click.ClickException(err_msg)
        return account

    def delete_auth(self, account_name):
        """ Used by the CLI commands to delete the persisted credentials, given the account_name.
        If a default authentication account is deleted,
        the next available account for the same type becomes the default auth account

        Parameters
        ----------
        account_name: str
            the name of the account to be deleted

        Returns
        -------
        None

        """

        try:
            auth_contents = self._load_auth_contents()
        except Exception:
            raise click.ClickException(
                f"Delete command failed. Unable to read {constants.F5_AUTH_FILE} contents")

        fetched_account = self._get_account(account_name, auth_contents)
        if fetched_account is None:
            raise click.ClickException(f"Delete command failed."
                                       f" No account named ${account_name} found")

        # Set the next available account of the same type as default
        if fetched_account.get('default'):
            for account in auth_contents:
                if fetched_account.get('name') != account.get('name') and \
                        fetched_account.get('authentication-type') == \
                        account.get('authentication-type'):
                    self._set_default_auth_contents(account.get('name'), auth_contents)
                    break
        auth_contents.remove(fetched_account)
        self._dump_auth_content_to_file(auth_contents)

    def list_auth(self):
        """ Used by the CLI commands to read all the persisted credentials

        Parameters
        ----------
        None

        Returns
        -------
        list
            a list containing all account credentials

        """

        try:
            auth_contents = self._load_auth_contents()
        except Exception:
            raise click.ClickException(
                f"Command failed. Unable to read {constants.F5_AUTH_FILE} contents")
        return auth_contents
