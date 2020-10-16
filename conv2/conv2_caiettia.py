import os
import datetime
from datetime import date
import numpy as np
from scipy.io import netcdf
import zipfile
import argparse


def ASCtoNetCDF():

    data_loc = 'data'
    dir_py = os.path.dirname(os.path.realpath(__file__))
    dir_data = os.path.join(dir_py, data_loc)

    if os.path.isdir(dir_data): # CATCH IF DATA FOLDER DOES/DOES NOT EXIST
        print("Data file found.")
        dataframes = []
        list_dir_data = os.listdir(dir_data)

    
        count_zip = 0
        for item in list_dir_data: # CATCH IF THERE IS NO DATA IN DATA FOLDER
            if item.endswith('.zip'):
                count_zip+=1

        if count_zip > 0:
            print("Found ", count_zip," zip files. Parsing now...")
            file_dates=[]
            file_info=[]
            for item in list_dir_data:
                if item != 'README.md':
                    temp_zip = zipfile.ZipFile(os.path.join(dir_data, item))
                    temp_string = str(item).replace('.zip','')
                    temp_array_data = []
                    file_dates.append(str(item).replace('MODIS_0.5rs-Raster_','').replace('.txt.zip',''))
                    temp_file_info=[]
                    i=0
                    for line in (temp_zip.open(temp_string)):
                        if i < 6:
                            temp_file_info.append(line.decode('utf-8').split())
                        else:
                            temp_temp_data=[]
                            for item in line.split():
                                data_point = int(item.decode('utf-8'))
                                temp_temp_data.append(data_point/10000)
                            temp_array_data.append(temp_temp_data)
                        i+=1
                    dataframes.append(temp_array_data)
                    file_info.append(temp_file_info)

            #### Get the nubmer of days since 1900-01-01 in an array
            date_anchor = date(1900,1,1)
            days_since = []
            for i in range(1,len(file_dates)+1):
                temp_days = date(2006,i,1) - date_anchor
                days_since.append(temp_days.days)
            days_since = np.asarray(days_since)
            ####


            #CONVERT TO NUMPY ARRAYS 
            dataframes = np.asarray(dataframes)


            #create netcdf
            file_name = 'test.nc'
            file_location = os.path.join(dir_py,file_name)
            print('Successfully parsed raster data. \nCreating NetCDF file now at: ', file_location)
            f = netcdf.netcdf_file(file_location, 'w')
            f.history = "created %s" % datetime.date.today() 
            f.contact = 'Andrew Caietti (aecaietti@email.wm.edu)'
            f.title = 'Monthly global Enhanced Vegetation Indexes (EVI) at 0.5 degree resolution'
            f.institution = 'College of William & Mary'
            f.satellite = 'Terra'


            # for this, we create dimensions long, lat, time
            f.createDimension('lat', 360)
            f.createDimension('log', 720)
            f.createDimension('time', 12)

            # define variables and set units
            latitude = f.createVariable('lat', 'i', ('lat',))
            longitude = f.createVariable('log', 'i', ('log',))
            time = f.createVariable('time', 'i', ('time',))
            latitude.units = 'deg_east'
            longitude.units = 'deg_south'
            time.units = 'days since 2006-01-01'

            #fill the each variable with values
            latitude[:] = np.arange(89.75,-90,-0.5,float)
            longitude[:] = np.arange(-179.75,180, 0.5,float)
            np.copyto(time[:], days_since)

            # Create the EVI variable
            evi = f.createVariable('evi', 'f4', ('time','lat','log'))
            evi._FillValue = -3000
            evi.missing_value = -3000
            evi.long_name = 'Enhanced Vegetation Index'
            evi.units = 'unitless'
            evi.valid_min = -0.2
            evi.valid_max = 1
            for i in range(len(dataframes)):
                dataframes[i] = np.flipud(dataframes[i]) # we flip the values in the rows of the array to match the calculated coordinates
            np.copyto(evi[:], dataframes) # here, we store the rasters into our EVI variable by month

            print('NetCDF file created. Done.')

            f.close()
        else:
            print("No .zip files detected in the data folder.")
    else:
        print('ERROR. Data file not found.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'The script coverts raster data in a .zip format in the data folder into valid netcdf files in the file path directory.')
    args=parser.parse_args()

    ASCtoNetCDF()
