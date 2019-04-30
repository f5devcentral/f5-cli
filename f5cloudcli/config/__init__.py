"""Configuration module for ths CLI """

import os
import pickle
import click

import f5cloudcli.constants as constants

CONFIG_DIR = '%s/%s'% (constants.TMP_DIR, 'f5_cloud_cli')

class ConfigClient(object):
    """ A class used to pass BIG-IP authentication
    tokens between CLI functions.

    It will store the object returned by the
    ManagementClient class.

    It will retrieve the management client object from storage.

    If a management client object is not present, it will return an error.

    Attributes
    ----------
    client : obj
        the BIG-IP management client object

    Methods
    -------
    write_client()
        See method documentation for more details
    read_client()
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
        client_obj : str
            the client object returned from bigip login

        Returns
        -------
        None
        """

        self.client_obj = kwargs.pop('client', '')

        self.config_file = CONFIG_DIR + '/auth.file'
        # create config directory
        self._create_dir(CONFIG_DIR)

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

    def write_client(self):
        """Used by BIG-IP login to write fresh token to local storage

        Parameters
        ----------
        None

        Returns
        -------
        str
            a string containing the filename
        """

        client_obj = self.client_obj

        with open(self.config_file, 'wb') as file:
            pickle.dump(client_obj, file)
        return str(self.config_file)

    def read_client(self):
        """Used by cli commands to check if there is an existing token

        Parameters
        ----------
        None

        Returns
        -------
        object
            a client object
        """

        exists = os.path.isfile(self.config_file)

        if exists:
            with open(self.config_file, 'rb') as file:
                client_obj = pickle.load(file)
            return client_obj

        raise click.ClickException('Command failed. You must login to BIG-IP!')
