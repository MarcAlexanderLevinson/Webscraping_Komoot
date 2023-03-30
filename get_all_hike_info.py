import get_hiking_urls as gu
import get_hike_info as hi
from tqdm.auto import tqdm
import csv
import json
import logging

logging.basicConfig(format='%(asctime)s ---- %(levelname)s:%(message)s - row %(lineno)d',
                    level=logging.INFO)

with open("komoot_config.json", 'r') as f:
    config = json.load(f)
NUMBER_OF_PAGES_TO_SCRAP = config["NUMBER_OF_PAGES_TO_SCRAP"]
BASE_URL = config["URL"]
HIKING_DATA_CSV = config["HIKES_INFO_CSV"]


def ask_user_choice():
    """
    Ask the user whether he wants to re-use the previous list of hike urls (choice Y) or re-run the whole code,
    including the collection of hike urls (choice N)
    """
    use_csv = input("""Would you like to use the links stored in the list_of_hiking_urls.csv file, then type "Y".
         If you would like to determine the list of urls by running the code then type "N".
         Answer: """)
    if use_csv == "N":
        hiking_urls = gu.get_all_hikes_urls(BASE_URL, NUMBER_OF_PAGES_TO_SCRAP)
        gu.write_urls_to_csv(hiking_urls)
    elif use_csv == "Y":
        with open("list_of_hiking_urls.csv", "r") as hike_urls_csv:
            hiking_urls = hike_urls_csv.read().splitlines()
    else:
        print("Please run code again and give correct input this time")
    print("list of hiking urls done")
    return hiking_urls


def list_of_keys(hikes_infos):
    """
    This function takes a list of dictionaries, and return the keys across all dictionaries
    This will be used to create the column of our csv
    In our code, each dictionary stores the info of one hike, and so the list of dictionaries store the info of all the hikes
    This step is necessary because all the hikes do not have the same info on the website, and therefore we do not have the same keys for each dictionary
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
    hiking_urls = ask_user_choice()
    # Create the list that will store all the hikes infos (the infos of one hike are stored in a dictionary)
    hikes_infos = []

    # For each hike url, we call get_hike_info(). Once we collected the info (and stored it in a dictionary),
    # we store it in the list 'hikes_infos'
    for hike_id, hike_url in enumerate(tqdm(hiking_urls)):
        hikes_infos.append(hi.get_hike_info(hike_id, hike_url))

    # We create a csv from the list of hikes infos
    write_csv(hikes_infos)


if __name__ == "__main__":
    main()
