import pymysql.cursors
from tqdm import tqdm
import logging

SURFACES = ['asphalt', 'gravel', 'natural_terrain', 'paved', 'unknown', 'unpaved', 'alpine']
WAY_TYPES = ['alpine_hiking_path', 'ferry', 'footpath', 'hiking_path', 'mountain_hiking_path', 'path', 'road',
             'state_road', 'street']


def ask_for_user_credentials():
    host = input("\n\nPlease give me your hostname/host: ")
    user = input("\n\nPlease give me your username/user: ")
    password = input("\n\nPlease give me your password: ")
    return host, user, password


def create_database(host, user, password):
    """
    Create the komoot database (or do nothing if already exists)
    :return:
    """
    # Connect to mysql
    mydb = pymysql.connect(
        host=host,
        user=user,
        password=password
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS komoot")
    mydb.commit()
    mycursor.close()
    mydb.close()
    logging.info(f'Success: database created')


def connect_to_komoot(host, user, password):
    """
    connect to komoot database
    Returns a connection and a cursor
    """
    mydb = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database="komoot"
    )
    mycursor = mydb.cursor()
    return mydb, mycursor


def connect_and_execute(sql, host, user, password):
    """
    Connect to komoot database and run the sql script (input).
    This function can be used when we don't expect SQL to returb anything (no fetching)
    """
    mydb, mycursor = connect_to_komoot(host, user, password)
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()


def create_table_country(host, user, password):
    sql = """
                          CREATE TABLE IF NOT EXISTS country (
                           id int AUTO_INCREMENT primary key
                           , country varchar(252)
                          )"""
    connect_and_execute(sql, host, user, password)
    logging.info(f'Success: country table created')


def create_table_city(host, user, password):
    sql = """CREATE TABLE IF NOT EXISTS city (
                      id int AUTO_INCREMENT primary key
                      , city varchar(252)
                      , country_id int
                      , FOREIGN KEY (country_id) REFERENCES country(id)
                    )"""
    connect_and_execute(sql, host, user, password)
    logging.info(f'Success: city table created')


def create_table_difficulty(host, user, password):
    sql = """
                         CREATE TABLE IF NOT EXISTS difficulty (
                          id int AUTO_INCREMENT primary key
                          , difficulty varchar(252)
                         )"""
    connect_and_execute(sql, host, user, password)
    logging.info(f'Success: difficulty table created')


def create_table_treks(host, user, password):
    sql = """CREATE TABLE IF NOT EXISTS treks (
                id int AUTO_INCREMENT primary key
                , title varchar(252)
                , description varchar(252)
                , url varchar(252) unique
                , city_id int
                , country_id int
                , FOREIGN KEY (city_id) REFERENCES city(id)
                , FOREIGN KEY (country_id) REFERENCES country(id)
                )"""
    connect_and_execute(sql, host, user, password)
    logging.info(f'Success: treks table created')


def create_table_main_info(host, user, password):
    sql = """ CREATE TABLE IF NOT EXISTS main_info (
                  trek_id int UNIQUE
                , difficulty_id int
                , duration TIME
                , distance float
                , average_speed float
                , uphill int
                , downhill int
                , tips varchar(252)
                , FOREIGN KEY (trek_id) REFERENCES treks(id)
                , FOREIGN KEY (difficulty_id) REFERENCES difficulty(id)
               )"""
    connect_and_execute(sql, host, user, password)
    logging.info(f'Success: main_info table created')


def create_table_way_types(host, user, password):
    sql = """
                CREATE TABLE IF NOT EXISTS way_types (
                 trek_id int UNIQUE
                , alpine_hiking_path float
                , ferry float
                , footpath float
                , hiking_path float
                , mountain_hiking_path float
                , path float
                , road float
                , state_road float
                , street float
                 , FOREIGN KEY (trek_id) REFERENCES treks(id)
                )"""
    connect_and_execute(sql, host, user, password)
    logging.info(f'Success: way_types table created')


def create_table_surfaces(host, user, password):
    sql = """CREATE TABLE IF NOT EXISTS surfaces (
         trek_id int UNIQUE
         , asphalt float
         , gravel float
         , natural_terrain float
         , paved float
         , unknown float
         , unpaved float
         , alpine float
         , FOREIGN KEY (trek_id) REFERENCES treks(id)
        )"""
    connect_and_execute(sql, host, user, password)
    logging.info(f'Success: surfaces table created')


def populate_country(hikes_infos, host, user, password):
    """
    Takes all the countries of the newly scrapped hikes and write them in SQL (if not already in there)
    """
    # Connect to mysql
    mydb, mycursor = connect_to_komoot(host, user, password)
    countries = set()
    for hike in hikes_infos:
        if "Country" in hike:
            countries.add(hike["Country"])
    countries = list(countries)

    for country in countries:
        sql = "SELECT distinct country FROM country"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        # We're testing if the country already exists in the database. If yes, we don't add it again
        if (country,) in result:
            print('pass country')
            pass
        else:
            sql = """INSERT INTO country (country)
                     VALUES(%s)
                    """
            mycursor.execute(sql, country)
    mydb.commit()
    mycursor.close()
    mydb.close()
    logging.info(f'Success: country table populated')


def populate_city(hikes_infos, host, user, password):
    """
        Takes all the citys of the newly scrapped hikes and write them in SQL (if not already in there)
    """
    mydb, mycursor = connect_to_komoot(host, user, password)
    cities = set()
    for hike in hikes_infos:
        print(hike)
        if "City" in hike:
            cities.add((hike["City"], hike["Country"]))
    cities = list(cities)

    for city, country in cities:
        if city == '':
            pass
        else:
            sql = "SELECT distinct city FROM city"
            mycursor.execute(sql)
            result = mycursor.fetchall()
            # We're testing if the city already exists in the database. If yes, we don't add it again
            if (city,) in result:
                print('pass city')
                pass
            else:
                sql = f"SELECT id FROM country WHERE country like '{country}'"
                mycursor.execute(sql)
                country_id = mycursor.fetchall()
                sql = """INSERT INTO city (city, country_id)
                         VALUES(%s,%s)
                        """
                mycursor.execute(sql, [city, country_id])
    mydb.commit()


def populate_difficulty(hikes_infos, host, user, password):
    """
        Takes all the difficulties of the newly scrapped hikes and write them in SQL (if not already in there)
    """
    mydb, mycursor = connect_to_komoot(host, user, password)

    difficulties = set()
    for hike in hikes_infos:
        difficulties.add(hike["3.difficulty"])
    difficulties = list(difficulties)

    for difficulty in difficulties:
        sql = "SELECT distinct difficulty FROM difficulty"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        # We're testing if the difficulty already exists in the database. If yes, we don't add it again
        if (difficulty,) in result:
            pass
        else:
            sql = """INSERT INTO difficulty (difficulty)
                     VALUES(%s)
                    """
            mycursor.execute(sql, difficulty)
    mydb.commit()


def populate_one_hike_into_treks(hike, mycursor):
    sql = " SELECT distinct url FROM treks"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    # We're testing if the url already exists in the database. If yes, we don't add it again
    if (hike["url"],) in result:
        pass
    else:
        sql_treks = """INSERT INTO treks (
                          title
                        , description
                        , url
                        , country_id
                        , city_id
                        ) 
                         VALUES(%s,%s,%s, (SELECT id FROM country WHERE country = %s), (SELECT id FROM city WHERE city = %s));
                            """
        title = hike["2.title"]
        description = hike["9.description"]
        url = hike["url"]
        if "Country" in hike:
            country = hike["Country"]
        else:
            country = ""
        if "City" in hike:
            city = hike["City"]
        else:
            city = ""
        mycursor.execute(sql_treks, [title, description, url, country, city])
        trek_id = mycursor.lastrowid
        return trek_id


def populate_one_hike_into_main_info(hike, mycursor, trek_id):
    sql_main_infos = """INSERT INTO main_info (
                                   trek_id
                                 , difficulty_id
                                 , duration
                                 , distance
                                 , average_speed
                                 , uphill
                                 , downhill
                                 , tips)
                                VALUES(%s,(SELECT id FROM difficulty WHERE difficulty = %s),%s,%s,%s,%s,%s,%s);
                                """
    difficulty = hike["3.difficulty"]
    duration = hike["4.duration"]
    distance = hike["5.distance"]
    average_speed = hike["6.average_speed"]
    uphill = hike["7.uphill"]
    downhill = hike["8.downhill"]
    tips = hike["91.tips"]
    mycursor.execute(sql_main_infos,
                     [trek_id, difficulty, duration, distance, average_speed, uphill, downhill, tips])


def populate_one_hike_into_surfaces(hike, mycursor, trek_id):
    sql_surfaces = """INSERT INTO surfaces (
                                               trek_id
                                             , asphalt
                                             , gravel
                                             , natural_terrain
                                             , paved
                                             , unknown
                                             , unpaved
                                             , alpine)
                                            VALUES(%s,%s,%s,%s,%s,%s,%s, %s);
                                            """

    surfaces_values = dict()
    for surface in SURFACES:
        if surface in hike:
            surfaces_values.update({surface: hike[surface]})
        else:
            surfaces_values.update({surface: 0})

    mycursor.execute(sql_surfaces,
                     [trek_id, surfaces_values['asphalt'], surfaces_values['gravel'],
                      surfaces_values['natural_terrain'], surfaces_values['paved'], surfaces_values['unknown'],
                      surfaces_values['unpaved'], surfaces_values['alpine']])


def populate_one_hike_into_way_types(hike, mycursor, trek_id):
    sql_way_types = """INSERT INTO way_types (
                                   trek_id
                                 , alpine_hiking_path
                                 , ferry
                                 , footpath
                                 , hiking_path
                                 , mountain_hiking_path
                                 , path
                                 , road
                                 , state_road
                                 , street)
                                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                                """
    way_types_values = dict()
    for way_type in WAY_TYPES:
        if way_type in hike:
            way_types_values.update({way_type: hike[way_type]})
        else:
            way_types_values.update({way_type: 0})

    mycursor.execute(sql_way_types,
                     [trek_id, way_types_values['alpine_hiking_path'], way_types_values['ferry'],
                      way_types_values['footpath'], way_types_values['hiking_path'],
                      way_types_values['mountain_hiking_path'],
                      way_types_values['path'], way_types_values['road'],
                      way_types_values['state_road'], way_types_values['street']])


def populate_hikes_tables(hikes_infos, host, user, password):
    """
    All the hikes tables (treks, main_info, way_types and surfaces) must be populated ina row
    from the same hike, because we re-use the trek_id created in treks into the other tables
    """
    mydb, mycursor = connect_to_komoot(host, user, password)

    for hike in tqdm(hikes_infos, total=len(hikes_infos)):
        trek_id = populate_one_hike_into_treks(hike, mycursor)
        populate_one_hike_into_main_info(hike, mycursor, trek_id)
        populate_one_hike_into_surfaces(hike, mycursor, trek_id)
        populate_one_hike_into_way_types(hike, mycursor, trek_id)
    mydb.commit()


def write_database(hikes_infos, host, user, password):
    create_database(host, user, password)
    create_table_country(host, user, password)
    create_table_city(host, user, password)
    create_table_difficulty(host, user, password)
    create_table_treks(host, user, password)
    create_table_main_info(host, user, password)
    create_table_way_types(host, user, password)
    create_table_surfaces(host, user, password)
    populate_country(hikes_infos, host, user, password)
    populate_city(hikes_infos, host, user, password)
    populate_difficulty(hikes_infos, host, user, password)
    populate_hikes_tables(hikes_infos, host, user, password)
