import zipfile
import sys
import os
import datetime
from datetime import date
import numpy as np
from scipy.io import netcdf
import argparse

def make_netcdf_from_ascii(data_folder):
    filelist = []
    data = []
    dates = []

    # access the zipfiles in the directory specified when calling the function
    for file in os.listdir(data_folder):

        # find zip files
        if file.endswith('.zip'):
            # add zip files to list of files we are going to pull data out of
            filelist.append(file)

    # make sure there was at least one zip file in the folder the user specified
    if len(filelist)<1:
        print('no zipfiles')

    # as long as there are zip files, proceed
    else:
        # sources for this part of the code:
        # https://stackoverflow.com/questions/36434764/permissionerror-errno-13-permission-denied
        # https://stackoverflow.com/questions/39296101/python-zipfile-removes-execute-permissions-from-binaries
        # https://numpy.org/devdocs/reference/generated/numpy.flipud.html
        # https://docs.python.org/3/library/zipfile.html

        for modis in filelist:

            # create empty list where the data will live temporarily
            data_container = []

            filename = 'data/' + modis

            raster = str(modis).replace('.zip', '')

            # pull the contents of the modis files out of the zipfiles
            with zipfile.ZipFile(filename) as zipfile1:

                with zipfile1.open(raster) as rasterdata:

                    rasterdata_all = rasterdata.read().decode('UTF-8')

                    headers = rasterdata_all.splitlines()[0:6]

                    data_from_raster = rasterdata_all.splitlines()[6:]

                    # get each individual row from the data in the raster
                    for i in range(len(data_from_raster)):

                        rows = []

                        row_split = data_from_raster[i].split(' ')

                        # get the individual cells or pixels or whatever they're called
                        # and fix the scale
                        for blah in range(len(row_split)):

                            individ_cell = int(row_split[blah]) / 10000

                            rows.append(individ_cell)

                    # add the individual cells to the container where the data lives
                        data_container.append(rows)

                    # make it an array
                    data_container2 = np.asarray(data_container)

                    # make it not upside down
                    data_container3 = np.flipud(data_container2)

                    # add it to the actual place where the data lives
                    data.append(data_container3)

        # now we're outside the for loop but still inside the else block
        data = np.asarray(data)

        # now we fix the dates and get it to find days since Jan 1 1900
        targetday = date(1900, 1, 1)
        dayssinceday = []

        # this tells it to subtract the target day from the date that the file are from (first of every month)
        for month in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
            dayssinceday.append((date(2006, (month+1), 1) - targetday).days)

        # make it an array
        dayssinceday2 = np.asarray(dayssinceday)

        # now we start making the actual netcdf file
        # make the file and give permission to write to the file
        mynewncfile = netcdf.netcdf_file('data/conv2_aehilla.nc', 'w')

        # set the attributes as specified in the instructions
        mynewncfile.title = 'monthly global Enhanced Vegetation Indexes (EVI) at 0.5 degree resolution'
        mynewncfile.satellite = 'Terra'
        mynewncfile.institution = 'The College of William & Mary'
        mynewncfile.contact = 'Amy Hilla (aehilla@email.wm.edu)'
        mynewncfile.history = "created %s" % datetime.date.today()

        # now we can start creating dimensions
        # we will make three dimensions: time, longitude, and latitude

        # start with longitude
        mynewncfile.createDimension('longitude', 720)
        longitude = mynewncfile.createVariable('longitude', 'i', ('longitude', ))
        # the cell size is half degree
        longitude[:] = np.arange(-179.75, 180, 0.5, float)
        longitude.units = 'degrees'

        # then do latitude
        mynewncfile.createDimension('latitude', 360)
        latitude = mynewncfile.createVariable('latitude', 'i', ('latitude', ))
        latitude[:] = np.arange(-89.75, 90, 0.5, float)
        latitude.units = 'degrees'

        # lastly do time
        mynewncfile.createDimension('time', 12)
        time = mynewncfile.createVariable('time', 'i', ('time', ))
        time[:] = dayssinceday2
        time.units = "Days since jan 1, 1900"

        # now that we've made the 3 dimensions of the box,
        # we can make the variable that will live in the box

        EVI = mynewncfile.createVariable('EVI', 'f4', ('time', 'latitude', 'longitude', ))
        EVI.missing_value = -0.3

        EVI._FillValue = -0.3

        EVI.units = 'unknown'
        EVI.valid_min = -0.2
        EVI.valid_max = 1

        # we have made the variable, now we stick the data in the variable
        EVI[:] = data

        # now we're done, yay, close the file so we don't mess it up
        mynewncfile.close()

        # tell the user that it worked:
        print('succesfully created new netcdf file called conv2_aehilla.nc')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'extracts raster data from zip files and turns into netcdf file')
    args = parser.parse_args()
    make_netcdf_from_ascii()
