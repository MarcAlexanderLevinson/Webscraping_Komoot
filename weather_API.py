import requests
import pandas as pd
from tqdm.auto import tqdm
import create_database as cd
import logging
import json

with open("komoot_config.json", 'r') as f:
    config = json.load(f)

LAT = config["lat"]
LONG = config["long"]
CITY2 = config["city2"]
COUNTRY2 = config["country2"]
LONGITUDE = config["longitude"]
LATITUDE = config["latitude"]
TIME = config["time"]
TEMPERATURE_2M_MAX = config["temperature_2m_max"]
TEMPERATURE_2M_MIN = config["temperature_2m_min"]
TEMPERATURE_2M_MEAN = config["temperature_2m_mean"]
PRECIPITATION_SUM = config["precipitation_sum"]
PRECIPITATION_HOURS = config["precipitation_hours"]
CITY_ID = config["city_id"]
VARIABLES = config["input_for_weather_api"]
BASE_API = config["base_for_weather_api"]


def create_table_weather(host, user, password):
    sql = """CREATE TABLE IF NOT EXISTS weather (
                      id INT AUTO_INCREMENT PRIMARY KEY,
                      city_id INT,
                      date DATE,
                      max_temperature FLOAT,
                      min_temperature FLOAT,
                      avg_temperature FLOAT,
                      daily_precipitation_mm FLOAT,
                      daily_precipitation_hours FLOAT,
                      FOREIGN KEY (city_id) REFERENCES city(id)
                    )"""
    cd.connect_and_execute(sql, host, user, password)
    logging.info(f'Success: weather table created')


def select_locations(host, user, password):
    """
    This function connects to the SQL database and fetches the cities and their corresponding countries and
    puts these in a pandas dataframe.
    :param host: hostname provided as parameter
    :param user: username provided as parameter
    :param password: password provided as parameter
    :return: pandas dataframe with three columns: city_id, city, country.
    """
    mydb, mycursor = cd.connect_to_komoot(host, user, password)
    sql = """SELECT city.id, city.city, country.country
                FROM city
                INNER JOIN country
                ON city.country_id = country.id
                WHERE city.id NOT IN (SELECT city_id FROM weather)"""
    mycursor.execute(sql)
    locations = mycursor.fetchall()
    df_locations = pd.DataFrame(locations, columns=[CITY_ID, CITY2, COUNTRY2])
    logging.info(f'Success: locations dataframe has been made')
    return df_locations


def get_latitude_longitude(df_locations):
    """
    This function takes in a pandas dataframe with cities and adds the latitude and longitude info to it by using an
    API.
    :param df_locations: pandas dataframe with three columns: city_id, city, country.
    :return: a pandas dataframe with 5 columns: city_id, city, country, lat, long.
    """
    df_locations[LAT] = 0
    df_locations[LONG] = 0

    # This adds lat and long per city to the locations
    for index, row in tqdm(df_locations.iterrows()):
        city = df_locations.loc[index, CITY2]
        country = df_locations.loc[index, COUNTRY2]

        api_url = f"https://api.api-ninjas.com/v1/geocoding?city={city}&country={country}"
        response = requests.get(api_url, headers={'X-Api-Key': 'qTqfq/KXTqb6JVfGoAynbA==Pmkuqirz5JiJL68B'})

        if response.status_code == requests.codes.ok:

            try:
                lat, long = response.json()[0][LATITUDE], response.json()[0][LONGITUDE]
                df_locations.loc[index, LAT] = lat
                df_locations.loc[index, LONG] = long

            except IndexError:
                pass

        else:
            pass

    logging.info(f'Success: latitude and longitude have been added to the locations dataframe')
    return df_locations


def create_weather_dataframe(df_locations_lat_long, SDATE, EDATE):
    """
    This function takes in a pandas dataframe with city locations and creates a new dataframe containing the daily
    weather information per city between 2013-04-01 and 2023-04-01. So that is approximately 3650 rows per city.
    :param df_locations_lat_long: a pandas dataframe with 5 columns: city_id, city, country, lat, long.
    :return: a pandas dataframe with 8 columns: id, city_id, date, max_temperature, min_temperature, avg_temperature,
    daily_precipitation_mm, daily_precipitation_hours.
    """

    weather_dataframe = pd.DataFrame()

    for index, row in tqdm(df_locations_lat_long.iterrows()):
        lat = df_locations_lat_long.loc[index, LAT]
        long = df_locations_lat_long.loc[index, LONG]
        url = f"""{BASE_API}latitude={str(lat)}&longitude={str(long)}&start_date={SDATE}&end_date={EDATE}&{VARIABLES}"""

        r = requests.get(url, timeout=10)
        data = r.json()
        weather_per_location = pd.DataFrame(data['daily'])
        weather_per_location['city_id'] = df_locations_lat_long['city_id'][index]

        weather_dataframe = pd.concat([weather_dataframe, weather_per_location], ignore_index=True)
        weather_dataframe['id'] = weather_dataframe.index

    logging.info(f'Success: weather dataframe has been made')
    return weather_dataframe


def populate_weather(weather_table, host, user, password):
    """
        Takes all the difficulties of the newly scrapped hikes and write them in SQL (if not already in there)
    """
    mydb, mycursor = cd.connect_to_komoot(host, user, password)

    for index, row in tqdm(weather_table.iterrows()):
        sql_weather = """INSERT INTO weather
                (city_id, date, max_temperature, min_temperature, avg_temperature, daily_precipitation_mm, daily_precipitation_hours)
                VALUES(%s, %s, %s, %s, %s, %s, %s)
                """

        city_id = row[CITY_ID]
        date = row[TIME]
        max_temperature = row[TEMPERATURE_2M_MAX]
        min_temperature = row[TEMPERATURE_2M_MIN]
        avg_temperature = row[TEMPERATURE_2M_MEAN]
        daily_precipitation_mm = row[PRECIPITATION_SUM]
        daily_precipitation_hours = row[PRECIPITATION_HOURS]

        mycursor.execute(sql_weather,
                         [city_id, date, max_temperature, min_temperature, avg_temperature, daily_precipitation_mm,
                          daily_precipitation_hours])

    logging.info(f'Success: weather table has been populated')
    mydb.commit()
