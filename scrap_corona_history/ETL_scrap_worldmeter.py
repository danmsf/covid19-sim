from scrap_corona_history.functions import *
from selenium import webdriver

# create a new instance of Chrome
browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=option)

# send a get request to the appropiate webpage
# (in this case the main archive page from "The Wayback Machine" for "https://www.worldometers.info/coronavirus/")
browser.get(WAYBACK_MACHINE_CORONA_URL)

# Handle a timeout
timeout_get_request(browser, 50)

# Get only new data
prev_refs = get_prev_urls()
new_refs =  get_fresh_urls(browser, prev_refs, URL_REGEX_PATTERN)

browser.quit()

# Iterate over hrefs and download tables from site
errors = download_csv_from_all_links(new_refs)



