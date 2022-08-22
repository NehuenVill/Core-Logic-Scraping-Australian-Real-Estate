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

    properties_info = []

    for suburb in suburbs['Available Suburbs']:

        search_btn = driver.find_element_by_id('addressLink')

        search_bar.send_keys(suburb)

        search_btn.click()

        properties = driver.find_elements_by_class_name('clickable')

        for prop in properties:

            prop_url = prop.get_attribute('href')

            prop.click()

            property_type = driver.find_element_by_class_name('overviewDetails-li').text.replace('Property Type: ', '')
            
            address = driver.find_element_by_id('expandedAddress_icons').text

            bedrooms = driver.find_element_by_class_name('attribute.bedroom').text

            bathrooms = driver.find_element_by_class_name('attribute.bathroom').text

            car_spaces = driver.find_element_by_class_name('attribute.carspace').text
    
            land_size_approx = driver.find_element_by_class_name('attribute.landAreaEst').text

            owners_list = driver.find_element_by_class_name('lastVert')

            owners = [owner.text for owner in owners_list.find_element_by_tag_name('strong')]

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

            rpd = legal_data[0].replace('RPD: ', '')

            vol_fol = legal_data[1].replace('Vol/Fol: ', '')

            la = legal_data[2].replace('LA: ', '')

            issue_date = legal_data[3].replace('Issue Date: ', '')

            #Last sale price

            last_sale_panel = driver.find_element_by_id('lastSalePanel')

            last_sale_data = last_sale_panel.find_element_by_tag_name('li')

            last_sale_price = last_sale_data[0].replace('Sale Price: ', '')

            last_sale_date = last_sale_data[1].replace('Sale Date: ', '')

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

            properties_info.append(property_info)

            driver.back()

        
        next_btn = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[6]/div[1]/div[23]/div[1]/div[3]/div/div/ul/li[6]')
        
        next_btn.click()

