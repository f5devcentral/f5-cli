""" Constants used throughout this package """

import tempfile
from os.path import expanduser, join

NAME = 'f5-cli'
VERSION = '0.9.2'
USER_AGENT = 'f5cli/%s' % (VERSION)
TMP_DIR = tempfile.gettempdir()
TELEMETRY_TYPE = 'Installation Usage'
TELEMETRY_TYPE_VERSION = '1'

# stateful file constants
F5_CLI_DIR = join(expanduser("~"), ".f5_cli")
F5_CONFIG_FILE = join(F5_CLI_DIR, "config.yaml")
F5_AUTH_FILE = join(F5_CLI_DIR, "auth.yaml")

DEFAULT_BIGIP_PORT = 443

# Environment variables
ENV_VARS = {
    'ALLOW_TELEMETRY': 'F5_ALLOW_TELEMETRY',
    'OUTPUT_FORMAT': 'F5_OUTPUT_FORMAT',
    'DISABLE_SSL_WARNINGS': 'F5_DISABLE_SSL_WARNINGS'
}

# Output data format(s)
FORMATS = {
    'JSON': 'json',
    'TABLE': 'table',
    'DEFAULT': 'json'
}
FORMATS_ENV_VAR = 'F5_OUTPUT_FORMAT_ENV'

# Command group names
CS_GROUP_NAME = 'CS'
BIGIP_GROUP_NAME = 'BIGIP'

AUTHENTICATION_PROVIDERS = {
    'BIGIP': 'bigip',
    'CS': 'cs'
}
