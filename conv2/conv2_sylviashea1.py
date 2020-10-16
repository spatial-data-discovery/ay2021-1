# IMPORT MODULES ######################
import os
import sys

from datetime import date
import numpy as np
from scipy.io import netcdf
from zipfile import ZipFile
import argparse

# FUNCTIONS ###########################
def extract_asc(data_dir,zf,filename):
    '''
    Inputs: - data_dir: directory containing zipfile
            - zf: zipfile containing ASC
            - filename: name of ASC txt file
    Purpose: Returns pixel values from each ASC in correct order.
    '''
    file_pixels = []
    z_dir = ZipFile(os.path.join(data_dir,zf))
    asc = z_dir.open(filename)
    line_count = 0
    for line in asc:
        if line_count>=6:
        # Storing pixels in each line
            line_arr = []
            line = line.split()
            for pixel in line:
                p = int(pixel.decode('utf-8'))
                line_arr.append(p/10000)
            file_pixels.append(line_arr)
        line_count+=1
    # All pixels in single ASC file
    file_pixels = np.asarray(file_pixels) 
    file_pixels = np.flipud(file_pixels) 
    return file_pixels 

# MAIN #################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extracts ASCII rasters containing EVI and combines them into single netCDF file.')
    args = parser.parse_args()

    # Path to zipfiles
    data_dir = 'data'
    abs_path = os.path.abspath(data_dir)
    try:
        zfiles = os.listdir(abs_path)
    except FileNotFoundError:
        print('Error: Data directory not found')
        sys.exit()

    print('------- Extracting ASCII raster values from zipfiles --------')
    total_pixels = []
    # Extract pixel values from each ASC
    for zf in zfiles:
        if zf.endswith('.zip'):
            filename = zf[:-4]
            file_pixels = extract_asc(data_dir,zf,filename)
            # Adds pixel values from each ASC file to single array
            total_pixels.append(file_pixels)
    total_pixels = np.asarray(total_pixels)

    # Calculate days since 1900-01-01
    days_since = []
    for i in range(1,13):
        # from https://www.w3resource.com/python-exercises/python-basic-exercise-14.php
        delta = date(2006,i,1) - date(1900,1,1)
        days_since.append(delta.days)
    days_since = np.asarray(days_since)    
    
    print('------- Generating netCDF --------')
    ## Initialize netCDF
    ncdf = 'conv2_sylviashea1.nc'
    nc_path = os.path.join(data_dir,ncdf)
    f = netcdf.netcdf_file(nc_path,'w')

    # Write file attributes
    f.history = "Created %s" % date.today()
    f.contact = 'Sylvia M. Shea (smshea@email.wm.edu)'
    f.institution = 'College of William & Mary'
    f.title = 'Monthly global Enhanced Vegetation Indexes (EVI) at 0.5 degree resolution'
    f.satellite = 'Terra'

    # Write dimensions and corresponding variables
    f.createDimension('latitude',360)
    latitude = f.createVariable('latitude','i',('latitude',))
    latitude[:] = np.arange(-89.75,90,0.5,float)
    latitude.units = 'deg_North'

    f.createDimension('longitude',720)
    longitude = f.createVariable('longitude','i',('longitude',))
    longitude[:] = np.arange(-179.75,180,0.5,float)
    longitude.units = 'deg_East'

    f.createDimension('time',12)
    time = f.createVariable('time','i',('time',))
    time[:] = days_since
    time.units = 'days since 1900-01-01'

    # Write EVI variable
    EVI = f.createVariable('EVI','f4',('time','latitude','longitude'))
    EVI._FillValue = -0.3
    EVI.missing_value = -0.3
    EVI.units = 'unitless'
    EVI.valid_min = -0.2
    EVI.valid_max = 1
    EVI[:] = total_pixels  

    f.close()
    print("------- netCDF file %s output in 'data' directory --------" % ncdf)