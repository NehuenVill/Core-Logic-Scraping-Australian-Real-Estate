import json
from matplotlib.font_manager import json_dump
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Global variables:

url = 'https://access-api.corelogic.asia/access/loginPage.html'

suburb_list = ['RICHMOND',
                'COBURG',
                'GEELONG',
                'KNOXFIELD',
                'MONTMORENCY',
                'BURWOOD EAST',
                'CLIFTON HILL',
                'ALBERT PARK',
                'ASHBURTON',
                'MURRUMBEENA',
                'SURREY HILLS',
                'BALWYN',
                'BALWYN NORTH',
                'KEW',
                'FOREST HILL',
                'CAULFIELD SOUTH',
                'DONCASTER',
                'TEMPLESTOWE LOWER',
                'BEAUMARIS',
                'VERMONT',
                'MOUNT WAVERLEY',
                'GLEN WAVERLY',
                'BENTLEIGH EAST',
                'KEW EAST',
                'HAMPTON',
                'FITZROY',
                'PARKDALE',
                'ELWOOD',
                'BRIGHTON',
                'MOUNT MARTHA',
                'ST KILDA',
                'EAST GEELONG',
                'MORNINGTON',
                'SEAFORD',
                'ALTONA',
                'WILIAMSTOWN',
                'CHELTNAM',
                'CHADSTONE',
                'BLACK ROCK',
                'BRIGHTON',
                'CLAYTON',
                'ST ANDREWS BEACH',
                'SORRENTO',
                'DROMANA',
                'ROSEBUD',
                'RYE',
                'TORQUAY',
                'ASPENDALE',
                'EDITHVALE',
                'MENTONE',
                'CHELSEA',
                'BON BEACH',
                'SANDRINGHAM',
                'East Geelong',
                'Belmont',
                'Herne Hill',
                'Norlane',
                'Newtown',
                'BROOKLYN',
                'NEWPORT',
                'BURWOOD EAST',
                'BURWOOD',
                'CLIFTON HILL',
                'KNOXFIELD']

def get_suburbs(url, suburb_list):

    driver = webdriver.Chrome()

    driver.get(url)

    element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "firstAddressLink"))
        )

    search_bar = driver.find_element_by_class_name('floatLeft.searchArrow.ui-autocomplete-input.defaultText')

    all_suburbs = []

    for suburb in suburb_list:

        search_bar.send_keys(suburb)

        results = driver.find_elements_by_class_name('ui-menu-item')

        for result in results:

            result_text = result.text

            if suburb + ' VIC' in result_text:

                all_suburbs.append(result_text)
            else:

                pass

        search_bar.clear()

    with open('sites_scraped.json') as f:

        data = json.load(f)

    with open('sites_scraped.json', 'w') as f:

        data['Available Suburbs'].append(all_suburbs)

        json.dump(data, f, indent=2)


def get_properties_info(url, suburbs):

    driver = webdriver.Chrome()

    driver.get(url)

    element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "firstAddressLink"))
        )

    search_bar = driver.find_element_by_class_name('floatLeft.searchArrow.ui-autocomplete-input.defaultText')

    for suburb in suburbs['Available Suburbs']:

        search_btn = driver.find_element_by_id('addressLink')

        search_bar.send_keys(suburb)

        search_btn.click()

        properties = driver.find_elements_by_class_name('clickable')

        for prop in properties:

            prop.click()

            
        




# search bar.sendkeys(state), for res in results(.ui-menu-item): find state + 'VIC', save_all, send_keys(for each res),
# click search(#addressLink), find all (.clickable).url save, driver.get(url), suburb = res, 
# property type = .overviewDetails-li.rep(proptype, ''), adress = #expandedAddress_icons, 