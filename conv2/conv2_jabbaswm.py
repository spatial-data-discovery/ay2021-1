#Jamil Abbas
#Last updated: 2020-10-15
#This script finds the raster files in the folder 'data' (in .zip form) and extracts the information from all of them and creates a netCDF file with the contents of the raster.



##################################
#        Required Modules        #
##################################
import zipfile
import sys
import os
import datetime
from datetime import date
import numpy as np
from scipy.io import netcdf
import argparse


def create_netcdf():

    #Find the raster files (in .zip form)
    zipfiles = []

    for file in os.listdir('data'):
        if file.endswith('.zip'):
            zipfiles.append(file)

    data = []
    dates = []

    if len(zipfiles) == 0: #Error handling
        print('ERROR: No Data files found')

    else:
        for z in zipfiles:
            tempdata = []
            fname = 'data/' + z
            rastfname = str(z).replace('.zip', '')
            with zipfile.ZipFile(fname) as zf: #open zip
                with zf.open(rastfname) as rdata: #open raster contents
                    info = rdata.read().decode('UTF-8')
                    header_info = info.splitlines()[0:6] #Save the header data of the raster
                    raster_info = info.splitlines()[6:] #Everything else in the raster

                    for i in range(len(raster_info)):
                        row = []
                        splitrow = raster_info[i].split(' ')

                        #Iterate through the raster one row at a time
                        for j in range(len(splitrow)):
                            pixel = int(splitrow[j]) / 10000 #Adjust pixel to scale


                            #Error handling (check in valid range of EVI)
                            if ((pixel < -0.2) or (pixel > 1)) and (pixel != -0.3):
                                print('Error: Pixel values out of EVI accepted range.')
                                sys.exit()

                            else:
                                row.append(pixel) #Append to the row array

                        tempdata.append(row)
                    tempdata = np.asarray(tempdata)
                    tempdata = np.flipud(tempdata) #Use np.flipud to adjust the raster so that it isn't upsidedown
                    data.append(tempdata) #Append tempdata to the main raster array

        data = np.asarray(data)

        #Loop to find days since 1900-01-01 to build time dimension and variable

        initiald = date(1900, 1, 1)
        num_days = []
        for i in range(0, 12):
            d = date(2006, i+1, 1) - initiald #All dates are in 2006, first day of the month, hence only the month changes
            d = d.days
            num_days.append(d)
        num_days = np.asarray(num_days)



    #Build the netCDF file
    f = netcdf.netcdf_file('data/conv2_jabbaswm.nc', 'w')

    #Attributes
    f.history = "created %s" % datetime.date.today()
    f.contact = 'Jamil K. Abbas (jkabbas@email.wm.edu)'
    f.institution = 'William and Mary'
    f.title = 'Monthly global Enhanced Vegetation Indexes (EVI) at 0.5 degree resolution'
    f.satellite = 'Terra'

    ### Dimensions ###

    #Longtitude dimension:
    f.createDimension('long', 720)
    longitude = f.createVariable('long', 'f', ('long', ))
    longitude[:] = np.arange(-179.75, 180, 0.5, float)
    longitude.units = 'degrees_east'

    #Latitude dimension:
    f.createDimension('lat', 360)
    latitude = f.createVariable('lat', 'f', ('lat', ))
    latitude[:] = np.arange(-89.75, 90, 0.5, float)
    latitude.units = 'degrees_north'

    #Time dimension:
    f.createDimension('time', 12)
    time = f.createVariable('time', 'i', ('time', ))
    time[:] = num_days
    time.units = "Days since 1900-01-01"


    #EVI variable:
    evi = f.createVariable('evi', 'f4', ('time', 'lat', 'long', ))
    evi._FillValue = -0.3
    evi.missing_value = -0.3
    evi.units = 'unitless'
    evi[:] = data

    f.close()

    print('Raster created successfully')



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'This script finds the raster files in the folder <data> (in .zip form) and extracts the information from all of them and creates a netCDF file with the contents of the raster.')

    args = parser.parse_args()

    create_netcdf()
