from functions import *
from settings import *
from selenium import webdriver

browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)

link_f = link_factory(browser,WAYBACK_MACHINE_CORONA_URL)
link_f.get_all_urls()

old_urls = get_prev_urls()
exluded_urls_csv = pd.read_csv(EXLUDED_URLS_CSV_PATH, index_col ='id').url.to_list()
todays_url = date_to_url(WAYBACK_MACHINE_CORONA_PATTERN,todays_date)

list_filter = in_list_filter()
list_filter.add_elements(old_urls)
list_filter.add_elements(exluded_urls_csv)
list_filter.add_elements(todays_url)

reg_filter = regex_filter(URL_REGEX_PATTERN)

link_f.add_filter(in_list_filter)
link_f.add_filter(regex_filter)

link_f.filter_urls()
link_f.valid_urls

link_f.quit()