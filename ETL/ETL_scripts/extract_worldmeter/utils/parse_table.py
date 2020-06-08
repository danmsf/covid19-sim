import requests
from bs4 import BeautifulSoup
import pandas as pd


class WorldMeterData:
    def __init__(self):
        pass
        # self.url = url
        # self.df = self.parse_url()

    def parse_url(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r)
        table = soup.select_one('#main_table_countries_today')
        headers = self._parse_headers(table)
        body = self._parse_body(table)
        pandas_df = pd.DataFrame(body, columns=headers)
        pandas_df['#'] = pd.to_numeric(pandas_df['#'], errors='coerce')
        pandas_df = pandas_df[~pandas_df['#'].isna()]
        return pandas_df

    @staticmethod
    def _parse_headers(table):
        headers_l = table.select('th')
        headers = [c.text.replace("\n", " ") for c in headers_l]
        headers = [c.replace("/", "_") for c in headers]
        headers = [c.replace("\xa0", "_") for c in headers]
        headers = [c.replace(" ", "_") for c in headers]
        return headers

    @staticmethod
    def _parse_body(table):
        body = []
        for row in table.select('tr'):
            temp = []
            for col in row.select('td'):
                temp.append(col.text)
            body.append(temp)
        return body
