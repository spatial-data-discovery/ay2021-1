#Import Modules
import os
import argparse
import numpy as np
from scipy.io import netcdf
import zipfile
import datetime

if __name__ == "__main__":
    p = argparse.ArgumentParser(
    description = "This script reads data from twelve ASC raster files \
    and creates a single netCDF file.")
    args = p.parse_args()

    print("Extracting data from ASC raster files...")

#Read data from ASC raster files
    #first, get all zip files
    zip_file_list = []
    for zfile in os.listdir('data'):
        if zfile.endswith('.zip'):
            zip_file_list.append(zfile)
    #intialize array for all data from all files
    all_data = []
    #now, need raster info from zip files
    for zfile in zip_file_list:
        #initialize array for all pixel data in file
        file_data = []
        #open zip files, raster files
        with zipfile.ZipFile('data/'+zfile) as zip_open:
            with zip_open.open(zfile[:-4]) as raster_file:
                raster_lines = raster_file.readlines()[6:]
                for line in raster_lines:
                    new_line = line.split()
                    #initialize array for pixel vals in line
                    data_lines = []
                    for pixel in new_line:
                        #decode and scale each pixel
                        decode_pixel = pixel.decode('UTF-8')
                        int_pixel = int(decode_pixel)
                        final_pixel = int_pixel/10000
                        #append pixel val to array
                        data_lines.append(final_pixel)
                    #append lines to data array
                    file_data.append(data_lines)
                #then, need data to be not upside down!
                correct_data = np.asarray(file_data)
                correct_data = np.flipud(correct_data)
        #finally, put all data from all files together
        all_data.append(correct_data)
        #specify data array for EVI variable
        evi_data = np.asarray(all_data)


#Calculate 'days since 1900-01-01' for time variable
    days_since_vals = []
    for zfile in zip_file_list:
        date = zfile[19:29]
        date2 = datetime.datetime.strptime(date, "%Y-%m-%d")
        #find difference between date and 1900-01-01
        diff = (date2-(datetime.datetime.strptime('1900-01-01', "%Y-%m-%d")))
        #add difference to list
        days_since_vals.append(diff.days)
    days_since_vals = np.asarray(days_since_vals)

#Create a new NetCDF file
    print("Creating netCDF file...")
    my_file = "conv2_natallzl.nc"
    nc_path = os.path.join('.', my_file)
    f = netcdf.netcdf_file(nc_path, 'w')

    #write attributes
    f.history = 'created %s' % datetime.date.today()
    f.contact = 'Natalie Larsen (nalarsen@email.wm.edu)'
    f.institution = 'William & Mary'
    f.title = 'Monthly global Enhanced Vegetation Indexes (EVI) at 0.5 degree resolution'
    f.satellite = 'Terra'

    #latitude dimension and variable
    f.createDimension('latitude', 360)
    latitude = f.createVariable('latitude', 'i', ('latitude',))
    latitude[:] = np.arange(-89.75, 90, 0.5)
    latitude.units = 'deg_North'

    #longitude dimension and variable
    f.createDimension('longitude', 720)
    longitude = f.createVariable('longitude', 'i', ('longitude',))
    longitude[:] = np.arange(-179.75, 180, 0.5)
    longitude.units = 'deg_East'

    #time dimension and variable
    f.createDimension('time', 12)
    time = f.createVariable('time', 'i', ('time',))
    time[:] = days_since_vals
    time.units = 'days since 1900-01-01'

    #EVI variable
    evi = f.createVariable('evi', 'f4', ('time', 'latitude', 'longitude'))
    evi.valid_min = -0.2
    evi.valid_max = 1
    evi._FillValue = -0.3
    evi.missing_value = -0.3
    evi.units = 'unitless'
    evi.scale_factor = 10000
    evi[:] = evi_data

    f.close()

    print("conv2_natallzl.nc created in local directory")

#Helpful sources:
    #https://docs.python.org/3/library/zipfile.html#zipfile-objects
        #zipfile.Zipfile
        #zipfile.open
    #https://www.kite.com/python/answers/how-to-skip-the-first-line-of-a-file-in-python
        #skip lines when reading in file
    #https://numpy.org/devdocs/reference/generated/numpy.flipud.html
        #flip rows
    #https://www.programiz.com/python-programming/datetime/strptime
        #create datetime object
    #http://www.bic.mni.mcgill.ca/users/sean/Docs/netcdf/guide.txn_18.html
        #scale_factor attribute
