from selenium import webdriver
from bs4 import BeautifulSoup as bs
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from server.routes.items import *
from time import sleep
import re


def start_driver():
    prefs = {
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
    }
    options = uc.ChromeOptions()
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    options.add_experimental_option("prefs", prefs)
    driver = uc.Chrome(options=options)
    return driver

def scrape_items(driver, search_term):

    sleep_time = 10
    base_url = 'https://www.olx.com.eg/en/'
    driver.get(base_url)
    sleep(sleep_time)

    search_box = driver.find_element(By.XPATH, '//input[@type="search"]')
    search_box.send_keys(search_term)

    search_button = driver.find_element(By.XPATH, '//button[@aria-label="Search"]')
    search_button.click()
    sleep(sleep_time)

    total_results = []

    while len(total_results) < 300:

        current_page = driver.page_source
        current_soup = bs(current_page, 'html.parser')
        current_items = current_soup.find_all('li', {'aria-label':'Listing'})
        total_results.extend(current_items)
        
        next_button = driver.find_element(By.XPATH, '//div[@title="Next"]')
        next_button.click()
        sleep(sleep_time)
    
    driver.quit()
    
    final_results = []

    for i in range(0, len(total_results)):

        current_item = {}

        try:
            current_item['product_name'] = total_results[i].find('div', {'aria-label':'Title'}).text.strip()
        except:
            current_item['product_name'] = ''
        try:
            current_item['price'] = total_results[i].find('div', {'aria-label':'Price'}).text.replace('EGP','').strip()
            current_item['price'] = int(''.join(re.findall(r'\d+', current_item['price'])))
        except:
            current_item['price'] = 0
        try:
            current_item['location'] = total_results[i].find('span', {'aria-label':'Location'}).text.strip()
        except:
            current_item['location'] = ''
        try:
            current_item['listed_date'] = total_results[i].find('span', {'aria-label':'Creation date'}).text.strip()
        except:
            current_item['listed_date'] = ''
        try:
            current_item['product_link'] = 'https://www.olx.com.eg' + total_results[i].find('a').get('href')
        except:
            current_item['product_link'] = ''
        try:
            current_item['product_image'] = total_results[i].find('img', {'aria-label':'Cover photo'}).get('src')
        except:
            current_item['product_image'] = ''
        current_item['product_search_term'] = search_term
            
        final_results.append(current_item)
        
    return final_results



