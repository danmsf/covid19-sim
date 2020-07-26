import requests
# from bs4 import BeautifulSoup
# from datetime import datetime
import pandas as pd
import os

import json

url = "https://datadashboardapi.health.gov.il/api/queries/_batch"

with requests.session() as session:
    header = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,he;q=0.8",
        "Access-Control-Request-Method": "POST",
        "Connection": "keep-alive",
        "Host": "datadashboardapi.health.gov.il",
        "Origin": "https://datadashboard.health.gov.il",
        "Referer": "https://datadashboard.health.gov.il/COVID-19/?utm_source=go.gov.il&utm_medium=referral",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
    }
    r = session.options(url=url, headers=header)

    header = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Content-Length": "1572",
        "Content-Type": "application/json",
        "Host": "datadashboardapi.health.gov.il",
        "Origin": "https://datadashboard.health.gov.il",
        "Referer": "https://datadashboard.health.gov.il/COVID-19/?utm_source=go.gov.il&utm_medium=referral",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
    }

    payload = {"requests": [{"id": "0", "queryName": "lastUpdate", "single": True, "parameters": {}},
                            {"id": "1", "queryName": "infectedPerDate", "single": False, "parameters": {}},
                            {"id": "2", "queryName": "updatedPatientsOverallStatus", "single": False, "parameters": {}},
                            {"id": "3", "queryName": "sickPerDateTwoDays", "single": False, "parameters": {}},
                            {"id": "4", "queryName": "sickPerLocation", "single": False, "parameters": {}},
                            {"id": "5", "queryName": "patientsPerDate", "single": False, "parameters": {}},
                            {"id": "6", "queryName": "deadPatientsPerDate", "single": False, "parameters": {}},
                            {"id": "7", "queryName": "recoveredPerDay", "single": False, "parameters": {}},
                            {"id": "8", "queryName": "testResultsPerDate", "single": False, "parameters": {}},
                            {"id": "9", "queryName": "infectedPerDate", "single": False, "parameters": {}},
                            {"id": "10", "queryName": "patientsPerDate", "single": False, "parameters": {}},
                            {"id": "11", "queryName": "doublingRate", "single": False, "parameters": {}},
                            {"id": "12", "queryName": "infectedByAgeAndGenderPublic", "single": False,
                             "parameters": {"ageSections": [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]}},
                            {"id": "13", "queryName": "isolatedDoctorsAndNurses", "single": True, "parameters": {}},
                            {"id": "14", "queryName": "testResultsPerDate", "single": False, "parameters": {}},
                            {"id": "15", "queryName": "contagionDataPerCityPublic", "single": False, "parameters": {}},
                            {"id": "16", "queryName": "hospitalStatus", "single": False, "parameters": {}}
                            ]}
    # payload = {"requests": [{"id": "0", "queryName": "lastUpdate", "single": True, "parameters": {}}]}
    r2 = session.post(url, json=payload, headers=header)

general = ["updatedPatientsOverallStatus", "infectedByAgeAndGenderPublic", "isolatedDoctorsAndNurses",
           "contagionDataPerCityPublic", "hospitalStatus"]

data_path = os.path.join(os.getcwd(), "Resources", "Datasets", "IsraelData")
tables = {}
data = r2.json()
with open(os.path.join(os.getcwd(), "Resources", "Datasets", "IsraelData",'data.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

for i, query in enumerate(payload['requests']):
    queryName = query['queryName']
    if queryName == 'lastUpdate':
        lastUpdate = data[i]['data']['lastUpdate']
    elif queryName in general:
        if queryName == 'isolatedDoctorsAndNurses':
            temp = pd.DataFrame(data[i]['data'], index=[0])
        else:
            temp = pd.DataFrame(data[i]['data'])
        temp['lastUpdate'] = lastUpdate
        temp['date'] = lastUpdate
        temp.to_csv(os.path.join(data_path, queryName + ".csv"), mode='a', index=False)
        tables[queryName] = temp
    else:
        temp = pd.DataFrame(data[i]['data'])
        temp['lastUpdate'] = lastUpdate
        temp.to_csv(os.path.join(data_path, queryName + ".csv"), index=False)
        tables[queryName] = temp

# data_path = os.path.join(os.getcwd(), "Resources", "Datasets", "IsraelData")
# for k, table in tables.items():
#     table.to_csv(os.path.join(data_path, k + ".csv"), index=False)

# from selenium import webdriver
# CHROMEDRIVER_PATH = 'C:\\Users\\User\\.wdm\\drivers\\chromedriver\\83.0.4103.39\\win32\\chromedriver.exe'
# browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)
# URL = "https://datadashboard.health.gov.il/COVID-19/?utm_source=go.gov.il&utm_medium=referral"
# browser.get(URL)
# browser.find_element_by_xpath("//div[@id='json']").text
#
# import os
#
# from selenium import webdriver
# URL = "https://datadashboard.health.gov.il/COVID-19/?utm_source=go.gov.il&utm_medium=referral"
# fp = webdriver.FirefoxProfile()
# url2 = "view-source:"+URL
# fp.set_preference("browser.download.folderList",2)
# fp.set_preference("browser.download.manager.showWhenStarting",False)
# fp.set_preference("browser.download.dir", os.getcwd())
# fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
# fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/json")
# browser = webdriver.Firefox(firefox_profile=fp)
# browser.get(url2)
# browser.find_element_by_tag_name("pre")
#
# browser.close()
# from browsermobproxy import Server
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# CHROMEDRIVER_PATH = 'C:\\Users\\User\\.wdm\\drivers\\chromedriver\\83.0.4103.39\\win32\\chromedriver.exe'
# caps = DesiredCapabilities.CHROME
# caps['loggingPrefs'] = {'performance': 'ALL'}
# # caps['goog:loggingPrefs'] = { 'performance':'ALL' }
#
# options = webdriver.ChromeOptions()
# options.set_capability( "goog:loggingPrefs", caps['loggingPrefs'] )
# driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, desired_capabilities=caps, options=options)
# driver.get(URL)
# browser_log = driver.get_log('performance')
# driver.get_log('network')
#
#
# caps = DesiredCapabilities.FIREFOX
#
# caps['loggingPrefs'] = {'performance': 'ALL'}
# driver = webdriver.Firefox(desired_capabilities=caps)
# driver.get(URL)
# browser_log = driver.get_log('performance')
# driver.get_log('network')
#
#
#
# from browsermobproxy import Server
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# CHROMEDRIVER_PATH = 'C:\\Users\\User\\.wdm\\drivers\\chromedriver\\83.0.4103.39\\win32\\chromedriver.exe'
# caps = DesiredCapabilities.CHROME
# caps['loggingPrefs'] = {'performance': 'ALL'}
#
# server = Server("C:\\ProgramData\\Miniconda3\\envs\\covad19sim\\Lib\\site-packages\\browsermobproxy\\browsermob-proxy-2.1.4\\bin\\browsermob-proxy.bat")
# server.start()
# proxy = server.create_proxy()
#
# # Configure the browser proxy in chrome options
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
# browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, desired_capabilities=caps, chrome_options = chrome_options)
#
# #tag the har(network logs) with a name
# proxy.new_har("datadashboard.health.gov.il")
# browser.get(URL)
# print(proxy.har)
# browser.close()
# proxy.close()
