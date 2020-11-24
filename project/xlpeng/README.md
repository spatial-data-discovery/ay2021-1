# README

- LAST UPDATED: 2020-11-24
- ORGANIZATION: spatial-data-discovery
- REPOSITORY: ay2021-1
- FOLDER: ay2021-1/project/xlpeng

## Files
### Script
* [coviddata_process.py](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/xlpeng/coviddata_process.py)

### Input Data
* [United State Shape file](https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html)
* [covid-19-data](https://github.com/nytimes/covid-19-data)

### Outputs
* [IntermediateOutput](https://github.com/spatial-data-discovery/ay2021-1/tree/master/project/xlpeng/intermediateOutput) (sixteen csv file contains covid-19 cases at specific dates)
* [FinalOutput](https://github.com/spatial-data-discovery/ay2021-1/tree/master/project/xlpeng/finalOutput)

## coviddata_process.py

### How it works 
This script reads and extracts the data from the given csv file that includes the covid-19 data of selected dates and saves the data into separate newly created csv files.

### How to runs the script
The script runs just like any other python script. The command to run it is: python coviddata_process.py

### Packages Required
* [os](https://docs.python.org/3/library/os.html)
* [sys](https://docs.python.org/3/library/sys.html)
* [argparse](https://pypi.org/project/argparse/)

## About the Data
* File
* format
* Source
* Contact
* Variable Used
