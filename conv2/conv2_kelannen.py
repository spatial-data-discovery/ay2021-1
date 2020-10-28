import os
import numpy as np
import argparse
from datetime import date
from scipy.io import netcdf
from zipfile import ZipFile

def net_cdf(folder_path):
    file_paths = []
    for files in os.listdir(folder_path):
        if files[-4:] == '.zip':
            file_paths.append(files)
    
    if len(file_paths) == 0:
        print("No zip files found in ./data.")
        return
    
    file_data = []

    for file in file_paths:
        temp = []
        file_name = file[:-4]
        with ZipFile(os.path.join('data',file)) as zipF:
            zf = zipF.open(file_name)
            raster_text = zf.read().decode('UTF-8')
            #headers = raster_text.splitlines()[:6]
            body = raster_text.splitlines()[6:]
            for x in range(len(body)):
                rows = []
                split_body = body[x].split(' ')
                for y in range(len(split_body)):
                    pixel = int(split_body[y]) / 10000
                    rows.append(pixel)
                temp.append(rows)
            temp = np.flipud(np.asarray(temp))
            file_data.append(temp)
    file_data = np.asarray(file_data)


    num_days = []
    for i in range(12):
        temp = date(2006,i+1,1) - date(1900,1,1)
        num_days.append(temp.days)
    num_days = np.asarray(num_days)


    netcdf_path = os.path.join(folder_path,'conv2_kelannen.nc')
    nc_file = netcdf.netcdf_file(netcdf_path, 'w')


    nc_file.history = "Created %s" % date.today()
    nc_file.contact = 'Katherine E. Lannen (kelannen@email.wm.edu)'
    nc_file.title = 'Monthly global Enhanced Vegetation Indexes (EVI) at 0.5 degree resolution'
    nc_file.institution = 'College of William & Mary'
    nc_file.satellite = 'Terra'


    nc_file.createDimension('latitude', 360)
    nc_file.createDimension('longitude', 720)
    nc_file.createDimension('time', 12)

    latitude = nc_file.createVariable('latitude', 'f', ('latitude',))
    latitude.units = 'deg_North'
    latitude[:] = np.arange(-89.75,90,0.5,float)

    longitude = nc_file.createVariable('longitude', 'f', ('longitude',))
    longitude.units = 'deg_East'
    longitude[:] = np.arange(-179.75,180,0.5,float)

    time = nc_file.createVariable('time', 'i', ('time',))
    time.units = "days since 1900-01-01"
    time[:] = num_days


    evi = nc_file.createVariable('evi','f4',('time','latitude','longitude'))
    evi._FillValue = -0.3
    evi.missing_value = -0.3
    evi.units = 'unitless'
    evi.valid_min = -0.2
    evi.valid_max = 1
    evi[:] = file_data 


    nc_file.close()
    print("Finished creating ./data/conv2_kelannen.nc file from the zipped raster data.")
    return

if __name__ == "__main__":
    parser= argparse.ArgumentParser(description='Converts the raster data from the various zipped .asc files in ./data to a netCDF file in ./data/conv2_kelannen.nc')               
    args = parser.parse_args()

    folder_path = os.path.abspath('data')
    if os.path.isdir(folder_path):
        net_cdf(folder_path)
    else:
        print("data is not a valid subfolder from the current working directory.")
