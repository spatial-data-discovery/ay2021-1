# README

* LAST UPDATED: 2020-11-11
* ORGANIZATION: spatial-data-discovery
* USERNAME: CSStarfish
* REPOSITORY: ay2021-1
* FOLDER: project/CSSTARFISH

_________________

### Files

#### Script

   * Python script: ["Shrimp"-ly Amazing](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/CSSTARFISH/shrimply_amazing-csstarfish.py) 

   * What Does This Script Do?
      * This script will read the provided CSV file from the indicated directory and transforms it into a Pandas DataFrame.
      Next, any null values will be dropped and the first row will be removed because it doesn't contain relevant data for this project.
      
      	  When exploring the Ocean Adapt user interface, I was able to determine the names of the species of shrimp that live in regions surrounding North America.
      Upon learning this information, I created a list containing these species' names.
      As such, the next step in the script is to create a new DataFrame containing only the rows pertaining to these particular species.
      From there, the "Region", "Species", "Latitude_std_err", and "Longitude_std_err" will be removed from the DataFrame, since the "Latitude", "Longitude", and "Year" are the most relevant for creating visualizations of spatial distribution over time.
      The indices will then be reset to begin at 0 and increment by 1 across this final, filtered DataFrame.
      
      	  With the DataFrame fully filtered to contain only time and location data about shrimp species, the script will then output these data entries to a "cleaned" CSV file.
      
      * The final portion of the script creates a scatter plot of the shrimp's latitude over time to allow one to detect any trends in their populations over the course of the past few decades, and the final visualization was created using kepler.gl from the CSV file output of this script.
  
   * How To Run:
      * To ease any potential burdens with GeoPandas installation, it may help to run the file in a Jupyter Hub notebook.
      Within this online Python notebook environment, the installation is as simple as running a "!pip install" statement and it will be ready to go.
      * A warning may apear when running the lines for converting the Pandas DataFrame to a GeoPandas DataFrame, but rerunning this portion of the script should make this warning message go away without any future implications for the success of the rest of script.

   * Required Package Installs and Imports:
      * Pandas
      * MatplotLib
      * GeoPandas
      * Shapely (more specifically, Point from shapely.geometry)

#### Dataset

  ##### Input
   * Original, raw dataset: [Raw Data](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/CSSTARFISH/datadownload.csv)
   * Original, raw dataset with metadata at beginning of file: [Raw Data with Metadata](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/CSSTARFISH/shrimp_metadata.csv)
   
  ###### Information About Input Dataset  
 * Data Origin:	[Ocean Adapt](https://oceanadapt.rutgers.edu/), a dataset created by Rutgers University in collaboration with NOAA Fisheries
 * Variable/Attribute Definitions: 
   * Year: Stores the year that the location data for the given species was collected
   * Region: Stores the general region of the ocean in which the given species was found
   * Species: Stores the name of the marine life species for which the location data was recorded
   * Missing values: Represented with NaN entries
 * Contact Info:	
   * Street Address: 71 Dudley Road
   * City: New Brunswick
   * State: New Jersey
   * Zip Code: 08901-8525

   * Contact Name: Michelle Stuart
   * Phone Number: (848) 932-5574
   * Email: michelle.stuart@rutgers.edu
	
 * Institution Name: Rutgers University and NOAA Fisheries
 * Date Created: Ocean Adapt was first published on December 11, 2014.  Even though the date created for the particular dataset used in this project is unknown, the most recent shrimp location data was recorded in 2019.
   
  ##### Output
 * Final, processed dataset: [Filtered Shrimp Data](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/CSSTARFISH/cleaned_shrimpdata.csv)

#### Animated Visualization
  * Video of North American Shrimp Population Distribution Over Time (1977-2019): [Shrimp Population Animation](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/CSSTARFISH/Shrimp%20Population%20Animation.mp4)
