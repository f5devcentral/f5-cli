""" Constants used throughout this package """

import tempfile
from os.path import expanduser, join

VERSION = '0.9.0' # should consolidate with setup version
USER_AGENT = 'f5cloudcli/%s' % (VERSION)
TMP_DIR = tempfile.gettempdir()
F5_CLI_DIR = join(expanduser("~"), ".f5_cli")
F5_CONFIG_FILE = join(F5_CLI_DIR, "config.json")

# Output data format
JSON_FORMAT = 'json'
TABLE_FORMAT = 'table'
