from settings import *
import glob
import re
import datetime


# --------------------
# Merge all seperate data files
# --------------------
conversion_dict= column_remapper.to_dict()

# Iterate and read csv files into df
all_files = glob.glob(data_dir + "/*.csv")
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
cutoff_date = '2020-02-10'
disease_data = disease_data[disease_data["date"] >= cutoff_date]
#
disease_data['Country'] = disease_data['Country'].str.lower()
#
disease_data.columns = disease_data.columns.str.lower().str.replace("\s+", "_")


# --------------------
# Join data and world_population data
# --------------------
population = pd.read_csv(population_path, index_col = 'id')
all_data = disease_data.merge(population).fillna(0)

all_data['S'] = all_data['population']
all_data['E'] = all_data.groupby('country')['activecases'].shift(4).fillna(0)
all_data['I'] = all_data['activecases']
all_data['R'] = all_data['total_recovered'] + all_data['total_deaths']

all_data = all_data[['S','E','I','R','country','date']]



# --------------------
# # Output to dile
# --------------------
all_data.to_csv(outfile)
