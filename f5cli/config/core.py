"""Configuration module for the CLI """

import os
import yaml
import click

import f5cli.constants as constants
import f5cli.utils.core as utils


class ConfigurationClient:
    """ A class used to interfact with stateful configuration

    Note: The backend storage method is simply a YAML file in
    the F5 CLI home directory (config.yaml)

    Attributes
    ----------
    None

    Methods
    -------
    list()
        See method documentation for more details
    create_or_update()
        See method documentation for more details
    """

    def __init__(self):
        """Class initialization

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # create parent directory (as needed)
        self._create_directory(constants.F5_CLI_DIR)

    @staticmethod
    def _create_directory(path):
        """Create directory (recursively)

        Parameters
        ----------
        path: str
            a string containing the directory to create

        Returns
        -------
        None
        """

        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def _load_content():
        """Loads content from backend

        Note: If the backend does not exist an empty
        dictionary will be returned

        Parameters
        ----------
        None

        Returns
        -------
        dict
            a dict containing the loaded contents
        """

        contents = {}
        if os.path.isfile(constants.F5_CONFIG_FILE):
            with open(constants.F5_CONFIG_FILE) as file:
                contents = yaml.safe_load(file) or {}
        return contents

    @staticmethod
    def _save_content(content):
        """Save content to backend

        Parameters
        ----------
        content: dict
            the contents to save

        Returns
        -------
        None
        """
        try:
            utils.write_file(constants.F5_CONFIG_FILE, content)
        except IOError as error:
            raise click.ClickException(f"Unable to save contents: {error}.")

    def list(self):
        """ List content

        Parameters
        ----------
        None

        Returns
        -------
        dict
        """

        return self._load_content()

    def create_or_update(self, content):
        """ Create or update content

        Parameters
        ----------
        content: dict
            the content to create or update

        Returns
        -------
        None
        """

        current_content = self._load_content()
        current_content.update(content)
        self._save_content(current_content)
