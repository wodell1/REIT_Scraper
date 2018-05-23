# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 11:13:44 2018

@author: walke
"""

from selenium import webdriver
import requests
import pandas as pd
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re


def scroll_until_element_clicked_on(names1, REIT):
    for i in [10, 25, 50, 75, 100]:
        try:
            print(i)
            print(names1[REIT].text)
            names1[REIT].click()
            time.sleep(1)
            print('Breaking out of loop')
            break
        except:
            script = "window.scrollTo(0, " + str(i) + ")"
            driver.execute_script(script)
            names1 = driver.find_elements_by_class_name('name')
            time.sleep(1)




driver = webdriver.Firefox(executable_path=r'C:/geckodriver.exe')
driver.get('https://www.reit.com/investing/reit-directory?field_rtc_listing_status_tid_selective[]=524&field_address_country_selective[]=US&sort_by=field_stock_return_30_value')

skip_page_button = driver.find_element_by_xpath('/html/body/div[7]/div/div[5]/a[1]')
skip_page_button.click()    
time.sleep(1)

df = pd.DataFrame({"Company_Name" : [],
                   "Ticker" : [],
                   "Address" : [],
                   "Sectors" : [],
                   "Description" : []
                   })


for page_num in range(0, 26):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    names = driver.find_elements_by_class_name('name')
    comp_names = [e.text for e in names]
    tickers = driver.find_elements_by_class_name('ticker')
    tick_names = [e.text for e in tickers]
    addresses = driver.find_elements_by_class_name('address')
    address_name = [e.text for e in addresses]
    sectors = soup.find_all('div', attrs={'class':"right"})
    sect_name = [e.text.split('   ')[2] for e in sectors]
    
    print(len(df))
    descriptions = []
    for REIT in range(0, len(names)):
        try:
            names1 = driver.find_elements_by_class_name('name')
            scroll_until_element_clicked_on(names1, REIT)
            time.sleep(5)
            text = driver.find_element_by_class_name('investor__body').text
            descriptions.append(text)
            driver.back()
            time.sleep(4)
        except:
            driver.get('https://www.reit.com/investing/reit-directory?field_rtc_listing_status_tid_selective[]=524&field_address_country_selective[]=US&sort_by=field_stock_return_30_value')
            try:
                skip_page_button = driver.find_element_by_xpath('/html/body/div[7]/div/div[5]/a[1]')
                skip_page_button.click()    
                time.sleep(1)
            except:
                print('')
            print(str(REIT) + "  Failed")
            descriptions.append("")
            for i in range(0, page_num):
                next_page_button = driver.find_element_by_xpath('//*[@title="Go to next page"]')
                next_page_button.click()
                time.sleep(3)
        
    df = df.append(pd.DataFrame({"Company_Name" : comp_names,
               "Ticker" : tick_names,
               "Address" : address_name,
               "Sector" : sect_name,
               "Description" : descriptions
               }))
    

    next_page_button = driver.find_element_by_xpath('//*[@title="Go to next page"]')
    next_page_button.click()
    time.sleep(5)



df.to_csv('REIT_data_all2.csv')
























