#! /usr/bin/env python
#
# pep8_xlpeng.py
#
# Author: Xianglu Peng
# 
# Last Update: 2020-11-18
#
# Purpose: 
# 
# This script extracts and convert the data from 
# a HDF5 file provided by the user and save the data 
# into a valid ascii raster file. 
#
##########################
#    REQUIRED MODULES    #
##########################

import os
import sys
import argparse
import h5py
import numpy as np


##################
#    Function    #
##################

def HDFConverter(folderpath, filename):
    """
    Name:       HDFConverter

    Params:     folderpath - string - the path of the folder where 
                the user store the hdf5 file, also the folder that 
                the script saves the created ascii file 

                filename - string - filename of the hdf5 file

    Features:   Read the HDF5 file provided by the user,
                extract the data and save the data into a ascii file
    """


    filepath = os.path.join(folderpath, filename)
    if os.path.exists(filepath):
        f = h5py.File(filepath, "r")
    else:
        print('File not found. Please check your file path.')
        sys.exit()
        

    
    data = [i for i in f['data']['assignment']]
    attributes = {}
    f_attr = f['data']['assignment']
    for key in f_attr.attrs.keys():
        attributes[key] = f_attr.attrs[key].decode('utf-8')
    asc_attr = ['nrows', 'ncols', 'xllcorner', 'yllcorner', 'cellsize', 'NODATA_value']

    
    
    asciipath = os.path.join(folderpath, "conv_1.txt")
    with open(asciipath,"w+") as asc:
        for key in asc_attr:
            asc.write("%s %s\n" % (key, attributes[key]))

        for y in data:
            for x in y: 
                asc.write(str(x)+"  ")
            asc.write("\n")
    


    prjpath = os.path.join(folderpath, "conv_1.prj")
    with open(prjpath,"w+") as prj:
        prj.write("%s" %attributes['crs'])



    print("Files created successfully! \n"
          "You can found them in the folder you provided us.")


################## 
#      Main      #
##################

if __name__ == "__main__":

    description = (
        'This script extracts the data from the HDF5 file'
        'and save the data into a valid ascii file.\n'
        'User needs to provide a valid filepath.')

    parser = argparse.ArgumentParser(description)
    args=parser.parse_args()


    folderpath = input("Enter the folder path:  ")
    filename = input("Enter the filaname:  ")
    HDFConverter(folderpath, filename)


    print("The raster image covers part of the Cedar Creek, Goolsby Road,"
          "and Fullerton Phillips Road. It's somewhere near Monticello, Georgia.")