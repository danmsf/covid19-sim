import pandas as pd
import json
import os

current_dir = os.path.dirname(__file__)

# Paths and Dirs
WORLDMETER_DATA = os.path.join(current_dir,'DW/raw_data/worldmeter')
GOV_RESOURCE_CSV = os.path.join(current_dir, 'resources/csv/gov_resource.csv')

MAPPER_PATH = os.path.join(current_dir,'resources/csv/column_remapper.csv')
mapper = pd.read_csv(MAPPER_PATH, index_col ='key', usecols = ['key', 'value'])
column_remapper = mapper.iloc[:,0]

POPULATION_MAPPER_PATH = os.path.join(current_dir,'resources/population_data_mapper.json')
with open(POPULATION_MAPPER_PATH, 'r') as f:
    population_data_mapper = json.loads(f.read())

GOVERNMENT_RESPONSE_URL = 'https://ocgptweb.azurewebsites.net/CSVDownload'
GOVERNMENT_RESPONSE_CSV = r'../../../Resources/Datasets/CountryData/OxCGRT_Download_190420_125856_Full.csv'
GOVERNMENT_RESPONSE_CSV = os.path.join(current_dir,GOVERNMENT_RESPONSE_CSV)
# GOVERNMENT_RESPONSE_CSV = os.path.normpath(os.path.join(current_dir, GOVERNMENT_RESPONSE_CSV))

POPULATION_CSV_PATH = os.path.join(current_dir,'resources/csv/population_data.csv')

GOV_DATA_RESULTS_DIR = os.path.join(current_dir, 'DW/raw_data/gov_data')

RESULTS_PATH = os.path.join(GOV_DATA_RESULTS_DIR, 'all_dates.csv')
RESULTS_PATH_SEIR = os.path.join(GOV_DATA_RESULTS_DIR, 'all_dates_seir.csv')

GOV_DATA_PATH = os.path.join(current_dir, 'DW/raw_data/gov_data')