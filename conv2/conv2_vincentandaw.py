###############################################################################
# IMPORT MODULES
###############################################################################

import zipfile, os, numpy as np, datetime, argparse
from scipy.io import netcdf

##############################################################################
# GLOBAL VARIABLES:
##############################################################################
ERROR_VAL = -0.3 #3000 (nodata from ASC) / 10000 (EVI scaling factor)

###############################################################################
# FUNCTIONS
###############################################################################
def netcdf_maker():
    #Locate data folder
    os.chdir(r'data')

    #unzip files
    files_to_unzip = []
    for file in os.listdir(os.getcwd()):
        if file.endswith('.zip'):
            files_to_unzip.append(file)

    if len(files_to_unzip) == 0: #Error catcher
        print('no data to unzip. please add zip files')
    else:
        for file in files_to_unzip:
            file_name = os.path.abspath(file)
            with zipfile.ZipFile(file_name,'r') as zip:
                zip.extractall()

    #take raster data 
    point_data = []
    for file in os.listdir(os.getcwd()):
        if file.endswith('.txt'):
            raw_grid = np.loadtxt(file,skiprows=6) #skips first 6 formatting rows
            grid = raw_grid.astype(float) #checks numeric status here.
            container.append(grid/10000) #rescaled to divide by 10000 for -0.3<EVI<10
    raster_slices = np.flipud(np.asarray(point_data)) 
    #flipped for correct visualization: ASC and latitude now start at same side (southernmost)
    
    
    ### Create a new NetCDF file ###

    my_file = "test_vince.nc"
    nc_path = os.path.join(".", my_file)
    f = netcdf.netcdf_file(nc_path, 'w')


    # Write file attributes:
    f.history = "created %s" % datetime.date.today()
    f.contact = 'Jonathan Vincent Tandaw (jvtandaw@email.wm.edu)'
    f.title = 'Monthly global Enhanced Vegetation Indexes (EVI) at 0.5 degree resolution'
    f.satelite = 'Terra'
    f.institution = 'William & Mary'

    # Create lon
    f.createDimension('longitude', 720) #720 represents 720 pixels 
    longitude = f.createVariable('longitude', 'f4', ('longitude',) ) #f4=32bit floating point
    longitude[:] = np.arange(-179.75, 180, 0.5) 
    longitude.units = 'degrees_east'

    # Create lat
    f.createDimension('latitude', 360) #360 represents 360 pixels 
    latitude = f.createVariable('latitude', 'f4', ('latitude',))
    latitude[:] = np.arange(-89.75, 90, 0.5) #Thanks Professor, would not have figured this out without hints!
    latitude.units = 'degrees_north'

    # Create time
    time_list = [(datetime.datetime(2006,1+i,1) - datetime.datetime(1900,1,1)).days for i in range(0,12)]
    time_array = np.asarray(time_list)

    f.createDimension('time', 12) #it's monthly data
    time = f.createVariable('time', 'i', ('time',))
    time[:] = time_array
    time.units = 'days since 1900-01-01'
    
    #Create EVI: Composite of time, lat, lon 
    evi = f.createVariable('evi', 'f4', ('time','latitude','longitude'))
    evi._FillValue = ERROR_VAL
    evi.missing_value = ERROR_VAL
    evi.long_name = 'Enhanced Vegetation Index with lat, long and time'
    evi.units = 'unitless'
    evi.valid_min = -0.2
    evi.valid_max = 10
    evi[:] = raster_slices

    f.close()
    print('NetCDF file created successfully!')
    return


###############################################################################
# MAIN
###############################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='takes in twelve asc files and puts them in a netCDF file')
    args = parser.parse_args() #no arguments are taken, so no help option necessary
    netcdf_maker()