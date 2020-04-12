from  ETL.ETL_scripts.extract_regular_csvs.settings import *
from ETL.ETL_scripts.extract_regular_csvs.utils.functions import *

def main():
    entries = df_to_entries(urls)
    entries_loaded = download_dfs(entries)
    entries = Entries(entries_loaded)
    return entries

if __name__ == '__main__':
    main()