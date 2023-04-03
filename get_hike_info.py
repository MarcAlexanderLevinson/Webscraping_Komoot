import time
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import logging

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
driver.set_window_size(2700, 2000)
driver.implicitly_wait(5)

url = """https://www.komoot.com/smarttour/e926612355/
         mont-colombier-massif-des-bauges-boucle?tour_origin=smart_tour_search"""


def distance_converter(distance_with_unit):
    """ Takes a string as an argument with a distance e.g. "10.20 mi" and converts this a float in km's, e.g. 16.41 """
    conversions_to_km = {"km": 1.0, "km/h": 1.0, "mi": 1.60934, "yd": 0.0009144, "m": 0.001, "m/h": 0.001,
                         "ft": 0.0003048, "mph": 1.60934}
    distance_in_km = float(distance_with_unit.split()[0]) * conversions_to_km[distance_with_unit.split()[1]]
    return distance_in_km


def driver_get_url(url):
    """
    :param url of the hike page to scrap
    """
    driver.get(url)
    driver.implicitly_wait(5)
    logging.info(f'Success: The drive of this url {url} was obtained')


def get_hike_title():
    """
    :return the title of the hike
    """
    try:
        title = driver.find_element(By.CSS_SELECTOR, "span[class*='tw-mr-1 tw-font-bold']").text
        return {f"2.title": title}
    except:
        logging.warning(f'The hike title of this url ({url}) was not found')
        return {"2.title": ""}


def get_difficulty():
    try:
        difficulty = driver.find_element(By.CSS_SELECTOR, "div[class*='tw-flex tw-items-center']").text
        return {f"3.difficulty": difficulty}
    except:
        logging.warning(f'The hike difficulty of this url ({url}) was not found')
        return {"3.difficulty": ""}


def get_duration():
    try:
        duration = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='t_duration_value']").text
        return {f"4.duration": duration}
    except:
        logging.warning(f'The hike duration of this url ({url}) was not found')
        return {"4.duration": ""}


def get_distance():
    url = driver.current_url
    try:
        distance_text = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='t_distance_value']").text
        distance = round(distance_converter(distance_text), 2)
        return {f"5.distance": distance}
    except:
        logging.warning(f'The hike distance of this url ({url}) was not found')
        return {"5.distance": ""}


def get_average_speed():
    url = driver.current_url
    try:
        average_speed_text = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='t_speed_value']").text
        average_speed = round(distance_converter(average_speed_text))
        return {f"6.average_speed": average_speed}
    except:
        logging.warning(f'The hike average speed of this url ({url}) was not found')
        return {"6.average_speed": ""}


def get_uphill():
    url = driver.current_url
    try:
        uphill_text = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='t_elevation_up_value']").text
        uphill_text = uphill_text.replace(",", "")
        uphill = round(distance_converter(uphill_text) * 1000, 2)  # This one is put in m instead of km's
        return {f"7.uphill": uphill}
    except:
        logging.warning(f'The hike uphill meters of this url ({url}) was not found')
        return {"7.uphill": ""}


def get_downhill():
    url = driver.current_url
    try:
        downhill_text = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='t_elevation_down_value']").text
        downhill_text = downhill_text.replace(",", "")
        downhill = round(distance_converter(downhill_text) * 1000, 2)  # This one is put in m instead of km's
        return {f"8.downhill": downhill}
    except:
        logging.warning(f'The hike downhill meters of this url ({url}) was not found')
        return {"8.downhill": ""}


def get_description():
    """
    :return: Collect the descriptions (description and tip) of the hike. On some pages, the description is split in 2
     classes. Some page don't have tips
    """
    url = driver.current_url
    try:
        descriptions_niv1 = driver.find_element(By.XPATH,
                                                "//div[@class='css-fxq50d']/div/span[@class='tw-text-secondary']").text
        logging.info(f'Success: The description level 1 of this url ({url}) was found')
    except:
        logging.warning(f'The description level 1 of this url ({url}) was not found')
        return {f"9.description": ""}

    try:  # Try/except to handle cases without the 2nd part of the description
        descriptions_niv2 = driver.find_element(By.XPATH,
                                        "//div[@class='css-fxq50d']/div/span/span[@class='tw-text-secondary']").text
    except:
        descriptions_niv2 = ''
    description = descriptions_niv1 + ' ' + descriptions_niv2
    return {f"9.description": description}


def get_tip():
    url = driver.current_url
    try:
        tips = driver.find_element(By.CSS_SELECTOR, "div[class='css-1xrtte3']").text
        logging.info(f'Success: The hike tip this url ({url}) was found')
        return {f"91.tips": tips}
    except:
        logging.warning(f'The hike tip of this url ({url}) was not found')
        return {f"91.tips": ""}


def way_type_converter(raw_way_type_info):
    """
    :param raw_way_type_info: This is a string containing information about a specific way type e.g. "Path: 0.66 mi",
    or "Path: < 0.1 mi".
    :return: a dictionary with way type as key and distance as value, if the input distance is not in km the function
    converts it into km, e.g. {"Path": 1.06}
    """
    way_type = raw_way_type_info.split(":")[
                   0] + " (km)"  # The way type will be the key to the dictionary we will create: e.g. "Path (km)"
    distance_string = raw_way_type_info.split(":")[1]
    if "<" in distance_string:
        distance_string = distance_string.replace("<",
                                                  "")  # From the second example given in the docstring, if the distance
        # includes the > sign, this sign will be removed
    distance = round(distance_converter(distance_string), 2)
    return {way_type: distance}


def get_way_types_and_surfaces():
    """
    :return: Collect the types of ways and types of surfaces of the hike
    """
    url = driver.current_url
    try:
        way_type_info = driver.find_element(By.XPATH, "//div[@class='tw-p-4 sm:tw-p-6 ']/div[@class='tw-mb-6']").text
        listed_text = way_type_info.split(
            "\n")  # This creates a list looking like: ['WAYTYPES', 'Path: 0.66 mi', 'Street: 0.45 mi', etc...]
        types_and_distances = {}
        for raw_way_type_info in listed_text[1:]:
            types_and_distances.update(way_type_converter(raw_way_type_info))
        logging.info(f'Success: The way types and surfaces of this url ({url}) was found')
        return types_and_distances
    except:
        logging.warning(f'The way types and surfaces of this url ({url}) was not found')
        return {}


def get_location():
    """
    :return: Collect the 3 levels of localisation following 'Hiking trails & Routes'
    Note1: the localisation are sometimes duplicated. The way to optimize the collection of unique values is to take
    the 3 first level after 'Hiking trails & Routes'
    Note2: There is no consistency between the collected levels and the official administrative geographical levels.
    """
    url = driver.current_url
    location = dict()
    try:
        geography = driver.find_elements(By.XPATH, "//div[@class='css-1jg13ty']/*[@href]")
        all_loc = [geo.text for geo in
                   geography]  # This returns a list of locations and some generic terms like "Discover" and "Hiking
                               # Trail", but also contains duplicates
        all_loc = list(filter(lambda x: x != 'Discover' and x != 'Hiking trails & Routes',
                              all_loc))  # This removes the generic terms
        all_loc = list(dict.fromkeys(all_loc))  # This removes all duplicates

        location["Country"] = all_loc[0]
        location["Region"] = all_loc[1]
        location["Most accurate location"] = all_loc[-1]
        logging.info(f'Success: The location of this url ({url}) was found')
        return location
    except:
        logging.warning(f'The location of this url ({url}) was not found')
        return {}


def get_hike_info(index, url, list_of_datatypes = ["all"]):
    """
    :param index: the id of the hike for the database, url: url of the link to the hike, list_of_datatypes: list of
    datatypes that the user wants to retrieve from the url. This can be set at "all" or as a list of strings, such as
    ["title", "description", "location"]
    :return: a dictionary of the requested hiking datatypes
    """
    driver_get_url(url)
    dictionary_of_datatype_functions = {"title": get_hike_title, "difficulty": get_difficulty, "duration": get_duration,
                                        "distance": get_distance, "average_speed": get_average_speed,
                                        "uphill": get_uphill,
                                        "downhill": get_downhill, "description": get_description, "tip": get_tip,
                                        "way_types_and_surfaces": get_way_types_and_surfaces, "location": get_location}

    if list_of_datatypes == "all":
        list_of_datatypes = list(dictionary_of_datatype_functions)
    try:
        hike_info = {"1.ID": index}
        for data_type in list_of_datatypes:
            hike_info.update(dictionary_of_datatype_functions[data_type]())
        hike_info.update({"url": url})
        return hike_info
    except:
        logging.warning(f'The hike of the {url} url was not recorded')


if __name__ == "__main__":
    try:
        print(get_hike_info(1, url, ["all"]))
        end = time.time() - start
        print(end)
    except:
        print('next hike')
