""" Constants used throughout this package """

import tempfile
from os.path import expanduser, join

VERSION = '0.9.0'  # should consolidate with setup version
USER_AGENT = 'f5cli/%s' % (VERSION)
TMP_DIR = tempfile.gettempdir()

# Stateful file constants
F5_CLI_DIR = join(expanduser("~"), ".f5_cli")
F5_CONFIG_FILE = join(F5_CLI_DIR, "config.yaml")
F5_AUTH_FILE = join(F5_CLI_DIR, "auth.yaml")

DEFAULT_BIGIP_PORT = 443

# output data format(s)
FORMATS = {
    'JSON': 'json',
    'TABLE': 'table',
    'DEFAULT': 'json'
}
FORMATS_ENV_VAR = 'F5_OUTPUT_FORMAT_ENV'

# Command Group names
CLOUD_SERVICES_GROUP_NAME = 'CLOUD_SERVICES'
BIGIP_GROUP_NAME = 'BIGIP'

AUTHENTICATION_PROVIDERS = {
    'BIGIP': 'bigip',
    'CLOUD_SERVICES': 'cloud-services'
}
