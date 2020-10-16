#!/usr/bin/env python3
#
# nc_write.py
#
# LAST EDIT: 2020-03-21
#
# This script writes an NetCDF file.
# Usage: run this script in tandem with nc_read.py.
# Each time, change the next False statement to True.

###############################################################################
# IMPORT MODULES
###############################################################################
import os
import os.path
import datetime
import numpy
from scipy.io import netcdf
import glob
from zipfile import ZipFile


##############################################################################
# GLOBAL VARIABLES:
##############################################################################
ERROR_VAL = -3000
basedate = date.fromisoformat("1900-01-01")
count = 0
convert = lambda x : (float(x)/1000)


###############################################################################
# FUNCTIONS
###############################################################################
def nc_history():
    """
    Name:     nc_history
    Input:    None.
    Output:   string (my_str)
    Features: Returns a string for netCDF file history field based on the file's
              creation date
    """
    my_str = "created %s" % datetime.date.today()
    return my_str



###############################################################################
# MAIN
###############################################################################
print("This program will convert zipped .asc files into one netCDF file.")
print("This program must be run three times to run properly.")
codebool = int(input('Have you run this program 0, 1, or 2 times previously?: '))
zip_folder = input('Enter folder path to the zipped .asc files you wish to convert: ')
zip_path = zip_folder + '\\' + "*.zip"
files = glob.glob(zip_path)
for zip in files:
    with ZipFile(zip,'r') as zippy:
        zippy.extractall(zip_folder)
data_path = zip_folder + '\\' + "*.txt"
datafiles = glob.glob(data_path)
my_file = "test.nc"
nc_path = os.path.join(zip_folder, my_file)
# Create a new NetCDF file
f = netcdf.netcdf_file(nc_path, 'w')

if codebool == 0:
    # Write file attributes:
    f.history = nc_history()
    f.contact = 'Ciaran Lowell (cllowell@email.wm.edu)'
    f.title = 'Monthly global Enhanced Vegetation Indexes (EVI) at 0.5 degree resolution'
    f.institution = 'William & Mary'
    f.satellite = "Terra"

if codebool == 1:
    # Create time dimension and a variable
    f.createDimension('time', 12)
    time = f.createVariable('time', 'i', ('time',) )
    time.units = 'days since 1900-01-01'
    for file in datafiles:
        filedate =  date.fromisoformat(file[-14:-4])
        print(filedate)
        filedelta = filedate-basedate
        print(filedelta)
        filedays = (str(filedelta)[0:-14])
        print(filedays)
        time[count] = filedays
        count +=1
    print(time)

    # Create lat dimension & variable
    f.createDimension('latitude', 360)
    latitude = f.createVariable('latitude', 'float', ('latitude'))
    latitude[:] = numpy.flipud(numpy.arange(-89.75, 90, .5))
    latitude.units = 'degrees_north'

    # Create long dimension & variable:
    f.createDimension('longitude', 720)
    longitude = f.createVariable('longitude', 'float', ('longitude',))
    longitude[:] = numpy.arange(-179.75, 180, 0.5)
    longitude.units = 'degrees_east'

if codebool == 2:
    # Read .asc files and fill cdf with data
    evi = f.createVariable('evi', 'f', ('time','latitude','longitude'))
    evi._FillValue = -.3
    evi.missing_value = -.3
    evi.units = 'unitless'
    evi.valid_min = -0.2
    evi.valid_max = 1
    for file in datafiles:
        evi[count] = numpy.genfromtxt(file, skip_header=7, converters = {1: convert})
    # Reference for Attribute convensions
    # http://www.bic.mni.mcgill.ca/users/sean/Docs/netcdf/guide.txn_18.html
    # David Fulker, Unidata Program Center Director, UCAR

f.close()
