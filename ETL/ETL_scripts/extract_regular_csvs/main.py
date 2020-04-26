from  .settings import *
from  .utils.functions import *
import os

def main(outdir=None):
    entries = df_to_entries(urls)
    entries_loaded = download_dfs(entries)
    d = {entry.name: entry.df for entry in entries_loaded}

    if outdir:
        for entry in entries_loaded:
            outpath = os.path.join(outdir, entry.name+'.csv')
            entry.df.to_csv(outpath)
        result = None
    else:
        entries = Entries(**d)
        result = entries

    return result

if __name__ == '__main__':
    main()