import h5py
import numpy as np
import argparse
import os
import sys
from pathlib import Path

def HDFtoRaster():

    #### identify the necessary directories
    d_f = 'data'
    data= 'test.hdf'
    raster_txt = 'caiettia_raster.txt'
    prj_txt = 'caiettia_metadata.prj'
    hdf_data = os.path.join(d_f, data)

    # get the working directory
    work_direct = os.path.dirname(os.path.realpath(__file__))

    # directories for hdf data, raster data target save-path, prj file taret save-path respectively
    data_dir = os.path.join(work_direct, hdf_data)
    raster_dir = os.path.join(work_direct, os.path.join(d_f, raster_txt))
    prj_dir = os.path.join(work_direct, os.path.join(d_f, prj_txt))
    ####

    # open the hdf file in read mode
    hdf = h5py.File(data_dir, "r")
    
    # navigate to the "data" group
    a = hdf['data']
    
    #### This block gets the numerical rows and columns raster data
    a_array=[]
    for item in a['assignment'][:]:
        a_array.append(item.tolist())

    a_array = np.asarray(a_array)
    ####

    #### This block extracts the metadata for the raster file (nrows, ncols, etc.)
    attributes = []
    for item in a['assignment'].attrs.items():
        attributes.append(item)

    # assign each attribute as a variable for a shorter f.write statement later
    nrows = attributes[4][1].decode('utf-8')
    ncols = attributes[3][1].decode('utf-8')
    xllcorner = attributes[5][1].decode('utf-8')
    yllcorner = attributes[6][1].decode('utf-8')
    cellsize = attributes[1][1].decode('utf-8')
    NODATA = attributes[0][1].decode('utf-8')
    crs = attributes[2][1].decode('utf-8')
    ####


    #### This block writes our extracted data to a .txt file and some metadata to a .prj file

    # write our extracted raster data into a txt file
    with open(raster_dir, "w+") as f:
        f.write("nrows "+ nrows+"\n"+"ncols "+ncols+"\n"+"xllcorner "+xllcorner+'\n'+'yllcorner '+yllcorner+'\n'+'cellsize '+cellsize+'\n' "NODATA_value "+NODATA+'\n'+'\n')
        for items in a_array:
            for ele in items:
                f.write(str(ele))
                f.write(" ")
            f.write('\n')

    # write the GEOGCS data to the .prj file
    with open(prj_dir, "w+") as f:
        f.write(crs)
    ####


if __name__ =='__main__':
    parser = argparse.ArgumentParser(description = 'Script navigates to hdf data, extracts, then returns the raster data in .txt format.')
    args=parser.parse_args()

    HDFtoRaster()
    print("The Raster Image is an image covering Cedar Creek by Goolsby Road just outside of Monticello, Georgia, USA")   



