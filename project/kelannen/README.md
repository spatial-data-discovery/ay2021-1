# README

* LAST UPDATED: 2020-11-20
* USERNAME: kelannen
* ORGANIZATION: spatial-data-discovery
* REPOSITORY: ay2021-1
* FOLDER: project/kelannen

## Files
### Scripts
- [kelannen_crop_yields.R](https://github.com/spatial-data-discovery/ay2021-1/tree/master/project/kelannen) 
- [kelannen-process-doc.txt](https://github.com/spatial-data-discovery/ay2021-1/tree/master/project/kelannen)

### Inputs
- [Africa Geojson](https://common-data.carto.com/tables/africa_adm0/public)
- [Africa Countries Crop Production](http://www.fao.org/faostat/en/#data/QC)
- [Africa Countries Average precipitation in depth](https://databank.worldbank.org/reports.aspx?source=2&series=AG.LND.PRCP.MM&country=)
- [Datasets - already downloaded and in the correct format](https::/github.com/spatial-data-discovery/ay2021-1/tree/master/project/kelannen/Datasets) (includes all files above)

### Outputs
- HTML file with the animation of Crop Yields from 1961-2018 with the average precipitation in depth for each country in Africa 
- The code will create supporting folders and files for the html file including a folder containing still images of the graph for each year should you wish to look at that 
- Note: 2 different html files are created based on what code sections are run, to alternate files you will need to rerun that corresponding code (more details on this below)

## kelannen_crop_yields.R
### Purpose
To visualize the change in crop yields across different countries in Africa for each year between 1961 and 2018. The animation of this not only shows general changes but also 
to show how it compares to changes in precipitation.

### How it Works
The first thing this script does is it reads in the different input files (assuming it is in the same directory as this script) into a format that is easy to use. Second, it 
cleans the different data sets as needed and makes sure that all of the country name variables are the same. Next, it filters and then aggregates the crop yield data set in 
two different ways so that it is representative of a single country and the units and measurement type is all the same. The first way is so that it sums all crops yields for 
each country in hg/ha. The second way is only summing the crop yields for groundnuts, wheat, cereals, cassava, millet, and maize for each country in hg/ha. Both of these 
different ways are done for each year from 1961 to 2018. These two different crop yield versions are each separately merged with the Africa geography and the average 
precipitation in depth. Finally a graph for each year and crop yield version is created and two different html's can be created to see the change over time. 

### How to Run
To run this script, users must have:
- RStudio installed on their computers
- a directory with the script and the datasets above

Open up the script in RStudio, click the run button. If you don't already have the packages required, uncomment the installation for it in the script by deleting the # in 
front of the line. After you finish installing the package comment the line out again by replacing the # mark. There are comments in the script itself should you need further 
direction. To alternate between the different animations (total crop yields versus specified crop yields) in the html file you will have to run the corresponding saveHTML call 
the comments identify which call goes to each version.

### Packages Needed
- [rstudioapi](https://cran.rstudio.com/web/packages/rstudioapi/index.html)
- [rgdal](https://cran.r-project.org/web/packages/rgdal/index.html)
- [rgeos](https://cran.r-project.org/web/packages/rgeos/index.html)
- [ggmap](https://cran.r-project.org/web/packages/ggmap/index.html)
- [sp](https://cran.r-project.org/web/packages/sp/index.html)
- [maptools](https://cran.r-project.org/web/packages/maptools/index.html)
- [dplyr](https://cran.r-project.org/web/packages/dplyr/index.html)
- [gridExtra](https://cran.r-project.org/web/packages/gridExtra/index.html)
- [sf](https://cran.r-project.org/web/packages/sf/index.html)
- [tidyr](https://cran.r-project.org/web/packages/tidyr/index.html)
- [geojsonio](https://cran.r-project.org/web/packages/geojsonio/index.html)
- [animation](https://cran.r-project.org/web/packages/animation/index.html)
- [readxl](https://cran.r-project.org/web/packages/readxl/index.html)

### File Types
- [geojson](https://docs.fileformat.com/gis/geojson/)
- [csv](https://docs.fileformat.com/spreadsheet/csv/)
- [xlsx](https://docs.fileformat.com/spreadsheet/xlsx/)

## Datasets Explanation
### Africa Geojson
- File name: [africa_adm0.geojson]
- File type: geojson
- Source: Carto (https://common-data.carto.com/tables/africa_adm0/public)
- Use: Contains the geometries for the different countries in Africa along with their names (used this to plot the crop production information onto a map of Africa).
- Variables: cartodb_id, geometry, adm0_a3 (shortened country names), name (county's full names), created_at (date), updated_at (date)
- Variables Used: Name and geometry (the other variables were kept but never called on)

### Africa Countries Crop Production
- File name: [Production_Crops_E_Africa.csv]
- File type: csv
- Source: FAOSTAT - Food and Agriculture Organization of the United Nations (http://www.fao.org/faostat/en/#data/QC)
- Use: Contains information of the crop yields for each country in Africa every year from 1961 to 2018.
- Variables: Area Code, Area (Country name), Item Code, Item (Crop type), Element (area harvest, crop yield, production, unit (ha, hg/ha, tonnes), a variable representing each year and another to contain any flags for that particular year.
- Variables Used: Area (Country name), Item (Crop type), Element (crop yield), unit (hg/ha), and the variables representing the values for each year (I did not use the flags).

### Africa Countries Average Precipitation
- File name: [Data_Extract_FromWorld Development Indicators.xlsx]
- File type: xlsx
- Source: The World Bank - World Development Indicators (https://databank.worldbank.org/reports.aspx?source=2&series=AG.LND.PRCP.MM&country=)
- Use: The Precipitation data for different countires, doesn't contain the data for all years but about every 5 years within that time frame.
- Variables: Name and years (the years have that countries average precipitation data in mm)
- Variables Used: Name and years
