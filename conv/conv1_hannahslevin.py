#Modules
import argparse
import sys
import h5py
import numpy as np

#Function to convert an HDFt file to an ASC raster file
def HDFConverter(path_hdf):

    #read HDF file in
    try:
        hdf = h5py.File(path_hdf,"r")
        print("File opened")
    except FileNotFoundError:
        print("File not found")

    print("Data is extraction has begun ... please hold")
    #open data
    data = hdf["data"]

    #put row col data into list named vlaues
    values = []
    for val in data["assignment"]:
         values.append(val)

    #convert list to an array
    values = np.array(values)
    attrs = []
    for attribute in data["assignment"].attrs.items():
        attrs.append(attribute)

    #Create attribute variables for the ASCII header
    NODATA_value = attrs[0][1].decode("UTF-8")
    cellsize = attrs[1][1].decode("UTF-8")
    crs = attrs[2][1].decode("UTF-8")
    ncols = attrs[3][1].decode("UTF-8")
    nrows = attrs[4][1].decode("UTF-8")
    xllcorner = attrs[5][1].decode("UTF-8")
    yllcorner = attrs[6][1].decode("UTF-8")

    #Create ascii raster by adding extracted data to an empty text file
    with open("./data/conv1_hannahslevin.asc", "w") as file:
        file.write("ncols " + ncols + "\n"
                    "nrows " + nrows + "\n"
                    "xllcorner " + xllcorner + "\n"
                    "yllcorner " + yllcorner + "\n"
                    "cellsize " + cellsize + "\n"
                    "NODATA_value " + NODATA_value + "\n")
        for val in values:
            for item in val:
                file.write(str(item) + " ")
            file.write("\n")

    #Create prj file
    with open("./data/conv1_hannahslevin.prj", "w") as file:
        file.write(crs)

    print("Data extraction completed!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "This script converts the an HDF5 file into an ASC raster file.  It also prints where in the world the converted test HDF5 file is located.")
    args = parser.parse_args()

    #establish file path to test.hdf
    path_hdf = "./data/test.hdf"
    #call function
    HDFConverter(path_hdf)
    #describe location of the test.hdf file
    print("This raster is located in Georgia near Monticello.  The raster encompasses the intersection of Goolsby and Fullerton Phillips road and Cedar Creek.")
