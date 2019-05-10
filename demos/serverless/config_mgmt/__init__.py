""" Azure Function """

import logging
import json

# pylint: disable=import-error
# pylint: disable=no-name-in-module
import azure.functions as func
from f5cloudsdk.bigip import ManagementClient

from f5cloudsdk.bigip.toolchain import ToolChainClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    """ special function """
    try:
        req_body = req.get_json()
    except Exception as _e:
        return func.HttpResponse(
            'Exception parsing JSON body: %s' % _e,
            status_code=400
        )
    host = req_body.pop('host', None)
    user = req_body.pop('user', None)
    password = req_body.pop('password', None)
    config_decl = req_body.pop('configDeclaration', None)

    if not (host and user and password):
        return func.HttpResponse('Host, user, password required', status_code=400)

    # init device
    device = ManagementClient(host, user=user, password=password)
    # get BIG-IP info (version, etc.)
    device_info = device.get_info()

    # optional configuration via AS3 declaration
    config_response = ''
    if config_decl:
        as3 = ToolChainClient(device, 'as3')
        # install AS3 - as needed
        if not as3.package.is_installed():
            as3.package.install()

        # 'POST' to AS3 service
        if as3.service.create(config=config_decl):
            config_response = {
                'message': 'success'
            }

    response = {
        'info': device_info,
        'configResponse': config_response
    }
    return func.HttpResponse(json.dumps(response))
