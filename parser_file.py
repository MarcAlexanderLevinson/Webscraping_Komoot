import argparse


def parser():
    parser = argparse.ArgumentParser(description="""
    Welcome to the Komoot webscraper, here you can get all the information
    you need about hikes around Lyon. Just choose the amount of hiking pages you want to scrape and the data types you want 
    to retrieve, the datatypes are set to all datatypes by default, the amount of hikes need specification and are multiplied 
    by 12, since this is how many hikes are present per hiking page!!!!
    Example for scraping all data from 24 hikes:
    python get_all_hike_info.py 2
    Example for scraping title, location and difficulty from 120 hikes:
    python get_all_hike_info.py 10 title location difficulty
    """)

    parser.add_argument('-a',
                        '--action_to_perform',
                        choices=["scrape", "weather_info", 'both'],
                        default="both",
                        help="""which action would you like to perform, please choose any of the following options:
                        - scrap: scrap the website and populate the database with the collected information
                        - weather_info : get the weather info from all the cities of hikes previously collected
                        """)

    parser.add_argument('-n', '--number_of_catalogue_pages_to_scrape',
                        action='store',
                        type=int,
                        default="1",
                        help="""each catalogue page contains 12 hikes, so the input given multiplied by 12 gives the 
                            total number of hikes that will be scraped. E.g. if the input is 5, a total of 60 hikes will 
                            be scraped""")

    parser.add_argument('-d', '--datatypes_to_be_scraped',
                        choices=["title", "difficulty", "duration", "distance", "average_speed", "uphill", "downhill",
                                 "description", "tip", "way_types_and_surfaces", "location", "all"],
                        nargs='*',
                        default="all",
                        help="""which datatypes would you like to scrape, please choose any of the following options: title,
                        difficulty, duration, distance, average_speed, uphill, downhill, description, tip,
                        way_types_and_surfaces, location or all. The later selects all of the elements. BEWARE!!!! You
                        can only add the scraped data to an SQL database if you scrape all datatypes. If that is what you
                        want the default input is good, so just skipp this part""")

    parser.add_argument('-c', '--old_catalogue',
                        choices=["Y", "N"],
                        default="N",
                        help="""with Y the scrapping won't re-scrap the catalogue pages, but will re-use the last scrapped 
                        catalogue pages results (stored in the list_of_hiking_urls.csv file).
                        With N, the list of hikes will be determined again, by scrapping first the catalogue page""")

    parser.add_argument('-s', '--storage',
                        choices=["SQL", "CSV", "BOTH"],
                        default="CSV",
                        help="""indicates where the result of the scrapping is stored: in the SQL database, in a csv, 
                        or in both""")

    parser.add_argument('-l', '--localhost', action='store', help="""required in case SQL is chosen for storage""")
    parser.add_argument('-u', '--user', action='store', help="""required in case SQL is chosen for storage""")
    parser.add_argument('-p', '--password', action='store', help="""required in case SQL is chosen for storage""")

    return parser.parse_args()
