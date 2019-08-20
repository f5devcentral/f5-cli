"""Configuration module for the CLI """

import os
import json
import click

import f5cloudcli.constants as constants

F5_AUTH_FILE_PATH = constants.F5_AUTH_FILE
F5_CLI_DIR = constants.F5_CLI_DIR

class ConfigClient():
    """ A class used to store any required authentication
    or configuration data used by the F5 Cloud CLI

    It will store the required credentials and connection information
    needed by the CLI groups (BigIP and Cloud Services), and persist
    that data to the F5 CLI configuration directory

    Attributes
    ----------

    Methods
    -------
    store_auth()
        See method documentation for more details
    read_auth()
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
        group_name: str
            the CLI command 'group' to store credentials under
        auth: dict
            dict of the required authentication credentials

        Returns
        -------
        None
        """
        self.group_name = kwargs.pop('group_name', '')
        self.auth = kwargs.pop('auth', '')

        # create config directory
        self._create_dir(F5_CLI_DIR)

    @staticmethod
    def _create_dir(_dir):
        """Create directory (recursively)

        Parameters
        ----------
        dir, str
            a string containing the directory to create

        Returns
        -------
        None
        """

        if not os.path.exists(_dir):
            os.makedirs(_dir)

    def store_auth(self):
        """ Persists the current authentication data to the configuration directory

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        auth_contents = {}
        if os.path.isfile(F5_AUTH_FILE_PATH):
            with open(F5_AUTH_FILE_PATH) as file:
                try:
                    auth_contents.update(json.load(file))
                except json.decoder.JSONDecodeError:
                    pass

        # update() auth_contents to 'merge' new credentials with existing credentials data
        auth_contents.update(
            {self.group_name: self.auth}
        )

        with open(F5_AUTH_FILE_PATH, 'w') as file:
            json.dump(auth_contents, file)

    def read_auth(self, group_name): # pylint: disable=no-self-use
        """ Used by the CLI commands to read the persisted credentials, when the CLI commands need
            to generate a new ManagementClient

        Parameters
        ----------
        group_name, str
            a string containing the CLI 'group' name to use as the credentials file key

        Returns
        -------
        dict
            a dictionary containing the credentials for the provided CLI group name
        """

        err_msg = f"Command failed. You must configure authentication for {group_name}!"

        if os.path.isfile(F5_AUTH_FILE_PATH):
            with open(F5_AUTH_FILE_PATH) as file:
                try:
                    auth = json.load(file)
                    if group_name not in auth:
                        raise click.ClickException(err_msg)
                    return auth[group_name]
                except json.decoder.JSONDecodeError:
                    raise click.ClickException(
                        f"Command failed. Unable to read {F5_AUTH_FILE_PATH} contents")

        raise click.ClickException(err_msg)
