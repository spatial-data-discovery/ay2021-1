# README

- LAST UPDATED: 2020-11-24
- ORGANIZATION: spatial-data-discovery
- REPOSITORY: ay2021-1
- FOLDER: ay2021-1/project/xlpeng

## Files
### Script
* [coviddata_process.py](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/xlpeng/coviddata_process.py)
* [xlpeng-process-doc.txt](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/xlpeng/xlpeng-process-doc.txt)

### Input Data
* [United State Shape File](https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html)
* [covid-19-data](https://github.com/nytimes/covid-19-data)

### Outputs
* [IntermediateOutput](https://github.com/spatial-data-discovery/ay2021-1/tree/master/project/xlpeng/intermediateOutput) (16 csv files contain covid-19 cases for specific dates)
* [FinalOutput](https://github.com/spatial-data-discovery/ay2021-1/tree/master/project/xlpeng/finalOutput)
    * [covid-data.gif] (https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/xlpeng/finalOutput/covid-data.gif) The data animation in gif format. 
    * [covid_animation.mp4] (https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/xlpeng/finalOutput/covid_animation.mp4) The data animation in mp4 format. 

## coviddata_process.py

### How it works 
This script reads and extracts the data from the given csv file that includes the covid-19 data of selected dates and saves the data into separate newly created csv files. Users can manually adjust the dates they need to get corresponding data by simply changing the string values in the python list.

### How to runs the script
The input file is supposed to be save in the default local directory, and the generated files will be saved into the same local folder. The script runs just like any other python script. The command to run it is: python coviddata_process.py

### Packages Required
* [os](https://docs.python.org/3/library/os.html)
* [sys](https://docs.python.org/3/library/sys.html)
* [argparse](https://pypi.org/project/argparse/)

## About the Data
### COVID-19 Confirmed Cases (2020-01-21 - present)  
* File: [covid-19-data](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/xlpeng/inputData/us-states.csv)
* Format: csv
* Date Updated: 2020-11-24
* Source: [The New York Times](https://github.com/nytimes/covid-19-data)
* Contact: covid-data@nytimes.com
* Variables & Units: 
  * Date (yyyy-mm-dd) - Date of publishing
  * State - Name of the state
  * FIPS - FIPS code for each state
  * Cases - The cumulative number of confirmed cases of COVID-19
  * Deaths - The cumulative number of deaths of COVID-19
* Variable Used: date, state, cases

### United States Shape File 
* File: [cb_2019_us_state_500k](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/xlpeng/inputData/cb_2019_us_state_500k.zip)
* Format: shapefile
* Source: [United States Census Bureau](https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html)

