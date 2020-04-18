import pandas as pd
import json
import urllib


def get_data(server_name:str,*args, **request_args)->pd.DataFrame:

    url = f'https://{server_name}/api/action/datastore_search'

    request_args = str.encode(json.dumps(request_args))
    r = urllib.request.urlopen(url,request_args)
    d = json.loads(r.read())
    records = d["result"]["records"]
    data = pd.DataFrame(records).set_index("_id")

    return data
