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


def get_all_hiking_urls(base_url, amount_of_pages_to_be_scraped):
    """
    :param  - url of the website containing the urls to the hikes that are to be scraped
            - amount of sub-webpages to be scraped (beware that the num of pages to be scraped must be less or equal
            than the available amount of webpages.
    :return: a list of urls each corresponding to a specific hike to be scraped
    """
    list_of_urls = []
    urls_of_hikes = []
    for page_num in range(1, amount_of_pages_to_be_scraped + 1):
        list_of_urls.append(f"{base_url}" + str(page_num))

    for url in tqdm(list_of_urls):
        driver.get(url)
        time.sleep(2)

        contents = driver.find_elements(By.CSS_SELECTOR, "div[class*='css-1dzdr7g']")
        for content in contents:
            urls_of_hikes.append(content.find_element(By.TAG_NAME, "a").get_attribute("href"))

    return urls_of_hikes
