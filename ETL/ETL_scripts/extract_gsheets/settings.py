import os
import json

THISDIR = os.path.dirname(__file__)
CREDS_PATH = os.path.join(THISDIR, 'resources/credentials.json')
TOKEN_PATH = os.path.join(THISDIR, 'resources/token.pickle')

JSON_INFO_PATH = os.path.join(THISDIR, 'resources/info.json')

with open(JSON_INFO_PATH, 'r') as f:
    info = json.loads(f.read())