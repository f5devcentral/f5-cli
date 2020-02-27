""" Extension package install, uninstall, upgrade, verify functions """
from f5sdk.bigip.extension import ExtensionClient


def verify_package(client, component, **kwargs):
    """ Return extension client """
    extension_client = ExtensionClient(client, component, **kwargs)
    return extension_client.package.is_installed()


def install_package(client, component, **kwargs):
    """ Install extension package """
    message = ""
    extension_client = ExtensionClient(client, component, **kwargs)
    component_info = extension_client.package.is_installed()
    if not component_info['installed']:
        installed = extension_client.package.install()
        message = ("Extension component package '%s' successfully installed "
                   "version '%s'" % (component, installed['version']))
    else:
        message = ("Extension component package '%s' version '%s' is already "
                   "installed" % (component, component_info['installed_version']))
    return message


def uninstall_package(client, component, **kwargs):
    """ Uninstall extension package"""
    extension_client = ExtensionClient(client, component, **kwargs)
    component_info = extension_client.package.is_installed()
    if not component_info['installed']:
        message = ("Extension component package '%s' is already uninstalled" % component)
    else:
        kwargs['version'] = component_info['installed_version']
        extension_client = ExtensionClient(client, component, **kwargs)
        extension_client.package.uninstall()
        message = ("Successfully uninstalled extension component package '%s' "
                   "version '%s'" % (component, kwargs['version']))
    return message


def upgrade_package(client, component, version):
    """ Upgrade extension package """
    message = ""
    kwargs = {}
    if version:
        kwargs['version'] = version
    extension_client = ExtensionClient(client, component, **kwargs)
    component_info = extension_client.package.is_installed()

    if component_info['installed']:
        if component_info['installed_version'] != component_info['latest_version']:
            kwargs['version'] = component_info['installed_version']
            extension_client = ExtensionClient(client, component, **kwargs)
            extension_client.package.uninstall()
            if not version:
                kwargs['version'] = component_info['latest_version']
            else:
                kwargs['version'] = version
            extension_client = ExtensionClient(client, component, **kwargs)
            extension_client.package.install()
            message = ("Successfully upgraded extension component package '%s' to version "
                       "'%s'" % (component, kwargs['version']))
        else:
            message = ("Extension component package '%s' version '%s' is already "
                       "installed" % (component, component_info['installed_version']))
    else:
        message = ("Extension component package '%s' is uninstalled, re-run install "
                   "command" % component)
    return message
