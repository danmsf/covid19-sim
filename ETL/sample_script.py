import ETL_scripts
import os

# lxml, chronium, aiohttp
country_data_dir = '../Resources/Datasets/CountryData'
worldmeter_data_dir = './DW/raw_data/worldmeter'
israel_data_dir = '../Resources/Datasets/IsraelData'
worldmeter_data_dir1 = os.path.join(os.getcwd(), worldmeter_data_dir)
ETL_scripts.extract_worldmeter_data(outdir=worldmeter_data_dir)
ETL_scripts.transform_worldmeter_data(indir=worldmeter_data_dir1,
                                      outdir=country_data_dir,
                                      cutoffdate='2020-02-10')
ETL_scripts.extract_gov_data(outdir=israel_data_dir)
# ETL_scripts.extract_sheet_data(outdir=israel_data_dir)
ETL_scripts.extract_regular_csvs(outdir=country_data_dir)
