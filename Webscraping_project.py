import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from tqdm.auto import tqdm
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.page_load_strategy = 'none'
chrome_path = ChromeDriverManager().install()
chrome_service = Service(chrome_path)
driver = Chrome(options=options, service=chrome_service)
driver.implicitly_wait(5)

base_url = "https://www.komoot.com/discover/Lyon/@45.7575926%2C4.8323239/tours?max_distance=5000&sport=hike&map=true&pageNumber=" #Url for 5km Lyon

list_of_urls = []
urls_of_hikes = []
for page_num in range(1,24):
    list_of_urls.append(f"{base_url}" + str(page_num))

for url in tqdm(list_of_urls):
    driver.get(url)
    time.sleep(1)

    contents = driver.find_elements(By.CSS_SELECTOR, "div[class*='css-1dzdr7g']")
    for content in contents:
        urls_of_hikes.append(content.find_element(By.TAG_NAME, "a").get_attribute("href"))

print(urls_of_hikes)
print(len(urls_of_hikes))

#274 hikes with time.sleep(10)





