
# Website scrapping project

## Introduction
As part of our data science studies at ITC, we have been asked to scrap a website of our choosing to practice our python skills.

Marc and I being both passionate about hiking, we decided to scrap [Komoot.com](https://www.komoot.com/), which references hikes around the world

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

### Step 2: call from terminal + create a database

- Call from terminal: We wrapped our code with argpase to be able to call it from the terminal. More details in the section below
- Database: we defined our database design and then populated the tables from python directly. More details below on the database structure


## Structure of the code

The code is structured in 4 files:
- File 1 (get_hiking_urls.py): a function that receives a catalogue page (ie a page that contains 12 url hikes) and collect the url of the hikes into a list. 
- File 2 (get_hiking_info.py): a series of function that receive the url of one hike and will collect the different relevant information of the hike (mainly the distance, difficulty, description, type of paths, localisation)
- File 3 (get_all_hikes_info.py): a main function that will call the functions from file 1 and 2, and loop over in a relevant way to collect all the data. In this file, we added the possibility to run the script from the terminal with different argument
- File 4 (create_database.py): a series of functions that create the database and tables, and then populate them



## How to run the file

Install the requirements (from requirements.txt)

Go into the komoot_config.json file:
- give the url of the catalogue page that you would like to scrap 
- indicate the csv in which you would like to store the scraped info (if not in the database)

Then go into the terminal (for the moment it can only be run from the terminal):
- run get_all_hike_info.py
- Add the number of catalogue page to scrape (one catalogue page contains 12 hikes)

The code will ask you a series of question:
- if you want to re-use the list of url hikes of previous launches (ie skip step 1 described above), or relaunch from start
- if you want to store the result in a csv, in a database, or both. In the case of a database (or both), what are you user name and password for mysql. 




## Argparse details

- First argument - number_of_hiking_pages_to_scrape: indicates the number of catalogue pages to scrape (one catalogue page = 12 hikes)
- Second argument - datatypes_to_be_scraped : indicates which information you want to scrape. You can one zero (default is all), 1, or several datatype among this list : ["title", "difficulty", "duration", "distance", "average_speed", "uphill", "downhill","description", "tip", "way_types_and_surfaces", "location", "all"]

/!\ Important note: you can only populate the database if you don't indicate a second argument (ie if you want to scrap all the information). If you scrap a narrower scope, it won't populate the database (as we want complete information in our database)

## Database 

### Tables

<img width="1018" alt="Capture d’écran 2023-04-03 à 23 56 54" src="https://user-images.githubusercontent.com/127126176/229629441-5cc8dbfc-b51e-4b05-bc8c-c3c851988c7e.png">


The database is made of 7 tables:
- treks: lists each treks 
- main_info: lists the main information about the treks
- way_types: indicates per trek the type of way and the distance of each type
- surfaces: indicates per trek the type of surfaces and the distance of each type
- country: lists the possible countries of the hikes
- region: lists the possible regions of the hikes
- difficulty: lists the possible difficulties of the hikes


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

region:
- id: key
- region : a region where we found hikes

difficulty:
- id: key
- difficulty : lists the possible difficulties of the hikes (easy, medium, hard,...)

## About the authors

- Marc: [github](https://github.com/MarcAlexanderLevinson/), [linkedin](https://www.linkedin.com/in/marclevinson070/)
- Eliott : [github](https://github.com/eliottcaen/), [linkedin](https://www.linkedin.com/in/eliott-c-a4a32884/)
