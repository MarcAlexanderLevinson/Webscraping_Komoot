import pymysql.cursors
from tqdm import tqdm


def create_database_tables():
    """
    TODO
    :return:
    """
    # Connect to mysql
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="89Root92"
        # TODO how not to put it here?
    )
    mycursor = mydb.cursor()

    # Check if the database already exists. Create it if not. We assume that if the database exists, it already has the right tables
    mycursor.execute("show databases")
    lst = mycursor.fetchall()
    if ('komoot',) in lst:
        print('The database already exists')
        # mycursor.execute("drop DATABASE komoot")
    else:
        mycursor.execute("CREATE DATABASE komoot")
        mycursor.execute("USE komoot")

        sql = """CREATE TABLE region (
                  id int AUTO_INCREMENT primary key
                  , region varchar(252)
                )"""
        mycursor.execute(sql)

        sql = """
                      CREATE TABLE country (
                       id int AUTO_INCREMENT primary key
                       , country varchar(252)
                      )"""
        mycursor.execute(sql)

        sql = """
                      CREATE TABLE difficulty (
                       id int AUTO_INCREMENT primary key
                       , difficulty varchar(252)
                      )"""
        mycursor.execute(sql)

        sql = """CREATE TABLE treks (
            id int AUTO_INCREMENT primary key
            , title varchar(252)
            , description varchar(252)
            , url varchar(252) unique
            , region_id int
            , country_id int
            , FOREIGN KEY (region_id) REFERENCES region(id)
            , FOREIGN KEY (country_id) REFERENCES country(id)
            )"""
        mycursor.execute(sql)

        sql = """ CREATE TABLE main_info (
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
        mycursor.execute(sql)

        sql = """
            CREATE TABLE way_types (
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
        mycursor.execute(sql)

        sql = """CREATE TABLE surfaces (
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
        mycursor.execute(sql)

        mydb.commit()

        mycursor.close()
        mydb.close()


def populate_country(hikes_infos):
    # Connect to mysql
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="89Root92",  # TODO how not to put it here?
        database="komoot"
    )
    mycursor = mydb.cursor()

    countries = set()
    for hike in hikes_infos:
        countries.add(hike["Country"])
    countries = list(countries)

    for country in countries:
        sql = "SELECT distinct country FROM country"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        # We're testing if the url already exists in the database. If yes, we don't add it again
        if (country,) in result:
            print('pass country')
            pass
        else:
            sql = """INSERT INTO country (country)
                     VALUES(%s)
                    """
            mycursor.execute(sql, country)
    mydb.commit()


def populate_region(hikes_infos):
    # Connect to mysql
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="89Root92",  # TODO how not to put it here?
        database="komoot"
    )
    mycursor = mydb.cursor()

    regions = set()
    for hike in hikes_infos:
        regions.add(hike["Country"])
    regions = list(regions)

    for region in regions:
        sql = "SELECT distinct region FROM region"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        # We're testing if the url already exists in the database. If yes, we don't add it again
        if (region,) in result:
            print('pass country')
            pass
        else:
            sql = """INSERT INTO region (region)
                     VALUES(%s)
                    """
            mycursor.execute(sql, region)
    mydb.commit()


def populate_difficulty(hikes_infos):
    # Connect to mysql
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="89Root92",  # TODO how not to put it here?
        database="komoot"
    )
    mycursor = mydb.cursor()

    difficulties = set()
    for hike in hikes_infos:
        difficulties.add(hike["Country"])
    difficulties = list(difficulties)

    for difficulty in difficulties:
        sql = "SELECT distinct difficulty FROM difficulty"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        # We're testing if the url already exists in the database. If yes, we don't add it again
        if (difficulty,) in result:
            pass
        else:
            sql = """INSERT INTO difficulty (difficulty)
                     VALUES(%s)
                    """
            mycursor.execute(sql, difficulty)
    mydb.commit()


def populate_hikes_tables(hikes_infos):
    # Connect to mysql
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="89Root92",  # TODO how not to put it here?
        database="komoot"
    )

    mycursor = mydb.cursor()

    for row in tqdm(hikes_infos, total=len(hikes_infos)):
        sql = " SELECT distinct url FROM treks"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        # We're testing if the url already exists in the database. If yes, we don't add it again
        if (row["url"],) in result:
            print('here')
            pass
        else:
            print('ici')
            sql_treks = """INSERT INTO treks (
                      title
                    , description
                    , url
                    )
                     VALUES(%s,%s,%s);
                        """ # TODO: rajouter les colonnes manquantes
            title = row["2.title"]
            description = row["9.description"]
            url = row["url"]
            mycursor.execute(sql_treks, [title, description, url])
            trek_id = mycursor.lastrowid

            sql_main_infos = """INSERT INTO main_info (
                               trek_id
                             , difficulty_id
                             , duration
                             , distance
                             , average_speed
                             , uphill
                             , downhill
                             , tips)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,(select url from treks limit 1));
                            """
            difficulty = row["3.difficulty"]
            duration = row["4.duration"]
            distance = row["5.distance"]
            average_speed = row["6.average_speed"]
            uphill = row["7.uphill"]
            downhill = row["8.downhill"]
            tips = row["91.tips"]  # TODO le numero a probablement change
            mycursor.execute(sql_main_infos, [trek_id, difficulty, duration, distance, average_speed, uphill, downhill])
    mydb.commit()


create_database_tables()
test_list = [{'1.ID': 0, '2.title': 'Pointe de Nantaux (2170m)', '3.difficulty': 'Expert', '4.duration': '06:06',
              '5.distance': 13.7, '6.average_speed': 2, '7.uphill': 1260.0, '8.downhill': 1250.0,
              '9.description': 'Expert Hiking Tour. Very good fitness required. Mostly accessible paths. Sure-footedness required. The starting point of the Tour is right next to a parking lot.',
              '91.tips': '', 'Mountain Hiking Path (km)': 0.63, 'Hiking Path (km)': 8.33, 'Path (km)': 1.99,
              'Street (km)': 0.58, 'Road (km)': 2.01, 'State Road (km)': 0.12, 'Natural (km)': 0.9,
              'Unpaved (km)': 8.01, 'Gravel (km)': 2.05, 'Paved (km)': 1.78, 'Asphalt (km)': 0.89, 'Unknown (km)': 0.1,
              'all levels': ['France', 'Auvergne Rhône Alpes', 'Thonon-Les-Bains', 'Montriond'],
              'url': 'https://www.komoot.com/smarttour/e808650908/pointe-de-nantaux-2170m?tour_origin=smart_tour_search'},
             {'1.ID': 1, '2.title': 'Pointe de Ressachaux (2173m)', '3.difficulty': 'Expert', '4.duration': '05:00',
              '5.distance': 12.1, '6.average_speed': 2, '7.uphill': 1150.0, '8.downhill': 1150.0,
              '9.description': 'Expert Hiking Tour. Very good fitness required. Mostly accessible paths. Sure-footedness required. The starting point of the Tour is accessible with public transport.',
              '91.tips': '', 'Mountain Hiking Path (km)': 6.15, 'Hiking Path (km)': 1.69, 'Path (km)': 1.91,
              'Street (km)': 0.75, 'Road (km)': 1.61, 'Alpine (km)': 6.15, 'Unpaved (km)': 3.22, 'Gravel (km)': 0.1,
              'Paved (km)': 1.27, 'Asphalt (km)': 1.09, 'Unknown (km)': 0.36,
              'all levels': ['France', 'Auvergne Rhône Alpes', 'Thonon-Les-Bains', 'Morzine'],
              'url': 'https://www.komoot.com/smarttour/e810584590/pointe-de-ressachaux-2173m?tour_origin=smart_tour_search'},
             {'1.ID': 2, '2.title': 'Randonnée des Orgues', '3.difficulty': 'Intermediate', '4.duration': '02:59',
              '5.distance': 9.04, '6.average_speed': 3, '7.uphill': 380.0, '8.downhill': 380.0,
              '9.description': 'Intermediate Hiking Tour. Good fitness required. Mostly accessible paths. Sure-footedness required. The starting point of the Tour is right next to a parking lot.',
              '91.tips': '', 'Mountain Hiking Path (km)': 0.84, 'Hiking Path (km)': 5.15, 'Path (km)': 0.1,
              'Street (km)': 1.4, 'Road (km)': 0.24, 'State Road (km)': 1.41, 'Alpine (km)': 0.84, 'Unpaved (km)': 5.15,
              'Paved (km)': 1.4, 'Asphalt (km)': 1.64, 'Unknown (km)': 0.1, 'all levels': [],
              'url': 'https://www.komoot.com/smarttour/e920140191/randonnee-des-orgues?tour_origin=smart_tour_search'},
             {'1.ID': 3, '2.title': 'Randonnée du château de Val', '3.difficulty': 'Intermediate',
              '4.duration': '04:06', '5.distance': 14.3, '6.average_speed': 4, '7.uphill': 320.0, '8.downhill': 310.0,
              '9.description': 'Intermediate Hiking Tour. Good fitness required. Easily-accessible paths. Suitable for all skill levels. The starting point of the Tour is right next to a parking lot.',
              '91.tips': '', 'Hiking Path (km)': 2.26, 'Path (km)': 7.35, 'Street (km)': 0.97, 'Road (km)': 0.52,
              'State Road (km)': 3.25, 'Unpaved (km)': 6.51, 'Paved (km)': 1.56, 'Asphalt (km)': 3.34,
              'Unknown (km)': 2.93, 'all levels': [],
              'url': 'https://www.komoot.com/smarttour/e924670619/randonnee-du-chateau-de-val?tour_origin=smart_tour_search'},
             {'1.ID': 4, '2.title': 'Le Mont Buet par Vallorcine - Chamonix-Mont-Blanc', '3.difficulty': 'Expert',
              '4.duration': '08:07', '5.distance': 19.8, '6.average_speed': 2, '7.uphill': 1730.0, '8.downhill': 1730.0,
              '9.description': 'Expert Hiking Tour. Very good fitness required. Mostly accessible paths. Sure-footedness required. The starting point of the Tour is accessible with public transport.',
              '91.tips': '', 'Mountain Hiking Path (km)': 16.6, 'Hiking Path (km)': 2.47, 'Path (km)': 0.68,
              'State Road (km)': 0.1, 'Alpine (km)': 1.01, 'Natural (km)': 18.3, 'Unpaved (km)': 0.26,
              'Gravel (km)': 0.1, 'Paved (km)': 0.1, 'Asphalt (km)': 0.1,
              'all levels': ['France', 'Auvergne Rhône Alpes', 'Bonneville', 'Vallorcine'],
              'url': 'https://www.komoot.com/smarttour/e924134691/le-mont-buet-par-vallorcine-chamonix-mont-blanc?tour_origin=smart_tour_search'},
             {'1.ID': 5, '2.title': 'L’Aiguille de la Grande Sassière - Alpes Grées', '3.difficulty': 'Expert',
              '4.duration': '06:21', '5.distance': 11.9, '6.average_speed': 2, '7.uphill': 1360.0, '8.downhill': 1360.0,
              '9.description': 'Expert Hiking Tour. Very good fitness required. Sure-footedness, sturdy shoes and alpine experience required. The starting point of the Tour is right next to a parking lot.',
              '91.tips': 'Includes a segment that is highly dangerous\nA part of this route comprises highly technical, difficult, or hazardous terrain. Specialist equipment and prior experience is required.',
              'Alpine Hiking Path (km)': 2.59, 'Mountain Hiking Path (km)': 9.19, 'Path (km)': 0.1, 'Road (km)': 0.1,
              'Alpine (km)': 11.9, 'Paved (km)': 0.1,
              'all levels': ['France', 'Auvergne Rhône Alpes', 'Albertville', 'Tignes', ''],
              'url': 'https://www.komoot.com/smarttour/e924150080/laiguille-de-la-grande-sassiere-alpes-grees?tour_origin=smart_tour_search'},
             {'1.ID': 6, '2.title': 'La Pointe des Fours par le Manchet - Parc National de la Vanoise',
              '3.difficulty': 'Expert', '4.duration': '05:04', '5.distance': 12.9, '6.average_speed': 2,
              '7.uphill': 1070.0, '8.downhill': 1070.0,
              '9.description': 'Expert Hiking Tour. Very good fitness required. Sure-footedness, sturdy shoes and alpine experience required. The starting point of the Tour is right next to a parking lot.',
              '91.tips': 'Includes a segment that may be dangerous\nA part of this route comprises technical, difficult, or hazardous terrain. Specialist equipment and prior experience may be required.',
              'Alpine Hiking Path (km)': 0.96, 'Mountain Hiking Path (km)': 9.12, 'Path (km)': 2.74, 'Road (km)': 0.12,
              'Alpine (km)': 9.87, 'Unpaved (km)': 2.94, 'Asphalt (km)': 0.12,
              'all levels': ['France', 'Auvergne Rhône Alpes', 'Albertville', "Val-D'Isère", ''],
              'url': 'https://www.komoot.com/smarttour/e925136370/la-pointe-des-fours-par-le-manchet-parc-national-de-la-vanoise?tour_origin=smart_tour_search'},
             {'1.ID': 7, '2.title': 'La Pointe de l’Observatoire par Aussois - Parc National de la Vanoise - Boucle',
              '3.difficulty': 'Expert', '4.duration': '06:01', '5.distance': 16.2, '6.average_speed': 3,
              '7.uphill': 1120.0, '8.downhill': 1120.0,
              '9.description': 'Expert Hiking Tour. Very good fitness required. Mostly accessible paths. Sure-footedness required. The starting point of the Tour is right next to a parking lot.',
              '91.tips': '', 'Mountain Hiking Path (km)': 13.9, 'Hiking Path (km)': 0.1, 'Path (km)': 2.02,
              'Road (km)': 0.18, 'Alpine (km)': 13.7, 'Natural (km)': 0.48, 'Unpaved (km)': 1.83, 'Paved (km)': 0.22,
              'Unknown (km)': 0.1,
              'all levels': ['Auvergne Rhône Alpes', 'Saint-Jean-De-Maurienne', 'Aussois', 'France'],
              'url': 'https://www.komoot.com/smarttour/e925750113/la-pointe-de-lobservatoire-par-aussois-parc-national-de-la-vanoise-boucle?tour_origin=smart_tour_search'},
             {'1.ID': 8, '2.title': 'La Pointe de Talamarche par Montremont - Boucle', '3.difficulty': 'Expert',
              '4.duration': '05:40', '5.distance': 11.0, '6.average_speed': 2, '7.uphill': 1040.0, '8.downhill': 1040.0,
              '9.description': 'Expert Hiking Tour. Very good fitness required. Sure-footedness, sturdy shoes and alpine experience required. The starting point of the Tour is right next to a parking lot.',
              '91.tips': 'Includes a segment that may be dangerous\nA part of this route comprises technical, difficult, or hazardous terrain. Specialist equipment and prior experience may be required.',
              'Alpine Hiking Path (km)': 0.33, 'Mountain Hiking Path (km)': 6.6, 'Hiking Path (km)': 2.78,
              'Path (km)': 0.43, 'Street (km)': 0.84, 'Alpine (km)': 6.95, 'Natural (km)': 2.51, 'Unpaved (km)': 0.69,
              'Paved (km)': 0.3, 'Asphalt (km)': 0.45, 'Unknown (km)': 0.1,
              'all levels': ['France', 'Auvergne Rhône Alpes', 'Annecy', 'Thônes', ''],
              'url': 'https://www.komoot.com/smarttour/e925786903/la-pointe-de-talamarche-par-montremont-boucle?tour_origin=smart_tour_search'},
             {'1.ID': 9, '2.title': 'La Trou de la Mouche - Chaîne des Aravis - Boucle', '3.difficulty': 'Expert',
              '4.duration': '04:15', '5.distance': 9.49, '6.average_speed': 2, '7.uphill': 930.0, '8.downhill': 930.0,
              '9.description': 'Expert Hiking Tour. Very good fitness required. Easily-accessible paths. Suitable for all skill levels. The starting point of the Tour is right next to a parking lot.',
              '91.tips': '', 'Hiking Path (km)': 7.53, 'Path (km)': 1.74, 'Road (km)': 0.22, 'Unpaved (km)': 9.27,
              'Paved (km)': 0.22, 'all levels': ['France', 'Auvergne Rhône Alpes', 'Annecy', 'La Clusaz'],
              'url': 'https://www.komoot.com/smarttour/e925813484/la-trou-de-la-mouche-chaine-des-aravis-boucle?tour_origin=smart_tour_search'},
             {'1.ID': 10, '2.title': 'Roc Lancrenaz et Col des Frêtes par la forêt', '3.difficulty': 'Expert',
              '4.duration': '04:42', '5.distance': 9.46, '6.average_speed': 2, '7.uphill': 770.0, '8.downhill': 770.0,
              '9.description': 'Expert Hiking Tour. Good fitness required. Sure-footedness, sturdy shoes and alpine experience required. ',
              '91.tips': 'Includes a segment that may be dangerous\nA part of this route comprises technical, difficult, or hazardous terrain. Specialist equipment and prior experience may be required.',
              'Alpine Hiking Path (km)': 0.17, 'Mountain Hiking Path (km)': 6.45, 'Hiking Path (km)': 0.53,
              'Path (km)': 2.25, 'Road (km)': 0.1, 'Alpine (km)': 7.72, 'Natural (km)': 1.15, 'Unpaved (km)': 0.53,
              'Paved (km)': 0.1, 'all levels': ['France', 'Auvergne Rhône Alpes', 'Annecy', 'Talloires-Montmin'],
              'url': 'https://www.komoot.com/smarttour/e925820759/roc-lancrenaz-et-col-des-fretes-par-la-foret?tour_origin=smart_tour_search'},
             {'1.ID': 11, '2.title': 'La Pointe de la Sambuy — Massif des Bauges - Boucle', '3.difficulty': 'Expert',
              '4.duration': '07:18', '5.distance': 16.3, '6.average_speed': 2, '7.uphill': 1340.0, '8.downhill': 1340.0,
              '9.description': 'Expert Hiking Tour. Very good fitness required. Sure-footedness, sturdy shoes and alpine experience required. ',
              '91.tips': 'Includes a segment that is highly dangerous\nA part of this route comprises highly technical, difficult, or hazardous terrain. Specialist equipment and prior experience is required.',
              'Alpine Hiking Path (km)': 1.56, 'Mountain Hiking Path (km)': 3.0, 'Hiking Path (km)': 2.59,
              'Path (km)': 5.33, 'Footpath (km)': 3.14, 'Street (km)': 0.66, 'Alpine (km)': 4.56, 'Natural (km)': 1.85,
              'Unpaved (km)': 9.2, 'Asphalt (km)': 0.56, 'Unknown (km)': 0.1,
              'all levels': ['France', 'Auvergne Rhône Alpes', 'Albertville', 'Plancherine'],
              'url': 'https://www.komoot.com/smarttour/e926594658/la-pointe-de-la-sambuy-massif-des-bauges-boucle?tour_origin=smart_tour_search'}]
test_list2 = [{'1.ID': 0, '2.title': 'Pointe de Nantaux (2170m)', '3.difficulty': 'Expert', '4.duration': '06:06',
               '5.distance': 13.7, '6.average_speed': 2, '7.uphill': 1260.0, '8.downhill': 1250.0,
               '9.description': 'Expert Hiking Tour. Very good fitness required. Mostly accessible paths. Sure-footedness required. The starting point of the Tour is right next to a parking lot.',
               '91.tips': '', 'Mountain Hiking Path (km)': 0.63, 'Hiking Path (km)': 8.33, 'Path (km)': 1.99,
               'Street (km)': 0.58, 'Road (km)': 2.01, 'State Road (km)': 0.12, 'Natural (km)': 0.9,
               'Unpaved (km)': 8.01, 'Gravel (km)': 2.05, 'Paved (km)': 1.78, 'Asphalt (km)': 0.89, 'Unknown (km)': 0.1,
               'all levels': ['France', 'Auvergne Rhône Alpes', 'Thonon-Les-Bains', 'Montriond'],
               'Country': 'England',
               'url': 'https://www.komoot.com/smarttour/e808650908/pointe-de-nantaux-2170m?tour_origin=smart_tour_search'},
              {'1.ID': 0, '2.title': 'Pointe de Nantaux (2170m)', '3.difficulty': 'Expert', '4.duration': '06:06',
               '5.distance': 13.7, '6.average_speed': 2, '7.uphill': 1260.0, '8.downhill': 1250.0,
               '9.description': 'Expert Hiking Tour. Very good fitness required. Mostly accessible paths. Sure-footedness required. The starting point of the Tour is right next to a parking lot.',
               '91.tips': '', 'Mountain Hiking Path (km)': 0.63, 'Hiking Path (km)': 8.33, 'Path (km)': 1.99,
               'Country': 'France',
               'Street (km)': 0.58, 'Road (km)': 2.01, 'State Road (km)': 0.12, 'Natural (km)': 0.9,
               'Unpaved (km)': 8.01, 'Gravel (km)': 2.05, 'Paved (km)': 1.78, 'Asphalt (km)': 0.89, 'Unknown (km)': 0.1,
               'all levels': ['France', 'Auvergne Rhône Alpes', 'Thonon-Les-Bains', 'Montriond'],
               'url': 'https://www.komoot.com/smarttour/e808650908/pointe-de-nantaux-2170m?tour_origin=smart_tour_searchokkk'}]
test_list3 = [{'1.ID': 0, '2.title': 'Pointe de Nantaux (2170m)', '3.difficulty': 'Expert', '4.duration': '06:06',
               '5.distance': 13.7, '6.average_speed': 2, '7.uphill': 1260.0, '8.downhill': 1250.0,
               '9.description': 'Expert Hiking Tour. Very good fitness required. Mostly accessible paths. Sure-footedness required. The starting point of the Tour is right next to a parking lot.',
               '91.tips': '', 'Mountain Hiking Path (km)': 0.63, 'Hiking Path (km)': 8.33, 'Path (km)': 1.99,
               'Street (km)': 0.58, 'Road (km)': 2.01, 'State Road (km)': 0.12, 'Natural (km)': 0.9,
               'Unpaved (km)': 8.01, 'Gravel (km)': 2.05, 'Paved (km)': 1.78, 'Asphalt (km)': 0.89, 'Unknown (km)': 0.1,
               'Country': 'France',
               'all levels': ['France', 'Auvergne Rhône Alpes', 'Thonon-Les-Bains', 'Montriond'],
               'url': 'https://www.komoot.com/smarttour/e808650908/pointe-de-nantaux-2170m?tour_origin=smart_tour_search'}]
# populate_database(test_list2)
populate_country(test_list2)
