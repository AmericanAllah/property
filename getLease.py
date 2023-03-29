
from openpyxl import load_workbook
from selenium import webdriver
import time
import sys
from datetime import date
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import threading
from selenium.common.exceptions import NoSuchElementException
import requests
import random
import datetime
import string
import os

#start headless chrome
options = webdriver.ChromeOptions()
#options.add_argument('headless')
driver = webdriver.Chrome(options=options)

username = 'thomassafar03@gmail.com'
password = 'eatit093'
pages = [
    "https://www.crexi.com/lease/properties?sqFtMax=3000&sqFtMin=0&types%5B%5D=Retail&sort=New%20Listings&placeIds%5B%5D=ChIJ66_O8Ra35YgR4sf8ljh9zcQ",
    "https://www.crexi.com/lease/properties?sqFtMax=3000&sqFtMin=0&types%5B%5D=Retail&sort=New%20Listings&placeIds%5B%5D=ChIJr46dPFY25IgRVZvncDr516U",
    "https://www.crexi.com/lease/properties?sqFtMax=3000&sqFtMin=0&types%5B%5D=Retail&sort=New%20Listings&placeIds%5B%5D=ChIJDSKjk6sx5IgRP_xEwnuYXL0",
    "https://www.crexi.com/lease/properties?sqFtMax=3000&sqFtMin=0&types%5B%5D=Retail&sort=New%20Listings&placeIds%5B%5D=ChIJw7zsvY7N5YgRP8kydmibdu0",
    "https://www.crexi.com/lease/properties?sqFtMax=3000&sqFtMin=0&types%5B%5D=Retail&sort=New%20Listings&placeIds%5B%5D=ChIJT3_fdVeC5ogRJ2AnixeDocI",
    "https://www.crexi.com/lease/properties?sqFtMax=3000&sqFtMin=0&types%5B%5D=Retail&sort=New%20Listings&placeIds%5B%5D=ChIJtxaCe8ed5ogRj-VYqbDRrdo",
    "https://www.crexi.com/lease/properties?sqFtMax=3000&sqFtMin=0&types%5B%5D=Retail&sort=New%20Listings&placeIds%5B%5D=ChIJg1YCJZTb5ogR6yrLHbc7ajY"
]

def waitUntilPageLoads():
    while True:
        try:
            driver.execute_script("return document.getElementsByClassName('text')[3].innerText")
            break
        except:
            time.sleep(1)
            continue
#login
driver.get("https://www.crexi.com/lease/properties?types%5B%5D=Retail&placeIds%5B%5D=ChIJ66_O8Ra35YgR4sf8ljh9zcQ&sqFtMax=2300&sort=New%20Listings")
time.sleep(10)
#remove popup if it exists
try:
    driver.execute_script("document.getElementsByClassName('cui-modal-close ng-star-inserted')[0].click()")
except:
    pass
#click login
driver.execute_script('document.querySelector("body > crx-app > div > ng-component > crx-normal-page > div > crx-header > crx-header-content > div > div.transclude-auth.right-header-section > crx-logged-out-header > button").click()')
time.sleep(2)
#click login tab
driver.execute_script("document.getElementsByClassName('tab switch')[0].click()")
time.sleep(2)
emailBox = driver.execute_script('return document.querySelector("#login-form > div:nth-child(1) > label > input")')
emailBox.send_keys(username)
passwordBox = driver.execute_script('return document.querySelector("#login-form > div:nth-child(2) > label > input")')
passwordBox.send_keys(password)
time.sleep(2)
#finally click login
driver.execute_script('document.querySelector("#login-form > button").click()')
time.sleep(5)
i=0
links = []
for i in range(0, len(pages)):
    #check if 'Oh no! There aren’t any spaces that match your search. Remove filters or update filters to find more spaces:' not in document.body.innerHTML
    driver.get(pages[i])
    time.sleep(10)
    if 'Oh no! There aren’t any spaces that match your search. Remove filters or update filters to find more spaces:' in driver.execute_script('return document.body.innerHTML'):
        continue
    time.sleep(12)
    try:
        driver.execute_script('document.querySelector("#pagination-container > div > div > crx-select > crx-dropdown-button > div > div").click()')
        time.sleep(2)
        driver.execute_script('document.querySelector("#pagination-container > div > div > crx-select > crx-dropdown-button > div > crx-dropdown-portal > div > div > div.options > div:nth-child(5)").click()')
        time.sleep(2)
    except:
        print('cant change showing size')
        pass
    #save document.getElementsByClassName('cover-link')[0-99].href to list
    for i in range(0, 100):
        try:
            links.append(driver.find_elements(By.CLASS_NAME,'cover-link')[i].get_attribute('href'))
            print(links[i])
        except:
            pass
print(str(len(links)) + " links found")



addresses = []
rates = []
sqft = []
print("getting data")
print("links: " + str(len(links)))

oldVapeShops = []
currentdir = os.getcwd()
filename = os.path.join(currentdir, 'oldVapeShops.txt')
with open(filename, 'r') as f:
    for line in f:
        oldVapeShops.append(line)


for link in links:
    if link in oldVapeShops:
        continue
    else:
        with open(filename, 'a') as f:
            f.write(str(link) + '\n')
    print(link)
    addresses.append(link.replace('\n', ''))






#close the driver
print("closing driver")
driver.close()

