from .settings import *
import glob
import re
import datetime
import pandas as pd
from typing import IO, Union, Optional
from collections import namedtuple


# --------------------
# Merge all seperate worldmeter files and join with outher data sources
# --------------------

def main(indir: IO,
         outdir: Optional[IO] = None,
         cutoffdate: Optional[str] = '2020-1-1') -> Union[namedtuple, None]:
    print(__file__, 'is running')
    conversion_dict = column_remapper.to_dict()

    # Iterate and read csv files into df
    all_files = glob.glob(indir + "/*.csv")
    df_list = []

    for filename in all_files:

        # Discard first column due to it contains id information
        df = pd.read_csv(filename, index_col=[0], header=0)
        df = df.iloc[:, 0:]

        # Iterate over column mapper and rename columns names to desired names
        for pat, str in conversion_dict.items():
            df = df.rename(columns=lambda x: re.sub(pat, str, x, flags=re.IGNORECASE))

        # Convert the filename which contains a date format to a date object and append as a column
        extracted_date = re.search("\w\w\w-\d\d-\d\d\d\d", filename).group()
        date_object = datetime.datetime.strptime(extracted_date, "%b-%d-%Y").date()
        df["date"] = date_object
        df["date"] = pd.to_datetime(df["date"])

        # Append to df list
        df_list.append(df)

    # Join df from all dates
    disease_data = pd.concat(df_list, ignore_index=True, sort=False)
    # Remove plus sign from columns
    disease_data['New Cases'] = disease_data['New Cases'].str.replace('[^\d]', '')
    # disease_data['New Deaths'] = disease_data['New Deaths'].astype(str).str.replace('[^\d]', '')
    # disease_data['Deaths/1M pop'] = disease_data['Deaths/1M pop'].astype(str)
    # Sort df by date
    disease_data = disease_data.sort_values('date')
    # Remove the totalrow
    disease_data = disease_data[disease_data["Country"] != 'Total:']
    # Get only reliable raw_data (from 10.2 and so on)
    disease_data = disease_data[disease_data["date"] >= cutoffdate]
    #
    disease_data['Country'] = disease_data['Country'].str.lower()
    #
    disease_data.columns = disease_data.columns.str.lower().str.replace("\s+", "_")

    disease_data['country'] = disease_data['country'].replace(population_data_mapper, regex=False)

    # --------------------
    # Read and format GOVERNMENT_RESPONSE raw_data
    # --------------------
    response_data = pd.read_csv(GOVERNMENT_RESPONSE_URL)
    response_data.CountryName = response_data.CountryName.str.lower()
    response_data.Date = pd.to_datetime(response_data.Date, format='%Y%m%d')
    response_data = response_data.rename({'CountryName': 'country',
                                          'Date': 'date'}, axis=1)

    # --------------------
    # Read population raw_data
    # --------------------
    population = pd.read_csv(POPULATION_CSV_PATH, index_col='id')

    # --------------------
    # Join raw_data
    # --------------------
    all_data = disease_data.merge(population, how='left').fillna(0)

    all_data['S'] = all_data['population']
    all_data['E'] = all_data.groupby('country')['activecases'].shift(4).fillna(0)
    all_data['I'] = all_data['activecases']
    all_data['R'] = all_data['total_recovered'] + all_data['total_deaths']

    all_data = all_data.merge(response_data, on=['date', 'country'], how='left')

    output_cols = ['S', 'E', 'I', 'R', 'country', 'date']
    all_data_seir = all_data[output_cols]

    # --------------------
    # Output to file/variable
    # --------------------
    if outdir:
        all_data.to_csv(os.path.join(outdir, 'all_dates.csv'), mode='a', header=False)
        all_data_seir.to_csv(os.path.join(outdir, 'all_dates_seir.csv'), mode='a', header=False)
        retval = None
    else:
        Container = namedtuple('dfs', 'all_data all_data_seir')
        continer = Container(all_data, all_data_seir)
        retval = continer

    return retval


if __name__ == '__main__':
    main()
