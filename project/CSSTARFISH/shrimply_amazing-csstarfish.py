# 
# Author: Caroline Freshcorn
# Date (Last Update): 2020-11-20
#
###########################################
#     IMPORT MODULES/INSTALL PACKAGES     #
###########################################
!pip install geopandas
import geopandas as gpd
from shapely.geometry import Point

import pandas as pd
import matplotlib.pyplot as plt

import argeparse

##########################################
#                  MAIN                  #
##########################################
# Provide help documentation for the user.
parse = argparse.ArgumentParser("Reads and processes a North American shrimp"
                                "population distribution dataset to create a"
                                "new CSV file containing only the time and location 
                                attributes."
                               )
parsing = parse.parse_args()

# Set file path.
path_input = input("Please enter the file path, "
                   "including the name of the .csv file: "
                  )
file_path = path_input

if os.path.isfile(file_path):
  # Open raw CSV dataset and convert to DataFrame.
  df = pd.read_csv(file_path)
  location_data = df.copy()
  
  # Drop null values and first row containing not applicable data.
  location_data = location_data.dropna()
  location_data = location_data[1:]
  
  # Extract rows pertaining only to species of shrimp.
  shrimp_species = [
                    "Argis lar", 
                    "Argis spp.", 
                    "Bryozoa spp.", 
                    "Chilomycterus schoepfii", 
                    "Crangon Communis", 
                    "Crangon spp.", 
                    "Litopenaeus setiferus", 
                    "Mesopenaeus tropicalis", 
                    "Metapenaeopsis goodei", 
                    "Pandalopsis dispar", 
                    "Pandalus eous", 
                    "Pandalus goniurus", 
                    "Pandalus hypsinotus", 
                    "Pandalus jordani", 
                    "Pandalus platyceros", 
                    "Pandalus spp.", 
                    "Parapenaeus politus", 
                    "Pasiphaea pacifica", 
                    "Penaeus aztecus", 
                    "Penaeus duorarum", 
                    "Sclerocrangon boreas", 
                    "Sergestes similis", 
                    "Sicyonia brevirostris", 
                    "Sicyonia burkenroadi", 
                    "Sicyonia dorsalis", 
                    "Solenocera spp.", 
                    "Squilla chydaea", 
                    "Squilla empusa", 
                    "Trachypeneus spp."
                    ]
  matching_species = location_data.Species.isin(shrimp_species)
  shrimp_filtered = location_data[matching_species]
  
  # Restrict attributes to time series and location.
  shrimp_filtered = shrimp_filtered[["Year", "Latitude", "Longitude"]]
  shrimp_filtered = shrimp_filtered.reset_index(drop=True)
  
  # Save new CSV file with just this filtered data.
  shrimp_filtered.to_csv('cleaned_shrimpdata.csv')
  
  # Begin processing this new CSV dataset for a GeoDataFrame.
  gpd_location_data = gpd.read_file("cleaned_shrimpdata.csv")
  gpd_location_data = gpd_location_data.drop(columns = ["field_1"])
  
  # Create a column for coordinates in GeoDataFrame from longitude and latitude of CSV file.
  gpd_location_data['geometry'] = gpd_location_data.apply(lambda x: Point(float(x.Longitude), float(x.Latitude)), axis=1)

  # Create the GeoDataFrame.
  shrimp_info = gpd.GeoDataFrame(gpd_location_data, geometry=gpd_location_data.geometry)
  
  # Create visualization of latitude over time.
  x = shrimp_filtered["Year"]
  y = shrimp_filtered["Latitude"]
  plt.scatter(x,y)
  plt.xlabel("Year")
  plt.ylabel("Degrees North")
  plt.show()
  
else: 
  print("No file found in this path.  Please try again with a different path name.")
