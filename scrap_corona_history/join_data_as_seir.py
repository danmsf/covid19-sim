from scrap_corona_history.settings import *
import glob
import re
import datetime

# --------------------
# Merge all seperate data files
# --------------------

def main():
    conversion_dict= column_remapper.to_dict()

    # Iterate and read csv files into df
    all_files = glob.glob(DATA_DIR + "/*.csv")
    df_list = []

    for filename in all_files:

        # Discard first column due to it contains id information
        df = pd.read_csv(filename, index_col=[0], header=0)
        df = df.iloc[:,0:]

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
    # Remove plus sign from "New Cases" col
    disease_data['New Cases'] = disease_data['New Cases'].str.extract('(\d+)')
    # Sort df by date
    disease_data = disease_data.sort_values('date')
    # Remove the totalrow
    disease_data = disease_data[disease_data["Country"] != 'Total:']
    # Get only reliable data (from 10.2 and so on)
    disease_data = disease_data[disease_data["date"] >= CUTOFF_DATE]
    #
    disease_data['Country'] = disease_data['Country'].str.lower()
    #
    disease_data.columns = disease_data.columns.str.lower().str.replace("\s+", "_")


    # --------------------
    # Read and format GOVERNMENT_RESPONSE data
    # --------------------
    response_data = pd.read_excel(GOVERNMENT_RESPONSE_URL)
    response_data.CountryName = response_data.CountryName.str.lower()
    response_data.Date = pd.to_datetime(response_data.Date,format = '%Y%m%d')
    response_data = response_data.rename({'CountryName':'country',
                                          'Date':'date'},axis =1)

    # --------------------
    # Read population data
    # --------------------
    population = pd.read_csv(POPULATION_PATH, index_col ='id')

    # --------------------
    # Join data
    # --------------------
    all_data = disease_data.merge(population).fillna(0)

    all_data['S'] = all_data['population']
    all_data['E'] = all_data.groupby('country')['activecases'].shift(4).fillna(0)
    all_data['I'] = all_data['activecases']
    all_data['R'] = all_data['total_recovered'] + all_data['total_deaths']

    output_cols = ['S', 'E', 'I', 'R', 'country', 'date']
    all_data = all_data[output_cols]

    all_data = all_data.merge(response_data, on =['date','country'], how = 'left')
    # --------------------
    # # Output to file
    # --------------------
    all_data.to_csv(RESULTS_PATH)
    return (all_data)


if __name__ == '__main__':
    main()



