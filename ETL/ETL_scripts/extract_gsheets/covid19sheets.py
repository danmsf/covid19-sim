from .settings import *
from .utils.functions import *
import requests
from typing import Union
from os import PathLike


# Set variables
# Set scope of gsheet api
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Get variables from json from data retrival, urls and such
# For the sheets api
spreadsheet_id = info.get('gsheets').get('spreadsheetId')
sheet_name = info.get('gsheets').get('sheet')
sheet_range = info.get('gsheets').get('range')
sample_range_name = f'{sheet_name}!{sheet_range}'


def main(outdir: Union[PathLike] = None) -> pd.DataFrame:
    print(__file__, 'is running')

    # ---------------------
    # -- Get covid19 data from google sheets
    # ----------------------

    service = create_service(SCOPES, CREDS_PATH, TOKEN_PATH)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=sample_range_name).execute()

    gsheet_df = values_to_df(result)

    # Dta output
    if outdir:
        outdir = os.path.join(outdir, 'gsheets.csv')
        gsheet_df.to_csv(outdir)
        retval = None
    else:
        retval = gsheet_df

    return retval


if __name__ == '__main__':
    main()
