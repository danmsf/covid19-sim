from datetime import datetime
from ETL_scripts.extract_worldmeter.settings import  *
import re
import glob
import pandas as pd
from typing import Iterable, Union, List, Pattern, IO
import numpy as np

# Impored for scraping TheWaybackMachine
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def handle_first_time()->None:

    files = os.listdir(OUTPUT_PATH)
    if len(files)!=0 and first_time_bit == 0:
        raise Exception('Dir is not empty')
    else:
        config['bin']['key'] = '1'
        with open(CONFIG_PATH, 'w') as configfile:
            config.write(configfile)

def timeout_get_request(browser:webdriver.Chrome, timeout:int = 50)->None:
    """Set timeout for response from site"""
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, XPATH)))
    except TimeoutException:
        logger.info("Timed out waiting for page to load")
        browser.quit()
        raise Exception('')


def download_csv_from_all_urls(new_refs:Iterable[str])->None:
    """downloads csv from all urls"""
    urls_len = len(new_refs)

    for i, ref in enumerate(new_refs):

        logger.info(f'Downloading file {i + 1} from {urls_len}: {ref}')

        try:
            # TODO match=
            container = pd.read_html(ref, match=READ_HTML_MATCH_PARAM)
            df = container[-1]
            df['ref'] = ref

            date_str = re.search('\d{8}',ref).group()
            date_obj = datetime.strptime(date_str, '%Y%m%d')
            df['date'] = date_obj

            date_repr_to_file = date_obj.strftime('%b-%d-%Y')

            outfile = date_repr_to_file + '.csv'
            outpath = os.path.join(OUTPUT_PATH, outfile)
            df.to_csv(outpath)
        except:
            logger.error(f'There have been a problem with {ref}')


def get_all_urls_matching_regex(browser:webdriver.Chrome,
                                regex_pattern:Pattern) ->List[str]:
    """Scraps the wayback machine for coronavirus worldmeter and gets all urls"""
    refs = []
    regex_pattern = re.compile(regex_pattern)
    elems = browser.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        ref = elem.get_attribute("href")
        match = regex_pattern.search(ref)
        if match:
            refs.append(match.group())
    return refs

def get_fresh_urls(all_urls:Iterable[str],
                   prev_urls:Iterable[str],
                   exluded_urls:Iterable[str]) -> Union[List[str],None]:
    """Compare downloaded urls to all scraped urls"""
    new_refs = list(set(all_urls) - set(prev_urls) - set(exluded_urls))
    # rmemove today's main_url
    new_refs.sort()
    new_refs = new_refs[:-1]
    retval = new_refs

    if len(new_refs) == 0:
        retval = None

    return retval

def exclude_prev_dates(all_urls:Iterable[str],
                   exluded_urls:Iterable[str]) -> Union[List[str],None]:
    prev_dates = [pd.to_datetime(re.findall(r'\d+', c)[0]) for c in excluded_urls]
    last_date = np.max(prev_dates)
    out_urls = [c for c in all_urls if pd.to_datetime(re.findall(r'\d+', c)[0]) > last_date]
    retval = out_urls
    if len(out_urls) == 0:
        retval = None

    return retval

def get_prev_urls(path:IO)->List[str]:
    """Read all downloaded csv's and make a list of all old urls"""
    prev_urls=[]
    all_files = glob.glob(path + "/*.csv")
    for filename in all_files:
        df = pd.read_csv(filename)
        try:
            prev_urls = prev_urls + df.ref.to_list()
        except:
            pass
    return list(set(prev_urls))



# Unused functions
# ------------------------------------------
def log_errors_and_runtime(errors, delta, log_dir):

    errors = "\n".join(errors)
    date_str = datetime.today().strftime("%d%m%Y")
    outfile = date_str + '.txt'
    outpath = os.path.join(log_dir, outfile)

    with open(outpath, 'w+') as filehandle:
        filehandle.writelines(f"errors:{errors}")
        filehandle.writelines('\n---------------------\n')
        filehandle.writelines(f"time elapsed in seconds: {delta}")
        filehandle.writelines('\n---------------------\n')

def update_ref_log(hrefs,new_refs, hrefs_path):

    new_refs = pd.DataFrame(new_refs, columns=["href"])
    hrefs = pd.concat([hrefs,new_refs],axis = 0, ignore_index=True, sort=False)
    hrefs.to_csv(hrefs_path, index_label = 'id')


def verbose(i, arrsize, url):
    """Function that prints state of download"""
    print(f'Downloading file {i + 1} from {arrsize}: {url}')



class regex_filter:
    def __init__(self,regex):
        self.regex = regex
    def __repr__(self):
        return 'regex_filter'

    def validate(self,string):
        match = re.match(self.regex,string)
        if match:
            return match.group()


class in_list_filter:
    def __init__(self, elems=[]):
        self.elems = elems

    def add_elements(self,elems):

        if  not hasattr(elems,'sort'):
            elems = [elems]

        self.elems = self.elems + elems

    def validate(self, string):
        return string in self.elems

    def __repr__(self):
        return 'in_list_filter'

class link_factory(object):
    def __init__(self, browser=None, main_url=None):

        self.main_url = main_url
        self.browser = browser
        self.all_links =[]
        self.filters=[]
        self.valid_urls =[]

    def get_all_urls(self):
        self.browser.get(self.main_url)
        timeout_get_request(self.browser, 50)
        elems = self.browser.find_elements_by_xpath("//a[@href]")
        elems = [elem.get_attribute("href") for elem in elems]
        self.all_links = elems

    def add_filter(self, filter_arr):
        if type(filter_arr) != list:
            filter_arr = [filter_arr]
        self.filters = self.filters + filter_arr

    def apply_filters(self, url):
        return_value = url
        results = []
        for filter in self.filters:
            result = filter.validate(url)
            results.append(result)

        if not all(results):
            return_value = None

        return return_value

    def filter_urls(self):
        for link in self.all_links:
            result = self.apply_filters(link)
            if result:
                self.valid_urls.append(result)

    def quit(self):
        self.browser.quit()

def date_to_url(url_pattern,date):
    url = 'https://web.archive.org/web/{}/https://www.worldometers.info/coronavirus/'.format(date)
    return url