from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(4)

bhk_2 =[]
bhk_3 = []
bhk_4 = []
columns = ['BHK_N_TYPE', 'PROPERTY_LOCATION', 'PROPERTY_PRICE', 'FURNISHING', 'FLOOR', 'AREA', 'OWNERSHIP', 'BATHROOM', 'FACING', 'STATUS', 'IMAGE']

def scroller() :
    global bhk_2
    global bhk_3
    global bhk_4

    x = 0
    while x < 4 :
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)
        x = x + 1

def page_changer() :
    global bhk_2
    global bhk_3
    global bhk_4
    global i

    driver.get('https://www.propertiesguru.com/residential-search/{0}bhk-residential_apartment_flat-for-sale-in-new_delhi'.format(i))
    driver.maximize_window()
    time.sleep(3)
    scroller()
    scraper()

def scraper() :
    global bhk_2
    global bhk_3
    global bhk_4

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    divisions = soup.findAll('div', {'class' : 'filter-property-list'})

    for division in divisions :
        h1 = division.find('h1', {'class' : 'filter-pro-heading'}).text.split('Sale')
        about = h1[0] + 'Sale'
        prop_loc = h1[1].strip()
        prop_price = division.find('span', {'class' : 'price'}).text
        div = division.find('div', {'class' : 'row filter-pro-details'})
        area = div.find('div', {'class' : 'col-4'}).text[4:]
        facing = div.find('div', {'class' : 'col-3'}).text[6:]
        status = div.find('div', {'class' : 'col-5'}).text[6:]
        ul = division.find('ul', {'class' : 'pro-list'})
        lis = ul.findAll('li')
        floor = lis[0].text
        furnishing = lis[1].text
        ownership = lis[2].text
        bathroom = lis[3].text[0]
        image = division.find('img').get('src')

        if about[0] == '2' :
            bhk_2.append([about, prop_loc, prop_price, furnishing, floor, area, ownership, bathroom, facing, status, image])
        elif about[0] == '3' :
            bhk_3.append([about, prop_loc, prop_price, furnishing, floor, area, ownership, bathroom, facing, status, image])
        elif about[0] == '4' :
            bhk_4.append([about, prop_loc, prop_price, furnishing, floor, area, ownership, bathroom, facing, status, image])

for i in range(2,5) :
    page_changer()

driver.quit()

df1 = pd.DataFrame(bhk_2, columns = columns)
df1.to_csv('2_bhk.csv', index = False)

df2 = pd.DataFrame(bhk_3, columns = columns)
df2.to_csv('3_bhk.csv', index = False)

df3 = pd.DataFrame(bhk_4, columns = columns)
df3.to_csv('4_bhk.csv', index = False)
