from dataclasses import replace
from email.mime import base
from enum import unique
import json
from matplotlib.font_manager import json_load
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver import ActionChains
import re
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


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


def get_links(url : str, suburbs : list):

    driver = webdriver.Chrome()

    driver.get(url)

    element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "firstAddressLink"))
        )

    for suburb in suburbs[97:]:
        
        try:

            search_bar = driver.find_element(By.CLASS_NAME, 'floatLeft.searchArrow.ui-autocomplete-input.defaultText')
        
        except NoSuchElementException:

            search_bar = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[3]/div[1]/div[3]/div[1]/div[1]/input')

        sleep(0.5)

        try:

            search_btn = driver.find_element(By.ID, 'firstAddressLink')
        
        except NoSuchElementException:

            search_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[3]/div[1]/div[3]/div[1]/a')

        search_bar.clear()

        sleep(0.5)

        search_bar.send_keys(suburb)

        sleep(0.3)
        
        search_btn.click()
        
        element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "clickable"))
            )
        
        checkbox = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[2]/div[2]/div[5]/div[1]/ul/li[1]/div/div[1]/div[2]/ul/li[2]/input')

        checkbox.click()

        refine_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[5]/div[1]/ul/li[1]/div/div[1]/a[1]')

        sleep(1)

        refine_btn.click()

        print('Visible')
        
        element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "spinner"))
            )

        element = WebDriverWait(driver, 30).until(
            EC.invisibility_of_element_located((By.ID, "spinner"))
            )

        print('Not visible')

        sleep(10)

        drop_down = wait_get_element(driver, (By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[6]/div[1]/div[1]/div[4]/div[1]/div[1]/span[1]'))

        drop_down.click()

        choice = wait_get_element(driver, (By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[6]/div[1]/div[1]/div[4]/div[1]/div[2]/ul/li[5]'))

        choice.click()

        print('Visible')
        
        element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "spinner"))
            )

        element = WebDriverWait(driver, 30).until(
            EC.invisibility_of_element_located((By.ID, "spinner"))
            )

        print('Not visible')

        sleep(10)

        try:
            
            properties = driver.find_elements(By.CSS_SELECTOR, 'a.clickable')

        except NoSuchElementException:

            continue

        # Start of experimental code:

        unique_addresses = []

        unique_hrefs = []

        while True:

            for i in range(len(properties)):

                try:

                    prop = wait_get_element(driver, (By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[6]/div[1]/div[%d]/div/div[3]/div[1]/h2/a' % (i+3)))

                except Exception as e:

                    print(e)
                    break

                full_addres = prop.text

                print(f' full addres: {full_addres}')

                add_patt = r'[0-9]*/'

                st_addres = re.sub(add_patt, '', full_addres)

                print(f'st add: {st_addres}')

                last_item = ''

                if unique_addresses:

                    last_item = re.sub(r'1-[0-9]* ', '', unique_addresses[len(unique_addresses)-1], 1)

                else:

                    last_item = ''

                print(f'last item: {last_item}')

                if st_addres in last_item:

                    units = re.search(r'([0-9]*/)', full_addres)

                    if units:
                        if unique_addresses:
                            unique_addresses.pop()
                        else:
                            pass

                        units = units.group(1).replace('/', '')

                        print(f'Number of units: {units}')

                        unique_addresses.append(f'1-{units} {st_addres}')

                else:
                    
                    units = re.search(r'([0-9]*/)', full_addres)

                    if units:

                        units = units.group(1).replace('/', '')

                        print(f'Number of units: {units}')

                        unique_addresses.append(f'1-{units} {st_addres}')

                    else:

                        unique_addresses.append(f'1-1 {st_addres}')

                    action = ActionChains(driver)

                    prop = wait_get_element(driver, (By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[6]/div[1]/div[%d]/div/div[3]/div[1]/h2/a' % (i+3)))
            
                    driver.execute_script("arguments[0].scrollIntoView(true);", prop)
                
                    prop = wait_get_element(driver, (By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[6]/div[1]/div[%d]/div/div[3]/div[1]/h2/a' % (i+3)))

                    action.context_click(prop).perform()
                
                    prop = wait_get_element(driver, (By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[6]/div[1]/div[%d]/div/div[3]/div[1]/h2/a' % (i+3)))

                    prop_url = prop.get_attribute('href')
                
                    print(f'prop URL: {prop_url}')
                
                    unique_hrefs.append(prop_url)

            try:
                try:
                    next_btn = wait_get_element(driver, (By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[6]/div[1]/div[53]/div[1]/div[3]/div/div/ul/li[6]'))
                except NoSuchElementException:
                    next_btn = wait_get_element(driver, (By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[6]/div[1]/div[53]/div[1]/div[3]/div/div/ul/li[5]'))

                driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)

                next_btn.click()

                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "spinner"))
                    )

                element = WebDriverWait(driver, 30).until(
                    EC.invisibility_of_element_located((By.ID, "spinner"))
                    )

            except Exception as e:

                print(e)

                break

        information = []

        for i in range(len(unique_addresses)):

            output = {
                'Addres' : unique_addresses[i],
                'Href' : unique_hrefs[i],
                'Suburb' : suburb
            }

            information.append(output)



        with open(f'{suburb}.json', 'w') as f:

            base_json ={
                    "Addresses and hrefs" : []
            }

            json.dump(base_json, f, indent=2)

        with open(f'{suburb}.json') as f:

            data = json.load(f)

        with open(f'{suburb}.json', 'w') as f:

            data['Addresses and hrefs'].append(information)

            json.dump(data, f, indent=2)


def get_properties_info(url : str, properties : list):
            
    # Algorith to extract information

    # Next: Adapt the code to scrape info from the hrefs of the json file with all the
    # unique addresses and hrefs, use the addresses as output.
    driver = webdriver.Chrome()

    driver.get(url)

    element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "firstAddressLink"))
        )

    for property in properties[6:]:

        main_window = driver.current_window_handle
  
        driver.execute_script(f"window.open(arguments[0], 'secondtab');", property['Href'])
        
        driver.switch_to.window("secondtab")
            
        element = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.ID, "overview"))
            )
            
        try:

            property_type = driver.find_element(By.CLASS_NAME, 'overviewDetails-li').text.replace('Property Type: ', '')
                
        except NoSuchElementException:

            property_type = driver.find_element(By.CLASS_NAME, 'overviewDetails').text.replace('Property Type: ', '')

            bedrooms = driver.find_element(By.CLASS_NAME, 'attribute.bedroom').text

            bathrooms = driver.find_element(By.CLASS_NAME, 'attribute.bathroom').text

            car_spaces = driver.find_element(By.CLASS_NAME, 'attribute.carspace').text
        try:
            land_size_approx = driver.find_element(By.CLASS_NAME, 'attribute.landAreaEst').text
        except NoSuchElementException:
            land_size_approx = '-'

        try:

            owners_list = driver.find_element(By.CLASS_NAME, 'lastVert')
            owners = [owner.text for owner in owners_list.find_elements(By.TAG_NAME, 'strong')]
                
        except Exception as e:
            
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

            legal_data_str += item + ', '

        #Last sale price

        last_sale_panel = driver.find_element(By.ID, 'lastSalePanel')

        last_sale_data = last_sale_panel.find_elements(By.TAG_NAME, 'li')

        try:
            last_sale_price = last_sale_data[0].text.replace('Sale Price: ', '')

        except Exception as e:
            
            last_sale_price = 'No info available'

        try:

            last_sale_date = last_sale_data[1].text.replace('Sale Date:', '')

            if last_sale_date == '':
                last_sale_date = 'No info available'
                    
        except Exception as e:
            
            last_sale_date = 'No info available'
        patt = r' VIC [0-9]*'

        suburb = re.sub(patt, '', property['Suburb'])

        patt_add = r', VIC, [0-9]*'

        address_op = re.sub(patt_add, '', property['Addres'])

        units_patt = r'(1-[0-9]*)'

        units_match = re.search(units_patt, address_op)

        units = units_match.group(1).replace('1-', '')

        property_info = {
                'Address' : address_op,
                'URL' : property['Href'],
                'Suburb': suburb,
                'Property Type': property_type,
                'Number of units' : units,
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

        with open('Properties.json') as f:

            prop_data = json.load(f)

            prop_data['Properties'].append(property_info)

        with open('Properties.json', 'w') as f:
                    
            json.dump(prop_data, f, indent=4)

        driver.close()

        driver.switch_to.window(main_window)

        WebDriverWait(driver, 40).until(EC.number_of_windows_to_be(1))       

def ref_click(driver, loc):

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(loc)).click()

def wait_get_element(driver, loc):

    return WebDriverWait(driver, 15).until(EC.presence_of_element_located(loc))


def save_props(Prop_data):

    df = pd.DataFrame(Prop_data, columns=['Address', 'URL', 'Suburb',
                                    'Property Type', 'Number of units', 'Number of Bedrooms',
                                    'Number of Bathrooms', 'Number of Car Spaces',
                                    'Approx. Land Size', 'Multiple Owners / One Owner / No Owner',
                                    'Number of Owners', 'Owner/s name', 'Legal Data',
                                    'Last Sale Price', 'Last Sale Date'])

    df.to_excel("Properties_sample.xlsx", index=False, columns=['Address', 'URL', 'Suburb',
                                    'Property Type', 'Number of units', 'Number of Bedrooms',
                                    'Number of Bathrooms', 'Number of Car Spaces',
                                    'Approx. Land Size', 'Multiple Owners / One Owner / No Owner',
                                    'Number of Owners', 'Owner/s name', 'Legal Data',
                                    'Last Sale Price', 'Last Sale Date'])



with open('Available Suburbs.json') as f:

    #get_links(url, json.load(f)['Available Suburbs'])
    get_properties_info(url, json.load(f)['Addresses and hrefs'])


"""
with open('Properties.json') as f:

    save_props(json.load(f)['Properties'])

"""