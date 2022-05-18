import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
import requests
import pandas as pd

print(f"{'-'*5}Chrome Driver Check{'-'*5}")
# chrome driver version check
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

# chrome driver option settings
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('headless') # headless 모드 설정
options.add_argument("disable-gpu")
options.add_argument("window-size=1440x900")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36")

prefs = {'profile.default_content_setting_values': {'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2,
                                                            'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2,
                                                            'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2,
                                                            'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2,
                                                            'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2,
                                                            'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2,
                                                            'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}
options.add_experimental_option('prefs', prefs)

# chrome driver autoinstaller
try:
    driver = webdriver.Chrome(f'./chromedriver/{chrome_ver}/chromedriver.exe', options = options)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./chromedriver/{chrome_ver}/chromedriver.exe', options = options)

driver.implicitly_wait(180)

print(f"{'-'*5}Crawler Ready{'-'*5}")

URL = "https://www.myhome.go.kr/hws/portal/mtx/selectFixesSportView.do?tySe=FIXES100"

driver.get(url=URL)

detail_content = []
welfare_name = []
welfare_des = []
lease_term = []
dedicated_area = []
lease_condition = []

detail_content = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[3]/div/div[2]/div[3]/div/div[2]/ul/li')

for i in range(len(detail_content)):
    welfare_name.append(driver.execute_script('return arguments[0].firstChild.textContent', detail_content[i]).strip())
    welfare_des.append(driver.execute_script('return arguments[0].childNodes[1].textContent', detail_content[i]).strip())
    lease_term.append(driver.execute_script('return arguments[0].childNodes[3].textContent', detail_content[i]).strip())
    dedicated_area.append(driver.execute_script('return arguments[0].childNodes[6].textContent', detail_content[i]).strip())
    lease_condition.append(driver.execute_script('return arguments[0].childNodes[9].textContent', detail_content[i]).strip())

for i in range(len(welfare_des)):
    welfare_des[i] = welfare_des[i].replace('\n\t\t\t', '')
    welfare_des[i] = welfare_des[i].replace('\t', '')



housing_welfare = pd.DataFrame({"title" : welfare_name[:6], "describe" : welfare_des[:6], "term" : lease_term[:6],
                                "dedicated_area" : dedicated_area[:6], "condition" : lease_condition[:6]})
housing_welfare.to_csv('./data/welfare_info/housing_welfare_service.csv', index = False, encoding="utf-8")

housing_support = pd.DataFrame({"title" : welfare_name[6:], "describe" : welfare_des[6:], "subject": lease_term[6:],
                                "support_description" : dedicated_area[6:], "how_apply": lease_condition[6:]})
housing_support.to_csv('./data/welfare_info/housing_support.csv', index = False, encoding="utf-8")

driver.close()