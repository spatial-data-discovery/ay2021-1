# !/usr/bin/env python3 
#
# conv1_CSSTARFISH.py
#
# AUTHOR: Caroline Freshcorn
# VERSION: 0.4
# DATE (LAST UPDATED): 2020-10-20
#
# This script reads an HDF5 file and writes it into an ASCII raster.
#
###############################################################################
# IMPORT MODULES
###############################################################################
import os
import os.path

import argparse
import numpy
import h5py

###############################################################################
# MAIN
###############################################################################

# Provide help documentation for the user.
parse = argparse.ArgumentParser("Reads a provided HDF5 file and converts it "
                                "into an ASC file format (i.e., an ASCII raster."
                               )
parsing = parse.parse_args()

# Set file path.
path_input = input("Please enter the file path, "
                   "including the name of the .hdf file: "
                  )
hdf_path = path_input

# Ensure the file is in the indicated path.
if os.path.isfile(hdf_path):
    # Open HDF file contents.
    print("\nOpening existing HDF file.")
    hdfile = h5py.File(hdf_path, "r")

    data_assignment_objects = hdfile["data"]["assignment"]
    data_attr = {}

    # Access data attributes.
    print("\nAccessing HDF file's attributes.")
    for key in data_assignment_objects.attrs.keys():
        value = data_assignment_objects.attrs[key]
        data_attr[key] = value.decode("utf-8")

    # Write new projection file.
    print("\nCreating projection file format.")
    with open(".\data\conv1_CSSTARFISH.prj", "w") as prj_file:
        prj_file.write(data_attr["crs"])

    # Write contents of ASCII raster file.
    print("\nConverting HDF to ASC...")
    del data_attr["crs"]
    with open(".\data\conv1_CSSTARFISH.asc", "w") as asc_file:
        asc_file.write("NCOLS " + str(int(data_attr["ncols"])))
        asc_file.write("\nNROWS " + str(int(data_attr["nrows"])))
        asc_file.write("\nXLLCORNER " + data_attr["xllcorner"])
        asc_file.write("\nYLLCORNER " + data_attr["yllcorner"])
        asc_file.write("\nCELLSIZE " + data_attr["cellsize"])
        asc_file.write("\nNODATA_VALUE " + data_attr["NODATA_value"])
        asc_file.write("\n")

        print("Filling in raster data.")
        for row in numpy.asarray(data_assignment_objects):
            for column in row:
                asc_file.write(str(column) + " ")
            asc_file.write("\n")

    hdfile.close()

    print("\nConversion complete.  Please open conv1_CSSTARFISH.asc to view your raster.")
else:
    print("No file found in this path.  Please try again with a different path name.")

# Output information about the location of the raster.
output_message = (
        "Where in the world is this raster from?\n"
        "This raster's bottom left corner is positioned at approximately\n"
        "83 degrees West and about 33 degrees North.  Consequently, the raster\n"
        "is located within a town from Jasper County, Georgia,\n"
        "to the southeast of Monticello.  The raster is also positioned within\n"
        "the bounds of GA Highway 11, Kinderhook Road, Fullerton-Phillips\n"
        "Road, and Perimeter Road."
    
)
print(output_message)
