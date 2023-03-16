import time
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


start = time.time()
# start by defining the options
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")  # it's more scalable to work in headless mode
options.page_load_strategy = 'none'
# this returns the path web driver downloaded
chrome_path = ChromeDriverManager().install()
chrome_service = Service(chrome_path)
# pass the defined options and service objects to initialize the web driver
driver = Chrome(options=options, service=chrome_service)
driver.implicitly_wait(5)


url = "https://www.komoot.com/smarttour/e926612355/mont-colombier-massif-des-bauges-boucle?tour_origin=smart_tour_search"



def get_hike_info(url):
    driver.get(url)
    time.sleep(1)
    title = driver.find_element(By.CSS_SELECTOR, "span[class*='tw-mr-1 tw-font-bold']").text
    difficulty = driver.find_element(By.CSS_SELECTOR, "div[class*='css-1644ev']").text
    duration = driver.find_element(By.CSS_SELECTOR, "div[class*='css-1f0x93j']").text
    distance = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='t_distance_value']").text
    # average_speed =
    # uphill =
    # downhill

    print(title, difficulty, duration, distance)



get_hike_info(url)
end = time.time()
print(end - start)
