# IMPORT MODULES ##############################
import os
import sys

import h5py
import numpy as np
import argparse

# MAIN ########################################
if __name__ == "__main__":
    parse = argparse.ArgumentParser(description='Extracts ASCII raster and prj from HDF5 file. Saves files in conv/data directory')
    args = parse.parse_args()
    d_dir = 'data'
    ffile = 'test.hdf'
    path = os.path.join(d_dir,ffile)

    # Read HDF 
    try:
        hdfile = h5py.File(path,'r')
    except FileNotFoundError:
        print('Error: File not found')
        sys.exit()
    
    print('---------- Starting Extraction ----------')
    
    data = hdfile['data']['assignment']

    # Retrieve headers and corresponding values
    params = []
    p_vals = []
    crs = []
    for i in data.attrs.keys():
        params.append(i)

    for i in data.attrs.values():
        i = i.decode('utf-8')
        p_vals.append(i)

    # Remove crs from headers
    crs.append(params.pop(2))
    crs.append(p_vals.pop(2))

    # Retrieve raster values
    r_vals = []
    for i in data:
        r_vals.append(i)
    r_vals = np.asarray(r_vals)

    # Validate columns
    c = p_vals[2]
    for i in range(len(r_vals)):
        if len(r_vals[i])!= int(c):
            print('Error: Number of columns in header does not match number of columns in dataset')
            print('Column parameter = %d, Actual columns = %d' % (c, r_vals[i]))
            sys.exit()
    
    # Validate rows
    r = p_vals[3]
    if len(r_vals)!=int(r):
        print('Error: Number of rows in header does not match number of rows in dataset')
        print('Row parameter = %d, Actual rows = %d' % (r, len(r_vals)))
        sys.exit()

    # Write ASCII file
    with open('data/conv1_sylviashea1.asc','w+') as asc:
        asc.write(
        params[2]+' '+p_vals[2]+'\n'+
        params[3]+' '+p_vals[3]+'\n'+
        params[4]+' '+p_vals[4]+'\n'+
        params[5]+' '+p_vals[5]+'\n'+
        params[1]+' '+p_vals[1]+'\n'+
        params[0]+' '+p_vals[0]+'\n')
        for row in data:
            for item in row:
                asc.write(str(item)+' ')
            asc.write('\n')
            
    # Write prj file
    with open('data/conv1_sylviashea1.prj','w+') as prj:
        prj.write(crs[1])

    hdfile.close()
    asc.close()
    prj.close()
    
    print('---------- Extraction Complete ----------')
    print('\nGenerated ASCII and prj files in conv/data directory\n')

    print('This raster is located in southeast corner of Jasper County, Georgia at the intersection of Fullerton Phillips Road and Goolsby Road. It is just southeast of Monticello, Georgia.')