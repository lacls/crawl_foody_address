from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import csv
import urllib
from selenium.webdriver.common.action_chains import ActionChains
import requests
import json
import re
import tqdm
import urllib.request
import os
from tqdm import tqdm
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,StaleElementReferenceException,InvalidArgumentException,ElementClickInterceptedException,WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pickle5 as pickle


import time
start_time = time.time()
driver = webdriver.Chrome()
driver.get("https://shopee.vn/baseus_official_store")
comments=[]
sleep(5)

while True:
        try:
            # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'shop-page__all-products-section')))
            elements=driver.find_element_by_class_name('shop-page__all-products-section')
            break
        except:
            ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
            continue

products_url=[]
##Get Products_URL
for products in driver.find_element_by_class_name('shop-page__all-products-section').find_element_by_class_name("row").find_elements_by_tag_name("a"):
    products_url.append(products.get_attribute("href"))

for url in tqdm(products_url,total=len(products_url)):
    if len(comments)==500:
        break
    driver.get(url)
    driver.find_element_by_tag_name("body").send_keys(Keys.END)
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'shopee-product-rating__main')))
    while True:
        try:
            element = driver.find_element_by_class_name("shopee-product-rating__main")
            break
        except:
            ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
            continue
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
    i=0
    current_commments=[]    
    for element in driver.find_elements_by_class_name("shopee-product-rating__main"):
        if element.find_element_by_class_name("shopee-product-rating__content").text:
            comments.append(element.find_element_by_class_name("shopee-product-rating__content").text)
            current_commments.append(element.find_element_by_class_name("shopee-product-rating__content").text)
            #  if element.find_element_by_class_name("shopee-product-rating__time").text not in comments.keys():
            #      comments[element.find_element_by_class_name("shopee-product-rating__time").text]=[element.find_element_by_class_name("shopee-product-rating__content").text]
            #  else:
            #      comments[element.find_element_by_class_name("shopee-product-rating__time").text].extend([element.find_element_by_class_name("shopee-product-rating__content").text])    
    run_to_main_comments=True
    for _ in range(15):
        try:
            ##check whether or not dublicate to stop loading the next page
            if driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[3]/div[2]").find_elements_by_tag_name("button")[-1].click():
                dublicate=0
                run_to_main_comments=True
                for element in driver.find_elements_by_class_name("shopee-product-rating__main"):
                    if element.find_element_by_class_name("shopee-product-rating__content").text:
                        if element.find_element_by_class_name("shopee-product-rating__content").text in current_commments:
                            dublicate+=1
                            continue
                        comments.append(element.find_element_by_class_name("shopee-product-rating__content").text)
            if dublicate==len(current_commments):
                break
        except:
            print("cannot click on")
            if run_to_main_comments:
                element = driver.find_element_by_class_name("shopee-product-rating__main")
                actions = ActionChains(driver)
                actions.move_to_element(element).perform()
                run_to_main_comments=False
            ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
            if i==5:
                break
            i+=1
            continue
    print(len(comments))        
print("--- %s seconds ---" % (time.time() - start_time))
    