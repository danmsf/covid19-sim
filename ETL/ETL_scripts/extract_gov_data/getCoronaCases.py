import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

url = "https://govextra.gov.il/ministry-of-health/corona/corona-virus/"

class CovidIsraelUpdate:
    def __init__(self, url):
        self.url = url
        self.doc = self.get_doc_from_webpage()
        self.df = pd.DataFrame()

    def get_doc_from_webpage(self):
        headers = {'Accept-Encoding': 'identity'}
        print("************Getting doc************")
        r = requests.get(self.url, headers)
        html_doc = r.content
        soup = BeautifulSoup(html_doc)
        return soup

    def _parse_doc(self):
        doc = self.doc
        stats = {}
        stats['tests_today'] = doc.select_one('.corona-bdikot .corona-sickheader .corona-sickheader-left .corona-md').text
        stats['tests_total'] = doc.select_one('.corona-bdikot .corona-sickmiddle').text
        stats['tests_first_positive'] = doc.select_one('.corona-bdikotfooter .corona-bold').text
        stats['new_cases'] = doc.select_one('.corona-sick .corona-sickheader .corona-sickheader-left .corona-md').text
        stats['total_cases'] = doc.select_one('.corona-sick .corona-sickmiddle').text
        stats['easy_cases'] = doc.select_one('.corona-sick .corona-green .corona-bold').text
        stats['mild_cases'] = doc.select_one('.corona-sick .corona-yellow .corona-bold').text
        stats['serious_cases'] = doc.select_one('.corona-sick .corona-red .corona-bold').text
        stats['respiratory_cases'] = doc.select_one('.corona-sick .corona-pink .corona-bold').text

        stats['total_deaths'] = doc.select('.corona-deadcontainer .corona-bold')[0].text
        stats['total_recovered'] = doc.select('.corona-deadcontainer .corona-bold')[1].text
        stats['hospitalized_cases'] = doc.select('.corona-inhospital .corona-bold')[0].text
        stats['home_cases'] = doc.select('.corona-inhospital .corona-bold')[1].text
        stats2 = {k: v.replace(",", "") for k, v in stats.items()}
        return stats2

    def get_df(self):
        parsed = self._parse_doc()
        t = pd.DataFrame(parsed, index=[0])
        t = t.apply(lambda x: pd.to_numeric(x, errors="coerce"))
        t = t.fillna(0)
        t['date'] = datetime.today().date()
        t = t[['date', 'tests_total', 'total_cases', 'hospitalized_cases', 'serious_cases', 'respiratory_cases', 'total_deaths',
               'tests_today', 'tests_first_positive', 'new_cases', 'easy_cases', 'mild_cases', 'total_recovered', 'home_cases']]
        cols_new = [
            'תאריך',
            'סך בדיקות לגילוי קורונה',
            'מספר מאומתים',
            'מספר חולים מאושפזים',
            'מספר חולים במצב קשה',
            'מספר מונשמים',
            'מספר נפטרים',
            'בדיקות ביממה האחרונה',
            'בדיקות חיוביות ראשונות',
            'מספר מאומתים שהתווספו היום',
            'מספר חולים במצב קל',
            'מספר חולים במצב בינוני',
            'מספר מחלימים',
            'מספר חולים בבית',
        ]
        t.columns = cols_new
        self.df = t

