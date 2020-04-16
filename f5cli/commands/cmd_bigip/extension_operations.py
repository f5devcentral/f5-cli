""" Extension package install, uninstall, upgrade, verify functions """

import importlib

from f5cli.utils import core as utils_core

COMPONENTS = {
    'as3': {
        'client': 'AS3Client',
        'actions': [
            'verify',
            'install',
            'uninstall',
            'upgrade',
            'create',
            'delete',
            'show',
            'show-info',
            'list-versions'
        ]
    },
    'do': {
        'client': 'DOClient',
        'actions': [
            'verify',
            'install',
            'uninstall',
            'upgrade',
            'create',
            'show',
            'show-info',
            'show-inspect',
            'list-versions'
        ]
    },
    'ts': {
        'client': 'TSClient',
        'actions': [
            'verify',
            'install',
            'uninstall',
            'upgrade',
            'create',
            'show',
            'show-info',
            'list-versions'
        ]
    },
    'cf': {
        'client': 'CFClient',
        'actions': [
            'verify',
            'install',
            'uninstall',
            'upgrade',
            'create',
            'show',
            'show-info',
            'show-failover',
            'show-inspect',
            'reset',
            'trigger-failover',
            'list-versions'
        ]
    }
}


class ExtensionOperationsClient(object):
    """Extension Operations Client"""

    def __init__(self, mgmt_client, component, version, package_url):
        """Class initialization

        Parameters
        ----------
        mgmt_client : instance
            the management client instance
        component : str
            the component name
        version : str
            the component version
        package_url : str
            the package url
        Returns
        -------
        None
        """

        self._mgmt_client = mgmt_client
        self._component = component
        self._version = version or None
        self._package_url = package_url or None
        self._extension_client_attr = self._get_extension_client_attr(self._component)

        component_kwargs = {}
        component_kwargs = {
            # the CLI should always attempt to download latest metadata file
            'use_latest_metadata': True
        }

        if self._version:
            component_kwargs['version'] = self._version

        self._extension_client = self._extension_client_attr(self._mgmt_client, **component_kwargs)

    @staticmethod
    def _get_extension_client_attr(component):
        """Factory method to get extension client instance

        Parameters
        ----------
        component : str
            the hostname of the device

        Returns
        -------
        None
        """

        module = importlib.import_module('f5sdk.bigip.extension')

        if component in COMPONENTS.keys():
            extension_client_class = getattr(module, COMPONENTS[component]['client'])
        else:
            raise Exception('Unknown component: {}'.format(component))

        return extension_client_class

    def install_component_if_required(self, install):
        """Install component - if required

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        if install and not self._extension_client.package.is_installed()['installed']:
            self._extension_client.package.install()
            self._extension_client.service.is_available()

    def verify_package(self):
        """Verify package

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        return self._extension_client.package.is_installed()

    def install_package(self):
        """Install package

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        component_info = self._extension_client.package.is_installed()
        if not component_info['installed']:
            component_kwargs = {}
            if self._package_url:
                component_kwargs['package_url'] = self._package_url
            installed = self._extension_client.package.install(**component_kwargs)
            message = (
                "Extension component package '%s' successfully installed "
                "version '%s'" % (self._component, installed['version'])
            )
        else:
            message = (
                "Extension component package '%s' version '%s' is already "
                "installed" % (self._component, component_info['installed_version'])
            )
        return message

    def uninstall_package(self):
        """Uninstall package

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        component_info = self._extension_client.package.is_installed()
        if not component_info['installed']:
            message = ("Extension component package '%s' is already uninstalled" % self._component)
        else:
            self._extension_client.package.uninstall()
            message = (
                "Extension component package '%s' successfully uninstalled" % self._component
            )
        return message

    def upgrade_package(self):
        """Upgrade package

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        message = ""

        component_info = self._extension_client.package.is_installed()
        if component_info['installed']:
            if component_info['installed_version'] != component_info['latest_version']:
                # uninstall old version
                self._extension_client.package.uninstall()

                # ok, now prep to install new version
                kwargs = {}
                if self._version:
                    kwargs['version'] = self._version
                else:
                    kwargs['version'] = component_info['latest_version']

                # get version specific extension client instance
                extension_client_attr = self._get_extension_client_attr(self._component)
                installer_client = extension_client_attr(self._mgmt_client, **kwargs)

                # install new version
                installer_client.package.install()
                message = (
                    "Successfully upgraded extension component package '%s' to version "
                    "'%s'" % (self._component, kwargs['version'])
                )
            else:
                message = (
                    "Extension component package '%s' version '%s' is already "
                    "installed" % (self._component, component_info['installed_version'])
                )
        else:
            message = (
                "Extension component package '%s' is uninstalled, re-run install "
                "command" % self._component
            )
        return message

    def list_package_versions(self):
        """List package versions

        Parameters
        ----------
        None

        Returns
        -------
        list
            a list containing available extension versions
        """
        return self._extension_client.package.list_versions()

    def show_service(self):
        """Show service

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        return self._extension_client.service.show()

    def create_service(self, declaration_file):
        """Create service

        Parameters
        ----------
        declaration_file : str
            the declaration file to use

        Returns
        -------
        None
        """

        if not self._extension_client.package.is_installed()['installed']:
            return (
                "Package is not installed, run command "
                "'f5 bigip extension <component> install'"
            )
        return self._extension_client.service.create(
            config_file=utils_core.convert_to_absolute(declaration_file)
        )

    def delete_service(self):
        """Delete service

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        return self._extension_client.service.delete()

    def show_info_service(self):
        """Show Info service

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        return self._extension_client.service.show_info()

    def show_failover_service(self):
        """Show Failover service

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        return self._extension_client.service.show_trigger()

    def trigger_failover_service(self, declaration_file):
        """Trigger service

        Parameters
        ----------
        declaration_file : str
            the declaration file to use

        Returns
        -------
        None
        """

        return self._extension_client.service.trigger(
            config_file=utils_core.convert_to_absolute(declaration_file)
        )

    def show_inspect_service(self):
        """Show Inspect service

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        return self._extension_client.service.show_inspect()

    def reset_service(self, declaration_file):
        """Reset service

        Parameters
        ----------
        declaration_file : str
            the declaration file to use

        Returns
        -------
        None
        """

        return self._extension_client.service.reset(
            config_file=utils_core.convert_to_absolute(declaration_file)
        )


def check_install(action):
    """Skip install check action

    Parameters
    ----------
    action : list

    Returns
    -------
    bool
    """

    return action not in ['install', 'upgrade', 'uninstall', 'verify']
