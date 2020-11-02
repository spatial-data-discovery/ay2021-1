import os
import os.path
import datetime
import numpy as np
from scipy.io import netcdf
import argparse
import zipfile36 as zipfile

def conversion_2(data_folder):

    frames = [] #evi data
    count_zip = 0
    zip_files = sorted(os.listdir(data_folder)) #list all files in folder
    for file in zip_files:
        if file.endswith('.zip'): #only check for zip files
            print("Processing file: ", file)
            print('\n')
            temp_data = []
            count_zip+=1
            zip = zipfile.ZipFile(os.path.join(data_folder,file)) #open zip file
            with zip.open(file.replace('.zip','')) as z: #open file inside the zip file
                for line in range(6): #skip the first 6 lines
                    next(z)
                for line in z:
                    sv = line.split() #get data as string vector
                    intv = [int(el.decode('utf-8'))/10000 for el in sv] #convert string vector to integer vector
                    temp_data.append(intv) #add to list
            frames.append(temp_data) #add to evi list


    days_after = [] #days since 1900-01-01 for 2006-i-1
    base_date = datetime.date(1900,1,1)
    for i in range(1,count_zip+1):
        new_date = datetime.date(2006,i,1)
        num_days = new_date - base_date
        days_after.append(num_days.days)

    days_after = np.asarray(days_after) #convert to numpy vector
    frames = np.asarray(frames) #convert to numpy matrix



    output_file = os.path.join(data_folder,'brain-bot.nc') #output file path

    #Create NetCDF file
    f = netcdf.netcdf_file(output_file, 'w')

    f.history = "created %s" % datetime.date.today()
    f.contact = 'Brian Z. Wu (bzwu@email.wm.edu)'
    f.institution = "William & Mary"
    f.title = "Monthly global Enhanced Vegetation Indexes (EVI) at 0.5 degree resolution"
    f.satellite = "Terra"
    #create time dimension
    f.createDimension('time',12)
    time = f.createVariable('time', 'i', ('time',))
    time.units = 'days since 1900-01-01'
    time[:] = days_after
    #create longitude dimension
    f.createDimension('longitude',720)
    longitude = f.createVariable('longitude','f',('longitude',))
    longitude.units = 'deg_East'
    longitude[:] = np.arange(-179.75,180,0.5)
    #create latitude dimension
    f.createDimension('latitude',360)
    latitude = f.createVariable('latitude','f',('latitude',))
    latitude.units = 'deg_North'
    latitude[:] = np.arange(90,-89.75,-0.5)


    #create evi variable
    evi = f.createVariable('evi','f4',('time','latitude','longitude'))
    evi.units = 'unitless'
    evi.valid_minimum = -0.2
    evi.valid_maximum = 1
    evi.fill_value = -3000
    evi.missing_value = -3000
    evi.long_name = 'Enhanced Vegetation Indexes'
    np.copyto(evi[:],frames)
    f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Takes content from 12 Ascii Raster files and puts them into one netCDF file. The parameter is a string that represents the folder where one must look for zip files')
    args = parser.parse_args()
    conversion_2('data') #the parameter that is taken is a string that represents the data folder
