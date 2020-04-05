import os
import pandas as pd
from selenium import webdriver

# Pandas options
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Paths and Dirs
RESOURCE_DIR = 'resources'
DATA_DIR = 'data'
LOG_DIR = 'logs'

LOG_CONFIG_PATH = r'logs'
OUT_FILE = 'all_dates.csv'
CUTOFF_DATE = '2020-02-10'
CHROMEDRIVER_PATH= os.path.join(RESOURCE_DIR, 'chromedriver.exe')
POPULATION_PATH = os.path.join(RESOURCE_DIR, 'population.csv')
URLS_PATH = os.path.join(RESOURCE_DIR, 'urls.csv')

MAPPER_FILE = 'column_remapper.csv'
MAPPER_PATH = os.path.join(RESOURCE_DIR, MAPPER_FILE)

# Selenium options
option = webdriver.ChromeOptions()
option.add_argument('— incognito')

# Resources
mapper = pd.read_csv(MAPPER_PATH, index_col ='key', usecols = ['key', 'value'])
column_remapper = mapper.iloc[:,0]

urls = pd.read_csv(URLS_PATH, index_col ='id')
WAYBACK_MACHINE_CORONA_URL = urls.loc[1, 'url']
URL_REGEX_PATTERN = urls.loc[2, 'url']
GOVERNMENT_RESPONSE_URL = urls.loc[4,'url']



