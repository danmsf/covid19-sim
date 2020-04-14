from ETL_scripts.extract_worldmeter.extract_worldmeter_data import main as extract_worldmeter_data
from ETL_scripts.transform_worldmeter_data.transform_worldmeter_data import main as transform_worldmeter_data
from ETL_scripts.extract_gov_data.extract_gov_data import main as extract_gov_data
from ETL_scripts.extract_gsheets.covid19sheets import main as extract_sheet_data
from ETL_scripts.extract_regular_csvs.main import main as extract_regular_csvs

results_dir = '../Resources/Datasets/CountryData'
worldmeter_dir = 'DW/raw_data/worldmeter'
gov_dir = '../Resources/Datasets/IsraelData'

# extract_worldmeter_data(worldmeter_dir)
# transform_worldmeter_data(worldmeter_dir,
#                            outpath = results_dir,
#                            cutoffdate = '2020-02-10')
# extract_gov_data(gov_dir)
extract_sheet_data(gov_dir)
extract_regular_csvs(results_dir)