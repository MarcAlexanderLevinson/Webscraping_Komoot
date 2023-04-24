
# Website scrapping project

## Introduction
As part of our data science studies at ITC, we have been asked as a training to scrap a website of our choosing, create a database from the collected information, and complement it with data from an API.

Marc and I being both passionate about hiking, we decided to scrap [Komoot.com](https://www.komoot.com/), which references hikes around the world.

## Goal

As a practice exercice, our goal was to scrap the information of 1000 hikes, and store them in a database. We also wanted to be able to run the script from the terminal with different arguments


## How did we approach the problem

### Step 1: scrapping

- We first investigated the structure of the website to find where we could access the catalogues of hikes:
   - We didn't find the complete catalogue, but we found that the 'Map' view of the discover page enabled us to create big enough temporary catalogues of hikes centered around one city.
   - See [here](https://www.komoot.com/discover/Lyon/@45.7575926%2C4.8323239/tours?max_distance=500000&sport=hike&map=true) an example with the city of Lyon as a starting point: a range of 500km gives us a cataologue of 62868 hikes (5239 pages x 12 hikes per page). More than enough!

- We then defined the steps to accomplish to get the information:
   - Step 1. Scrap the catalogue to retrieve all the hikes url. This information is saved into a csv, so that the next time the user runs the code, he can re-use it and go directly to step 2 (a command will ask the user's choice). This enable to save time if the user already collected the needed information of step 1 in previous launches.
   - Step 2. Scrap each hikes url page 
   - Step 3. Print the collected information, or store it into any type of storage way (we choose a csv file to start with) 

### Step 2: wrap the code with a parser + create a database

- Parser: We wrapped our code with argpase to be able to call it from the terminal. More details in the section below
- Database: we defined our database design and then populated the tables from python directly. More details below on the database structure


### Step 3: complement the database with historical weather information based on the location of the hikes

- We first collect the latitude & longitudes for all the cities in our database thanks to api_ninjas.com
- From these locations, we collect 10 years of weather information thanks to open-meteo.com


## Structure of the code

The code is structured in 6 files:
- File 1 (get_hiking_urls.py): a series of functions that return a list of hikes urls by receiving a catalogue page as input (a catalogue page is a page that contains 12 url hikes, like [this one](https://www.komoot.com/discover/Tel_Aviv/@32.0803000%2C34.7805000/tours?max_distance=30000&sport=hike&map=true&startLocation=))
- File 2 (get_hike_info.py): a series of function that receive the url of one hike and will collect the different relevant information of the hike (mainly the distance, difficulty, description, type of paths, location)
- File 3 (create_database.py): a series of functions that create the database and hikes related tables (excluding the weather related tables), and then populate them
- File 4 (weather_API.py): a series of functions that collect historical weather information for the hikes cities in our database through APIs, create a table to store them, and populate it
- File 5 (parser_file.py): the file that contains the parser wrapping our code. Thanks to it, the user will be able to select whether they want to scrape hikes or complement the locations scrapped with weather info. It also offers additional functionalities : 
- File 6 (main.py): the file that runs all the others, depending on the choice of the users given through the parser: how many hikes to scrape, which data to scrape, where to store the data (CSV, SQL or both) are configurations that the user can specify in the parser (if SQL or both is choosen, file 3 will also be called)
   - If the user chooses to scrape, the main function will call the functions from file 1 and 2, and loop over in a relevant way to scrape the data on Kommot. 
   - If the user chooses to complement the previously scraped info with weather info, the main function will run the file 4 and collect weather info



## How to run the file

1) Install the requirements (from requirements.txt)

2) Go into the komoot_config.json file:
- give the url of the catalogue page that you would like to scrape 
- indicate the csv in which you would like to store the scraped info (if not in the database)

3) Add in the Edit Configuration page the parser argument (see below for more details on the parser)

4) Run the main file


## Argparse details

- action_to_perform (optional, default = both): indicates whether you want to scrape komoot ("scrape"), complement the collected hike with weather info ("weather_info") or do both ("both")
- number_of_catalogue_pages_to_scrape (optional, default = 1): the number of catalogue pages to scrape (one catalogue page = 12 hikes)
- datatypes_to_be_scraped (optional, default = all) : indicates which information you want to scrape, among this list : ["title", "difficulty", "duration", "distance", "average_speed", "uphill", "downhill","description", "tip", "way_types_and_surfaces", "location", "all"]

/!\ Important note: you can only populate the database if you don't indicate a second argument (ie if you want to scrap all the information). If you scrape a narrower scope and ask to store the info in SQL, it will raise an error

- old_catalogue (optional, default = N): with Y the scrapping won't re-scrap the catalogue pages, but will re-use the last scrapped catalogue pages results (stored in the list_of_hiking_urls.csv file). With N, the list of hikes will be determined again, by scrapping first the catalogue page
- storage (optional, default = CSV): indicates where the result of the scrapping is stored: in the SQL database, in a csv, or in both
- localhost : used to connect to MySQL. Required in case SQL (or both) is chosen for storage 
- user : SQL user used to connect to MySQL. Required in case SQL (or both) is chosen for storage 
- password : SQL password used to connect to MySQL. Required in case SQL (or both) is chosen for storage 

## Database 

### Tables

<img width="778" alt="Capture d’écran 2023-04-24 à 23 13 45" src="https://user-images.githubusercontent.com/127126176/234106008-64a456de-3dfe-4f05-a404-77ac8af28ddc.png">



The database is made of 8 tables:
- Hiking tables:
   - treks: lists each treks 
   - main_info: lists the main information about the treks
   - way_types: indicates per trek the type of way and the distance of each type
   - surfaces: indicates per trek the type of surfaces and the distance of each type
   - country: lists the countries of the hikes
   - city: lists the cities of the hikes
   - difficulty: lists the difficulties of the hikes
- Weather tables:
   - weather : lists for each city and day over the last 10 years some key weather info: the min, max and average temperature of the day, and the daily precipitation in mm and hours

### Columns

treks:
- id: key
- title: title of the hike
- description : description of the hike
- url : url of the hike
- region_id : id giving the region when joined with the table region
- country_id : id giving the country when joined with the table country

main_infos:
- trek_id : foreign key related to id of the treks table
- difficult_id : id giving the difficulty of the hike when joined with the table difficulty
- duration: duration of the hike
- distance : lenght of the hike (km)
- average_speed : averge walking speed on the hike (km/h)
- uphill : uphill meters 
- downhill: uphill meters
- tips : tips about the hike

way_types: 
- trek_id : foreign key related to id of the treks table
- all the other columns refere to one type of way (e.g. hiking_path, road,...) encountered on the hike. The value indicates the distance (in km) walked on the given type of way

surfaces:
- trek_id : foreign key related to id of the treks table
- all the other columns refere to one type of surface (e.g. asphalt, paved,...) encountered on the hike. The value indicates the distance (in km) walked on the given type of surface

country:
- id: key
- country : a country where we found hikes

city:
- id: key
- city : a region where we found hikes
- country_id : the country related to this city

difficulty:
- id: key
- difficulty : lists the possible difficulties of the hikes (easy, medium, hard,...)

weather:
- id : key
- city_id : the id of the city
- date : the date of the weather info
- max_temperature : the maximum temperature for this city on the given date
- min_temperature : the minimum temperature for this city on the given date
- avg_temperature : the average temperature for this city on the given date
- daily_precipitation_mm : the mm of rains for this city on the given date
- daily_precipitation_hours : the hours of rains for this city on the given date

## About the authors

- Marc: [github](https://github.com/MarcAlexanderLevinson/), [linkedin](https://www.linkedin.com/in/marclevinson070/)
- Eliott : [github](https://github.com/eliottcaen/), [linkedin](https://www.linkedin.com/in/eliott-c-a4a32884/)
