

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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#start headless chrome
options = webdriver.ChromeOptions()
#options.add_argument('headless')
chrome_path = os.path.join(os.getcwd(), 'chromedriver')
driver = webdriver.Chrome(chrome_path, chrome_options=options)


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
old_filename = os.path.join(currentdir, 'oldVapeShops.txt')
currentVapeShops = []
#check if oldVapeShops.txt exists
try:
    with open(old_filename, 'r') as f:
        for line in f:
            oldVapeShops.append(line.replace('\n', ''))
    print("Old shops: ", oldVapeShops)

except:
    print("oldVapeShops.txt does not exist")
    with open(old_filename, 'w') as f:
        f.write("")
    print("oldVapeShops.txt created")

print("oldVapeShops.txt length: " + str(len(oldVapeShops)))
#remove duplicates from oldVapeShops
oldVapeShops = list(dict.fromkeys(oldVapeShops))
print("oldVapeShops.txt length after removing duplicates: " + str(len(oldVapeShops)))
#add every link that is not in oldVapeShops to currentVapeShops
for link in links:
    if link not in oldVapeShops:
        currentVapeShops.append(link)
 
print("New shops: ", currentVapeShops)

#add every link in currentVapeShops to oldVapeShops
f = open(old_filename, 'w')
for link in oldVapeShops + currentVapeShops:
    f.write(link + "\n")


#close the driver
print("closing driver")
driver.close()
print('new shops: ' + str(len(currentVapeShops)))

# Replace these with your Gmail account credentials
gmail_user = 'torinsappail@gmail.com'
gmail_password = 'igtxbqpahhukdoxf'

# Replace these with the recipient's email address and the email subject
to = 'thomassafar03@gmail.com'
subject = 'Subject of the email'
#seperate each link with a new line
body = ''
for link in currentVapeShops:
    body += link + "\n"

# Create the email
msg = MIMEMultipart()
msg['From'] = gmail_user
msg['To'] = to
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

# Send the email
try:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(gmail_user, gmail_password)
        if len(currentVapeShops) > 0:
            server.sendmail(gmail_user, to, msg.as_string())
        server.quit()

    print('Email sent!')
except Exception as e:
    print('Something went wrong...', e)
