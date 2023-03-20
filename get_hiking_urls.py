from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from tqdm.auto import tqdm
from selenium import common
import time
import logging
import csv

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.page_load_strategy = 'none'
chrome_path = ChromeDriverManager().install()
chrome_service = Service(chrome_path)
driver = Chrome(options=options, service=chrome_service)
driver.implicitly_wait(5)


def get_all_hiking_urls(base_url, amount_of_pages_to_be_scraped):
    """
    :param  - url of the website containing the urls to the hikes that are to be scraped
            - amount of sub-webpages to be scraped (beware that the num of pages to be scraped must be less or equal
            than the available amount of webpages.
    :return: a list of urls each corresponding to a specific hike to be scraped
    """
    list_of_urls = []
    urls_of_hikes = []

    # The hikes are displayed by set of 12. Each set of 12 hikes is on a different page.
    # In this first step, we collect the url of all the main pages.
    for page_num in range(1, amount_of_pages_to_be_scraped + 1):
        list_of_urls.append(f"{base_url}" + str(page_num))

    # The step 2 is to go through each one of these main pages, and collect the url of each of the hike
    number_of_hikes_found = 0
    for url in tqdm(list_of_urls):
        try:
            driver.get(url)
            time.sleep(2)
        except common.exceptions.WebDriverException as err:
            logging.error(f'url {url} was not reached: {err}')
            continue

        try:
            contents = driver.find_elements(By.CSS_SELECTOR, "div[class*='css-1dzdr7g']")
        except common.exceptions.WebDriverException as err:
            logging.error(f'the contents of url {url} was not found: {err}')
            continue

        number_of_hikes_found_on_this_page = 0
        for content in contents:
            try:
                urls_of_hikes.append(content.find_element(By.TAG_NAME, "a").get_attribute("href"))
                number_of_hikes_found_on_this_page += 1
                number_of_hikes_found += 1
                logging.info(
                    f'{number_of_hikes_found_on_this_page} hikes url found on this page, {number_of_hikes_found} in total')
            except common.exceptions.WebDriverException as err:
                logging.warning(f'The url of one hike on page ({url}) was not found: {err}')
    return urls_of_hikes


def write_urls_to_csv(urls_of_hikes):
    urls_of_hikes = [[url_of_hikes] for url_of_hikes in urls_of_hikes]
    with open("list_of_hiking_urls.csv", "w", newline="") as hike_urls_csv:
        writer = csv.writer(hike_urls_csv)
        for url_of_hike in urls_of_hikes:
            writer.writerow(url_of_hike)