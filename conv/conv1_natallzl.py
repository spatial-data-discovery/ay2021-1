#Import Modules
import h5py
import numpy as np
import argparse
import os
import sys

def HDF5toASCII():
    if not os.path.isfile('data/test.hdf'):
        print ("HDF5 file not found!")
        sys.exit()

    #Read HDF5 file
    my_file = 'data/test.hdf'
    hdfile = h5py.File(my_file, 'r')
    #Navigate to 'data' group
    data_group = hdfile['data']

    #Extract raster cell values,
        #raster headers,
        #and raster header values
    assignment_data = []
    for x in data_group['assignment']:
        assignment_data.append(x)

    attributes = []
    for y in data_group['assignment'].attrs.keys():
        attributes.append(y)

    attribute_vals = []
    for attr_val in data_group['assignment'].attrs.values():
        attribute_vals.append((attr_val).decode('utf-8'))

    #Create dictionary with raster headers and their values
    attribute_dict = dict(zip(attributes, attribute_vals))

    #Write ASCII raster file
    raster_file = open('data/conv1_natallzl.txt', 'w')
    raster_file.write("NROWS " + attribute_dict['nrows'] + '\n' + \
                        "NCOLS " + attribute_dict['ncols'] + '\n' + \
                        "XLLCORNER " + attribute_dict['xllcorner'] + '\n' + \
                        "YLLCORNER " + attribute_dict['yllcorner'] + '\n' + \
                        "CELLSIZE " + attribute_dict['cellsize'] + '\n' + \
                        "NODATA_VALUE " + attribute_dict['NODATA_value'] + \
                        '\n' + '\n')

    for row in np.array(assignment_data):
        for num in row:
            raster_file.write(str(num) + ' ')
        raster_file.write('\n')

    raster_file.close()

    #Write .prj file that contains GCS information
    prj_file = open('data/conv1_natallzl.prj', 'w')
    prj_file.write(attribute_dict['crs'])


    raster_file.close()
    prj_file.close()
    hdfile.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser(
    description = "This script extracts data from the test.hdf HDF5 file, \
    produces an ASC raster file and a .prj file, and prints the location of the raster file.")
    args = p.parse_args()

    HDF5toASCII()

    print("This raster is from southeast Jasper County, outside of Monticello, GA, U.S.A. " \
    "It covers part of Cedar Creek and Goolsby Branch, as well as " \
    "Goolsby Road and Fullerton Phillips Road.")
