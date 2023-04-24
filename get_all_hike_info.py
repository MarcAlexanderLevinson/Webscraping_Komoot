import get_hiking_urls as gu
import get_hike_info as hi
import create_database as cd
import pymysql.cursors
from tqdm.auto import tqdm
import csv
import json
import logging
import parser_file as pa
import weather_API as w_api

logging.basicConfig(format='%(asctime)s ---- %(levelname)s:%(message)s - row %(lineno)d',
                    level=logging.INFO)

with open("komoot_config.json", 'r') as f:
    config = json.load(f)
BASE_URL = config["URL"]
HIKING_DATA_CSV = config["HIKES_INFO_CSV"]
######
BOTH = config["BOTH"]
SQL = config["SQL"]
CSV = config["CSV"]
ALL = config["ALL"]
N = config["N"]
Y = config["Y"]


def check_sql_info(storage, localhost, user, password, datatypes_to_be_scraped):
    """
    This function will:
    - check that the choices of the user are consistent :
      - if he chooses to store in SQL, he must provide the connection information (localhost, user, password).
        Otherwise it raises an error
      - if he chooses to store in SQL, he must choose to scrape all the information, not just a subset
    - if he chooses to store in SQL, that the connection can be made. Otherwise it returns an error
    """
    if (BOTH in storage or SQL in storage) and (localhost is None or user is None or password is None):
        raise Exception(
            "Sorry, if you want to store the data in SQL, you need to provide the localhost, user and password info")
    elif BOTH in storage or SQL in storage:
        try:
            mydb = pymysql.connect(
                host=localhost,
                user=user,
                password=password
            )
        except RuntimeError:
            raise Exception("There was a problem to connect to MySQL. You may need to"
                            " open MySQL first on your computer, and/or check the SQL information provided "
                            " (localhost, user or password)")

    if datatypes_to_be_scraped != ALL and (BOTH in storage or SQL in storage):
        raise Exception("You want to store the data in SQL but have only selected a subset of datatypes to scrap."
                        " This is not possible. If you want to store in SQL, you need to select 'all' datatypes")


def list_of_keys(hikes_infos):
    """
    This function takes a list of dictionaries, and return the keys across all dictionaries
    This will be used to create the column of our csv
    In our code, each dictionary stores the info of one hike, and so the list of dictionaries store the info of all the
    hikes.  This step is necessary because all the hikes do not have the same info on the website, and therefore we do
    not have the same keys for each dictionary
    """
    set_of_all_keys = set()
    for hike in hikes_infos:
        set_of_all_keys.update(list(hike.keys()))
    return sorted(list(set_of_all_keys))


def write_csv(hikes_infos):
    """
    Write the csv from the list of hikes infos
    """
    csv_colums = list_of_keys(hikes_infos)
    with open(HIKING_DATA_CSV, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_colums)
        writer.writeheader()
        for data in hikes_infos:
            writer.writerow(data)


def scraper(old_catalogue, user_inputs, list_of_datatypes, data_storage, host, user, password):
    # Get the list of hiking urls to scrap: either re-use the previous list of hiking_urls (Y) or re-scrap from scratch (N)
    if old_catalogue == N:
        hiking_urls = gu.get_all_hikes_urls(BASE_URL, user_inputs.number_of_catalogue_pages_to_scrape)
        gu.write_urls_to_csv(hiking_urls)
    elif old_catalogue == Y:
        with open("list_of_hiking_urls.csv", "r") as hike_urls_csv:
            hiking_urls = hike_urls_csv.read().splitlines()

    # Create the list that will store all the hikes infos (the infos of one hike are stored in a dictionary)
    hikes_infos = []

    # For each hike url, we call get_hike_info(). Once we collected the info (and stored it in a dictionary),
    # we store it in the list 'hikes_infos'
    for hike_id, hike_url in enumerate(tqdm(hiking_urls)):
        hikes_infos.append(hi.get_hike_info(hike_id, hike_url, list_of_datatypes))

    # We create a csv from the list of hikes infos
    if data_storage == CSV or data_storage == BOTH:
        write_csv(hikes_infos)

    # Writing all data into the database
    if data_storage == SQL or data_storage == BOTH:
        cd.write_database(hikes_infos, host, user, password)


def add_weather_info(host, user, password):
    w_api.create_table_weather(host, user, password)
    df_locations = w_api.select_locations(host, user, password)
    df_locations_lat_long = w_api.get_latitude_longitude(df_locations)
    weather_table = w_api.create_weather_table(df_locations_lat_long)
    w_api.populate_weather(weather_table, host, user, password)


def main():
    user_inputs = pa.parser()
    action_to_perform = user_inputs.action_to_perform
    old_catalogue = user_inputs.old_catalogue
    data_storage = user_inputs.storage
    host = user_inputs.localhost
    user = user_inputs.user
    password = user_inputs.password
    list_of_datatypes = user_inputs.datatypes_to_be_scraped

    # Stop the program if there is a mismatch in the user inputs
    check_sql_info(data_storage, host, user, password, list_of_datatypes)

    if action_to_perform == 'scrape' or action_to_perform == 'both':
        scraper(old_catalogue, user_inputs, list_of_datatypes, data_storage, host, user, password)

    if action_to_perform == 'weather_info' or action_to_perform == 'both':
        add_weather_info(host, user, password)


if __name__ == "__main__":
    main()