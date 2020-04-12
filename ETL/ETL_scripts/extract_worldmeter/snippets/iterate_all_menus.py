from ETL_scripts.extract_worldmeter.settings import  *
import re

from selenium.webdriver import ActionChains

browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=options)
browser.get(WAYBACK_MACHINE_CORONA_URL)

actions = ActionChains(browser)
days = browser.find_elements_by_css_selector('div[class="calendar-day "]')
elems_arr =[]
for day in days[:1]:

    # Hover div and open drop down menu
    actions.move_to_element(day).perform()

    elems = browser.find_elements_by_xpath("//a[@href][@class='s2xx snapshot-link']")
    for elem in elems:
        ref = elem.get_attribute("href")
        match = re.search(URL_REGEX_PATTERN, ref)
        if match:
            elems_arr.append(match.group())