import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib.request

# ------------------------------------------------------------------------------------------------------
service_code = {'통합공공임대' : 'RH112', '영구임대' : 'RH103', '국민임대' : 'RH104',
                '장기전세' : 'RH105', '공공임대' : 'RH106', '전세임대' : 'RH107',
                '행복주택' : 'RH108', '공공지원민간임대' : 'RH109', '주거복지동주택' : 'RH110',
                '공공기숙사' : 'RH111'}

URL = "https://www.myhome.go.kr/hws/portal/cont/selectContRentalView.do#guide="
# ------------------------------------------------------------------------------------------------------

def selenium_set():
    print(f"{'-'*5}Chrome Driver Check{'-'*5}")
    # chrome driver version check
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

    # chrome driver option settings
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('headless') # headless 모드 설정
    options.add_argument("disable-gpu")
    options.add_argument("window-size=1440x900")
    options.add_argument(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36")

    prefs = {'profile.default_content_setting_values': {'cookies' : 2, 'images': 2, 'plugins' : 2,
                                                        'popups': 2,
                                                        'geolocation': 2, 'notifications' : 2,
                                                        'auto_select_certificate': 2,
                                                        'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2,
                                                        'media_stream' : 2,
                                                        'media_stream_mic' : 2, 'media_stream_camera': 2,
                                                        'protocol_handlers' : 2,
                                                        'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2,
                                                        'push_messaging' : 2,
                                                        'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2,
                                                        'protected_media_identifier': 2,
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

    return driver

class Total_Public:
    def __init__(self):
        self.url_set = URL + service_code['통합공공임대']

    def homeless_houshold_note(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ------- 무주택세대구성원 ----------------------------------------------------------------------------------------
        household_member = []
        household_note = []

        homeless_household_member_table = driver.find_element_by_xpath(
            '//*[@id="sub_content"]/div[3]/div/ul/li[1]/ul/li[2]/table')
        homeless_household_member_table_tbody = homeless_household_member_table.find_element_by_tag_name('tbody')

        for tr in homeless_household_member_table_tbody.find_elements_by_tag_name('tr')[:5]:
            household_member.append(tr.find_element_by_tag_name('th').get_attribute('innerText'))
            for td in tr.find_elements_by_tag_name('td')[:1]:
                household_note.append(td.get_attribute('innerText'))

        for i in range(len(household_member)):
            household_member[i] = household_member[i].replace('\n', ', ')

        household_note.insert(2, household_note[2])

        house_hold_df = pd.DataFrame({"member": household_member, "note": household_note})
        house_hold_df.to_csv('./data/service_guide/total_public/homeless_household_note.csv',
                             index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------
        driver.close()

    def median_income_table(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 가구원수별 기준 중위 소득-----------------------------------------------------------------------------------
        household_num = []
        household_num_1 = []
        median_income_100 = []
        median_income_100_1 = []
        median_income_150 = []
        median_income_150_1 = []

        household_num.append(driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[3]/div/ul/li[2]/div/div/table/tbody/tr/th[1]'))
        median_income_100.append(driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[3]/div/ul/li[2]/div/div/table/tbody/tr/th[2]'))
        median_income_150.append(driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[3]/div/ul/li[2]/div/div/table/tbody/tr/th[3]'))

        for i in range(len(household_num[0])):
            household_num_1.append(household_num[0][i].text)
            median_income_100_1.append(median_income_100[0][i].text)
            median_income_150_1.append(median_income_150[0][i].text)

        median_income_df = pd.DataFrame({"member_num": household_num_1, "median_income(100%)": median_income_100_1,
                                         "median_income(150%)": median_income_150_1})
        median_income_df.to_csv('./data/service_guide/total_public/household_num_median_income.csv',
                                index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------

        # ----- 자산가액 -------------------------------------------------------------------------------------------------
        asset_value = []
        asset_criteria = []
        asset_criteria_money = []
        asset_criteria_extra = []

        total_asset = driver.find_element_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li[2]/div/div/span[3]').text
        tmp1 = total_asset[:7]
        tmp1 = tmp1.replace('(', '')
        tmp1 = tmp1.replace(')', '')
        asset_value.append(tmp1)
        asset_criteria.append(total_asset[8:])

        car_asset = driver.find_element_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li[2]/div/div/span[5]').text
        tmp1 = car_asset[:7]
        tmp1 = tmp1.replace('(', '')
        tmp1 = tmp1.replace(')', '')
        asset_value.append(tmp1[:7])
        asset_criteria.append(car_asset[8:])

        asset_criteria_money.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li[2]/div/div/strong[1]').text)
        asset_criteria_money.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li[2]/div/div/strong[2]').text)

        asset_criteria_extra.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li[2]/div/div/span[4]').text)
        asset_criteria_extra.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li[2]/div/div/span[6]').text)

        asset_value_df = pd.DataFrame({"type" : asset_value, "criteria" : asset_criteria,
                                       "criteria_money" : asset_criteria_money,
                                       "criteria_extra" : asset_criteria_extra})

        asset_value_df.to_csv('./data/service_guide/total_public/median_income_extra.csv',
                              index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------
        driver.close()

    def income_asset_cal(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 소득, 자산 산정 방법 --------------------------------------------------------------------------------------
        asset_class = []
        how_cal = []

        asset_class.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li/table/tbody/tr[1]/th').text)
        asset_class.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li/table/tbody/tr[2]/th[2]').text)
        asset_class.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li/table/tbody/tr[3]/th').text)
        asset_class.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li/table/tbody/tr[4]/th').text)
        asset_class.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li/table/tbody/tr[5]/th').text)
        asset_class.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li/table/tbody/tr[6]/th').text)

        how_cal = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li/table/tbody/tr/td')

        for i in range(len(how_cal)):
            how_cal[i] = how_cal[i].text
            how_cal[i] = how_cal[i].replace('\n', '')

        income_asset_cal = pd.DataFrame({"class": asset_class, "how": how_cal})
        income_asset_cal.to_csv('./data/service_guide/total_public/income_asset_cal.csv', index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------
        driver.close()

    def normal_supply_qul_choose(self):
        driver = selenium_set(self)
        driver.get(self.url_set)
        # ----- 일반공급 입주자격 및 입주자 선정방법 -------------------------------------------------------------------------
        normal_supply_class = []
        moving_in_qualification = []
        how_choose = []

        normal_supply_class = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[5]/div/ul/li/table/tbody/tr/th')
        for i in range(len(normal_supply_class)):
            normal_supply_class[i] = normal_supply_class[i].text
            normal_supply_class[i] = normal_supply_class[i].replace('\n', '')

        moving_in_qualification = driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[5]/div/ul/li/table/tbody/tr/td[1]')
        for i in range(len(moving_in_qualification)):
            moving_in_qualification[i] = moving_in_qualification[i].text
            moving_in_qualification[i] = moving_in_qualification[i].replace('\n', '')
            moving_in_qualification[i] = moving_in_qualification[i].replace('     ', ' ')

        how_choose = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[5]/div/ul/li/table/tbody/tr/td[2]')
        for i in range(len(how_choose)):
            how_choose[i] = how_choose[i].text

        normal_supply_qul_choose_df = pd.DataFrame({"class": normal_supply_class,
                                                    "qualification": moving_in_qualification,
                                                    "how_choose": how_choose})
        normal_supply_qul_choose_df.to_csv('./data/service_guide/total_public/normal_supply_qual_choose.csv',
                                           index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------
        driver.close()

    def priority_supply_qualification(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 우선공급 입주자격 -----------------------------------------------------------------------------------------
        prio_supply_class = []
        prio_supply_qual = []

        prio_supply_class = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[6]/div/ul/li/table/tbody/tr/th')

        for i in range(len(prio_supply_class)):
            prio_supply_class[i] = prio_supply_class[i].text
            prio_supply_class[i] = prio_supply_class[i].replace('\n', '')

        prio_supply_qual = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[6]/div/ul/li/table/tbody/tr/td')

        for i in range(len(prio_supply_qual)):
            prio_supply_qual[i] = prio_supply_qual[i].text
            prio_supply_qual[i] = prio_supply_qual[i].replace('\n\n', '')
            prio_supply_qual[i] = prio_supply_qual[i].replace('\n    ', '')

        prio_supply_df = pd.DataFrame({"class": prio_supply_class, "qualification": prio_supply_qual})
        prio_supply_df.to_csv('./data/service_guide/total_public/priorty_supply_qualification.csv',
                              index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------
        driver.close()

    def prio_points(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 우선공급 경쟁시 입주자 선정방법 ------------------------------------------------------------------------------
        point_item = []
        plus_point_3 = []
        plus_point_2 = []
        plus_point_1 = []
        minus_point_5 = []
        minus_point_3 = []

        point_item = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[7]/div/ul/li/table/tbody/tr/td[1]')

        for i in range(len(point_item)):
            point_item[i] = point_item[i].text
            point_item[i] = point_item[i].replace('\n    ', '')

        plus_point_3 = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[7]/div/ul/li/table/tbody/tr/td[2]')

        for i in range(len(plus_point_3)):
            plus_point_3[i] = plus_point_3[i].text

        plus_point_2 = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[7]/div/ul/li/table/tbody/tr/td[3]')

        for i in range(len(plus_point_2)):
            plus_point_2[i] = plus_point_2[i].text
            plus_point_2[i] = plus_point_2[i].replace('\n', ' ')

        plus_point_1 = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[7]/div/ul/li/table/tbody/tr/td[4]')

        for i in range(len(plus_point_1)):
            plus_point_1[i] = plus_point_1[i].text
            plus_point_1[i] = plus_point_1[i].replace('\n', ' ')

        minus_point_5 = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[7]/div/ul/li/table/tbody/tr/td[5]')

        for i in range(len(minus_point_5)):
            minus_point_5[i] = minus_point_5[i].text

        minus_point_3 = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[7]/div/ul/li/table/tbody/tr/td[6]')

        for i in range(len(minus_point_3)):
            minus_point_3[i] = minus_point_3[i].text

        prio_points_df = pd.DataFrame({"item": point_item, "plus_3": plus_point_3, "plus_2": plus_point_2,
                                       "plus_1": plus_point_1, "minus_5": minus_point_5, "minus_3": minus_point_3})

        prio_points_df.to_csv('./data/service_guide/total_public/prio_points.csv', index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------
        driver.close()

    def moving_in_selection_criteria(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 입주자 선정 기준 ------------------------------------------------------------------------------------------
        supply_item = []
        item = []
        item_des = []

        supply_item = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[8]/div[1]/ul/li')
        for i in range(len(supply_item)):
            supply_item[i] = supply_item[i].text
            item.append(supply_item[i][:4])
            item_des.append(supply_item[i][7:])

        selection_criteria_df = pd.DataFrame({"supply": item, "supply_selection": item_des})
        selection_criteria_df.to_csv('./data/service_guide/total_public/moving_in_seleciton_criteria.csv',
                                     index=False, encoding='utf-8')

        # --------------------------------------------------------------------------------------------------------------
        driver.close()
    def lease_condition(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 임대조건 -------------------------------------------------------------------------------------------------

        st_mid_income = [driver.find_element_by_xpath(
            '//*[@id="sub_content"]/div[8]/div[4]/ul/li/table/tbody/tr/td[1]').text]
        under_30 = [driver.find_element_by_xpath(
            '//*[@id="sub_content"]/div[8]/div[4]/ul/li/table/tbody/tr/td[2]').text]
        c_30_50 = [driver.find_element_by_xpath(
            '//*[@id="sub_content"]/div[8]/div[4]/ul/li/table/tbody/tr/td[3]').text]
        c_50_70 = [driver.find_element_by_xpath(
            '//*[@id="sub_content"]/div[8]/div[4]/ul/li/table/tbody/tr/td[4]').text]
        c_70_100 = [driver.find_element_by_xpath(
            '//*[@id="sub_content"]/div[8]/div[4]/ul/li/table/tbody/tr/td[5]').text]
        c_100_130 = [driver.find_element_by_xpath(
            '//*[@id="sub_content"]/div[8]/div[4]/ul/li/table/tbody/tr/td[6]').text]
        c_130_150 = [driver.find_element_by_xpath(
            '//*[@id="sub_content"]/div[8]/div[4]/ul/li/table/tbody/tr/td[7]').text]

        lease_condition = pd.DataFrame({'st_mid_income': st_mid_income,
                                        'under_30%': under_30,
                                        '30_50%': c_30_50,
                                        '50_70%': c_50_70,
                                        '70_100%': c_70_100,
                                        '100_130%': c_100_130,
                                        '130_150%': c_130_150})

        lease_condition.to_csv('./data/service_guide/total_public/lease_condition.csv',
                               index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------
        driver.close()

    def apply_step(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 신청절차 -------------------------------------------------------------------------------------------------
        step = []
        step_des = []

        step = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[8]/div[5]/ul/li/ul/li/dl/dt')
        for i in range(len(step)):
            step[i] = step[i].text
            step[i] = step[i].replace('\n', ' ')

        step_des = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[8]/div[5]/ul/li/ul/li/dl/dd')
        for i in range(len(step_des)):
            step_des[i] = step_des[i].text
            step_des[i] = step_des[i].replace('\n  ', '')
            step_des[i] = step_des[i].replace('\n', ' ')

        apply_step = pd.DataFrame({"step": step, "describe": step_des})
        apply_step.to_csv('./data/service_guide/total_public/apply_step.csv',
                          index=False, encoding='utf-8')

        # --------------------------------------------------------------------------------------------------------------
        driver.close()

class Permanent_Lease:
    def __init__(self):
        self.url_set = URL + service_code['영구임대']

    def homeless_houshold_note(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ------- 무주택세대구성원 ----------------------------------------------------------------------------------------
        household_member = []
        household_note = []

        homeless_household_member_table = driver.find_element_by_xpath(
            '//*[@id="sub_content"]/div[3]/div/ul/li[1]/ul/li[2]/table')
        homeless_household_member_table_tbody = homeless_household_member_table.find_element_by_tag_name('tbody')

        for tr in homeless_household_member_table_tbody.find_elements_by_tag_name('tr')[:5]:
            household_member.append(tr.find_element_by_tag_name('th').get_attribute('innerText'))
            for td in tr.find_elements_by_tag_name('td')[:1]:
                household_note.append(td.get_attribute('innerText'))

        for i in range(len(household_member)):
            household_member[i] = household_member[i].replace('\n', ', ')

        household_note.insert(2, household_note[2])

        house_hold_df = pd.DataFrame({"member": household_member, "note": household_note})
        house_hold_df.to_csv('./data/service_guide/permanent_lease/homeless_household_note.csv',
                             index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------
        driver.close()
    def moving_in_qual_rank(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 입주자격 및 선정순위 ---------------------------------------------------------------------------------------
        rank = []
        moving_in_qual = []
        note = []

        tmp = driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li/table/tbody/tr[1]/th').text
        for i in range(3):
            rank.append(tmp)

        tmp = driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li/table/tbody/tr[4]/th[2]').text
        for i in range(9):
            rank.append(tmp)

        tmp = driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li/table/tbody/tr[13]/th').text
        for i in range(3):
            rank.append(tmp)

        moving_in_qual = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li/table/tbody/tr/td[1]')
        for i in range(len(moving_in_qual)):
            moving_in_qual[i] = moving_in_qual[i].text
            moving_in_qual[i] = moving_in_qual[i].replace('\n   ', '')

        note = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li/table/tbody/tr/td[2]')
        for i in range(len(note)):
            note[i] = note[i].text
            note[i] = note[i].replace('\n  ', '')
            note[i] = note[i].replace('\n', ' ')

        moving_in_qual_rank = pd.DataFrame({'rank': rank, 'qualification': moving_in_qual, 'note': note})
        moving_in_qual_rank.to_csv('./data/service_guide/permanent_lease/moving_in_qual_rank.csv',
                                   index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------
        driver.close()

    def lease_condtion(self):
        # ----- 임대조건 -------------------------------------------------------------------------------------------------
        lease_condition = ['시중시세의 30% 수준']

        lease_condition_df = pd.DataFrame({'condition': lease_condition})
        lease_condition_df.to_csv('./data/service_guide/permanent_lease/lease_condition.csv', index=False,
                                  encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------

    def apply_step(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 신청절차 -------------------------------------------------------------------------------------------------
        step = []
        step_des = []

        step = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[8]/div/ul/li/ul/li/dl/dt')
        for i in range(len(step)):
            step[i] = step[i].text
            step[i] = step[i].replace('\n', ' ')

        step_des = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[8]/div/ul/li/ul/li/dl/dd')
        for i in range(len(step_des)):
            step_des[i] = step_des[i].text
            step_des[i] = step_des[i].replace('\n  ', '')
            step_des[i] = step_des[i].replace('\n', ' ')

        apply_step = pd.DataFrame({"step": step, "describe": step_des})
        apply_step.to_csv('./data/service_guide/permanent_lease/apply_step.csv',
                          index=False, encoding='utf-8')

        # --------------------------------------------------------------------------------------------------------------
        driver.close()

class Kukmin_Lease:
    def __init__(self):
        self.url_set = URL + service_code['국민임대']

    def homeless_houshold_note(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ------- 무주택세대구성원 ----------------------------------------------------------------------------------------
        household_member = []
        household_note = []

        homeless_household_member_table = driver.find_element_by_xpath(
            '//*[@id="sub_content"]/div[3]/div/ul/li[1]/ul/li[2]/table')
        homeless_household_member_table_tbody = homeless_household_member_table.find_element_by_tag_name('tbody')

        for tr in homeless_household_member_table_tbody.find_elements_by_tag_name('tr')[:5]:
            household_member.append(tr.find_element_by_tag_name('th').get_attribute('innerText'))
            for td in tr.find_elements_by_tag_name('td')[:1]:
                household_note.append(td.get_attribute('innerText'))

        for i in range(len(household_member)):
            household_member[i] = household_member[i].replace('\n', ', ')

        household_note.insert(2, household_note[2])

        house_hold_df = pd.DataFrame({"member": household_member, "note": household_note})
        house_hold_df.to_csv('./data/service_guide/kukmin_lease/homeless_household_note.csv', index=False,
                             encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------
        # ------- 소득 전년도 도시근로자 -----------------------------------------------------------------------------------
        household_mem_num = []
        month_avg_income_100 = []
        month_avg_income_50 = []
        month_avg_income_70 = []

        household_mem_num = driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[3]/div/ul/li[2]/div/div/table/tbody/tr/th[1]')
        for i in range(len(household_mem_num)):
            household_mem_num[i] = household_mem_num[i].text

        month_avg_income_100 = driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[3]/div/ul/li[2]/div/div/table/tbody/tr/th[2]')
        for i in range(len(month_avg_income_100)):
            month_avg_income_100[i] = month_avg_income_100[i].text

        month_avg_income_50 = driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[3]/div/ul/li[2]/div/div/table/tbody/tr/th[3]')
        for i in range(len(month_avg_income_50)):
            month_avg_income_50[i] = month_avg_income_50[i].text

        month_avg_income_70 = driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[3]/div/ul/li[2]/div/div/table/tbody/tr/th[4]')
        for i in range(len(month_avg_income_70)):
            month_avg_income_70[i] = month_avg_income_70[i].text

        income_df = pd.DataFrame({"mem_num": household_mem_num, "month_avg_income(100%)": month_avg_income_100,
                                  "month_avg_income(50%)": month_avg_income_50,
                                  "month_avg_income(70%)": month_avg_income_70})

        income_df.to_csv('./data/service_guide/kukmin_lease/month_avg_income.csv',
                         index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------

        # ----- 자산가액 -------------------------------------------------------------------------------------------------
        asset_value = []
        asset_criteria = []
        asset_criteria_money = []
        asset_criteria_extra = []

        total_asset = driver.find_element_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li[2]/div/div/span[3]').text
        tmp1 = total_asset[:7]
        tmp1 = tmp1.replace('(', '')
        tmp1 = tmp1.replace(')', '')
        asset_value.append(tmp1)
        asset_criteria.append(total_asset[8:])

        car_asset = driver.find_element_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li[2]/div/div/span[5]').text
        tmp1 = car_asset[:7]
        tmp1 = tmp1.replace('(', '')
        tmp1 = tmp1.replace(')', '')
        asset_value.append(tmp1[:7])
        asset_criteria.append(car_asset[8:])

        asset_criteria_money.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li[2]/div/div/strong[2]').text)
        asset_criteria_money.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li[2]/div/div/strong[3]').text)

        asset_criteria_extra.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li[2]/div/div/span[4]').text)
        asset_criteria_extra.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li[2]/div/div/span[6]').text)

        asset_value_df = pd.DataFrame({"type": asset_value, "criteria": asset_criteria,
                                       "criteria_money": asset_criteria_money, "criteria_extra": asset_criteria_extra})

        asset_value_df.to_csv('./data/service_guide/kukmin_lease/month_avg_income_extra.csv',
                              index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------
        driver.close()

    def income_asset_cal(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 소득, 자산 산정 방법 --------------------------------------------------------------------------------------
        asset_class = []
        how_cal = []

        asset_class.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li/table/tbody/tr[1]/th').text)
        asset_class.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li/table/tbody/tr[2]/th[2]').text)
        asset_class.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li/table/tbody/tr[3]/th').text)
        asset_class.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li/table/tbody/tr[4]/th').text)
        asset_class.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li/table/tbody/tr[5]/th').text)
        asset_class.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li/table/tbody/tr[6]/th').text)

        how_cal = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li/table/tbody/tr/td')

        for i in range(len(how_cal)):
            how_cal[i] = how_cal[i].text
            how_cal[i] = how_cal[i].replace('\n', '')

        income_asset_cal = pd.DataFrame({"class": asset_class, "how": how_cal})
        income_asset_cal.to_csv('./data/service_guide/kukmin_lease/income_asset_cal.csv',
                                index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------

        driver.close()

    def normal_supply_qul_choose(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 일반공급 입주자격 및 입주자 선정방법 -------------------------------------------------------------------------
        normal_supply_class = []
        moving_in_qualification = []
        rank = []

        normal_supply_class = driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[5]/div/ul/li/table/tbody/tr/th')
        for i in range(len(normal_supply_class)):
            normal_supply_class[i] = normal_supply_class[i].text
            normal_supply_class[i] = normal_supply_class[i].replace('\n', '')

        moving_in_qualification = driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[5]/div/ul/li/table/tbody/tr/td[1]')
        for i in range(len(moving_in_qualification)):
            moving_in_qualification[i] = moving_in_qualification[i].text
            moving_in_qualification[i] = moving_in_qualification[i].replace('\n', '')
            moving_in_qualification[i] = moving_in_qualification[i].replace('     ', ' ')

        rank = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[5]/div/ul/li/table/tbody/tr/td[2]')
        for i in range(len(rank)):
            rank[i] = rank[i].text
            rank[i] = rank[i].replace('\n', '')
            rank[i] = rank[i].replace('            ', '')

        normal_supply_qul_choose_df = pd.DataFrame({"class": normal_supply_class,
                                                    "qualification": moving_in_qualification,
                                                    "rank": rank})
        normal_supply_qul_choose_df.to_csv('./data/service_guide/kukmin_lease/normal_supply_qual_choose.csv',
                                           index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------

    def priority_supply_qualification(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 우선공급 입주자격 -----------------------------------------------------------------------------------------
        prio_supply_class = []
        prio_supply_qual = []

        prio_supply_class = driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[6]/div/ul/li[1]/table/tbody/tr/th')

        for i in range(len(prio_supply_class)):
            prio_supply_class[i] = prio_supply_class[i].text
            prio_supply_class[i] = prio_supply_class[i].replace('\n', '')

        prio_supply_qual = driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[6]/div/ul/li[1]/table/tbody/tr/td')

        for i in range(len(prio_supply_qual)):
            prio_supply_qual[i] = prio_supply_qual[i].text
            prio_supply_qual[i] = prio_supply_qual[i].replace('\n\n', '')
            prio_supply_qual[i] = prio_supply_qual[i].replace('\n    ', '')
            prio_supply_qual[i] = prio_supply_qual[i].replace('\n', ' ')

        prio_supply_df = pd.DataFrame({"class": prio_supply_class, "qualification": prio_supply_qual})
        prio_supply_df.to_csv('./data/service_guide/kukmin_lease/priorty_supply_qualification.csv',
                              index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------
        # ----- 신혼부부 -------------------------------------------------------------------------------------------------
        class_new_marriage = []
        how_choose = []

        class_new_marriage = driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[6]/div/ul/li[2]/table/tbody/tr/th')

        for i in range(len(class_new_marriage)):
            class_new_marriage[i] = class_new_marriage[i].text

        how_choose = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[6]/div/ul/li[2]/table/tbody/tr/td')
        for i in range(len(how_choose)):
            how_choose[i] = how_choose[i].text
            how_choose[i] = how_choose[i].replace('\n   ', ' ')
            how_choose[i] = how_choose[i].replace('\n\n', ' ')
            how_choose[i] = how_choose[i].replace('\n', ' ')

        case_new_marriage = pd.DataFrame({"class": class_new_marriage, "how_choose": how_choose})
        case_new_marriage.to_csv('./data/service_guide/kukmin_lease/case_new_marriage.csv',
                                 index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------
        driver.close()

    def moving_in_selection_criteria(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # -----일반 공급 대상자 입주자 선정기준-------------------------------------------------------------------------------
        img_1 = driver.find_element_by_xpath(
            '//*[@id="sub_content"]/div[8]/div/ul/li/ul/li[1]/div[1]/img').get_attribute('src')
        urllib.request.urlretrieve(img_1, './data/service_guide/kukmin_lease/nor_under_50m^2_house.jpg')

        img_2 = driver.find_element_by_xpath(
            '//*[@id="sub_content"]/div[8]/div/ul/li/ul/li[1]/div[2]/img').get_attribute('src')
        urllib.request.urlretrieve(img_2, './data/service_guide/kukmin_lease/nor_over_50m^2_house.jpg')
        driver.close()
        # --------------------------------------------------------------------------------------------------------------

        # ---- 우선공급 대상자 입주가 선정기준 -------------------------------------------------------------------------------
        class_prio = []
        class_area = []
        selection_procedure = []
        note = []

        tmp = driver.find_element_by_xpath(
            '//*[@id="sub_content"]/div[8]/div/ul/li/ul/li[2]/table/tbody/tr[1]/th').text
        tmp = tmp.replace('\n', ' ')
        class_prio.append(tmp)
        class_prio.append(tmp)

        tmp = driver.find_element_by_xpath(
            '//*[@id="sub_content"]/div[8]/div/ul/li/ul/li[2]/table/tbody/tr[3]/th').text
        class_prio.append(tmp)
        class_prio.append(tmp)

        tmp = driver.find_element_by_xpath(
            '//*[@id="sub_content"]/div[8]/div/ul/li/ul/li[2]/table/tbody/tr[5]/th').text
        tmp = tmp.replace('\n', ' ')
        class_prio.append(tmp)
        class_prio.append(tmp)

        class_area = driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[8]/div/ul/li/ul/li[2]/table/tbody/tr/td[1]')
        for i in range(len(class_area)):
            class_area[i] = class_area[i].text

        selection_procedure = driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[8]/div/ul/li/ul/li[2]/table/tbody/tr/td[2]')
        for i in range(len(selection_procedure)):
            selection_procedure[i] = selection_procedure[i].text

        prio_selection_criteria = pd.DataFrame({"class": class_prio, "area": class_area,
                                                "selection_step": selection_procedure})
        prio_selection_criteria.to_csv('./data/service_guide/kukmin_lease/prio_selection_criteria.csv',
                                       index=False, encoding='utf-8')
        # ------------------------------------------------------------------------------------------------------------------
        driver.close()

    def lease_condition(self):
        lease_condition = ['시중시세의 60~80% 수준']
        lease_condition_df = pd.DataFrame({"condition": lease_condition})
        lease_condition_df.to_csv('./data/service_guide/kukmin_lease/lease_condition.csv',
                                  index=False, encoding='utf-8')

    def apply_step(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 신청절차 ---------------------------------------------------------------------------------------------
        step = []
        step_des = []

        step = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[9]/div[4]/ul/li/ul/li/dl/dt')
        for i in range(len(step)):
            step[i] = step[i].text
            step[i] = step[i].replace('\n', ' ')

        step_des = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[9]/div[4]/ul/li/ul/li/dl/dd')
        for i in range(len(step_des)):
            step_des[i] = step_des[i].text
            step_des[i] = step_des[i].replace('\n  ', '')
            step_des[i] = step_des[i].replace('\n', ' ')

        apply_step = pd.DataFrame({"step": step, "describe": step_des})
        apply_step.to_csv('./data/service_guide/kukmin_lease/apply_step.csv',
                          index=False, encoding='utf-8')

        # --------------------------------------------------------------------------------------------------------------
        driver.close()

class Long_Term_Rent:
    def __init__(self):
        self.url_set = URL + service_code['장기전세']

    def about_deposit(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ------- 임대보증금 수준 ---------------------------------------------------------------------------------------
        deposit_des = []

        deposit_des.append(driver.find_element_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li').text)

        for i in range(len(deposit_des)):
            deposit_des[i] = deposit_des[i].replace('\n', '')

        about_deposit = pd.DataFrame({"deposit": deposit_des})

        about_deposit.to_csv('./data/service_guide/long_term_rent/about_deposit.csv',
                             index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------

        driver.close()

    def homeless_houshold_note(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ------- 무주택세대구성원 ----------------------------------------------------------------------------------------
        household_member = []
        household_note = []

        homeless_household_member_table = driver.find_element_by_xpath(
            '//*[@id="sub_content"]/div[4]/div/ul/li[1]/ul/li[2]/table')
        homeless_household_member_table_tbody = homeless_household_member_table.find_element_by_tag_name('tbody')

        for tr in homeless_household_member_table_tbody.find_elements_by_tag_name('tr')[:5]:
            household_member.append(tr.find_element_by_tag_name('th').get_attribute('innerText'))
            for td in tr.find_elements_by_tag_name('td')[:1]:
                household_note.append(td.get_attribute('innerText'))

        for i in range(len(household_member)):
            household_member[i] = household_member[i].replace('\n', ', ')

        household_note.insert(2, household_note[2])

        house_hold_df = pd.DataFrame({"member": household_member, "note": household_note})
        house_hold_df.to_csv('./data/service_guide/long_term_rent/homeless_household_note.csv',
                             index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------

        driver.close()
    def income_criteria(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ------- 소득 - 1 ---------------------------------------------------------------------------------------
        income_class = []
        income_des = []

        income_class = driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[4]/div/ul/li[2]/div/div/table[1]/tbody/tr/th')

        for i in range(len(income_class)):
            income_class[i] = income_class[i].text
            income_class[i] = income_class[i].replace('\n', ' ')

        income_des = driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[4]/div/ul/li[2]/div/div/table[1]/tbody/tr/td')

        for i in range(len(income_des)):
            income_des[i] = income_des[i].text
            income_des[i] = income_des[i].replace('\n', '')

        income_by_area = pd.DataFrame({"class": income_class, "description": income_des})
        income_by_area.to_csv('./data/service_guide/long_term_rent/income_by_area.csv',
                              index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------

        # ------- 소득 전년도 도시근로자 -----------------------------------------------------------------------------------
        household_mem_num = []
        month_avg_income_100 = []
        month_avg_income_50 = []
        month_avg_income_70 = []

        household_mem_num = driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[4]/div/ul/li[2]/div/div/table[2]/tbody/tr/th[1]')
        for i in range(len(household_mem_num)):
            household_mem_num[i] = household_mem_num[i].text

        month_avg_income_100 = driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[4]/div/ul/li[2]/div/div/table[2]/tbody/tr/th[2]')
        for i in range(len(month_avg_income_100)):
            month_avg_income_100[i] = month_avg_income_100[i].text

        month_avg_income_50 = driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[4]/div/ul/li[2]/div/div/table[2]/tbody/tr/th[3]')
        for i in range(len(month_avg_income_50)):
            month_avg_income_50[i] = month_avg_income_50[i].text

        month_avg_income_70 = driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[4]/div/ul/li[2]/div/div/table[2]/tbody/tr/th[4]')
        for i in range(len(month_avg_income_70)):
            month_avg_income_70[i] = month_avg_income_70[i].text

        income_df = pd.DataFrame({"mem_num": household_mem_num, "month_avg_income(100%)": month_avg_income_100,
                                  "month_avg_income(50%)": month_avg_income_50,
                                  "month_avg_income(70%)": month_avg_income_70})

        income_df.to_csv('./data/service_guide/long_term_rent/month_avg_income.csv',
                         index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------

        # ----- extra -------------------------------------------------------------------------------------------------
        asset_criteria = []
        asset_criteria_money = []
        asset_criteria_extra = []

        for i in [3, 5]:
            asset_criteria.append(driver.find_element_by_xpath(
                f'//*[@id="sub_content"]/div[4]/div/ul/li[2]/div/div/span[{i}]').text)

        for i in [1, 2]:
            asset_criteria_money.append(driver.find_element_by_xpath(
                f'//*[@id="sub_content"]/div[4]/div/ul/li[2]/div/div/strong[{i}]').text)

        for i in [4, 6]:
            asset_criteria_extra.append(driver.find_element_by_xpath(
                f'//*[@id="sub_content"]/div[4]/div/ul/li[2]/div/div/span[{i}]').text)

        asset_value_df = pd.DataFrame({"criteria": asset_criteria, "criteria_money": asset_criteria_money,
                                       "criteria_extra": asset_criteria_extra})

        asset_value_df.to_csv('./data/service_guide/long_term_rent/month_avg_income_extra.csv',
                              index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------
        driver.close()

    def priority_supply_qualification(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 우선공급 입주자격 -----------------------------------------------------------------------------------------
        prio_supply_class = []
        prio_supply_qual = []

        prio_supply_class = driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[5]/div/ul/li[1]/table/tbody/tr/th')

        for i in range(len(prio_supply_class)):
            prio_supply_class[i] = prio_supply_class[i].text
            prio_supply_class[i] = prio_supply_class[i].replace('\n', '')

        prio_supply_qual = driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[5]/div/ul/li[1]/table/tbody/tr/td')

        for i in range(len(prio_supply_qual)):
            prio_supply_qual[i] = prio_supply_qual[i].text
            prio_supply_qual[i] = prio_supply_qual[i].replace('\n\n', '')
            prio_supply_qual[i] = prio_supply_qual[i].replace('\n    ', '')
            prio_supply_qual[i] = prio_supply_qual[i].replace('\n', ' ')

        prio_supply_df = pd.DataFrame({"class": prio_supply_class, "qualification": prio_supply_qual})
        prio_supply_df.to_csv('./data/service_guide/long_term_rent/priorty_supply_qualification.csv',
                              index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------
        # ----- 신혼부부 -------------------------------------------------------------------------------------------------
        class_new_marriage = []
        how_choose = []

        class_new_marriage = driver.find_elements_by_xpath(
            '//*[@id="sub_content"]/div[5]/div/ul/li[2]/table/tbody/tr/th')

        for i in range(len(class_new_marriage)):
            class_new_marriage[i] = class_new_marriage[i].text

        how_choose = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[5]/div/ul/li[2]/table/tbody/tr/td')
        for i in range(len(how_choose)):
            how_choose[i] = how_choose[i].text
            how_choose[i] = how_choose[i].replace('\n   ', ' ')
            how_choose[i] = how_choose[i].replace('\n\n', ' ')
            how_choose[i] = how_choose[i].replace('\n', ' ')

        case_new_marriage = pd.DataFrame({"class": class_new_marriage, "how_choose": how_choose})
        case_new_marriage.to_csv('./data/service_guide/long_term_rent/case_new_marriage.csv',
                                 index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------

        driver.close()

class Public_Lease:
    def __init__(self):
        self.url_set = URL + service_code['공공임대']

    def housing_type(self):
        driver = selenium_set()
        driver.get(self.url_set)

        # ----- 주택 유형 -----------------------------------------------------------------------------------------
        type = []
        type_des = []

        tmp = driver.find_element_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li[1]').text

        type.append(tmp[:13])
        type_des.append(tmp[16:])

        tmp = driver.find_element_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li[2]').text

        type.append(tmp[:8])
        type_des.append(tmp[11:])

        housing_type = pd.DataFrame({"type": type, "description": type_des})
        housing_type.to_csv("./data/service_guide/public_lease/housing_type.csv",
                            index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------

        driver.close()

    def moving_in_selection_rank(self):
        driver = selenium_set()
        driver.get(self.url_set)

        # ----- 입주자 선정 순위 -----------------------------------------------------------------------------------------
        rank = []
        qual = []

        rank = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li/table/tbody/tr/th')
        for i in range(len(rank)):
            rank[i] = rank[i].text

        qual = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li/table/tbody/tr/td')
        for i in range(len(qual)):
            qual[i] = qual[i].text
            qual[i] = qual[i].replace('\n                    ', '')
            qual[i] = qual[i].replace('\n          ', '')
            qual[i] = qual[i].replace('\n', '')

        moving_in_selection_rank = pd.DataFrame({"rank": rank, "qualification": qual})
        moving_in_selection_rank.to_csv("./data/service_guide/public_lease/moving_in_selection_rank.csv",
                                        index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------

        driver.close()
    def sepcial_supply(self):
        driver = selenium_set()
        driver.get(self.url_set)

        # ----- 특별공급 -----------------------------------------------------------------------------------------
        classification = []
        ratio = []
        qual = []

        classification = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[5]/div/ul/li/table/tbody/tr/th')
        for i in range(len(classification)):
            classification[i] = classification[i].text
            classification[i] = classification[i].replace('\n', ' ')

        ratio = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[5]/div/ul/li/table/tbody/tr/td[1]')
        for i in range(len(ratio)):
            ratio[i] = ratio[i].text

        qual = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[5]/div/ul/li/table/tbody/tr/td[2]')
        for i in range(len(qual)):
            qual[i] = qual[i].text
            qual[i] = qual[i].replace('\n', ' ')

        special_supply = pd.DataFrame({"class": classification, "ratio": ratio, "qual": qual})
        special_supply.to_csv("./data/service_guide/public_lease/special_supply.csv",
                              index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------

    def lease_condition(self):
        # ----- 임대조건 -----------------------------------------------------------------------------------------
        con = ['시중 전세 시세의 90% 수준']

        lease_condition = pd.DataFrame({'condition': con})
        lease_condition.to_csv('./data/service_guide/public_lease/lease_condition.csv',
                               index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------

    def apply_step(self):
        driver = selenium_set()
        driver.get(self.url_set)

        # ----- 신청절차 -----------------------------------------------------------------------------------------
        step = []
        step_des = []

        step = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[6]/div[4]/ul/li/ul/li/dl/dt')
        for i in range(len(step)):
            step[i] = step[i].text
            step[i] = step[i].replace('\n', ' ')

        step_des = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[6]/div[4]/ul/li/ul/li/dl/dd')
        for i in range(len(step_des)):
            step_des[i] = step_des[i].text
            step_des[i] = step_des[i].replace('\n  ', '')
            step_des[i] = step_des[i].replace('\n', ' ')

        apply_step = pd.DataFrame({"step": step, "describe": step_des})
        apply_step.to_csv('./data/service_guide/public_lease/apply_step.csv',
                          index=False, encoding='utf-8')

        # --------------------------------------------------------------------------------------------------------------

        driver.close()

class Deposit_Lease:
    def __init__(self):
        self.url_set = URL + service_code['전세임대']

    def moving_in_subject(self):
        driver = selenium_set()
        driver.get(self.url_set)

        # ----- 입주 대상 -----------------------------------------------------------------------------------------
        big_class = ['기존주택 전세임대', '기존주택 전세임대', '기존주택 전세임대', '기존주택 전세임대', '기존주택 전세임대',
                     '기존주택 전세임대', '청년 전세임대', '신혼부부 전세임대', '신혼부부 전세임대', '소년소녀가정 등 전세지원',
                     '소년소녀가정 등 전세지원', '소년소녀가정 등 전세지원', '소년소녀가정 등 전세지원', '소년소녀가정 등 전세지원',
                     '소년소녀가정 등 전세지원', ]

        small_class = []
        des = []

        small_class = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li/table/tbody/tr/th')
        for i in range(len(small_class)):
            small_class[i] = small_class[i].text
            small_class[i] = small_class[i].replace('\n', ' ')

        print(small_class)

        small_class.remove('기존주택 전세임대')
        small_class.remove('청년 전세임대')
        small_class.remove('신혼부부 전세임대')
        small_class.remove('소년소녀가정 등 전세지원')

        print(small_class)

        des = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li/table/tbody/tr/td')
        for i in range(len(des)):
            des[i] = des[i].text
            des[i] = des[i].replace('\n            ', ' ')
            des[i] = des[i].replace('             ', '')
            des[i] = des[i].replace('\n', ' ')

        moving_in_subject = pd.DataFrame({'class_1': big_class, 'class_2': small_class, 'description': des})
        moving_in_subject.to_csv('./data/service_guide/deposit_lease/moving_in_subject.csv',
                                 index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------

        driver.close()

    def house_object(self):
        driver = selenium_set()
        driver.get(self.url_set)

        # ----- 대상 주택 -----------------------------------------------------------------------------------------
        object = []
        note = []

        object.append(driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div[1]/ul/li').text)
        note.append(driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div[1]/ul/li/span').text)

        object[0] = object[0].replace(note[0], '')

        house_object = pd.DataFrame({"object": object, 'note': note})
        house_object.to_csv('./data/service_guide/deposit_lease/house_object.csv',
                            index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------

        driver.close()

    def deposit_support_limit(self):
        driver = selenium_set()
        driver.get(self.url_set)

        # ----- 전세금지원 한도액 -----------------------------------------------------------------------------------------
        money = []
        note = []

        money.append(driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div[2]/ul/li/strong').text)
        note.append(driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div[2]/ul/li/span').text)

        deposit_support_limit = pd.DataFrame({"money": money, "note": note})
        deposit_support_limit.to_csv('./data/service_guide/deposit_lease/deposit_support_limit.csv',
                                     index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------

        driver.close()

    def lease_condition(self):
        driver = selenium_set()
        driver.get(self.url_set)

        # ----- 임대조건 -----------------------------------------------------------------------------------------
        con = []
        des = []
        note = []

        tmp = driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div[3]/ul/li[1]').text
        con.append(tmp[:5])
        des.append(tmp[8:])
        note.append(None)

        tmp = driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div[3]/ul/li[2]').text
        tmp_note = driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div[3]/ul/li[2]/span').text

        tmp = tmp.replace(tmp_note, '')
        con.append(tmp[:4])
        des.append(tmp[7:])
        note.append(tmp_note)

        lease_condition = pd.DataFrame({'condition': con, 'description': des, 'note': note})
        lease_condition.to_csv('./data/service_guide/deposit_lease/lease_condition.csv',
                               index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------

        driver.close()

    def lease_term(self):
        driver = selenium_set()
        driver.get(self.url_set)

        # ----- 임대기간 -----------------------------------------------------------------------------------------
        term = []
        note = []

        tmp = driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div[4]/ul/li').text
        tmp_note = driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div[4]/ul/li/span').text

        tmp = tmp.replace(tmp_note, '')

        term.append(tmp)
        note.append(tmp_note)

        lease_term = pd.DataFrame({'term': term, 'note': note})
        lease_term.to_csv('./data/service_guide/deposit_lease/lease_term.csv',
                          index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------
        driver.close()

    def how_apply(self):
        driver = selenium_set()
        driver.get(self.url_set)

        # ----- 신청방법 -----------------------------------------------------------------------------------------
        sub = []
        how = []

        sub = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[4]/div[5]/ul/li/table/tbody/tr/th')
        for i in range(len(sub)):
            sub[i] = sub[i].text

        how = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[4]/div[5]/ul/li/table/tbody/tr/td')
        for i in range(len(how)):
            how[i] = how[i].text
            how[i] = how[i].replace('\n', ' ')

        how_apply = pd.DataFrame({'subject': sub, 'how_apply': how})
        how_apply.to_csv('./data/service_guide/deposit_lease/how_apply.csv',
                         index=False, encoding='utf-8')

        # --------------------------------------------------------------------------------------------------------------

        driver.close()

class Happy_House:
    def __init__(self):
        self.url_set = URL + service_code['행복주택']

    def feature_def(self):
        driver = selenium_set()
        dirver.get(self.url_set)

        # ----- 특장점 -----------------------------------------------------------------------------------------
        feature = []
        note = []

        tmp = driver.find_element_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li/ul/li[2]').text
        tmp_note = driver.find_element_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li/ul/li[2]/span').text
        tmp = tmp.replace(tmp_note, '')
        tmp = tmp.replace('\n', '')
        tmp = tmp.replace('· ', '')
        tmp_note = tmp_note.replace('- ', '')
        feature.append(tmp)
        note.append(tmp_note)

        tmp = driver.find_element_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li/ul/li[3]').text
        tmp_note = driver.find_element_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li/ul/li[3]/span').text
        tmp = tmp.replace(tmp_note, '')
        tmp = tmp.replace('\n', '')
        tmp = tmp.replace('· ', '')
        tmp_note = tmp_note.replace('- ', '')
        feature.append(tmp)
        note.append(tmp_note)

        tmp = driver.find_element_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li/ul/li[4]').text
        tmp_note = driver.find_element_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li/ul/li[4]/span').text
        tmp = tmp.replace(tmp_note, '')
        tmp = tmp.replace('\n', '')
        tmp = tmp.replace('· ', '')
        tmp_note = tmp_note.replace('- ', '')
        feature.append(tmp)
        note.append(tmp_note)

        feature = pd.DataFrame({"feature": feature, "note": note})
        feature.to_csv('./data/service_guide/happy_house/feature.csv',
                       index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------
        # ----- 행복 vs 공공 -----------------------------------------------------------------------------------------
        classification = []
        happy = []
        public_lease = []
        kukmin_lease = []
        per_lease = []

        classification = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li/table/tbody/tr/th')
        for i in range(len(classification)):
            classification[i] = classification[i].text

        happy = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li/table/tbody/tr/td[1]')
        for i in range(len(happy)):
            happy[i] = happy[i].text
            happy[i] = happy[i].replace('\n', ' ')

        public_lease = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li/table/tbody/tr/td[2]')
        for i in range(len(public_lease)):
            public_lease[i] = public_lease[i].text

        kukmin_lease = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li/table/tbody/tr/td[3]')
        for i in range(len(kukmin_lease)):
            kukmin_lease[i] = kukmin_lease[i].text
            kukmin_lease[i] = kukmin_lease[i].replace('\n', ' ')

        per_lease = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[3]/div/ul/li/table/tbody/tr/td[4]')
        for i in range(len(per_lease)):
            per_lease[i] = per_lease[i].text
            per_lease[i] = per_lease[i].replace('\n', ' ')

        vs_table = pd.DataFrame({'class': classification, 'happy': happy, 'public_lease(10yr)': public_lease,
                                 'kukmin_lease': kukmin_lease, 'permanent_lease': per_lease})

        vs_table.to_csv('./data/service_guide/happy_house/vs_table.csv',
                        index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------

        driver.close()

    def qualification_def(self):
        driver = selenium_set()
        dirver.get(self.url_set)

        # ----- 입주 자격 -----------------------------------------------------------------------------------------
        classification = ['대학생', '취업준비생', '청년 계층', '신혼부부', '예비신혼부부', '한부모가족', '고령자', '주거급여 수급자',
                          '산업단지근로자']
        qual = []
        income_cri = []

        qual.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li[1]/table/tbody/tr[1]/td[1]').text)
        qual.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li[1]/table/tbody/tr[2]/td').text)
        qual.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li[1]/table/tbody/tr[3]/td[1]').text)
        qual.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li[1]/table/tbody/tr[4]/td[1]').text)
        qual.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li[1]/table/tbody/tr[5]/td').text)
        qual.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li[1]/table/tbody/tr[6]/td').text)
        qual.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li[1]/table/tbody/tr[7]/td[1]').text)
        qual.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li[1]/table/tbody/tr[8]/td[1]').text)
        qual.append(
            driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li[1]/table/tbody/tr[9]/td[1]').text)

        for i in range(len(qual)):
            qual[i] = qual[i].replace('\n ', '')
            qual[i] = qual[i].replace('\n', ' ')

        tmp = driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li[1]/table/tbody/tr[1]/td[2]').text
        tmp = tmp.replace('\n  ', ' ')
        income_cri.append(tmp)
        income_cri.append(tmp)

        tmp = driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li[1]/table/tbody/tr[3]/td[2]').text
        tmp = tmp.replace('\n  ', ' ')
        income_cri.append(tmp)

        tmp = driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li[1]/table/tbody/tr[4]/td[2]').text
        tmp = tmp.replace('\n  ', ' ')
        income_cri.append(tmp)
        income_cri.append(tmp)
        income_cri.append(tmp)

        tmp = driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li[1]/table/tbody/tr[7]/td[2]').text
        tmp = tmp.replace('\n  ', ' ')
        tmp = tmp.replace('\n', ' ')
        income_cri.append(tmp)

        tmp = driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li[1]/table/tbody/tr[8]/td[2]').text
        tmp = tmp.replace('\n  ', ' ')
        tmp = tmp.replace('\n', ' ')
        income_cri.append(tmp)

        tmp = driver.find_element_by_xpath('//*[@id="sub_content"]/div[4]/div/ul/li[1]/table/tbody/tr[9]/td[2]').text
        tmp = tmp.replace('\n  ', ' ')
        tmp = tmp.replace('\n', ' ')
        income_cri.append(tmp)

        moving_in_qual = pd.DataFrame({'class': classification, 'qualification': qual, 'income_criteria': income_cri})

        moving_in_qual.to_csv('./data/service_guide/happy_house/moving_in_qual.csv',
                              index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------

        driver.close()

    def max_living_term(self):
        driver = selenium_set()
        dirver.get(self.url_set)

        # ----- 최대 거주 기간 -----------------------------------------------------------------------------------------
        qual = []
        max_term = []

        qual = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[5]/div[3]/table/tbody/tr/th')
        for i in range(len(qual)):
            qual[i] = qual[i].text

        max_term = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[5]/div[3]/table/tbody/tr/td')
        for i in range(len(max_term)):
            max_term[i] = max_term[i].text

        max_term_df = pd.DataFrame({'qualification': qual, 'max_term': max_term})
        max_term_df.to_csv('./data/service_guide/happy_house/max_term.csv',
                           index=False, encoding='utf-8')

        # --------------------------------------------------------------------------------------------------------------

    def lease_condition(self):
        # ----- 임대 조건 -----------------------------------------------------------------------------------------
        lease_con = ['공급대상자별 시중시세의 60~80%']
        lease_condition = pd.DataFrame({'condition': lease_con})
        lease_condition.to_csv('./data/service_guide/happy_house/lease_condition.csv',
                               index=False, encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------
    def apply_step(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 신청절차 -------------------------------------------------------------------------------------------------
        step = []
        step_des = []

        step = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[5]/div[5]/ul/li/ul/li/dl/dt')
        for i in range(len(step)):
            step[i] = step[i].text
            step[i] = step[i].replace('\n', ' ')

        step_des = driver.find_elements_by_xpath('//*[@id="sub_content"]/div[5]/div[5]/ul/li/ul/li/dl/dd')
        for i in range(len(step_des)):
            step_des[i] = step_des[i].text
            step_des[i] = step_des[i].replace('\n  ', '')
            step_des[i] = step_des[i].replace('\n', ' ')

        apply_step = pd.DataFrame({"step": step, "describe": step_des})
        apply_step.to_csv('./data/service_guide/happy_house/apply_step.csv',
                          index=False, encoding='utf-8')

        # --------------------------------------------------------------------------------------------------------------
        driver.close()

if __name__ == '__main__':
    url_set = URL + service_code['행복주택']
    
    driver = selenium_set()
    driver.get(url_set)

    # ----- 신청절차 -------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------------------
    driver.close()