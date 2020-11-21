# README

* LAST UPDATED: 2020-11-20
* USERNAME: jabbas
* ORGANIZATION: spatial-data-discovery
* REPOSITORY: ay2021-1
* FOLDER: project/jabbas

## Files
### Scripts
- [jabbas_script.py](https://github.com/spatial-data-discovery/ay2021-1/tree/master/project/jabbas)
- [jabbas-process-doc.txt](https://github.com/spatial-data-discovery/ay2021-1/tree/master/project/jabbas)

### Inputs
- [US Crisis Monitor Data](https://acleddata.com/special-projects/us-crisis-monitor/)
- The data is originally an excel spreadsheet (.xlsx), so open the spreadsheet and save it as a ".csv" file for the purpose of the script functionality.

### Outputs
 - The script creates four new .csv files which are increments of the main data set, with each new file including the next 40 days worth of data points than the previous. The first file "40_day_segment1.csv" contains the data points corresponding to the first 40 days of the data set (5/24/2020 - 7/3/2020). The next file "40_day_segment1.csv" contains data points corresponding to the first 80 days worth of data in the data set (5/24/2020 - 9/21/2020). The same for the other two data files.

## jabbas_script.py
### Purpose
To create four new data files (.csv) that are parts of the original dataset in order for us to create separate images for each new data file for the final animation. The script does creates these splits by 40 day date increments.

### How it works
The first thing the script does is ask for an absolute file path to the original dataset. Once the file path is given, it reads in the original data set (in .csv format) and creates a pandas data frame that matches the entirety of the data set. The next thing the script does is iterate through the entire dataset's "EVENT_DATE" column and convert the dates into YYYY_MM-DD format. This is because we wish to create the partitioned data sets based on date, but in order for us to use the datetime package for this, we need to adjust the format the date is in. The next part of the script is a for loop that loops 4 times, one for each new data set we are creating. It creates a temporary datetime object that is set to the last day of available data in the data set. Then, create a temporary copy of the main data frame containing all the data. Iterate through the new data and create a datetime object for each data point. The script then compares the date of the given point versus the interval of days that we wish to write a new data set with. If the date is within the intended interval of days, the counter increases. Once iterated through the data set, the counter is the value of the index in which the partition needs to be made. The script then writes a new .csv file with the data frame that is indexed to the intended 40-day incremented data set.

### How to Run
Enter the absolute file path to the data set once running the script in your terminal/command prompt. NOTE: The script assumes that the data set is in .csv format. The original dataset is provided as an excel spreadsheet (.xlsx). Prior to running the script, open the original spreadsheet in excel and choose to save as a .csv file. The file path initially given will also be the file path to which the script will write the new data set .csv files. Make sure the necessary python packages are installed prior to running the script.

### Packages Needed
- [Datetime](https://docs.python.org/3/library/datetime.html)
- [Pandas](https://pandas.pydata.org/)

### File Types
- [csv](https://docs.fileformat.com/spreadsheet/csv/)
- [xlsx](https://docs.fileformat.com/spreadsheet/xlsx/)

## Datasets Explanation
### US Crisis Monitor Dataset
- File name: [USA_2020_Oct31.xlsx]
- File type: Excel Spreadsheet
- Source: ACLED (https://acleddata.com/special-projects/us-crisis-monitor/)
- Date Updated: 10-31-2020
- Use: Contains all instances of political violence and demonstration in the United States which the ACLED defines as battles, riots, protests, strategic developments, and violence against civilians. Contains data from May 24, 2020 to October 31, 2020.
- Variables: ISO, EVENT_ID_CNTY, EVENT_ID_NO_CNTY, EVENT_DATE, YEAR, TIME_PRECISION, EVENT_TYPE, ACTOR1 (Actors for the event, eg. protestors, rioters), ASSOC_ACTOR_1 (Associated actors, eg. Women, BLM, GOP, APSP, Labour group), INTER1, ACTOR2, ASSOC_ACTOR_2, INTER2, INTERACTION, REGION, COUNTRY, ADMIN1 (State), ADMIN2 (County), LOCATION (City), LATITUDE, LONGITUDE, GEO_PRECISION, SOURCE (Source of the incident eg. FOX News, Los Angeles Times etc.), SOURCE_SCALE (national, subnational, regional), NOTES (Notes and description of the event), FATALITIES    
