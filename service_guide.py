import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
import requests
import pandas as pd

# ------------------------------------------------------------------------------------------------------
service_code = {'통합공공임대' : 'RH112', '영구임대' : 'RH103', '국민임대' : 'RH104', '장기전세' : 'RH105',
                '공공임대' : 'RH106', '전세임대' : 'RH107', '행복주택' : 'RH108', '공공지원민간임대' : 'RH109',
                '주거복지동주택' : 'RH110', '공공기숙사' : 'RH111'}

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
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36")

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

    return driver

class total_public:
    def __init__(self):
        self.url_set = URL + service_code['통합공공임대']

    def homeless_houshold_note(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ------- 무주택세대구성원 ----------------------------------------------------------------------------------------------------
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
        house_hold_df.to_csv('./data/service_guide/total_public/homeless_household_note.csv', index=False, encoding='utf-8')
        # ----------------------------------------------------------------------------------------------------------------------
        driver.close()

    def median_income_table(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 가구원수별 기준 중위 소득-------------------------------------------------------------------------------------------
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
        # -----------------------------------------------------------------------------------------------------------------

        # ----- 자산가액 ---------------------------------------------------------------------------------------------------
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
                                       "criteria_money" : asset_criteria_money, "criteria_extra" : asset_criteria_extra})

        asset_value_df.to_csv('./data/service_guide/total_public/median_income_extra.csv', index=False, encoding='utf-8')
        # ----------------------------------------------------------------------------------------------------------------
        driver.close()

    def income_asset_cal(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 소득, 자산 산정 방법 ----------------------------------------------------------------------------------------
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
        # -----------------------------------------------------------------------------------------------------------------
        driver.close()

    def normal_supply_qul_choose(self):
        driver = selenium_set(self)
        driver.get(self.url_set)
        # ----- 일반공급 입주자격 및 입주자 선정방법 -----------------------------------------------------------------------------
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
        # ------------------------------------------------------------------------------------------------------------------
        driver.close()

    def priority_supply_qualification(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 우선공급 입주자격 ---------------------------------------------------------------------------------------------
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
        # -------------------------------------------------------------------------------------------------------------------
        driver.close()

    def prio_points(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 우선공급 경쟁시 입주자 선정방법 ---------------------------------------------------------------------------------------------
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
        # -------------------------------------------------------------------------------------------------------------------
        driver.close()

    def moving_in_selection_criteria(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 입주자 선정 기준 ---------------------------------------------------------------------------------------------
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

        # -------------------------------------------------------------------------------------------------------------------
        driver.close()
    def lease_condition(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 임대조건 ---------------------------------------------------------------------------------------------

        st_mid_income = [driver.find_element_by_xpath(
            '//*[@id="sub_content"]/div[8]/div[4]/ul/li/table/tbody/tr/td[1]').text]
        under_30 = [driver.find_element_by_xpath('//*[@id="sub_content"]/div[8]/div[4]/ul/li/table/tbody/tr/td[2]').text]
        c_30_50 = [driver.find_element_by_xpath('//*[@id="sub_content"]/div[8]/div[4]/ul/li/table/tbody/tr/td[3]').text]
        c_50_70 = [driver.find_element_by_xpath('//*[@id="sub_content"]/div[8]/div[4]/ul/li/table/tbody/tr/td[4]').text]
        c_70_100 = [driver.find_element_by_xpath('//*[@id="sub_content"]/div[8]/div[4]/ul/li/table/tbody/tr/td[5]').text]
        c_100_130 = [driver.find_element_by_xpath('//*[@id="sub_content"]/div[8]/div[4]/ul/li/table/tbody/tr/td[6]').text]
        c_130_150 = [driver.find_element_by_xpath('//*[@id="sub_content"]/div[8]/div[4]/ul/li/table/tbody/tr/td[7]').text]

        lease_condition = pd.DataFrame({'st_mid_income': st_mid_income,
                                        'under_30%': under_30,
                                        '30_50%': c_30_50,
                                        '50_70%': c_50_70,
                                        '70_100%': c_70_100,
                                        '100_130%': c_100_130,
                                        '130_150%': c_130_150})

        lease_condition.to_csv('./data/service_guide/total_public/lease_condition.csv', index=False, encoding='utf-8')
        # -------------------------------------------------------------------------------------------------------------------
        driver.close()

    def apply_step(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 신청절차 ---------------------------------------------------------------------------------------------
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
        apply_step.to_csv('./data/service_guide/total_public/apply_step.csv', index=False, encoding='utf-8')

        # -------------------------------------------------------------------------------------------------------------------
        driver.close()

class permanent_lease:
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
        # ----- 임대조건 ---------------------------------------------------------------------------------------------
        lease_condition = ['시중시세의 30% 수준']

        lease_condition_df = pd.DataFrame({'condition': lease_condition})
        lease_condition_df.to_csv('./data/service_guide/permanent_lease/lease_condition.csv', index=False,
                                  encoding='utf-8')
        # --------------------------------------------------------------------------------------------------------------

    def apply_step(self):
        driver = selenium_set(self)
        driver.get(self.url_set)

        # ----- 신청절차 ---------------------------------------------------------------------------------------------
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
        apply_step.to_csv('./data/service_guide/permanent_lease/apply_step.csv', index=False, encoding='utf-8')

        # -------------------------------------------------------------------------------------------------------------------
        driver.close()

if __name__ == '__main__':
    url_set = URL + service_code['영구임대']
    
    driver = selenium_set()
    driver.get(url_set)

    # -----  ---------------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------------------------------------------
    driver.close()