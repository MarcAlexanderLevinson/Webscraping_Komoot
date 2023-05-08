import time
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import common
from webdriver_manager.chrome import ChromeDriverManager
import logging
import json

with open("komoot_config.json", 'r') as f:
    config = json.load(f)
ALL = config["ALL"]
WINDOW_SIZE_WIDTH = config["set_window_size_width"]
WINDOW_SIZE_HEIGHT = config["set_window_size_height"]
IMPLICIT_WAIT_1 = config["implicit_wait_1"]
IMPLICIT_WAIT_2 = config["implicit_wait_2"]
CONVERSIONS_TO_KM = config["conversions_to_km"]
TITLE_HTML = config["title_html"]
DIFFICULTY_HTML = config["difficulty_html"]
DURATION_HTML = config["duration_html"]
DISTANCE_HTML = config["distance_html"]
SPEED_HTML = config["speed_html"]
UPHILL_HTML = config["uphill_html"]
DOWNHILL_HTML = config["downhill_html"]
DESCRIPTION_1_HTML = config["description_1_html"]
DESCRIPTION_2_HTML = config["description_2_html"]
TIP_HTML = config["tip_html"]
WAY_TYPES_SURFACES_HTML = config["way_types_surfaces_html"]
LOCATION_HTML = config["location_html"]
ID_NAME = config["id_name"]
TITLE_NAME = config["title_name"]
DIFFICULTY_NAME = config["difficulty_name"]
DURATION_NAME = config["duration_name"]
DISTANCE_NAME = config["distance_name"]
AVERAGE_SPEED_NAME = config["average_speed_name"]
UPHILL_NAME = config["uphill_name"]
DOWNHILL_NAME = config["downhill_name"]
DESCRIPTION_NAME = config["description_name"]
TIPS_NAME = config["tips_name"]
TEST_URL = config["test_url"]

start = time.time()
# start by defining the options
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")  # it's more scalable to work in headless mode
options.page_load_strategy = config["page_load_strategy"]
# this returns the path web driver downloaded
chrome_path = ChromeDriverManager().install()
chrome_service = Service(chrome_path)
# pass the defined options and service objects to initialize the web driver
driver = Chrome(options=options, service=chrome_service)
driver.set_window_size(WINDOW_SIZE_WIDTH, WINDOW_SIZE_HEIGHT)
driver.implicitly_wait(IMPLICIT_WAIT_1)


def distance_converter(distance_with_unit):
    """ Takes a string as an argument with a distance e.g. "10.20 mi" and converts this a float in km's, e.g. 16.41 """
    unit = distance_with_unit.split()[1]
    distance_with_unit = distance_with_unit.split()[0].replace(",", ".")
    distance_in_km = float(distance_with_unit) * CONVERSIONS_TO_KM[unit]
    return distance_in_km


def driver_get_url(url):
    """
    :param url of the hike page to scrap
    """
    driver.get(url)
    driver.implicitly_wait(IMPLICIT_WAIT_2)
    logging.info(f'Success: The drive of this url {url} was obtained')


def get_hike_title():
    """
    :return the title of the hike
    """
    url = driver.current_url
    try:
        title = driver.find_element(By.CSS_SELECTOR, TITLE_HTML).text
        return {TITLE_NAME: title}
    except common.exceptions.WebDriverException as err:
        logging.warning(f'The hike title of this url ({url}) was not found: {err}')
        return {TITLE_NAME: ""}


def get_difficulty():
    """
    :return the difficulty of the hike
    """
    url = driver.current_url
    try:
        difficulty = driver.find_element(By.CSS_SELECTOR, DIFFICULTY_HTML).text
        return {DIFFICULTY_NAME: difficulty}
    except common.exceptions.WebDriverException as err:
        logging.warning(f'The hike difficulty of this url ({url}) was not found: {err}')
        return {DIFFICULTY_NAME: ""}


def get_duration():
    """
    :return the duration of the hike
    """
    url = driver.current_url
    try:
        duration = driver.find_element(By.CSS_SELECTOR, DURATION_HTML).text
        return {DURATION_NAME: duration}
    except common.exceptions.WebDriverException as err:
        logging.warning(f'The hike duration of this url ({url}) was not found: {err}')
        return {DURATION_NAME: ""}


def get_distance():
    """
    :return the distance of the hike
    """
    url = driver.current_url
    try:
        distance_text = driver.find_element(By.CSS_SELECTOR, DISTANCE_HTML).text
        distance = round(distance_converter(distance_text), 2)
        return {DISTANCE_NAME: distance}
    except common.exceptions.WebDriverException as err:
        logging.warning(f'The hike distance of this url ({url}) was not found: {err}')
        return {DISTANCE_NAME: ""}


def get_average_speed():
    """
    :return the average speed of the hike
    """
    url = driver.current_url
    try:
        average_speed_text = driver.find_element(By.CSS_SELECTOR, SPEED_HTML).text
        average_speed = round(distance_converter(average_speed_text))
        return {AVERAGE_SPEED_NAME: average_speed}
    except common.exceptions.WebDriverException as err:
        logging.warning(f'The hike average speed of this url ({url}) was not found: {err}')
        return {AVERAGE_SPEED_NAME: ""}


def get_uphill():
    """
    :return the total uphill of the hike
    """
    url = driver.current_url
    try:
        uphill_text = driver.find_element(By.CSS_SELECTOR, UPHILL_HTML).text
        uphill_text = uphill_text.replace(",", "")
        uphill = round(distance_converter(uphill_text) * 1000, 2)  # This one is put in m instead of km's
        return {UPHILL_NAME: uphill}
    except common.exceptions.WebDriverException as err:
        logging.warning(f'The hike uphill meters of this url ({url}) was not found: {err}')
        return {UPHILL_NAME: ""}


def get_downhill():
    """
    :return the total downhill of the hike
    """
    url = driver.current_url
    try:
        downhill_text = driver.find_element(By.CSS_SELECTOR, DOWNHILL_HTML).text
        downhill_text = downhill_text.replace(",", "")
        downhill = round(distance_converter(downhill_text) * 1000, 2)  # This one is put in m instead of km's
        return {DOWNHILL_NAME: downhill}
    except common.exceptions.WebDriverException as err:
        logging.warning(f'The hike downhill meters of this url ({url}) was not found: {err}')
        return {DOWNHILL_NAME: ""}


def get_description():
    """
    :return: Collect the descriptions (description and tip) of the hike. On some pages, the description is split in 2
     classes. Some page don't have tips
    """
    url = driver.current_url
    try:
        descriptions_niv1 = driver.find_element(By.XPATH,
                                                DESCRIPTION_1_HTML).text
        logging.info(f'Success: The description level 1 of this url ({url}) was found')
    except common.exceptions.WebDriverException as err:
        logging.warning(f'The description level 1 of this url ({url}) was not found: {err}')
        return {DESCRIPTION_NAME: ""}

    try:  # Try/except to handle cases without the 2nd part of the description
        descriptions_niv2 = driver.find_element(By.XPATH,
                                                DESCRIPTION_2_HTML).text
    except common.exceptions.WebDriverException:
        descriptions_niv2 = ''
    description = descriptions_niv1 + ' ' + descriptions_niv2
    return {DESCRIPTION_NAME: description}


def get_tip():
    """
    :return the tips of the hike
    """
    url = driver.current_url
    try:
        # tips = driver.find_element(By.CSS_SELECTOR, TIP_HTML).text
        # logging.info(f'Success: The hike tip this url ({url}) was found')
        return {TIPS_NAME: "Taken out of latest version"}
    except common.exceptions.WebDriverException as err:
        logging.warning(f'The hike tip of this url ({url}) was not found')
        return {TIPS_NAME: ""}


def way_type_converter(raw_way_type_info):
    """
    :param raw_way_type_info: This is a string containing information about a specific way type e.g. "Path: 0.66 mi",
    or "Path: < 0.1 mi".
    :return: a dictionary with way type as key and distance as value, if the input distance is not in km the function
    converts it into km, e.g. {"Path": 1.06}
    """
    way_type = raw_way_type_info.split(":")[0].lower()
    if way_type == 'natural':  # we change the name of this column because 'natural' is a word in SQL,
        # which poses problem down the line
        way_type = 'natural_terrain'
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
        way_type_info = driver.find_element(By.XPATH, WAY_TYPES_SURFACES_HTML).text
        listed_text = way_type_info.split(
            "\n")  # This creates a list looking like: ['WAYTYPES', 'Path: 0.66 mi', 'Street: 0.45 mi', etc...]
        types_and_distances = {}
        for raw_way_type_info in listed_text[1:]:
            types_and_distances.update(way_type_converter(raw_way_type_info))
        logging.info(f'Success: The way types and surfaces of this url ({url}) was found')
        return types_and_distances
    except common.exceptions.WebDriverException as err:
        logging.warning(f'The way types and surfaces of this url ({url}) was not found: {err}')
        return {}


def get_location():
    """
    :return: Collect the 3 levels of localisation following 'Hiking trails & Routes'
    Note1: the localisation are sometimes duplicated. The way to optimize the collection of unique values is to take
    the 3 first level after 'Hiking trails & Routes'
    Note2: There is no consistency between the collected levels and the official administrative geographical levels.
    """
    driver.implicitly_wait(IMPLICIT_WAIT_1)
    url = driver.current_url
    location = dict()
    try:
        geography = driver.find_elements(By.XPATH, "//div[@class='css-1jg13ty']/*[@href]")
        all_loc = [geo.text for geo in
                   geography]  # This returns a list of locations and some generic terms like "Discover" and
        # "Hiking Trail", but also contains duplicates
        all_loc = list(filter(lambda x: x != 'Discover' and x != 'Hiking trails & Routes' and x != '',
                              all_loc))  # This removes the generic terms

        unique_loc = []
        for index, place in enumerate(all_loc):
            if place not in all_loc[index + 1:]:
                unique_loc.append(place)

        location["Country"] = unique_loc[0]
        location["Region"] = unique_loc[1]
        location["City"] = unique_loc[-1]
        logging.info(f'Success: The location of this url ({url}) was found')
        return location

    except common.exceptions.WebDriverException as err:
        logging.warning(f'The location of this url ({url}) was not found: {err}')
        return {}


def get_hike_info(index, url, list_of_datatypes="all"):
    """
    :param
    index: the id of the hike for the database,
    url: url of the link to the hike,
    list_of_datatypes: list of datatypes that the user wants to retrieve from the url.
    This can be set at "all" or as a list of strings, such as
    ["title", "description", "location"]
    :return: a dictionary of the requested hiking datatypes
    """

    driver_get_url(url)
    DICTIONARY_OF_DATATYPE_FUNCTIONS = {"title": get_hike_title, "difficulty": get_difficulty, "duration": get_duration,
                                        "distance": get_distance, "average_speed": get_average_speed,
                                        "uphill": get_uphill,
                                        "downhill": get_downhill, "description": get_description, "tip": get_tip,
                                        "way_types_and_surfaces": get_way_types_and_surfaces, "location": get_location}

    if list_of_datatypes == ALL:
        list_of_datatypes = list(DICTIONARY_OF_DATATYPE_FUNCTIONS)
    try:
        hike_info = {ID_NAME: index}
        for data_type in list_of_datatypes:
            hike_info.update(DICTIONARY_OF_DATATYPE_FUNCTIONS[data_type]())
        hike_info.update({"url": url})
        return hike_info
    except:
        logging.warning(f'The hike of the {url} url was not recorded')

