# README
 - LAST UPDATED: 2020-11-18
 - USERNAME: sylviashea1
 - ORGANIZATION: spatial-data-discovery
 - REPOSITORY: ay2021-1
 - FOLDER: project/sylviashea1

## Files
### Scripts
- [sylviashea1_generate_plot.py](https://github.com/spatial-data-discovery/ay2021-1/tree/master/project/sylviashea1) 
- [sylviashea1-process-doc.txt](https://github.com/spatial-data-discovery/ay2021-1/tree/master/project/sylviashea1)
- [download_jupyter_dir.py](https://github.com/spatial-data-discovery/ay2021-1/tree/master/project/sylviashea1)

### Inputs
- [United States shapefile (ADM1)](https://www2.census.gov/geo/tigerGENZ2018/shp/cb_2018_us_state_500k.zip)
- [Gun law stricness score cards (one for each year, from 2014-2019)](https://giffords.org/lawcenter/resources/scorecard/#rankings)
- [Mass shootings in the United States from 2009-2020](https://maps.everytownresearch.orgmassshootingsreports/mass-shootings-in-america-2009-2019/)
- [Preprocessed data](https://github.com/spatial-data-discovery/ay2021-1/tree/master/project/sylviashea1/preprocessed_data_inputs) (includes all files above)

### Outputs
- Plots: for each month and year, a choropleth map representing gun law strictness and a layer of graduated symbols representing the total number of people shot 

# sylviashea1_generate_plot.py
## Purpose
This script generates a visualization of gun law strictness by state and the number of mass shootings for each month from 2009 to 2020. When the plots are made into a video, it shows how the relationship between gun law strictness and mass shootings changes over time.

## How it Works (Pseudocode)
* Reads in the US shapefile and gun law scorecards from the given directory
    - Removes non-contiguous states
* For each scorecard (representing a year):
    - Merge with US shapefile to create a geodataframe
    - Year and geodataframe stored in dictionary {Year: Corresponding geodataframe}
* Reads in mass shootings geojson
    - Reformat date to create separate month and year columns
* For each month and year between 1/2009 and 8/2020
    - Acquires corresponding gun law geodataframe (for that year)
    - Gets subset of mass shooting dataframe (for that date)
    - Plots gun laws as choropleth layer (color indicating strictness/grade)
    - Plots shootings as graduated symbol layer (size indicating total shot)
    - Outputs plot in designated directory

## How to Run
To run the script, the user must have:
- a subdirectory within the working directory for the input files
- a subdirectory within the working directory for the generated plots

Run command in terminal/shell: python3 sylviashea1_generate_plot.py 

## Packages Needed
- [numpy](https://pypi.org/project/numpy/)
- [geopandas](https://pypi.org/project/geopandas/)
- [pandas](https://pypi.org/project/pandas/)
- [matplotlib](https://pypi.org/project/matplotlib/)
- [datetime](https://docs.python.org/3.4/library/datetime.html)
- [argparse](https://pypi.org/project/argparse/)
- [os](https://docs.python.org/3/library/os.html)

## File Types
- [shapefile](https://docs.fileformat.com/gis/shp/)
- [geojson](https://docs.fileformat.com/gis/geojson/)
- [csv](https://docs.fileformat.com/spreadsheet/csv/)

## Data Explained
### United States Shapefile (ADM1)
- File name: [cb_2018_us_state_500k.zip](https://github.com/spatial-data-discovery/ay2021-1/tree/master/project/sylviashea1/preprocessed_data_inputs)
- File type: shapefile
- Source: [United States Census Bureau](https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html)
- Use: functions as the spatial component for joining gun law scorecard. Must be extracted before running script.
### Gun Law Strictness Score Cards
- File name: [gunlaws_strict_YEAR.csv](https://github.com/spatial-data-discovery/ay2021-1/tree/master/project/sylviashea1/preprocessed_data_inputs)
- File type: csv
- Source: [Giffords Law Center](https://giffords.org/lawcenter/resources/scorecard/#rankings)
- Use: Contains the rating of gun control laws by state. Gun laws are ranked similarly to grades, from a scale of A to F.
- Variable used: grade
### Mass Shootings, 2009-2020
- File name: [massshootings_g.geojson](https://github.com/spatial-data-discovery/ay2021-1/tree/master/project/sylviashea1/preprocessed_data_inputs)
- File type: geojson
- Source: [Everytown for Gun Safety](https://maps.everytownresearch.org/massshootingsreports/mass-shootings-in-america-2009-2019/)
- Use: Contains locations and dates of mass shootings in the United States from 2009 to 2020.
- Variables used: date, Total_shot

# download_jupyter_dir.py
If the user runs sylviashea1_generate_plot.py in a Jupyter notebook, the download_jupyter_dir.py script may be helpful for downloading all the generated plots.
Source: [Stack Overflow](https://stackoverflow.com/questions/48122744/how-to-download-all-files-and-folder-hierarchy-from-jupyter-notebook)
## Purpose
Download all files and folder hierarchy from Jupyter notebook.
## How to Run
Copy the code into a Jupyter notebook in the same directory as the plots. Run the cell. The code will generate a .tar file that contains all files and subdirectories within working directory. 
