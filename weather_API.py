import warnings
import requests
import pandas as pd
from tqdm.auto import tqdm
import create_database as cd
import logging

warnings.filterwarnings('ignore')

host = "localhost"
user = "root"
password = "root"

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
    mydb, mycursor = cd.connect_to_komoot(host, user, password)
    sql = """SELECT city.id, city.city, country.country
                FROM city
                INNER JOIN country
                ON city.country_id = country.id
                WHERE city.id NOT IN (SELECT city_id FROM weather)"""
    mycursor.execute(sql)
    locations = mycursor.fetchall()
    df_locations = pd.DataFrame(locations, columns=['city_id', 'city', 'country'])
    logging.info(f'Success: locations dataframe has been made')
    return df_locations


def get_latitude_longitude(df_locations):
    df_locations['lat'] = 0
    df_locations['long'] = 0

    # This adds lat and long per city to the locations
    for index, row in tqdm(df_locations.iterrows(), len(df_locations)):
        city = df_locations.loc[index, 'city']
        country = df_locations.loc[index, 'country']

        api_url = f"https://api.api-ninjas.com/v1/geocoding?city={city}&country={country}"
        response = requests.get(api_url, headers={'X-Api-Key': 'qTqfq/KXTqb6JVfGoAynbA==Pmkuqirz5JiJL68B'})

        if response.status_code == requests.codes.ok:

            try:
                lat, long = response.json()[0]['latitude'], response.json()[0]['longitude']
                df_locations.loc[index, 'lat'] = lat
                df_locations.loc[index, 'long'] = long

            except IndexError:
                pass

        else:
            pass

    logging.info(f'Success: locations dataframe has been made')
    return df_locations


def create_weather_table(df_locations_lat_long):
    start_date = '2013-04-01'
    end_date = '2023-04-01'

    weather_table = pd.DataFrame()

    for index, row in tqdm(df_locations_lat_long.iterrows(), len(df_locations_lat_long)):
        lat = df_locations_lat_long.loc[index, 'lat']
        long = df_locations_lat_long.loc[index, 'long']

        url = f"https://archive-api.open-meteo.com/v1/archive?latitude={str(lat)}&longitude={str(long)}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,precipitation_hours&timezone=Europe%2FBerlin"
        r = requests.get(url, timeout=10)
        data = r.json()
        weather_per_location = pd.DataFrame(data['daily'])
        weather_per_location['city_id'] = df_locations_lat_long['city_id'][index]

        weather_table = pd.concat([weather_table, weather_per_location], ignore_index=True)
        weather_table['id'] = weather_table.index

    return weather_table

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

        city_id = row["city_id"]
        date = row["time"]
        max_temperature = row["temperature_2m_max"]
        min_temperature = row["temperature_2m_min"]
        avg_temperature = row["temperature_2m_mean"]
        daily_precipitation_mm = row["precipitation_sum"]
        daily_precipitation_hours = row["precipitation_hours"]

        mycursor.execute(sql_weather, [city_id, date, max_temperature, min_temperature, avg_temperature, daily_precipitation_mm, daily_precipitation_hours])

    mydb.commit()
