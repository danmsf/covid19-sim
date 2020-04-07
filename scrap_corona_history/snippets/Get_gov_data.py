import urllib.request
import pandas as pd
from collections import namedtuple
import json
import os

# Use defined params
OUTDIR = 'Resources/Datasets/IsraelData' # Path to outfolder
RESOURCE_1_NAME = 'isolations' # Filename for isolations csv
RESOURCE_2_NAME = 'lab_tests'  # Filename for labtests csv
RECORDS_LIMIT = 10000000

# Link data
GOVSITE_BASE_URL = "https://data.gov.il/api/action/datastore_search?"
RESOURCE_ID1= "9eedd26c-019b-433a-b28b-efcc98de378d" # isolations data
RESOURCE_ID2= "dcf999c1-d394-4b57-a5e0-9d014a62e046" # lab test data

# Build querystrings
query1 = f"{GOVSITE_BASE_URL}resource_id={RESOURCE_ID1}&limit={RECORDS_LIMIT}"
query2 = f"{GOVSITE_BASE_URL}resource_id={RESOURCE_ID2}&limit={RECORDS_LIMIT}"

# Get data into containers (for elegant data access )
DFholder = namedtuple("DFholder", "link name")
holder_labs = DFholder(query1, RESOURCE_1_NAME)
holder_isolations = DFholder(query2, RESOURCE_2_NAME)
holders = [holder_labs,holder_isolations]

# Send a get request for each query string - save csv to file
for holder in holders:
    with urllib.request.urlopen(holder.link) as url:
        s = url.read()

    s = json.loads(s.decode('utf-8'))

    records = s["result"]["records"]
    df = pd.DataFrame(records).set_index("_id")

    outfile = holder.name+'.csv'
    outpath = os.path.join(OUTDIR,outfile)
    df.to_csv(outpath)



