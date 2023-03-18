import get_hiking_urls as GU
import get_hike_info as HI
from tqdm.auto import tqdm
import csv


def main():
    base_url = "https://www.komoot.com/discover/Lyon/@45.7575926%2C4.8323239/tours?max_distance=5000&sport=hike&map=true&pageNumber="  # Url for 5km Lyon
    amount_of_pages_to_be_scraped = 23
    list_of_hiking_urls = GU.get_all_hiking_urls(base_url, amount_of_pages_to_be_scraped)

    hike_ID = 1
    list_of_hikes = []

    for url in tqdm(list_of_hiking_urls):
        hike = {}
        drive = HI.driver_get_url(url)
        hike["1.ID"] = hike_ID
        hike.update(HI.get_hike_info(drive))
        hike_ID += 1
        list_of_hikes.append(hike)
        print(hike)

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