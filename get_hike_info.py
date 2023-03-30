import time
# from selenium import common
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import logging

# import traceback

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
driver.set_window_size(2700,2000)
driver.implicitly_wait(5)

url = "https://www.komoot.com/smarttour/e926612355/mont-colombier-massif-des-bauges-boucle?tour_origin=smart_tour_search"


# url = "https://www.komoot.com/smarttour/e925015085/le-chemin-des-papetiers-boucle-au-depart-de-valeyre-parc-naturel-regional-livradois-forez?tour_origin=smart_tour_search"
# url = "https://www.komoot.com/smarttour/e925015085/le-chemin-des-papetiers-boucle-au-depart-de-valeyre-parc-naturel-regional-livradois-forez?tour_origin=smart_tour_search"
# url = "https://www.komoot.com/smarttour/e991077160/le-tour-du-malorum-boucle-au-depart-de-bas-en-basset?tour_origin=smart_tour_search"
# url = "https://www.komoot.com/smarttour/e991085326/mont-miaune-boucle-au-depart-de-retournac?tour_origin=smart_tour_search"
# url = "https://www.komoot.com/smarttour/e808650908/pointe-de-nantaux-2170m?tour_origin=smart_tour_search "
#
# logging.basicConfig( format='%(asctime)s ---- %(levelname)s:%(message)s - row %(lineno)d',
#                     level=logging.INFO)


def driver_get_url(url):
    """
    :param url of the hike page to scrap
    :return: a drive object that is gonna be used for all the get_hike_info functions below
    """
    try:
        drive = driver.get(url)
        # time.sleep(1)
        logging.info(f'Success: The drive of this url {url} was obtained')
        return drive
    except:
        logging.warning(f'The drive of this url {url} was not obtained')



def get_basic_hike_info(drive):
    """
    :param driver
    :return: Collect the basic info of the hike
    """
    url = driver.current_url
    try:
        title = driver.find_element(By.CSS_SELECTOR, "span[class*='tw-mr-1 tw-font-bold']").text
        difficulty = driver.find_element(By.CSS_SELECTOR, "div[class*='tw-flex tw-items-center']").text
        duration = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='t_duration_value']").text
        conversions_to_km = {"km": 1.0, "km/h": 1.0, "mi": 1.60934, "yd": 0.0009144, "m": 0.001, "m/h": 0.001,
                             "ft": 0.0003048, "mph": 1.60934}

        distance_text = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='t_distance_value']").text
        distance = round(float(distance_text.split()[0]) * conversions_to_km[distance_text.split()[1]], 2)

        average_speed_text = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='t_speed_value']").text
        average_speed = round(float(average_speed_text.split()[0]) * conversions_to_km[average_speed_text.split()[1]],
                              2)

        uphill_text = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='t_elevation_up_value']").text
        uphill_text = uphill_text.replace(",", "")
        uphill = round(float(uphill_text.split()[0]) * conversions_to_km[uphill_text.split()[1]] * 1000,
                       2)  # put this one in m

        downhill_text = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='t_elevation_down_value']").text
        downhill_text = downhill_text.replace(",", "")
        downhill = round(float(downhill_text.split()[0]) * conversions_to_km[downhill_text.split()[1]] * 1000,
                         2)  # put this one in m
        logging.info(f'Success: The basic hike info of this url ({url}) was found')
        return {"2.Title": title, "3.Difficulty": difficulty, "4.Duration (hr)": duration, "5.Distance (km)": distance,
                "6.Average_speed (km/hr)": average_speed, "7.Uphill (m)": uphill, "8.Downhill (m)": downhill}
    except:
        logging.warning(f'The basic hike info of this url ({url}) was not found')
        return {}


def get_descriptions(drive):
    """
    :param driver
    :return: Collect the descriptions (description and tip) of the hike. On some pages, the description is split in 2 classes. Some page don't have tips
    """
    url = driver.current_url
    try:
        descriptions_niv1 = driver.find_element(By.XPATH,
                                                "//div[@class='css-fxq50d']/div/span[@class='tw-text-secondary']").text
        logging.info(f'Success: The description level 1 of this url ({url}) was found')
    except:
        logging.warning(f'The description level 1 of this url ({url}) was not found')
        return {}

    # Try/except to handle cases without the 2nd part of the description
    try:
        descriptions_niv2 = driver.find_element(By.XPATH,
                                                "//div[@class='css-fxq50d']/div/span/span[@class='tw-text-secondary']").text
    except:
        descriptions_niv2 = ''
    description = descriptions_niv1 + ' ' + descriptions_niv2

    # Try/except to handle cases without tips
    try:
        tips = driver.find_element(By.CSS_SELECTOR, "div[class='css-1xrtte3']").text
    except:
        tips = ''
    return {"9.Description": description, "10.tips": tips}


def get_way_type_and_surfaces(drive):
    """
    :param driver
    :return: Collect the types of ways and types of surfaces of the hike
    """
    url = driver.current_url
    try:
        way_type = driver.find_element(By.XPATH, "//div[@class='tw-p-4 sm:tw-p-6 ']/div[@class='tw-mb-6']").text
        listed_text = way_type.split("\n")
        types_and_distances = {}
        for type_and_distance in listed_text[1:]:
            distances_in_km = {"km": 1.0, "mi": 1.60934, "yd": 0.0009144, "m": 0.001}
            key = type_and_distance.split(":")[0] + " (km)"
            if len(type_and_distance.split(":")[1].split()) == 2:
                unit = type_and_distance.split(":")[1].split()[1]
                distance = float(type_and_distance.split(":")[1].split()[0]) * distances_in_km[unit]
            elif len(type_and_distance.split(":")[
                         1].split()) == 3:  ###ASSUMPTION: if the distance shows > 109m the "less than" is neglected
                unit = type_and_distance.split(":")[1].split()[2]
                distance = float(type_and_distance.split(":")[1].split()[1]) * distances_in_km[unit]
            value = round(distance, 2)
            types_and_distances[key] = value
        logging.info(f'Success: The way types and surfaces of this url ({url}) was found')
        return types_and_distances
    except:
        logging.warning(f'The way types and surfaces of this url ({url}) was not found')
        return {}


def get_localisation(drive):
    """
    :param driver
    :return: Collect the 3 levels of localisation following 'Hiking trails & Routes'
    Note1: the localisation are sometimes duplicated. The way to optimize the collection of unique values is to take the 3 first level after 'Hiking trails & Routes'
    Note2: There is no consistency between the collected levels and the official administrative geographical levels.
    """
    url = driver.current_url
    localisation = dict()
    try:
        geography = driver.find_elements(By.XPATH, "//div[@class='css-1jg13ty']/*[@href]")
        record = 0
        all_loc = list()
        # The scrapping returns several times the same info: we identified that starting to record after Hiking trails & Routes is a good method. We stop after 3 levels because there can be repetition
        for geo in geography:
            all_loc.append(geo.text)
            if geo.text == 'Discover':
                pass
            else:
                if geo.text == 'Hiking trails & Routes':
                    record += 1
                elif record == 1:
                    localisation["level 1"] = geo.text
                    record += 1
                elif record == 2:
                    localisation["level 2"] = geo.text
                    record += 1
                elif record == 3:
                    localisation["level 3"] = geo.text
        localisation["all levels"] = all_loc
        logging.info(f'Success: The localisation of this url ({url}) was found')
        print(localisation)
        return localisation
    except:
        logging.warning(f'The localisation of this url ({url}) was not found')
        return {}


def get_hike_info(drive):
    """
    :param driver
    :return: Activate the get_info functions and return a dictionary with all the infos
    """
    url = {"url": driver.current_url}
    basic_hike_info = get_basic_hike_info(drive)
    way_type_and_surfaces = get_way_type_and_surfaces(drive)
    description = get_descriptions(driver)
    localisation = get_localisation(driver)
    information = {**basic_hike_info, **description, **localisation, **way_type_and_surfaces, **url}
    return (information)


if __name__ == "__main__":
    try:
        drive = driver_get_url(url)
        print(get_hike_info(drive))
        # print(get_localisation(drive))
        end = time.time() - start
        print(end)


    except:
        print('next hike')
