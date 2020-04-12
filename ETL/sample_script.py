from ETL.ETL_scripts.extract_worldmeter.extract_worldmeter_data import main as extract_worldmeter_data
from ETL.ETL_scripts.transform_worldmeter_data import main as transform_worldmeter_data
from ETL.ETL_scripts.extract_gov_data import main as extract_gov_data
from ETL.ETL_scripts.extract_gsheets.covid19sheets import main as extract_sheet_data
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
worldmeter_dir = os.path.join(current_dir,'DW/raw_data/worldmeter')
results_dir = os.path.join(current_dir,'DW/loaded_data')
gov_dir = os.path.join(current_dir,'DW/raw_data/gov_data')

extract_worldmeter_data(worldmeter_dir)
transform_worldmeter_data(worldmeter_dir,
                          outpath = results_dir,
                          cutoffdate = '2020-02-10')
extract_gov_data(gov_dir)
extract_sheet_data(gov_dir)

