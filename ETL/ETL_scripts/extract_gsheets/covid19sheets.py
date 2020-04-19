from .utils.functions import *
from .settings import *
from typing import IO
import requests

# Set variables
# Set scope of gsheet api
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Get variables from json from data retrival, urls and such
# For the sheets api
spreadsheet_id = info.get('gsheets').get('spreadsheetId')
sheet_name = info.get('gsheets').get('sheet')
range = info.get('gsheets').get('range')
sample_range_name = f'{sheet_name}!{range}'

# For gov ckan api
pop_per_city_url = info.get('pop_per_city').get('url')


def main(outdir:IO = None)->pd.DataFrame:

    print(__file__, 'is running')
    # ---------------------
    # -- Get covid19 data from google sheets
    # ----------------------
    service = create_service(SCOPES, CREDS_PATH, TOKEN_PATH)
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=sample_range_name).execute()

    gsheet_df = values_to_df(result)

    # ---------------------
    # -- Get population data from gov.il
    # ----------------------
    response = requests.get(pop_per_city_url)
    records= response.json().get('result').get('records')
    pop_per_city_base = pd.DataFrame(records).drop('_id',axis = 1)

    # ---------------------
    # -- Transform dataframes and merge
    # ----------------------
    basecols = ['shk', 'gyl_0_6','gyl_6_18', 'gyl_19_45', 'gyl_46_55', 'gyl_56_64', 'gyl_65_plvs']
    city_col = 'SHm_ySHvb'
    distrct_col = 'mv`TSh_Azvryt'

    # Create two tables from the first df -
    #   one for cities
    #   and another aggregated for distrticts,
    # union them.
    pop_per_city = pop_per_city_base[basecols+[city_col]]
    pop_per_distrct = pop_per_city_base.groupby(distrct_col)[basecols]\
                                        .sum().\
                                        reset_index().\
                                        rename({distrct_col:city_col},axis = 1)

    pop_per_city_district= pd.concat([pop_per_city,pop_per_distrct],sort=False).drop_duplicates(city_col)

    # Some final data manifulations
    left_on = 'יישוב'
    right_on = 'SHm_ySHvb'

    gsheet_df[left_on] = gsheet_df[left_on].str.strip()
    pop_per_city_district[right_on] = pop_per_city_district[right_on].str.strip()

    # Merge sets
    gsheet_df_unified = gsheet_df.merge(pop_per_city_district,
                                        left_on = left_on,
                                        right_on = right_on,
                                        how ='left')\
                        .drop(right_on,axis =1)

    # Dta output
    if outdir:
        outdir = os.path.join(outdir, 'gsheets.csv')
        gsheet_df_unified.to_csv(outdir)
        retval = None
    else:
        retval = gsheet_df

    return retval


if __name__ == '__main__':
    main()
