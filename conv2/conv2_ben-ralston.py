import os
import zipfile
import datetime

from scipy.io import netcdf


def read_all_rasters():
    directory = 'data'
    zip_template = 'MODIS_0.5rs-Raster_2006-%02d-01.txt.zip'

    # This is a list of tuples in the format (matrix, headers), where
    # matrix is a two-dimensional array and headers is a dictionary
    # storing the raster headers.
    rasters = []

    for i in range(1, 13):
        zip_name = os.path.join(directory, zip_template % i)
        unzip_name = zip_name[:-4]

        with zipfile.ZipFile(zip_name, 'r') as zipped:
            zipped.extractall(directory)

        matrix, headers = read_raster(unzip_name)
        rasters.append((matrix, headers))

    return rasters


def read_raster(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    headers = {}
    matrix = []
    for i, line in enumerate(lines):
        if i < 6:
            name, value = line.strip().split()
            headers[name] = value

        else:
            split_line = line.strip().split()
            split_line = list(map(int, split_line))
            matrix.append(split_line)

    for key in headers:
        if key in ['NCOLS', 'NROWS']:
            headers[key] = int(headers[key])
        else:
            headers[key] = float(headers[key])

    return matrix, headers


def nc_history():
    creation_str = 'created %s' % datetime.date.today()
    return creation_str


def get_long_lat(headers):
    nrows = headers['NROWS']
    ncols = headers['NCOLS']
    xll = headers['XLLCORNER']
    yll = headers['YLLCORNER']
    size = headers['CELLSIZE']

    base_long = xll + size / 2
    longitude = [base_long + i * size for i in range(ncols)]

    base_lat = yll + size / 2
    latitude = [base_lat + i * size for i in range(nrows)]

    # Need to reverse the order of latitude array because the lower
    # left Y cell is at the bottom of the raster.
    latitude = latitude[::-1]

    return longitude, latitude


def get_time_array():
    date_template = '2006-%02d-01'
    days_since_array = []

    for i in range(1, 13):
        date = date_template % i
        days_since_array.append(get_days_since_1900(date))

    return days_since_array


def get_days_since_1900(date):
    # date parameter is in 'YYYY-MM-DD' string format
    start_date = datetime.date(1900, 1, 1)
    dt_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

    delta = dt_date - start_date
    return delta.days


def combine_rasters(rasters):
    all_rasters = []

    for i in range(12):
        raster = rasters[i][0]
        new_raster = []
        for row in raster:
            adjusted_row = list(map(lambda x: x / 10000, row))
            new_raster.append(adjusted_row)
        all_rasters.append(new_raster)

    return all_rasters


def make_netcdf(rasters):
    filename = 'data/ben-ralston_NETCDF.nc'
    net_file = netcdf.netcdf_file(filename, 'w')

    # Set file attributes:
    net_file.history = nc_history()
    net_file.contact = 'Ben Ralston (bjralston@email.wm.edu)'
    net_file.institution = 'William & Mary'
    net_file.title = 'Monthly global Enhanced Vegetation Indexes (EVI) at 0.5 degree resolution'
    net_file.satellite = 'Terra'

    # Make arrays to fill dimensions/variables with data:
    long_array, lat_array = get_long_lat(rasters[0][1])
    time_array = get_time_array()
    evi_array = combine_rasters(rasters)

    # Calculate adjusted NO_DATA value:
    no_data_value = rasters[0][1]['NODATA_VALUE'] / 10000

    # Make dimensions and variables:
    net_file.createDimension('longitude', rasters[0][1]['NCOLS'])
    longitude = net_file.createVariable('longitude', 'f', ('longitude',))
    longitude[:] = long_array
    longitude.units = 'deg_East'

    net_file.createDimension('latitude', rasters[0][1]['NROWS'])
    latitude = net_file.createVariable('latitude', 'f', ('latitude',))
    latitude[:] = lat_array
    latitude.units = 'deg_North'

    net_file.createDimension('time', 12)
    time = net_file.createVariable('time', 'i', ('time',))
    time[:] = time_array
    time.units = 'days since 1900-01-01'

    evi = net_file.createVariable('evi', 'f', ('time', 'latitude', 'longitude'))
    evi.units = 'unitless'
    evi._FillValue = no_data_value
    evi.missing_value = no_data_value
    evi.valid_min = -0.2
    evi.valid_max = 1

    evi[:] = evi_array

    net_file.close()


def main():
    rasters = read_all_rasters()
    make_netcdf(rasters)


if __name__ == '__main__':
    main()
