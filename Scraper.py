import json
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

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

    search_bar = driver.find_element_by_class_name('floatLeft.searchArrow.ui-autocomplete-input.defaultText')

    all_suburbs = []

    for suburb in suburb_list:

        search_bar.send_keys(suburb)

        element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'ui-menu-item')))

        sleep(1)

        results = driver.find_elements_by_class_name('ui-menu-item')

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

    search_bar = driver.find_element_by_class_name('floatLeft.searchArrow.ui-autocomplete-input.defaultText')

    properties_info = []

    for suburb in suburbs:

        search_btn = driver.find_element_by_id('firstAddressLink')

        search_bar.send_keys(suburb)

        search_btn.click()

        element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "clickable"))
            )

        properties = driver.find_elements_by_class_name('thumbnail.noPhoto.clickable')
        
        properties_click = [prop.find_element_by_tag_name('a') for prop in properties]

        for i in range(len(properties_click)):

            driver.execute_script('arguments[0].click();', properties_click[i])

            element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "overviewDetails-li"))
            )

            property_type = driver.find_element_by_class_name('overviewDetails-li').text.replace('Property Type: ', '')
            
            address = driver.find_element_by_id('expandedAddress_icons').text

            bedrooms = driver.find_element_by_class_name('attribute.bedroom').text

            bathrooms = driver.find_element_by_class_name('attribute.bathroom').text

            car_spaces = driver.find_element_by_class_name('attribute.carspace').text
    
            land_size_approx = driver.find_element_by_class_name('attribute.landAreaEst').text

            try:

                owners_list = driver.find_element_by_class_name('lastVert')
                owners = [owner.text for owner in owners_list.find_element_by_tag_name('strong')]
            
            except Exception:
                print(Exception)
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

            legal_panel = driver.find_element_by_id('legalPanel')

            legal_data = legal_panel.find_elements_by_tag_name('li')

            try:

                rpd = legal_data[0].replace('RPD: ', '')

            except Exception:

                rpd = 'No info available'

            try:

                vol_fol = legal_data[1].replace('Vol/Fol: ', '')

            except Exception:

                vol_fol = 'No info available'

            try:

                la = legal_data[2].replace('LA: ', '')

            except Exception:

                la = 'No info available'

            try:

                issue_date = legal_data[3].replace('Issue Date: ', '')

            except Exception:

                issue_date = 'No info available'

            #Last sale price

            last_sale_panel = driver.find_element_by_id('lastSalePanel')

            last_sale_data = last_sale_panel.find_element_by_tag_name('li')

            try:

                last_sale_price = last_sale_data[0].replace('Sale Price: ', '')

            except Exception:

                last_sale_price = 'No info available'

            try:

                last_sale_date = last_sale_data[1].replace('Sale Date: ', '')

            except Exception:

                last_sale_date = 'No info available'

            property_info = {
                'Address' : address,
                'URL' : prop_url,
                'Property Type': property_type,
                'Number of Bedrooms' : bedrooms,
                'Number of Bathrooms' : bathrooms,
                'Number of Car Spaces' : car_spaces,
                'Approx. Land Size' : land_size_approx,
                'Multiple Owners / One Owner / No Owner' : mult_one_or_no_owner,
                'Number of Owners' : owners_num,
                'Owner/s name' : owners_str,
                'RPD' : rpd,
                'Vol/Fol' : vol_fol,
                'LA' : la,
                'Issue Date' : issue_date,
                'Last Sale Price' : last_sale_price,
                'Last Sale Date' : last_sale_date
            }

            print(property_info)

            properties_info.append(property_info)

            driver.back()

        
        next_btn = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[6]/div[1]/div[23]/div[1]/div[3]/div/div/ul/li[6]')
        
        next_btn.click()



with open('Available Suburbs.json') as f:

    get_properties_info(url, json.load(f)['Available Suburbs'])