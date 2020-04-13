import pandas as pd
import os

THISDIR = os.path.dirname(__file__)
URLS_PATH = os.path.join(THISDIR,'resources/csv/urls.csv')
urls = pd.read_csv(URLS_PATH)


