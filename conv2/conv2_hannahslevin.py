##IMPORT MODULES##
import datetime
from datetime import date
import zipfile
from zipfile import ZipFile
import argparse
import os
import numpy as np
from scipy.io import netcdf

##MAIN FRAME##

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extracts ASCII rasters exports rasters into single netCDF file.')
    args = parser.parse_args()

##BEGIN EXTRACTION##
# Acess files from path and put them in an array
    directory = 'data'
    abs_path = os.path.abspath(directory)
    zipfile_dir = os.listdir(abs_path)
    pixels = list()
    for zip in zipfile_dir:
        if zip.endswith('.zip'):
            f = zip[:-4]
            file_body = []
            dir = ZipFile(os.path.join(directory,zip))
            ascii = dir.open(f)
            count = 0
            for i in ascii:
                if count>=6:
                # Storing pixels in each line
                    line = []
                    i = i.split()
                    for j in i:
                        cell = int(j.decode('utf-8'))
                        line.append(cell/10000)
                    file_body.append(line)
                count+=1
            # All pixels in single ASC file
            file_body = np.asarray(file_body)
            file_body = np.flipud(file_body)
            pixels.append(file_body)
    pixels = np.asarray(pixels)

# Calculate days since 1900-01-01
    days = []
    for i in range(1,13):
        change_inT = date(2006,i,1) - date(1900,1,1)
        days.append(change_inT.days)




#Generate NetCDF file
    netcdf = netcdf.netcdf_file('data/conv2_hannahslevin.nc', 'w')
#Set attributes
    netcdf.title = '(12) ASC raster data files containing monthly global Enhanced Vegetation Indexes (EVI) from the Terra satellite at 0.5-degree resolution'
    netcdf.satellite = 'Terra'
    netcdf.institution = 'The College of William & Mary'
    netcdf.contact = 'Hannah Slevin (hmslevin@email.wm.edu)'
    netcdf.history = "Created on " +  str(datetime.date.today())

#Write dimensions
#Longitude
    netcdf.createDimension('longitude', 720)
    longitude = netcdf.createVariable('longitude', 'f', ('longitude', ))
    longitude[:] = np.arange(-179.75, 180, .5, float)
    longitude.units = 'degrees_East'

#Latitude
    netcdf.createDimension('latitude', 360)
    latitude = netcdf.createVariable('latitude', 'f', ('latitude', ))
    latitude[:] = np.arange(-89.75, 90, .5, float)
    latitude.units = 'degrees_North'
# Time
    netcdf.createDimension('time', 12)
    time = netcdf.createVariable('time', 'i', ('time', ))
    time[:] = days
    time.units = "days since 1900-01-01"

    EVI =  netcdf.createVariable('EVI', 'f4', ('time', 'latitude', 'longitude'))
    EVI.missing_value = -0.3
    EVI._FillValue = -0.3
    EVI.units = 'unknown'
    EVI.valid_min = -.2
    EVI.valid_max = 1
    EVI[:] = pixels

    #Close file
    netcdf.close()
