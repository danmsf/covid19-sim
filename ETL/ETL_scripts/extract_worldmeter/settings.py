# Imports
import os
from selenium import webdriver
import logging.config
from datetime import date
import configparser

current_dir = os.path.dirname(__file__)


# Paths and Dirs
OUTPUT_PATH = r'D:\PycharmProjects\covid19ETL\DW\raw_data\worldmeter'
SITE_URL = 'https://www.worldometers.info/coronavirus/'

RESOURCE_DIR = os.path.join(current_dir,'resources')
WAYBACK_URL_BASE = r'https://web.archive.org/web'
WAYBACK_FULLPATH = WAYBACK_URL_BASE + "/*/" + SITE_URL
URL_REGEX_PATTERN = WAYBACK_URL_BASE + "/\d{8}/" + SITE_URL

# Selenium options
CHROMEDRIVER_PATH= os.path.join(RESOURCE_DIR, 'chromedriver.exe')
prefs = {"profile.managed_default_content_settings.images": 2}
options = webdriver.ChromeOptions()
options.add_argument('— incognito')
# options.add_argument('--headless')
options.add_experimental_option("prefs", prefs)

# Webpage enteties
XPATH = "//div[@class='calendar-day ']"
READ_HTML_MATCH_PARAM = 'Country'

# Exluded urls
EXLUDED_URLS_PATH = os.path.join(RESOURCE_DIR, 'excluded_urls.csv')
with open(EXLUDED_URLS_PATH) as f:
    excluded_urls = f.read().splitlines()

# Start logger
CONFIG_PATH = os.path.join(RESOURCE_DIR, 'logger.conf')
VERBOSE_LEVEL = 'INFO'
logging.config.fileConfig(fname=CONFIG_PATH, disable_existing_loggers=False)
logger = logging.getLogger('errorLogger')
logger.handlers[0].setLevel(VERBOSE_LEVEL)

# Date
todays_date = date.today().strftime("%Y%m%d")

config = configparser.ConfigParser()
config.read(CONFIG_PATH)
first_time_bit = config['bin']['key']
first_time_bit = int(first_time_bit)
