from settings import *
import urllib.request
import pandas as pd
import json
import os
from typing import IO, Union, Optional
from collections import namedtuple



def main(outdir:Optional[IO]=None)->Union[namedtuple,None]:

    print(__file__, 'is running')
    RECORDS_LIMIT = 10000000

    df = pd.read_csv(GOV_RESOURCE_PATH)

    df['datastore_structure'] = df['resource_id'].apply(lambda x: {'resource_id': x,'limit':RECORDS_LIMIT})\
                                            .apply(lambda x: str.encode(json.dumps(x)))

    df_names = []
    for _, entry in df.iterrows():
        response  = urllib.request.urlopen(entry["url"], entry['datastore_structure'])
        s = json.loads(response.read())
        records = s["result"]["records"]
        data = pd.DataFrame(records).set_index("_id")
        df_names.append([data,entry['name']])

    if outdir:
        for df_name in df_names:
            df = df_name[0]
            filename = df_name[1]+'.csv'
            fullpath = os.path.join(outdir, filename)
            df.to_csv(fullpath)
        retval = None

    else:
        dfs = ([df_name[0] for df_name in df_names])
        names = " ".join([df_name[1] for df_name in df_names])

        Container = namedtuple('dfs', names)
        continer = Container(*dfs)
        retval = continer

    return retval

if __name__ == '__main__':
    main()
