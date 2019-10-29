""" Constants used throughout this package """

import tempfile
from os.path import expanduser, join

VERSION = '0.9.0'  # should consolidate with setup version
USER_AGENT = 'f5cloudcli/%s' % (VERSION)
TMP_DIR = tempfile.gettempdir()
F5_CLI_DIR = join(expanduser("~"), ".f5_cli")
F5_CONFIG_FILE = join(F5_CLI_DIR, "config.json")
F5_AUTH_FILE = join(F5_CLI_DIR, "auth.json")

# output data format(s)
FORMATS = {
    'JSON': 'json',
    'TABLE': 'table',
    'DEFAULT': 'json'
}
FORMATS_ENV_VAR = 'F5_OUTPUT_FORMAT_ENV'

# Providers
AWS_PROVIDER = 'aws'
AZURE_PROVIDER = 'azure'

# Command Group names
CLOUD_SERVICES_GROUP_NAME = 'CLOUD_SERVICES'
BIGIP_GROUP_NAME = 'BIGIP'

# Auth kwargs
CLI_OPTIONS_USER_AUTH = {
    'required': True,
    'metavar': '<USERNAME>'
}
CLI_OPTIONS_PASSWORD_AUTH = {
    'required': False,
    'prompt': True,
    'confirmation_prompt': False
}
