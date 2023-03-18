import time
from selenium import common
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
# url = "https://www.komoot.com/smarttour/e991085326/mont-miaune-boucle-au-depart-de-retournac?tour_origin=smart_tour_search"
# url = "https://www.komoot.com/smarttour/11996476?tour_origin=smart_tour_search"

def driver_get_url(url):
    drive = driver.get(url)
    time.sleep(1)
    return drive


def get_basic_hike_info(drive):
    drive
    title = driver.find_element(By.CSS_SELECTOR, "span[class*='tw-mr-1 tw-font-bold']").text
    difficulty = driver.find_element(By.CSS_SELECTOR, "div[class*='tw-flex tw-items-center']").text
    duration = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='t_duration_value']").text
    
    conversions_to_km = {"km": 1.0, "mi": 1.60934, "yd": 0.0009144, "m": 0.001, "ft": 0.0003048, "mph": 1.60934}
    
    distance_text = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='t_distance_value']").text
    distance = round(float(distance_text.split()[0]) * conversions_to_km[distance_text.split()[1]],2)
    
    average_speed_text = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='t_speed_value']").text
    average_speed = round(float(average_speed_text.split()[0]) * conversions_to_km[average_speed_text.split()[1]],2)

    uphill_text = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='t_elevation_up_value']").text
    uphill_text = uphill_text.replace(",","")
    uphill = round(float(uphill_text.split()[0]) * conversions_to_km[uphill_text.split()[1]] * 1000,2)  #put this one in m

    downhill_text = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='t_elevation_down_value']").text
    downhill_text = downhill_text.replace(",","")
    downhill = round(float(downhill_text.split()[0]) * conversions_to_km[downhill_text.split()[1]] * 1000,2)  #put this one in m
    return {"2.Title":title,"3.Difficulty":difficulty,"4.Duration (hr)":duration,"5.Distance (km)":distance,"6.Average_speed (km/hr)":average_speed,"7.Uphill (m)":uphill,"8.Downhill (m)":downhill}

def get_descriptions(drive):
    drive
    descriptions_niv1 = driver.find_element(By.XPATH,"//div[@class='css-fxq50d']/div/span[@class='tw-text-secondary']").text
    try:
        descriptions_niv2 = driver.find_element(By.XPATH,"//div[@class='css-fxq50d']/div/span/span[@class='tw-text-secondary']").text
    except common.exceptions.NoSuchElementException:
        descriptions_niv2 = ''
    description = descriptions_niv1 +' '+ descriptions_niv2
    try:
        tips = driver.find_element(By.CSS_SELECTOR, "div[class='css-1xrtte3']").text
    except common.exceptions.NoSuchElementException:
        tips = ''
    return {"9.Description": "text still to be made"}

def get_way_type_and_surfaces(drive):
    drive
    way_type = driver.find_element(By.XPATH, "//div[@class='tw-p-4 sm:tw-p-6 ']/div[@class='tw-mb-6']").text
    listed_text = way_type.split("\n")
    types_and_distances = {}
    for type_and_distance in listed_text[1:]:
        distances_in_km = {"km": 1.0, "mi": 1.60934, "yd": 0.0009144, "m": 0.001}
        key = type_and_distance.split(":")[0] + " (km)"
        if len(type_and_distance.split(":")[1].split()) == 2:
            unit = type_and_distance.split(":")[1].split()[1]
            distance = float(type_and_distance.split(":")[1].split()[0]) * distances_in_km[unit]
        elif len(type_and_distance.split(":")[1].split()) == 3: ###ASSUMPTION: if the distance shows > 109m the "less than" is neglected
            unit = type_and_distance.split(":")[1].split()[2]
            distance = float(type_and_distance.split(":")[1].split()[1]) * distances_in_km[unit]
        value = round(distance, 2)
        types_and_distances[key] = value
    return types_and_distances


def get_hike_info(drive):
    drive
    basic_hike_info = get_basic_hike_info(drive)
    way_type_and_surfaces = get_way_type_and_surfaces(drive)
    description = get_descriptions(driver)
    dictionary = {**basic_hike_info, **way_type_and_surfaces, **description}
    return(dictionary)


if __name__ == "__main__":
    drive = driver_get_url(url)
    get_hike_info(drive)

end = time.time() - start
print(end)