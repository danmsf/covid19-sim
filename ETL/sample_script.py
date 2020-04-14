from ETL_scripts.extract_worldmeter.extract_worldmeter_data import main as extract_worldmeter_data
from ETL_scripts.transform_worldmeter_data.transform_worldmeter_data import main as transform_worldmeter_data
from ETL_scripts.extract_gov_data.extract_gov_data import main as extract_gov_data
from ETL_scripts.extract_gsheets.covid19sheets import main as extract_sheet_data
from ETL_scripts.extract_regular_csvs.main import main as extract_regular_csvs

country_data_dir = '../Resources/Datasets/CountryData'
worldmeter_data_dir = 'DW/raw_data/worldmeter'
israel_data_dir = '../Resources/Datasets/IsraelData'

extract_worldmeter_data(outdir = worldmeter_data_dir)
transform_worldmeter_data(indir= worldmeter_data_dir,
                          outdir= country_data_dir,
                          cutoffdate = '2020-02-10')
extract_gov_data(outdir=israel_data_dir)
extract_sheet_data(outdir=israel_data_dir)
extract_regular_csvs(outdir=country_data_dir)