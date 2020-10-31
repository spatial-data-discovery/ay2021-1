import os
import sys
import argparse

import zipfile
import datetime
from datetime import date
import numpy as np
from scipy.io import netcdf

def RasterToCDF():

    filelist = os.listdir("data")
    print(filelist)

    #get zip file from data folder 
    for file in filelist:
        if file.endswith('.zip'):
            pass
        else:
            filelist.remove(file)


    #initialize array
    attribute = []
    rasterdata = []

    #Check if file exist 
    if len(filelist) == 0:
        print("ERROR: File not exist.")
        sys.exit()

    else:
        print("%d files found. Processing..." %len(filelist))
        for i in filelist:
            path = "data/" + i
            filename = i[:-4]
            file_temp = []
            #unzip file
            with zipfile.ZipFile(path) as zipf: 
                #open file
                read = zipf.open(filename,"r")
                data=read.read().decode('UTF-8')
                data = data.splitlines()
                #get attributes and pixel data
                attribute = data[0:6]
                raster = data[6:]
                #store pixel data into array
                for row in range(len(raster)):
                    raster_row = raster[row].split(' ')
                    row_temp = []
                    for value in range(len(raster_row)):
                        pixel = int(raster_row[value])/10000

                        #check if values are in the EVI range
                        if (pixel < -0.2 or pixel > 1) and pixel != -0.3:
                            print("ERROR: Invalid EVI value!")
                            sys.exit()
                        else:
                            row_temp.append(pixel)

                    file_temp.append(row_temp)

                file_temp = np.asarray(file_temp)
                file_temp = np.flipud(file_temp)
                rasterdata.append(file_temp)

        rasterdata = np.asarray(rasterdata)
        #print(rasterdata)

        #find days since 1900-01-01
        days_since_1900 = []
        for i in range(1,13):
            days_since_1900.append((date(2006,i,1) - date(1900,1,1)).days)
        days_since_1900 = np.asarray(days_since_1900)

        #Create netCDF
        ncdf = netcdf.netcdf_file('data/conv2_xlpeng.nc', 'w')
        ncdf.contact = 'Xianglu Peng (xpeng04@email.wm.edu)'
        ncdf.history = 'created %s' % datetime.date.today()
        ncdf.institution = 'College of William and Mary'
        ncdf.title = 'Monthly global Enhanced Vegetation Indexes (EVI) at 0.5 degree resolution'
        ncdf.satellite = 'Terra'

        #longitude
        ncdf.createDimension("longitude", 720)
        longitude = ncdf.createVariable('longitude', 'f', ('longitude', ))
        longitude.units = 'deg_East'
        longitude[:] = np.arange(-179.75, 180, 0.5, float)

        #latitude
        ncdf.createDimension("latitude", 360)
        latitude = ncdf.createVariable('latitude', 'f', ('latitude', ))
        latitude.units = 'deg_North'
        latitude[:] = np.arange(-89.75, 90, 0.5, float)

        #time
        ncdf.createDimension('time', 12)
        time = ncdf.createVariable('time', 'i', ('time',))
        time.units ="days since 1900-01-01"
        time[:] = days_since_1900
        
        #EVI variables 
        evi = ncdf.createVariable('evi', 'f4', ('time', 'latitude', 'longitude'))
        evi._FillValue = -0.3
        evi.missing_value = -0.3
        evi.units = 'unitless'
        evi.valid_min = -0.2
        evi.valid_max = 1
        evi[:] = rasterdata

        ncdf.close()
        print("NetCDF file successfully created!")





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'This script extracts raster data from zip files and converts the data into Netcdf file.')
    args = parser.parse_args()

    RasterToCDF()