import get_hiking_urls as GU
import get_hike_info as HI
from selenium import common
from tqdm.auto import tqdm
import csv
import logging

logging.basicConfig( format='%(asctime)s ---- %(levelname)s:%(message)s - row %(lineno)d',
                    level=logging.INFO)
# filename='hike_scrapping.log',



def main():
    base_url = "https://www.komoot.com/discover/Lyon/@45.7575926%2C4.8323239/tours?max_distance=200000&sport=hike&map=true&pageNumber="  # Url for 5km Lyon
    amount_of_pages_to_be_scraped = 3
    use_csv = input("""Would you like to use the links stored in the list_of_hiking_urls.csv file, then type "Y".
     If you would like to determine the list of urls by running the code then type "N".
     Answer: """)
    if use_csv == "N":
        list_of_hiking_urls = GU.get_all_hiking_urls(base_url, amount_of_pages_to_be_scraped)
        GU.write_urls_to_csv(list_of_hiking_urls)
    elif use_csv == "Y":
        with open("list_of_hiking_urls.csv", "r") as hike_urls_csv:
            list_of_hiking_urls = hike_urls_csv.read().splitlines()
    else:
        print("Please run code again and give correct input this time")
    print("list of hiking urls done")
    hike_ID = 1
    list_of_hikes = []

    for url in tqdm(list_of_hiking_urls):  # check if iterator is well set, for testing put [:2]
        print(url)
        # For each hike, we try to retrieve all the hike infos and put the resulting dictionary in a list
        try:
            hike = {}
            drive = HI.driver_get_url(url)
            hike["1.ID"] = hike_ID
            hike.update(HI.get_hike_info(drive))
            hike_ID += 1
            list_of_hikes.append(hike)
            print(hike)
        # In case one of the info of the hike was not retrieved, we don't record this hike at all
        except:
            logging.warning(f'The hike of the {url} url was not recorded')

    set_of_all_keys = set()
    for hike in list_of_hikes:
        set_of_all_keys.update(list(hike.keys()))
    list_of_keys = (list(set_of_all_keys))
    list_of_keys.sort()

    csv_colums = list_of_keys
    print(list_of_keys)

    csv_file = "Hiking_data.csv"
    with open(csv_file, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_colums)
        writer.writeheader()
        for data in list_of_hikes:
            writer.writerow(data)

if __name__ == "__main__":
    main()