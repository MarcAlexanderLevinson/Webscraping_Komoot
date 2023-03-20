
# Website scrapping project

## Introduction
As part of our data science studies at ITC, we have been asked to scrap a website of our choosing to practice our python skills.

Marc and I being both passionate about hiking, we decided to scrap [Komoot.com](https://www.komoot.com/), which references hikes around the world

## Goal

As a practice exercice, our goal was to scrap the information of 1000 hikes

## How did we approach the problem

- We first investigated the structure of the website to find where we could access the catalogues of hikes:
   - We didn't find the complete catalogue, but we found that the 'Map' view of the discover page enabled us to create big enough temporary catalogues of hikes centered around one city.
   - See [here](https://www.komoot.com/discover/Lyon/@45.7575926%2C4.8323239/tours?max_distance=500000&sport=hike&map=true) an example with the city of Lyon as a starting point: a range of 500km gives us a cataologue of 62868 hikes (5239 pages x 12 hikes per page). More than enough!

- We then defined the steps to accomplish to get the information:
   - Step 1. Scrap the catalogue to retrieve all the hikes url. This information is saved into a csv, so that the next time the user runs the code, he can re-use it and go directly to step 2 (a command will ask the user's choice). This enable to save time if the user already collected the needed information of step 1 in previous launches.
   - Step 2. Scrap each hikes url page 
   - Step 3. Print the collected information, or store it into any type of storage way (we choose a csv file to start with) 

## Structure of the code

The code is structured in 3 files:
- File 1 (get_hiking_urls.py): a function that receives a catalogue page (ie a page that contains 12 url hikes) and collect the url of the hikes into a list. 
- File 2 (get_hiking_info.py): a series of function that receive the url of one hike and will collect the different relevant information of the hike (mainly the distance, difficulty, description, type of paths, localisation)
- File 3 (get_all_hikes_info.py): a main function that will call the functions from file 1 and 2, and loop over in a relevant way to collect all the data

## How to run the file

Go into file 3. In the main function, indicate :
- the catalogue page that you would like to scrap 
- indicate how many pages of the catalogue you would like to scrap (a catalogue being made of several pages of 12 hikes)

And run the code. The code will ask you if you want to re-use the list of url hikes of previous launches (ie skip step 1 described above), or relaunch from start

The result will be stored in the hiking_data.csv