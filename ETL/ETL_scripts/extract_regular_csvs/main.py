from  ETL.ETL_scripts.extract_regular_csvs.settings import *
from ETL.ETL_scripts.extract_regular_csvs.utils.functions import download_dfs

def main():
    dfs = download_dfs(url_list)
    return dfs

if __name__ == '__main__':
    main()