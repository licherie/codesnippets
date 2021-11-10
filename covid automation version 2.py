# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 16:03:50 2021

@author: SEAB
"""
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 15:42:56 2021

@author: SEAB
"""
import time
import pandas as pd
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException, WebDriverException, InvalidArgumentException
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = False
#service = Service('C://Users//SEAB//Documents//chromedriver.exe')
#service.start()
#driver = webdriver.Remote(service.service_url)
driver = webdriver.Chrome(options=options, executable_path='C://Users//SEAB//Documents//chromedriver.exe')
driver.maximize_window()
#driver.get('https://covid.cdc.gov//covid-data-tracker//')
#driver.implicitly_wait(200)
driver.set_page_load_timeout(10)

my_transmission_levels_result = [] * 20
#time.sleep(7)
try:
    my_states = {
                "Arizona": [{"Maricopa County" : "4013"}], 
                  "California" : [{"Sacramento County" : "6067"}],
                  "Colorado" : [{"Arapahoe County" : "8005"},
                                {"Boulder County" : "8013"},
                                {"Douglas County": "8035"}],
                  "Florida" : [{"Duval County" : "12031"},
                               {"Hillsborough County" : "12057"}],
                  "Georgia": [{"Cobb County" : "13067"},
                              {"Columbia County" : "13073"}, 
                               {"Fulton County" : "13121"}], 
                  "Idaho" : [{"Ada County" : "16001"},
                             {"Bonneville County": "16019"}],
                  "Illinois": [{"Cook County" : "17031"}, 
                               {"DuPage County" : "17043"}, 
                               {"Lake County" : "17097"}],
                  "Indiana" : [{"Hamilton County" : "18057"}, 
                               {"Marion County" : "18097"}],
                  "Iowa" : [{"Polk County" : "19153"}], 
                  "Kansas" : [{"Johnson County" : "20091"}, 
                              {"Saline County" : "20169"}, 
                              {"Sedgwick County" : "20173"}],
                  "Louisiana" : [{"Ascension Parish" : "22005"}, 
                                {"East Baton Rouge Parish" : "22033"},
                                {"Jefferson Parish" : "22051"},
                                {"Lafayette Parish" : "22055"},
                                {"Livingston Parish" : "22063"},
                                {"Orleans Parish" : "22071"}, 
                                {"St. Tammany Parish" : "22103"},
                                {"Tangipahoa Parish" : "22105"}, 
                                {"Terrebonne Parish" : "22109"},
                                {"West Baton Rouge Parish" : "22121"}],
                  "Massachusetts": [{"Middlesex County" : "25017"},
                                    {"Suffolk County" : "25025"},
                                    {"Worcester County" : "25027"}],                 
                  "Minnesota": [{"Fillmore County" : "27045"}, 
                                {"Hennepin County" : "27053"}, 
                                {"Ramsey County" : "27123"}],
                  "Missouri": [{"Buchanan County" : "29021"}, 
                              {"Callaway County" : "29027"},
                              {"Greene County" : "29077"}, 
                              {"Jackson County" : "29095"},
                              {"St. Louis County" : "29189"}], 
                  "North Carolina" : [{"Buncombe County" : "37021"}],
                  "North Dakota" : [{"Cass County" : "38017"}], 
                  "Nebraska" : [{"Douglas County" : "31055"}],
                  "Nevada" : [{"Clark County" : "32003"}], 
                "New Hampshire" : [{"Cheshire County" : "33005"}],
                "New Jersey" : [{"Monmouth County" : "34025"}],
                "New York" : [{"New York County" : "36061"}, 
                              #"Bronx County",
                              #"Kings County",
                              #"Queens County", 
                              #"Richmond County", 
                              {"Onondaga County" : "36067"}],
                "Ohio": [{"Cuyahoga County" : "39035"}, 
                          {"Franklin County" : "39049"}, 
                          {"Summit County" : "39153"}],
                "Oregon": [{"Multnomah County" : "41051"}, 
                           {"Washington County" : "41067"}],
                "Tennessee" : [{"Davidson County" : "47037"}, 
                               {"Franklin County" : "47051"}],
                "Texas" : [{"Dallas County" : "48113"}],
                "Utah" : [{"Salt Lake County" : "49035"}],
                "Virginia" : [{"Henrico County" : "51087"}, 
                              {"Loudoun County" : "51107"}], 
                "Washington" : [{"Clark County" : "53011"}, 
                                {"King County" : "53033"}], 
                "Wisconsin": [{"Brown County" : "55009"}, 
                              {"Dane County" : "55025"}, 
                              {"Marathon County" : "55073"}, 
                              {"Milwaukee County" : "55079"}, 
                              {"Waukesha County" : "55133"}] }

    count = 0 
    #driver.get('https://covid.cdc.gov//covid-data-tracker//#county-view|' + 'Florida' +  '|' +  '12003')
    for state in my_states.keys(): 
        print(state)
        my_counties_dict = my_states[state]
        for county_dict in my_counties_dict:
            #time.sleep(5)
            #try: 
            county = "".join(list(county_dict.keys()))
            print(county)
            print(county_dict[county])
            time.sleep(7)
            try:    
                url =  'https://covid.cdc.gov//covid-data-tracker//#county-view|' + state + '|' +  county_dict[county] + '|Risk|community_transmission_level' 
                driver.get(url)
                driver.refresh()
            except InvalidArgumentException:
                 print(url)
            #except TimeoutException: 
                #county_list = Select(driver.find_element_by_xpath("//select[@id = 'list_select_county']"))
            #all_options = county_list.find_elements_by_tag_name("option")
            #for option in all_options:
                #print("Text is: %s" % option.get_attribute("text"))
            #select_county.select_by_visible_text(county)
            #try: 
            found_element_transmission_text = False
            tries = 0 
            while not(found_element_transmission_text): 
                try: 
                    transmission_level_text = driver.find_element_by_xpath("//div[@id='community_transmission_level']").text
                    if transmission_level_text == '': 
                        driver.get(url)
                        driver.refresh()
                        time.sleep(7)
                        print('blank_text')
                    else:
                        print(transmission_level_text)
                        found_element_transmission_text = True
                except StaleElementReferenceException:
                    print('stale_text')
                    pass
                except NoSuchElementException:
                    url =  'https://covid.cdc.gov//covid-data-tracker//#county-view|' + state +  '|' +  county_dict[county] + '|Risk|community_transmission_level'
                    driver.get(url)
                    driver.refresh()
                    time.sleep(7)
                    print('nosuch_text')
                    pass
                except TimeoutException:
                    print('timeout_text')
                    tries = tries + 1
                    driver.refresh()
                    time.sleep(5)
                    if tries <= 5: 
                        continue 
                    else:
                        transmission_level_text = 'timed out'
                        break
            #transmission_level_text = driver.find_element_by_xpath("//div[@id='community_transmission_level']").text
           # except TimeoutException: 
            #    transmission_level_text = driver.find_element_by_xpath("//div[@id='community_transmission_level']").text
            my_transmission_levels_result.append([state, county, transmission_level_text])
            print([state, county, transmission_level_text])
            #print(county)
            #print(transmission_level_text)
        print(count)
        
finally:
    driver.quit()

df = pd.DataFrame(my_transmission_levels_result, columns=['State', 'County', 'Transmission_Level'])
df.to_csv('C://Users//SEAB//Documents//transmission_levels_today.csv', index = 'FALSE')
    
