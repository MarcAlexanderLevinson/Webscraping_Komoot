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
#url = "https://www.komoot.com/smarttour/e925015085/le-chemin-des-papetiers-boucle-au-depart-de-valeyre-parc-naturel-regional-livradois-forez?tour_origin=smart_tour_search"
# url = "https://www.komoot.com/smarttour/e991077160/le-tour-du-malorum-boucle-au-depart-de-bas-en-basset?tour_origin=smart_tour_search"

def get_hike_info(url):
    driver.get(url)
    time.sleep(1)
    title = driver.find_element(By.CSS_SELECTOR, "span[class*='tw-mr-1 tw-font-bold']").text
    difficulty = driver.find_element(By.CSS_SELECTOR, "div[class*='tw-flex tw-items-center']").text
    duration = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='t_duration_value']").text
    distance = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='t_distance_value']").text
    average_speed = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='t_speed_value']").text
    uphill = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='t_elevation_up_value']").text
    downhill = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='t_elevation_down_value']").text
    total_info = {"title": title, "difficulty": difficulty, "duration": duration, "distance": distance}
    return total_info

print(get_hike_info(url))


def main():
    get_hike_info(url)
    end = time.time()
    print(end - start)


if __name__ == "__main__":
    main()
