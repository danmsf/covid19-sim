# Retrieval of old coronavirus entries from WorldMeter site 

## Project Description
The goal of this project is to retrieve data about the covid19 pandamic. Out main resource is the [worldmeter site](https://www.worldometers.info/). 

The Worldmeter site maintains live world statistics on population, government ,economics etc. 
During the time of the covid19 pandamic Worldmeter also maintained live statistics about covid19 cases.
Worldmeter presents to the public only live data, and not archive data. 

[The Wayback Machine](https://archive.org/web/) is a site which scraps and stores old copies of other sites. We will use this 
site to gain the old data from Worldmeter.

The links for the covid19 locations in each site are:
1. https://web.archive.org/web/*/https://www.worldometers.info/coronavirus/ 
2. https://www.worldometers.info/coronavirus/

## Project Structure

```
project
│   README.md
│   functions.py
│   ETL_scrap_worldmeter.py    
│   join_data_as_seir.py
│   settings.py
│
└───data
│      ...
│   
└───logs
│      ...
│	
└───resources
│      column_remapper.csv
│      refs.csv
│      urls.csv
│      file.conf
│      package_list.yml
│      population.csv
│
└───snippets
│        ...

```
The project contains two main files that are found in the projects main directory - main.py and join_data.py.  

ETL_scrap_worldmeter.py - *NEEDS TO BE EXECUTED AUTOMATICALLY*.  
connects to The Wayback Machine which contains links to archived pages
from Worldmeter, regarding covid19 statistics,  
downloads csv from these links to the data folder.  

scrap_corona_history.py - takes all the downloaded dataframes does some column name manipulation  
(the number and names of the dataframes is different) and outputs to file.  

The project also have some a additional files:  

settings.py - contains important global variables and also reads important .csv files to memory, these  
will be used throughout the two main files.

functions.py - contains the functions of the project

package_list.yml - an anaconda generated file contains all packages used in the project.  
can be used by anaconda to create an environment with the same packages. 

The files found in the /resource directory are .csv file which contain links that are used throughout project files  
and also mapper .csv files.

The /data folder contains the downloaded dataframes in .csv format. 

The /log folder contains logs.



















