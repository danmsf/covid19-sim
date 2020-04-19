from .utils.functions import *
from .settings import *
from typing import IO
import requests

# Enable sheets api at: https://developers.google.com/sheets/api/quickstart/python
# Choose desktop app
# Download the client configuration file and place in the folder of this script

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.

spreadsheet_id = info.get('gsheets').get('spreadsheetId')
sheet_name = info.get('gsheets').get('sheet')
range = info.get('gsheets').get('range')
sample_range_name = f'{sheet_name}!{range}'
pop_per_city_url = info.get('pop_per_city').get('url')

def main(outdir:IO = None)->pd.DataFrame:
    print(__file__, 'is running')

    service = create_service(SCOPES, CREDS_PATH, TOKEN_PATH)
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=sample_range_name).execute()

    gsheet_df = values_to_df(result)

    response = requests.get(pop_per_city_url)
    records= response.json().get('result').get('records')
    pop_per_city = pd.DataFrame(records).drop('_id',axis = 1)

    left_on = 'יישוב'
    right_on = 'SHm_ySHvb'

    gsheet_df[left_on] = gsheet_df[left_on].str.strip()
    pop_per_city[right_on] = pop_per_city[right_on].str.strip()

    gsheet_df = gsheet_df.merge(pop_per_city, left_on = left_on, right_on = right_on, how ='left')

    if outdir:
        outdir = os.path.join(outdir, 'gsheets.csv')
        gsheet_df.to_csv(outdir)
        retval = None
    else:
        retval = gsheet_df

    return retval


if __name__ == '__main__':
    main()
