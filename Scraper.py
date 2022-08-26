import json
from tkinter import W
from matplotlib.pyplot import text
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver import ActionChains
import re


# Global variables:

url = 'https://rpp.rpdata.com/rpp/dashboard.html?execution=e4s1'

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

def get_suburbs(url : str, suburb_list : list):

    driver = webdriver.Chrome()

    driver.get(url)

    element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "firstAddressLink"))
        )

    search_bar = driver.find_element(By.CLASS_NAME,'floatLeft.searchArrow.ui-autocomplete-input.defaultText')

    all_suburbs = []

    for suburb in suburb_list:

        search_bar.send_keys(suburb)

        element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'ui-menu-item')))

        sleep(1)

        results = driver.find_elements(By.CLASS_NAME,'ui-menu-item')

        for result in results:

            result_text = result.text

            if 'VIC' in result_text:

                all_suburbs.append(result_text)

                print(result_text)
                print('Saved')
            else:

                print('Not Processed')

                pass

        search_bar.clear()

    with open('Available Suburbs.json') as f:

        data = json.load(f)

    with open('Available Suburbs.json', 'w') as f:

        data['Available Suburbs'].append(all_suburbs)

        json.dump(data, f, indent=2)


def get_properties_info(url : str, suburbs : list):

    driver = webdriver.Chrome()

    driver.get(url)

    element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "firstAddressLink"))
        )

    for suburb in suburbs:

        search_bar = driver.find_element(By.CLASS_NAME, 'floatLeft.searchArrow.ui-autocomplete-input.defaultText')

        search_btn = driver.find_element(By.ID, 'firstAddressLink')

        search_bar.send_keys(suburb)

        search_btn.click()

        element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "clickable"))
            )

        properties = driver.find_elements(By.CLASS_NAME ,'clickable')

        for i in range(len(properties)):

            prop = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[6]/div[1]/div[%d]/div/div[3]/div[1]/h2/a' % (i+3))

            action = ActionChains(driver)

            driver.execute_script("arguments[0].scrollIntoView(true);", prop)

            action.context_click(prop).perform()

            prop_url = prop.get_attribute('href')

            print(prop_url)

            with open('Properties.json') as f:

                prop_data = json.load(f)

            is_scraped = False

            for property in prop_data['Properties']:

                if prop_url in property['URL']:
                    is_scraped = True
                    break
                else:
                    pass

            print(is_scraped)

            if is_scraped:
                print(f'URL: {prop_url} already scraped')
                continue

            prop = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[6]/div[1]/div[%d]/div/div[3]/div[1]/h2/a' % (i+3))

            prop.click()

            element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "overview"))
            )
            
            try:

                property_type = driver.find_element(By.CLASS_NAME, 'overviewDetails-li').text.replace('Property Type: ', '')
            
            except Exception as e:

                property_type = driver.find_element(By.CLASS_NAME, 'overviewDetails').text.replace('Property Type: ', '')

            address = driver.find_element(By.ID, 'expandedAddress_icons').text

            bedrooms = driver.find_element(By.CLASS_NAME, 'attribute.bedroom').text

            bathrooms = driver.find_element(By.CLASS_NAME, 'attribute.bathroom').text

            car_spaces = driver.find_element(By.CLASS_NAME, 'attribute.carspace').text
    
            land_size_approx = driver.find_element(By.CLASS_NAME, 'attribute.landAreaEst').text

            try:

                owners_list = driver.find_element(By.CLASS_NAME, 'lastVert')
                owners = [owner.text for owner in owners_list.find_elements(By.TAG_NAME, 'strong')]
            
            except Exception as e:
                print(e)
                owners = []
            
            owners_num = None
            mult_one_or_no_owner = ''
            owners_str = ''

            if len(owners) > 1:
                
                owners_num = len(owners)
                mult_one_or_no_owner = 'Multiple owners'

                for owner in owners:

                    owners_str += ', ' + owner

            elif len(owners) == 1:

                owners_num = 1
                mult_one_or_no_owner = 'One owner'

                owners_str = owners[0]

            else:

                owners_num = 0
                mult_one_or_no_owner = 'No Owner'

                owners_str = 'Not specified'

            #Legar description:

            legal_panel = driver.find_element(By.ID, 'legalPanel')

            legal_data = legal_panel.find_elements(By.TAG_NAME,'li')

            legal_data_list = [item.text for item in legal_data] 

            legal_data_str = ''

            for item in legal_data_list:

                legal_data_str += item + '\n'

            #Last sale price

            last_sale_panel = driver.find_element(By.ID, 'lastSalePanel')

            last_sale_data = last_sale_panel.find_elements(By.TAG_NAME, 'li')

            try:

                last_sale_price = last_sale_data[0].text.replace('Sale Price: ', '')

            except Exception as e:
                print(e)
                last_sale_price = 'No info available'

            try:

                last_sale_date = last_sale_data[1].text.replace('Sale Date:', '')

                if last_sale_date == '':
                    last_sale_date = 'No info available'

            except Exception as e:
                print(e)
                last_sale_date = 'No info available'

            patt = r' VIC [0-9]*'

            property_info = {
                'Address' : re.sub(patt, '', address).replace('Road','Rd').replace('Street', 'St'),
                'URL' : prop_url,
                'Suburb': re.sub(patt, '', suburb),
                'Property Type': property_type,
                'Number of Bedrooms' : bedrooms,
                'Number of Bathrooms' : bathrooms,
                'Number of Car Spaces' : car_spaces,
                'Approx. Land Size' : land_size_approx,
                'Multiple Owners / One Owner / No Owner' : mult_one_or_no_owner,
                'Number of Owners' : owners_num,
                'Owner/s name' : owners_str,
                'Legal Data' : legal_data_str, 
                'Last Sale Price' : last_sale_price,
                'Last Sale Date' : last_sale_date
            }

            print(property_info)

            prop_data['Properties'].append(property_info)

            with open('Properties.json', 'w') as f:
                
                json.dump(prop_data, f, indent=4)

            driver.back()

        
        next_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[6]/div[1]/div[23]/div[1]/div[3]/div/div/ul/li[6]')
        
        next_btn.click()



with open('Available Suburbs.json') as f:

    get_properties_info(url, json.load(f)['Available Suburbs'])