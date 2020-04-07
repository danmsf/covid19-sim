import gdown
import os
url = 'https://docs.google.com/spreadsheets/d/1Y-ieLWMDzFzzeJKW-SygD90dBH80d4x0db8I3UFNj_c/edit#gid=920403791'
# output = 'spam.txt'
# gdown.download(url, output, quiet=False)
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output = os.path.join(project_path, "Resources", "Israel_cities")
gdown.download(url, output, quiet=False, postprocess=gdown.extractall)



from __future__ import print_function

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/drive.readonly.metadata'
url = 'https://docs.google.com/spreadsheets/d/1Y-ieLWMDzFzzeJKW-SygD90dBH80d4x0db8I3UFNj_c/edit#gid=920403791'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))
DRIVE = discovery.build('drive', 'v3')
# files = DRIVE.files().list().execute().get('files', [])
# for f in files:
#     print(f['name'], f['mimeType'])


file_id = '1Y-ieLWMDzFzzeJKW-SygD90dBH80d4x0db8I3UFNj_c'
request = DRIVE.files().export_media(fileId=file_id,
                                               mimeType='application/csv')
fh = io.BytesIO ()
downloader = MediaIoBaseDownload (fh, request)
done = False
while done is False:
    status, done = downloader.next_chunk ()
    print
    "Download %d%%." % int (status.progress () * 100)