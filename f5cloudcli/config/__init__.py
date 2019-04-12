"""Configuration moduel for ths CLI """

import os
import pickle
import click

import f5cloudcli.constants as constants

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
        Write management client object storage
    read_client()
        Read management client object from storage
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

        filename = constants.TMP_DIR + '/auth.file'
        client_obj = self.client_obj

        with open(filename, 'wb') as file:
            pickle.dump(client_obj, file)
        return str(filename)

    @staticmethod
    def read_client():
        """Used by cli commands to check if there is an existing token

        Parameters
        ----------
        None

        Returns
        -------
        object
            a client object
        """

        filename = constants.TMP_DIR + '/auth.file'
        exists = os.path.isfile(filename)

        if exists:
            with open(filename, 'rb') as file:
                client_obj = pickle.load(file)
            return client_obj

        raise click.ClickException('Command failed. You must login to BIG-IP!')
