#Author- Ciaran Lowell
#Last Updated- 11/20/2020
#This script creates a netcdf function from zipped .asc raster files
###############################################################################
# IMPORT MODULES
###############################################################################
import os
import os.path
import datetime
from datetime import date
import numpy
from scipy.io import netcdf
import glob
from zipfile import ZipFile


##############################################################################
# GLOBAL VARIABLES:
##############################################################################
ERROR_VAL = -3000
basedate = date.fromisoformat('1900-01-01')
count = 0

###############################################################################
# FUNCTIONS
###############################################################################


def nc_history():
    """
    Name:     nc_history
    Input:    None.
    Output:   string (my_str)
    Features: Returns a file creation date string"""
    my_str = 'created %s' % datetime.date.today()
    return my_str


def writeFileAttributes(ncFile):
    """
    Name:        writeFileAttributes
    Input:       netCDF file
    Output:      None.
    Features:    Writes netCDF file attributes such as author"""
    ncFile.history = nc_history()
    ncFile.contact = 'Ciaran Lowell (cllowell@email.wm.edu)'
    ncFile.title = 'Monthly global EVI. 0.5 degree resolution'
    ncFile.institution = 'William & Mary'
    ncFile.satellite = 'Terra'
    return


def writeDimensions(ncFile, datafiles):
    """
    Name:        writeDimensions
    Input:       netCDF file, filepath
    Ouput:       None.
    Features:    Creates time, lat, and long dimensions for netcdf file"""

    # Date info is calculated based on filename
    # and represents days since January 1st, 1900
    ncFile.createDimension('time', 12)
    time = ncFile.createVariable('time', 'i', ('time', ))
    time.units = 'days since 1900-01-01'
    for file in os.listdir(datafiles):
        if file.endswith('.txt'):
            count = 0
            print(file)
            filedate = date.fromisoformat(file[-14:-4])
            print(filedate)
            filedelta = filedate-basedate
            print(filedelta)
            filedays = (str(filedelta)[0:-14])
            print(filedays)
            time[count] = filedays
            count += 1

    # Creates latitude dimension & variable
    ncFile.createDimension('latitude', 360)
    latitude = ncFile.createVariable('latitude', 'float', ('latitude', ))
    latitude[:] = numpy.flipud(numpy.arange(-89.75, 90, .5))
    latitude.units = 'degrees_north'

    # Create longitude dimension & variable:
    ncFile.createDimension('longitude', 720)
    longitude = ncFile.createVariable('longitude', 'float', ('longitude', ))
    longitude[:] = numpy.arange(-179.75, 180, 0.5)
    longitude.units = 'degrees_east'
    return


def writeData(ncFile, datafiles):
    """
    Name:        writeData
    Input:       netCDF file, filepath
    Output:      None.
    Features:    Reads .asc rasters, skips headers, and adds data to netcdf"""
    # Read .asc files and fill cdf with data
    evi = ncFile.createVariable('evi', 'f', ('time', 'latitude', 'longitude',))
    evi._FillValue = -.3
    evi.missing_value = -.3
    evi.units = 'unitless'
    evi.valid_min = -0.2
    evi.valid_max = 1
    evi.scale_factor = 10000
    evicount = 0
    for file in os.listdir(datafiles):
        if file.endswith('.txt'):
            print(file)
            evi[evicount] = numpy.genfromtxt(file, skip_header=6)
            evi[evicount] = (evi[evicount]/10000)
            print(evi[evicount])
            evicount += 1
    return


###############################################################################
# MAIN
###############################################################################
print('This program will convert zipped .asc files into one netCDF file.')
print('type "-h" for help')
zip_folder = input('Enter folder path to the zipped .asc files: ')
if zip_folder == '-h':
    print('This is a script for converting .asc raster files',
          'into the netCDF file format. You can read more about',
          'the netCDF format at:')

    print('https://www.unidata.ucar.edu/software/',
          'netcdf/docs/netcdf_introduction.html')
    zip_folder = input('Enter folder path to the'
                       'zipped .asc files you wish to convert: ')
for file in os.listdir(zip_folder):
    if file.endswith('.zip'):
        print(file)
        my_file = os.path.join(zip_folder, file)
        with ZipFile(my_file, 'r') as zip_ref:
            zip_ref.extractall(os.path.join(zip_folder))
my_file = 'test.nc'
nc_path = os.path.join(zip_folder, my_file)
f = netcdf.netcdf_file(nc_path, 'w')

writeFileAttributes(f)
writeDimensions(f, zip_folder)
writeData(f, zip_folder)
# Reference for Attribute convensions
# http://www.bic.mni.mcgill.ca/users/sean/Docs/netcdf/guide.txn_18.html
# David Fulker, Unidata Program Center Director, UCAR

f.close()
