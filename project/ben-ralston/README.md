# README

LAST UPDATED: 2020-11-20  
ORGANIZATION: spatial-data-discovery  
REPOSITORY: ay2021-1  
FOLDER: project/ben-ralston

## Files

### Scripts
* [process_datasets.py](https://github.com/spatial-data-discovery/ay2021-1/project/ben-ralston/process_datasets.py)
* [create_visualizations.r](https://github.com/spatial-data-discovery/ay2021-1/project/ben-ralston/create_visualizations.r)
* [create_animation.py](https://github.com/spatial-data-discovery/ay2021-1/project/ben-ralston/create_animation.py)

### Inputs
* [ststdnsadata.xlsx](https://github.com/spatial-data-discovery/ay2021-1/project/ben-ralston/Data/ststdnsadata.xlsx)
* [United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.csv](https://github.com/spatial-data-discovery/ay2021-1/project/ben-ralston/Data/United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.csv)
* [nst-est2019-alldata.csv](https://github.com/spatial-data-discovery/ay2021-1/project/ben-ralston/Data/nst-est2019-alldata.csv)
* [states.csv](https://github.com/spatial-data-discovery/ay2021-1/project/ben-ralston/Data/states.csv)

### Outputs
* [unemployment_by_state.csv](https://github.com/spatial-data-discovery/ay2021-1/project/ben-ralston/IntermediateOutput/unemployment_by_state.csv)
* [monthly_covid_cases_by_state.csv](https://github.com/spatial-data-discovery/ay2021-1/project/ben-ralston/IntermediateOutput/monthly_covid_cases_by_state.csv)
* [Pandemic_Unemployment.gif](https://github.com/spatial-data-discovery/ay2021-1/project/ben-ralston/Pandemic_Unemployment.gif)
* [map_1.tiff](https://github.com/spatial-data-discovery/ay2021-1/project/ben-ralston/IntermediateOutput/map_1.csv)
* [map_2.tiff](https://github.com/spatial-data-discovery/ay2021-1/project/ben-ralston/IntermediateOutput/map_2.csv)
* [map_3.tiff](https://github.com/spatial-data-discovery/ay2021-1/project/ben-ralston/IntermediateOutput/map_3.csv)
* [map_4.tiff](https://github.com/spatial-data-discovery/ay2021-1/project/ben-ralston/IntermediateOutput/map_4.csv)
* [map_5.tiff](https://github.com/spatial-data-discovery/ay2021-1/project/ben-ralston/IntermediateOutput/map_5.csv)
* [map_6.tiff](https://github.com/spatial-data-discovery/ay2021-1/project/ben-ralston/IntermediateOutput/map_6.csv)
* [map_7.tiff](https://github.com/spatial-data-discovery/ay2021-1/project/ben-ralston/IntermediateOutput/map_7.csv)
* [map_8.tiff](https://github.com/spatial-data-discovery/ay2021-1/project/ben-ralston/IntermediateOutput/map_8.csv)
* [map_9.tiff](https://github.com/spatial-data-discovery/ay2021-1/project/ben-ralston/IntermediateOutput/map_9.csv)


# process_datasets.py

## How It Works

This script reads the four input files listed above and converts them into two CSV files (unemployment_by_state.csv and monthly_covid_cases_by_state.csv).
I defined two primary/high-level functions, `unemployment()` and `covid()`, which are responsible for creating the two csv output files.
In the unemployment function, ststdnsadata.xlsx is read and converted to dataframe using the pandas package.
The original Excel file provides monthly unemployment rates for each state, but each monthly unemployment rate is provided on a different line.
To make this data more usable, the script iterates through the entire dataframe and copies the unemployment rate to a different dataframe with columns for each state and rows for each month.
After reading through the original dataset, the new dataframe is transposed, resulting in the states being row names and the months being column names.
(This is done for ease of use when importing and using the data in the R file responsible for creating the visualization.)
This dataframe is then written to CSV format.

In the covid function, the three other input files are read into pandas dataframes as well.
United_States_COVID-19_Cases_and_Deaths_by_State_over_Time.csv is the main data source, which provides daily new COVID case numbers for each state.
But like ststdnsadata.xlsx, these are all stored on separate lines in the CSV, so the script iterates through the rows and adds up the new cases, storing the total in a new dataframe after seeing all days in a given month for a given state.
This dataframe is similar to the final dataframe for the unemployment data with states arranged as row names and months arranged as column names.

Next, nst-est2019-alldata.csv, which contains population data by state, is read into a dataframe.
This data is used to adjust the values in the COVID cases dataframe to represent cases per 100,000 people.
Finally, states.csv, which contains coordinates for the centroid of each state, is read into a dataframe.
(The reason I'm using geographic coordinates here is that in the visualization script, COVID cases are represented as circles of various sizes overlaid onto a map of the US, and the R script needs to know the locations to place each circle.)
This coordinate dataframe is merged with the COVID cases dataframe, and the resulting dataframe is written to CSV format.

## How to Run It

To run this script, the four input files must be located in Data directory.
Then, the script can be run just like any other Python script would, as long as pandas and numpy are installed.
The script does not require any input from the user.


# create_visualizations.r

## How It Works

This script reads in the two CSV created by process_datasets.py (unemployment_by_state.csv and monthly_covid_cases_by_state.csv) located in IntermediateOutput directory.
Then, using primarily the ggplot2 and usmap packages, the data is shown on a map of the US with unemployment rates represented by color and COVID cases represented by the size of circles located on top of each state.
I used a for loop to create nine different plots, the first one showing data from January 2020 and the last one showing data from September 2020.
Each of these plots are saved in IntermediateOutput directory as TIFF images named map_#.tiff where # is the number of the month (i.e. January would be saved as map_1.tiff, and so on).

## How to Run It

To run this script, you must have the R language installed.
(RStudio is also very useful for running any R scripts, and can be downloaded [here](https://rstudio.com/products/rstudio/download/).)
You will also need to install the packages listed under the "R Packages Needed" header.
This can be done by running `install.packages("package")` in the R console.
Finally, the two CSV files created by process_datasets.py must be in IntermediateOutput.
If using RStudio, you may need to set your working directory to source file location by selecting Session > Set Working Directory > To Source File Location.


# create_animation.py

## How It Works

This is a simple script that takes the TIFF images created by create_visualizations.r and creates a GIF animation.
It uses the imageio package, which does essentially all of the work necessary for creating the animation.
After providing the filenames, the TIFF images are read and appended to a list.
That list is then passed to the imageio.mimsave function, which combines them and saves the animation as a GIF.

## How to Run It

To run this script, the nine TIFF images named map_1.tiff, map_2.tiff, ..., map_9.tiff must be located in the IntermediateOutput directory.
The script can be run just like any other Python script would, as long as imageio is installed, and does not require any user input.


# Required Packages

## Python Packages Needed
* [pandas](https://pandas.pydata.org/)
* [numpy](https://numpy.org/)
* [imageio](https://pypi.org/project/imageio/)
* [xlrd](https://pypi.org/project/xlrd/)

## R Packages Needed
* [ggplot2](https://ggplot2.tidyverse.org/)
* [usmap](https://usmap.dev/)
* [stringr](https://stringr.tidyverse.org/)
* [maptools](http://maptools.r-forge.r-project.org/)
* [rgdal](http://rgdal.r-forge.r-project.org/)


## Monthly Unemployment Data
 
* Provider - [U.S. Bureau of Labor Statistics](https://www.bls.gov/)
* [Download](https://www.bls.gov/web/laus/ststdnsadata.zip)
* Variables: 
  * FIPS Code - numeric string representing geographic area (i.e. city/state/territory) (string)
  * State and area - name of geographic area (string)
  * Period:Year - year (int)
  * Period:Month - month (int)
  * Civilian non-institutional population - number of non-incarcerated people in a given region (int)
  * Civilian labor force:Total - number of people in the workforce (employed or unemployed) (int)
  * Civilian labor force:Percent of population - percent of people in workforce compared to total population (float)
  * Civilian labor force:Employment:Total - number of people employed (int)
  * Civilian labor force:Employment:Percent of population - percent of employed people compared to total population (float)
  * Civilian labor force:Unemployment:Total - number of people seeking jobs but unemployed (int)
  * Civilian labor force:Unemployment:Rate - percent of unemployed people compared to total in workforce (float)

* Contact info - (202) 691-5200
* Institution - U.S. Bureau of Labor Statistics
* Dates Covered - 1976-01-01 to 2020-09-30
  * Dates Used - 2020-01-01 to 2020-09-30
  * Date Created - 2020-10-11

## Monthly Unemployment Variables Used
* FIPS Code
* State and area
* Period:Year
* Period:Month
* Civilian labor force:Unemployment:Rate

## Monthly Unemployment Variables Created
* Date - first day of associated month (YYYY-MM-DD)


## COVID Data
 
* Provider - [Centers for Disease Control and Prevention](https://www.cdc.gov/)
* [Download](https://data.cdc.gov/api/views/9mfq-cb36/rows.csv?accessType=DOWNLOAD)
* Variables: 
  * submission_date - date (DD/MM/YYYY)
  * state - abbreviated name of state (string)
  * tot_cases - total COVID-19 cases to date (int)
  * conf_cases - confirmed COVID-19 cases to date (int)
  * prob_cases - probable COVID-19 cases to date (int)
  * new_case - number of COVID-19 cases discovered on the associated date (int)
  * pnew_case - number of probable COVID-19 cases discovered on the associated date (int)
  * tot_death - total deaths caused by COVID-19 to date (int)
  * conf_death - confirmed deaths caused by COVID-19 to date (int)
  * prob_death - probable deaths caused by COVID-19 to date (int)
  * new_death - number of deaths caused by COVID-19 on the associated date (int)
  * pnew_death - number of probable deaths caused by COVID-19 on the associated date (int)
  * created_at - date and time of reporting (DD/MM/YYYY HH:MM:SS)
  * consent_cases - whether a state/territory consents to tracking COVID-19 cases (Agree/Disagree)
  * consent_deaths - whether a state/territory consents to tracking COVID-19 deaths (Agree/Not Agree)
  
* Contact info - (800) 232-4636
* Institution - Centers for Disease Control and Prevention
* Dates Covered - 2020-01-22 to 2020-11-15
  * Dates Used - 2020-01-22 to 2020-09-30
  * Date Created - 2020-11-18

## COVID Variables Used
* submission_date
* state
* new_case

## COVID Variables Created
* Date - first day of associated month (YYYY-MM-DD)
* Monthly New Cases - new cases occurring in a given month (int)
* Monthly New Cases Per Capita - new cases occurring in a given month per 100,000 people(int)


## Population Data

* Provider - [U.S. Census Bureau](https://www.census.gov/en.html)
* [Download](http://www2.census.gov/programs-surveys/popest/datasets/2010-2019/national/totals/nst-est2019-alldata.csv)
* Variables: 
  * SUMLEV - Geographic summary level (int)
  * REGION - Census Region code (int)
  * DIVISION - Census Division code (int)
  * STATE - State FIPS code (string)
  * NAME - State name (string)
  * CENSUS2010POP - 4/1/2010 resident total Census 2010 population (int)
  * ESTIMATESBASE2010 - 4/1/2010 resident total population estimates base (int)
  * POPESTIMATE2010 - 7/1/2010 resident total population estimate (int) *
  * NPOPCHG_2010 - Numeric change in resident total population 4/1/2010 to 7/1/2010 (int) *
  * BIRTHS2010 - Births in period 4/1/2010 to 6/30/2010 (int) *
  * NATURALINC2010 - Natural increase in period 4/1/2010 to 6/30/2010 (int) *
  * INTERNATIONALMIG2010 - Net international migration in period 4/1/2010 to 6/30/2010 (int) *
  * DOMESTICMIG2010 - Net domestic migration in period 4/1/2010 to 6/30/2010 (int) *
  * NETMIG2010 - Net migration in period 4/1/2010 to 6/30/2010 (int) *
  * RESIDUAL2010 - Residual for period 4/1/2010 to 6/30/2010 (int) *
  * RBIRTH2011 - Birth rate in period 7/1/2010 to 6/30/2011 (float) *
  * RNATURALINC2011 - Natural increase rate in period 7/1/2010 to 6/30/2011 (float) *
  * RINTERNATIONALMIG2011 - Net international migration rate in period 7/1/2010 to 6/30/2011 (float) *
  * RDOMESTICMIG2011 - Net domestic migration rate in period 7/1/2010 to 6/30/2011 (float) *
  * RNETMIG2011 Net migration rate in period 7/1/2010 to 6/30/2011 (float) *
  
* Contact info - (800) 923-8282
* Institution - U.S. Census Bureau
* Dates Covered - 2010-04-01 to 2019-07-01
  * Dates Used - 2019-01-01 to 2019-07-01
  * Date Created - 2019-07-01
  
(Note: any variables marked with an asterisk are repeated for other years, but they are omitted here to save space)

## Population Variables Used
* STATE
* POPESTIMATE2019

## Population Variables Created
None


## State Centroid Coordinate Data
 
* Provider - [Google Developers](https://developers.google.com/)
* [View](https://developers.google.com/public-data/docs/canonical/states_csv)
* Variables: 
  * state - abbreviated name of state (string)
  * latitude - latitude of centroid (float)
  * longitude - longitude of centroid (float)
  * name - name of state (string)
  
* Contact info - (650) 253-0000
* Institution - Google, LLC
* Date Created - 2012-01-20

## State Centroid Coordinate Variables Used
* state
* latitude
* longitude
* name

## State Centroid Coordinate Variables Created
None
