from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import csv


# Task 1: Login to Linkedin

# Task 1.1: Open Chrome and Access Linkedin login site
driver = webdriver.Chrome()
sleep(2)
url = 'https://juno.vn/collections/giay?itm_source=homepage&itm_medium=menu&itm_campaign=normal&itm_content=giay'
driver.get(url)


