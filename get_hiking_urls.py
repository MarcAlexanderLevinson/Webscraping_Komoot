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

url = "https://www.komoot.com/discover/Lyon/@45.7575926%2C4.8323239/tours?max_distance=200000&sport=hike&map=true&pageNumber="


def get_all_catalogues_urls(base_url, number_of_page_to_scrap):
    """
    The hikes are displayed by set of 12. Each set of 12 hikes is on a different "catalogue page".
    This function collects as many catalogue urls as the input "number_of_page_to_scrap" says.
    """
    catalogues_urls = list()
    for page_num in range(1, number_of_page_to_scrap + 1):
        catalogues_urls.append(f"{base_url}" + str(page_num))
    return catalogues_urls

# <div class="css-1tdtx4c">
def get_html_blocks(catalogue_url):
    """
    On one catalogue page, get the 12 html blocks that contains the 12 hikes url
    """
    driver.get(catalogue_url)
    time.sleep(5)
    try:
        return driver.find_elements(By.CSS_SELECTOR, 'div[class="css-1u8qly9"]')[0:12]  # this is 12 "blocks"
    except common.exceptions.WebDriverException as err:
        logging.error(f'the contents of this url {catalogue_url} was not found: {err}')


def get_one_hike_url(block, urls_of_hikes, number_of_hikes_found_on_this_page, number_of_hikes_found, catalogue_url):
    """
    From one given block on a catalogue page, extracts the url of the hike
    """
    try:
        block.click()
        url = block.find_element(By.XPATH,
                        '//*[@id="pageMountNode"]/div/div[3]/div[3]/div[2]/div[2]/div[8]/ul/li[2]/a').get_attribute(
            "href")
        block_quiter = block.find_element(By.XPATH, '//*[@id="pageMountNode"]/div/div[3]/div[3]/div[1]/div/button[3]')
        block_quiter.click()
        urls_of_hikes.append(url)
        number_of_hikes_found_on_this_page += 1
        number_of_hikes_found += 1
        logging.info(
            f'{number_of_hikes_found_on_this_page} hikes url found on this page, {number_of_hikes_found} in total')
    except common.exceptions.WebDriverException as err:
        logging.warning(f'The url of one hike on page ({catalogue_url}) was not found: {err}')
    return number_of_hikes_found_on_this_page, number_of_hikes_found


def get_all_hikes_urls(base_url, number_of_pages_to_scrap):
    """
    This function puts in music the above functions and get the url within each block
    From a base url and a number of pages to scrap, it will return the list of hike url
    """
    catalogues_urls = get_all_catalogues_urls(base_url, number_of_pages_to_scrap)
    urls_of_hikes = []
    number_of_hikes_found = 0

    for catalogue_url in tqdm(catalogues_urls):
        blocks = get_html_blocks(catalogue_url)

        number_of_hikes_found_on_this_page = 0
        for block in blocks:
            result = get_one_hike_url(block, urls_of_hikes, number_of_hikes_found_on_this_page, number_of_hikes_found,
                                      catalogue_url)
            print(urls_of_hikes)
            number_of_hikes_found_on_this_page = result[0]
            number_of_hikes_found = result[1]
    return urls_of_hikes


def write_urls_to_csv(urls_of_hikes):
    urls_of_hikes = [[url_of_hikes] for url_of_hikes in urls_of_hikes]
    with open("list_of_hiking_urls.csv", "w", newline="") as hike_urls_csv:
        writer = csv.writer(hike_urls_csv)
        for url_of_hike in urls_of_hikes:
            writer.writerow(url_of_hike)
