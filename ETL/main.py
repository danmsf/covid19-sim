from ETL.ETL_scripts.extract_worldmeter.extract_worldmeter_data import main as extract_worldmeter_data
from ETL.ETL_scripts.transform_worldmeter_data import main as transform_worldmeter_data
from ETL.ETL_scripts.extract_gov_data import main as extract_gov_data
from ETL.ETL_scripts.extract_gsheets.covid19sheets import main as extract_sheet_data


extract_worldmeter_data(r'D:\PycharmProjects\covid19ETL\DW\raw_data\worldmeter')
transform_worldmeter_data(r'D:\PycharmProjects\covid19ETL\DW\raw_data\worldmeter',
                          outpath = 'D:\PycharmProjects\covid19ETL\DW\loaded_data',
                          cutoffdate = '2020-02-10')
extract_gov_data(r'D:\PycharmProjects\covid19ETL\DW\raw_data\gov_data')
extract_sheet_data(r'D:\PycharmProjects\covid19ETL\DW\raw_data\gov_data')

