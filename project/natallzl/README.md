# README
LAST UPDATED: 2020-11-20   
ORGANIZATION: spatial-data-discovery  
REPOSITORY: ay2021-1  
FOLDER: project/natallzl  

## Files
* [natallzl-process-doc.txt](natallzl-process-doc.txt)
* [natallzl_process_script.py](natallzl_process_script.py)

# natallzl_process_script.py

## How It Works
This script reads in IBTrACS historic tropical cyclone data (file name: ibtracs.since1980.list.v04r00.csv) from the local directory, creates a dataframe using pandas, then processes the dataset for visualization. First, the script creates a new .csv file for map visualization. Then, a new dataframe groups the data by season (year) and ocean basin, and counts of the number of named tropical cyclones (per season and basin) are obtained. Finally, the script creates bar charts that visualize tropical cyclone counts for all basins and for the North Atlantic. *Note:* we ignore warnings to avoid getting a datatype warning upon reading in the input file.

## How To Run It
To run this script, the necessary packages must be installed and the input file (ibtracs.since1980.list.v04r00.csv) must be in the local directory (same directory as the process script). Then, simply run the script in the command line and the script will output the output files to the local directory.

## Required Packages
* [argparse](https://docs.python.org/3/library/argparse.html)
* [warnings](https://docs.python.org/3/library/warnings.html)
* [pandas](https://pandas.pydata.org/)
* [matplotlib](https://matplotlib.org/)

### Input File
* CSV file from IBTrACS ([download link](https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r00/access/csv/ibtracs.since1980.list.v04r00.csv))

## Output Files
* ibtracs_processed.[csv](https://docs.fileformat.com/spreadsheet/csv/)
* cyclone_plot.[png](https://docs.fileformat.com/image/png/)
* cycloneNA_plot.[png](https://docs.fileformat.com/image/png/)

## Tropical Cyclone Data
* **Data Origin/Provider:** [NOAA; World Data Center for Meteorology, Asheville](https://www.ncdc.noaa.gov/ibtracs/index.php?name=ib-v4-access)
  * [CSV data](https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r00/access/csv/)
* **Variables & Units:**
  * SID - unique storm identifier
  * SEASON - year
  * BASIN - ocean basin location of storm occurrence
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
* **Missing Data Value:** blank cell in .csv; NaN in pandas dataframe
* **Contact Information:** IBTrACS.Team@noaa.gov
* **Institution:** [NOAA](https://www.noaa.gov/)
* **Dates Included:** 1980-01-01 to 2020-11-15
* **Date Dataset Last Updated:** 2020-11-15, 04:07

## Variables Used
* SID
* SEASON
* BASIN
* NAME
* LAT
* LON
