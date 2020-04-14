import ETL

country_data_dir = '../Resources/Datasets/CountryData'
worldmeter_data_dir = 'DW/raw_data/worldmeter'
israel_data_dir = '../Resources/Datasets/IsraelData'

ETL.extract_worldmeter_data(outdir = worldmeter_data_dir)
ETL.transform_worldmeter_data(indir= worldmeter_data_dir,
                          outdir= country_data_dir,
                          cutoffdate = '2020-02-10')
ETL.extract_gov_data(outdir=israel_data_dir)
ETL.extract_sheet_data(outdir=israel_data_dir)
ETL.extract_regular_csvs(outdir=country_data_dir)

