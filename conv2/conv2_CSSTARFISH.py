# conv2_CSSTARFISH.py
#
# VERSION 0.1
#
# LAST EDIT: 2020-10-16
#
# This script reads an ASCII raster into a netCDF file.
#
################################################################
# IMPORT MODULES
################################################################
import os
import os.path
import argparse
import numpy as np
from scipy.io import netcdf
import datetime
from zipfile import ZipFile as zf

################################################################
# MAIN
################################################################

# Provide help documentation
parse = argparse.ArgumentParser("Reads a provided set of ASC files and converts them into a single netCDF file.")
parsing = parse.parse_args()

# Set file path
path_input = input("Please enter the directory path to the .ZIP file of ASCII rasters: ")

# Opening zip file
if os.path.isfile(path_input):
    for file in path_input:
        if file.endswith(".zip"):
            with zf(file, "r") as zip_file:
                print("\nExtracting all .asc files from the .ZIP file")
                zip_file.extractall()
                print("")

    # Extracting data from asc files
    print("Processing ASCII raster data...")
    asc_files = []
    for file in path_input:
        file_data = []
        if file.endswith(".txt"):
            with open(file, "r") as open_file:
                decoded_file = open_file.read().decode("UTF-8")
                body = decoded_file.splitlines()[:6]
                for line in range(len(body)):
                    lines = []
                    line = line.split()

                    for point in line:
                        point_val = int(point)/10000
                        lines.append(point)

                lines = np.flipud(np.asarray(lines))
                file_data.append(lines)
        asc_files.append(file_data)
    asc_files = np.asarray(asc_files)

    # Writing nc file
    print("\nWriting netCDF file...")

    nc_file = "conv2_CSSTARFISH.nc"
    file_path = os.path.join(".", nc_file)
    nc = netcdf.netcdf_file(file_path, "w")

    # Set up attributes
    nc.history = "Created %s" % datetime.date.today()
    nc.contact = "Caroline Freshcorn"
    nc.institution = "William & Mary"
    nc.title = "Monthly global Enhanced Vegetation Indexes (EVI) at 0.5 degree resolution"
    nc.satellite = "Terra"

    # Calculating time
    time_line = []
    for i in range(1,13):
        distance = datetime.date(2006,i,1) - datetime.date(1900,1,1)
        time_line.append(distance.days)
    time_line = np.asarray(time_line)

    nc.createDimension("Time", 12)
    time = nc.createVariable("Time", "i", ("Time", ))
    time[:] = time_line
    time.units = "days since 1900-01-01"

    # Calculating longitude and latitude
    nc.createDimension("Longitude", 720)
    nc.createDimension("Latitude", 360)

    longitude = nc.createVariable("Longitude", "i", ("Longitude", ))
    latitude = nc.createVariable("Latitude", "i", ("Latitude", ))

    longitude[:] = np.arange(-179.75, 180, 0.5)
    latitude[:] = np.arange(-89.75, 90, 0.5)

    longitude.units = "deg_East"
    latitude.units = "deg_North"

    # Set up EVI
    evi = nc.createVariable("EVI", "f4", ("Time", "Longitude", "Latitude"))
    evi._FillValue = -0.3
    evi.missing_Value = -0.3
    evi.units = "unitless"
    evi.scale_factor = 10000
    evi.valid_min = -0.2
    evi.valid_max = 1.0
    evi[:] = asc_files

    nc.close()

    print("\nConversion complete.  Please open conv2_CSSTARFISH.nc to view your netCDF file.")