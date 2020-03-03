"""Telemetry client for the CLI

Example::

    telemetry_client = TelemetryClient(context=ctx)
    telemetry_client.report()
"""

import os
import uuid

from f5teem import AnonymousDeviceClient
from f5cli import constants
from f5cli.config import ConfigurationClient

FIRST_RUN_COMPLETE_KEY = 'firstRunComplete'


class TelemetryClient:
    """ A class used to report telemetry

    It will send installation usage data on "first run",
    this will be controlled by the presence of a key in
    the configuration file

    Attributes
    ----------

    Methods
    -------
    report()
        See method documentation for more details
    """

    def __init__(self, **kwargs):
        """Class initialization

        Parameters
        ----------
        **kwargs
            keyword arguments

        Keyword Arguments
        -----------------
        context
            CLI context

        Returns
        -------
        None
        """

        self._context = kwargs.pop('context', None)

        self._config_client = ConfigurationClient()

    def get_first_run_complete_status(self):
        """Get first run complete status, default to false if it
        does not exist

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        return self._config_client.list().get(FIRST_RUN_COMPLETE_KEY, False)

    @staticmethod
    def get_telemetry_env_var():
        """Get allow telemetry environment variable

        Note: Force 'false' string to boolean

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        env_var = os.environ.get(constants.ENV_VARS['ALLOW_TELEMETRY'], True)
        if isinstance(env_var, str) and env_var.lower() == 'false':
            env_var = False
        return env_var

    def report(self):
        """Report telemetry

        - Telemetry must NOT result in uncaught exception,
        it is best effort.  If unable to send a warning will
        be logged.
        - Underlying telemetry library is providing a
        short timeout on requests of 5 seconds as the default.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # If "first run key" is false (i.e. does not exist)
        # and telemetry environment variable is not false
        # - Send telemetry
        # - Set "first run key" to true
        if not self.get_first_run_complete_status() and self.get_telemetry_env_var():
            telemetry_client = AnonymousDeviceClient({
                'name': constants.NAME,
                'version': constants.VERSION,
                'id': str(uuid.uuid4())
            })
            try:
                telemetry_client.report(
                    {
                        'installed': True
                    },
                    telemetry_type=constants.TELEMETRY_TYPE,
                    telemetry_type_version=constants.TELEMETRY_TYPE_VERSION
                )
            except Exception as err:  # pylint: disable=broad-except
                self._context.vlog('Telemetry reporting failed: {}'.format(err))
            self._config_client.create_or_update({FIRST_RUN_COMPLETE_KEY: True})
