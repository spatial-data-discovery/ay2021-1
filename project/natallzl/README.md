# README
LAST UPDATED: 2020-11-19
ORGANIZATION: spatial-data-discovery  
REPOSITORY: ay2021-1  
FOLDER: project/natallzl  

##Files
* [natallzl-process-doc.txt](natallzl-process-doc.txt)
* [natallzl_process_script.py](natallzl_process_script.py)

###Input File
* CSV file from IBTrACS (ibtracs.since1980.list.v04r00.csv)

#natallzl_process_script.py

##How it Works
This script reads in IBTrACS historic tropical cyclone data (file name: ibtracs.since1980.list.v04r00.csv) from the local directory, creates a dataframe using pandas, then processes the dataset for visualization. First, the script creates a new .csv file for map visualization. Then, a new dataframe groups the data by season (year) and ocean basin, and counts of the number of named tropical cyclones (per season and basin) are obtained. Finally, the script creates bar charts that visualize tropical cyclone counts for all basins and for the North Atlantic. Note: we ignore warnings to avoid getting a datatype warning upon reading in the input file.

##How to Run it
To run this script, the necessary packages must be installed and the input file must be in the local directory (same directory as the process script). Then, simply run the script in the command line and the script will output the output files to the local directory.

##Required Packages
* argparse
* warnings
* pandas
* matplotlib

##Input Files
* [ibtracs.since1980.list.v04r00.csv]

##Output Files
* ibtracs_processed.csv
* cyclone_plot.png
* cycloneNA_plot.png

##Tropical Cyclone Data
* Data Origin/Provider: [NOAA; World Data Center for Meteorology, Asheville](https://www.ncdc.noaa.gov/ibtracs/index.php?name=ib-v4-access)
  * Specifically, the [since 1980 .csv data](https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r00/access/csv/)
* Variables & Units:
  * SID - unique storm identifier
  * SEASON - year
  * BASIN - general oceanic location of storm occurrence
    * NA - North Atlantic
    * EP - Eastern North Pacific
    * WP - Western North Pacific
    * NI - North Indian
    * SI - South Indian
    * SP - Southern Pacific
    * SA - South Atlantic
  * NAME - name of storm provided by reporting agency
  * LAT - latitude; degrees north
  * LON - longitude; degrees east
  * 160+ columns; see [IBTrACS column documentation](https://www.ncdc.noaa.gov/ibtracs/pdf/IBTrACS_v04_column_documentation.pdf) for a more comprehensive variable description
* Missing Data Value: blank cell in .csv; NaN in pandas dataframe
* Contact Information: IBTrACS.Team@noaa.gov
* Institution: NOAA
* Dates Included: 1980-01-01 to 2020-11-15
* Date Data Last Updated: 2020-11-15 04:07

##Variables Used
* SID
* SEASON
* BASIN
* NAME
* LAT
* LON

##Variables Created
No new variables created for map visualization; however, created temporary counts for creation of bar charts. See process script.
