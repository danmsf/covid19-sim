from ETL.ETL_scripts.extract_worldmeter.extract_worldmeter_data import main as extract_worldmeter_data
from ETL.ETL_scripts.transform_worldmeter_data import main as transform_worldmeter_data
from ETL.ETL_scripts.extract_gov_data import main as extract_gov_data
from ETL.ETL_scripts.extract_gsheets.covid19sheets import main as extract_sheet_data
import pathlib


worldmeter_dir = pathlib.Path(__file__).parent.joinpath('DW/raw_data/worldmeter').__str__()
results_dir = pathlib.Path(__file__).parent.parent.joinpath('Resources/Datasets').__str__()
gov_dir = pathlib.Path(__file__).parent.parent.joinpath('Resources/Datasets/IsraelData').__str__()

extract_worldmeter_data(worldmeter_dir)
transform_worldmeter_data(worldmeter_dir,
                          outpath = results_dir,
                          cutoffdate = '2020-02-10')
extract_gov_data(gov_dir)
extract_sheet_data(gov_dir)