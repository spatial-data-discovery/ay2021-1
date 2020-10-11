import argparse
import h5py
import numpy as np

def HDFConverter():

    # read file
    f = h5py.File("data/test.hdf", "r")


    #get raster data
    data = [i for i in f['data']['assignment']]
    
    #get attribute data 
    attributes = {}
    f_attr = f['data']['assignment']
    for key in f_attr.attrs.keys():
        attributes[key] = f_attr.attrs[key].decode('utf-8')

    #write attributes into asc file
    asc_attr = ['nrows', 'ncols', 'xllcorner', 'yllcorner', 'cellsize', 'NODATA_value']
    with open("data/conv1_xp.txt","w+") as asc:
        for key in asc_attr:
            asc.write("%s %s\n" % (key, attributes[key]))

        #write raster data into asc file
        for y in data:
            for x in y: 
                asc.write(str(x)+"  ")
            asc.write("\n")
    
    with open("data/conv1_xp.prj","w+") as prj:
        prj.write("%s" %attributes['crs'])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = 'This script extract the data from the HDF5 file and save the data into a valid ascii file. Users need to provide a valid filepath.')
    args=parser.parse_args()

    #filename = input("Enter the path to your file:  ")
    #HDFConverter("/Users/pxl/Documents/2020_Fall/DATA_431/test.hdf")
    HDFConverter()
    print("The raster image covers part of the Cedar Creek, Goolsby Road, and Fullerton Phillips Road. It's somewhere near Monticello, Georgia.")