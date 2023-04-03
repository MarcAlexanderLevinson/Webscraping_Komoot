import get_hiking_urls as gu
import get_hike_info as hi
import create_database as cd
from tqdm.auto import tqdm
import csv
import json
import logging
import argparse

logging.basicConfig(format='%(asctime)s ---- %(levelname)s:%(message)s - row %(lineno)d',
                    level=logging.INFO)

with open("komoot_config.json", 'r') as f:
    config = json.load(f)
BASE_URL = config["URL"]
HIKING_DATA_CSV = config["HIKES_INFO_CSV"]


parser = argparse.ArgumentParser(description="""
Welcome to the Komoot webscraper, here you can get all the information
you need about hikes around Lyon. Just choose the amount of hiking pages you want to scrape and the data types you want 
to retrieve, the datatypes are set to all datatypes by default, the amount of hikes need specification and is multiplied 
by 12, since this is how many hikes are present per hiking page!!!!
Example for scraping all data from 24 hikes:
python get_all_hike_info.py 2
Example for scraping title, location and difficulty from 120 hikes:
python get_all_hike_info.py 10 title location difficulty
""")

parser.add_argument('number_of_hiking_pages_to_scrape',
                    type=int,
                    default="1",
                    help="""each hiking page contains 12 hikes, to the input given is multiplied by 12 for the total of
                         hikes that will be scraped. E.g. if the input is 5, a total of 60 hikes will be scraped""")

    parser.add_argument("datatypes_to_be_scraped",
                    choices=["title", "difficulty", "duration", "distance", "average_speed", "uphill", "downhill",
                             "description", "tip", "way_types_and_surfaces", "location", "all"],
                    nargs='*',
                    default="all",
                    help="""which datatypes would you like to scrape, please choose any of the following options: title, 
                    difficulty, duration, distance, average_speed, uphill, downhill, description, tip,
                    way_types_and_surfaces, location or all. The later selects all of the elements. BEWARE!!!! You 
                    can only add the scraped data to an SQL database if you scrape all datatypes. If that is what you
                    want the default input is good, so just skipp this part""")

args = parser.parse_args()
number_of_pages_to_scrape = args.number_of_hiking_pages_to_scrape
list_of_datatypes = args.datatypes_to_be_scraped

def ask_user_choice(list_of_datatypes):
    """
    Ask the user whether he wants to re-use the previous list of hike urls (choice Y) or re-run the whole code,
    including the collection of hike urls (choice N)
    """
    use_csv = input("""\n\nWould you like to use the links stored in the list_of_hiking_urls.csv file, then type "Y".
         \n\nIf you would like to determine the list of urls by running the code then type "N".
         \n\nAnswer: """)
    if list_of_datatypes == "all":
        data_storage = input("""\n\nDo you want the data to be stored in a csv, then type "CSV".\n If you want it stored in 
                                    an SQL database then type "SQL".\n If you want it stored in both then type "BOTH"\n\nAnswer: 
                                    """)
    else:
        data_storage = "CSV"

    if data_storage == "SQL" or data_storage == "BOTH":
        host, user, password = cd.ask_for_user_credentials()
    else:
        host, user, password = "", "", ""

    if use_csv == "N":
        hiking_urls = gu.get_all_hikes_urls(BASE_URL, number_of_pages_to_scrape)
        gu.write_urls_to_csv(hiking_urls)
    elif use_csv == "Y":
        with open("list_of_hiking_urls.csv", "r") as hike_urls_csv:
            hiking_urls = hike_urls_csv.read().splitlines()
    else:
        print("Please run code again and give correct input this time")

    return hiking_urls, data_storage, host, user, password


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


def main():
    # Ask the choice of the user: re-use the last saved list of hike urls, or collect them again from a catalogue page
    hiking_urls, data_storage, host, user, password = ask_user_choice(list_of_datatypes)
    # Create the list that will store all the hikes infos (the infos of one hike are stored in a dictionary)
    hikes_infos = []

    # For each hike url, we call get_hike_info(). Once we collected the info (and stored it in a dictionary),
    # we store it in the list 'hikes_infos'
    for hike_id, hike_url in enumerate(tqdm(hiking_urls)):
        hikes_infos.append(hi.get_hike_info(hike_id, hike_url, list_of_datatypes))

    # We create a csv from the list of hikes infos
    if data_storage == "CSV" or data_storage == "BOTH":
        write_csv(hikes_infos)

    # Writing all data into the database
    if data_storage == "SQL" or data_storage == "BOTH":
        cd.create_database_tables(host, user, password)
        cd.populate_country(hikes_infos, host, user, password)
        cd.populate_region(hikes_infos, host, user, password)
        cd.populate_difficulty(hikes_infos, host, user, password)
        cd.populate_hikes_tables(hikes_infos, host, user, password)


if __name__ == "__main__":
    main()
