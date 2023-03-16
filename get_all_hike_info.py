import get_hiking_urls as GU
import get_hike_info as HI
from tqdm.auto import tqdm


base_url = "https://www.komoot.com/discover/Lyon/@45.7575926%2C4.8323239/tours?max_distance=5000&sport=hike&map=true&pageNumber=" #Url for 5km Lyon
list_of_hiking_urls = GU.get_all_hiking_urls(base_url)
print(list_of_hiking_urls)
print(len(list_of_hiking_urls))

hike_ID = 1
hikes = {}

# for url in tqdm(list_of_hiking_urls):
#     hikes[hike_ID] = HI.get_hike_info(url)
#     hike_ID += 1
#
# print(hikes)





