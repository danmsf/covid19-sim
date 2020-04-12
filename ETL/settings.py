import pandas as pd
import os

current_dir = os.path.dirname(__file__)

# Paths and Dirs
WORLDMETER_DATA = os.path.join(current_dir,'DW/raw_data/worldmeter')
GOV_RESOURCE_PATH = os.path.join(current_dir,'resources/csv/gov_resource.csv')

MAPPER_PATH = os.path.join(current_dir,'resources/csv/column_remapper.csv')
mapper = pd.read_csv(MAPPER_PATH, index_col ='key', usecols = ['key', 'value'])
column_remapper = mapper.iloc[:,0]

GOVERNMENT_RESPONSE_URL = 'https://ocgptweb.azurewebsites.net/CSVDownload'

POPULATION_CSV_PATH = os.path.join(current_dir,'DW/raw_data/population_data.csv')

GOV_DATA_RESULTS_DIR = os.path.join(current_dir, 'DW/raw_data/gov_data')

RESULTS_PATH = os.path.join(GOV_DATA_RESULTS_DIR, 'all_dates.csv')
RESULTS_PATH_SEIR = os.path.join(GOV_DATA_RESULTS_DIR, 'all_dates_seir.csv')

GOV_DATA_PATH = os.path.join(current_dir, 'DW/raw_data/gov_data')