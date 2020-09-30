import sys
import os
import csv
import json
from argparse import ArgumentParser

import h5py
import numpy as np
try:
    import requests
    imported_requests = True
except ImportError:
    imported_requests = False


def read_hdf(hdf_path):
    file = h5py.File(hdf_path, 'r')
    data = file['data']
    assign = data['assignment']

    attribute_dict = dict(assign.attrs.items())
    for key in attribute_dict:
        attribute_dict[key] = attribute_dict[key].decode('utf-8')

    shape = (int(attribute_dict['ncols']), int(attribute_dict['nrows']))

    np_array = np.empty(shape, dtype=int)
    assign.read_direct(np_array)

    return np_array, attribute_dict


def write_raster(array, headers, output_path):
    header_order = ('ncols', 'nrows', 'xllcorner', 'yllcorner', 'cellsize', 'NODATA_value')
    with open(output_path, 'w+') as out_file:
        writer = csv.writer(out_file, delimiter=' ', quoting=csv.QUOTE_MINIMAL)

        # Writes headers to file.
        for key in header_order:
            writer.writerow((key, headers[key]))

        # Writes data rows to file.
        for row in array:
            writer.writerow(row)


def print_location(headers):
    rows = int(headers['nrows'])
    cols = int(headers['ncols'])
    xll = float(headers['xllcorner'])
    yll = float(headers['yllcorner'])
    size = float(headers['cellsize'])

    lat = (yll, yll + size * rows)
    lon = (xll, xll + size * cols)
    mid_lat = (lat[0] + lat[1]) / 2
    mid_lon = (lon[0] + lon[1]) / 2

    if imported_requests:
        api_key = input('Enter your Google Maps Platform API key (press '
                        'enter if you would like to skip this step): ')
    else:
        api_key = None

    print('\nThis raster shows the area from latitude {:.3f} to {:.3f} and from'
          ' longitude {:.3f} to {:.3f}.'.format(lat[0], lat[1], lon[0], lon[1]))

    if api_key:
        town, state, country = get_geography(mid_lat, mid_lon, api_key)
        if town and state and country:
            print('This raster is centered around %s, %s in %s.' %
                  (town, state, country))
        elif state and country:
            print('This raster is centered around %s in %s.' %
                  (state, country))
        elif town and country:
            print('This raster is centered around %s in %s.' %
                  (town, country))
        elif country:
            print('This raster is centered around %s.' % country)
        else:
            print('Could not find geographic location for this raster.')


def get_geography(lat, lon, key):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    url += 'key=%s&latlng=%s,%s&sensor=false' % (key, lat, lon)

    response = requests.get(url)

    try:
        j = json.loads(response.text)
        components = j['results'][0]['address_components']
    except:
        return None, None, None

    country = state = town = None
    for c in components:
        if 'country' in c['types']:
            country = c['long_name']
        if 'administrative_area_level_1' in c['types']:
            state = c['long_name']
        if 'locality' in c['types']:
            town = c['long_name']

    return town, state, country


def requirements():
    package_list = ['h5py', 'numpy', 'requests']

    print('Required packages:')
    for package in package_list:
        print(package)

    sys.exit()


def api_help():
    print('1.  Create a new Google Cloud Platform project (see \n'
          '    https://cloud.google.com/resource-manager/docs/creating-managing-projects/ for help).\n'
          '2.  Go to https://developers.google.com/maps/documentation/embed/get-api-key\n'
          '    to find instructions on creating a Google API key.\n'
          '3.  Go to https://console.cloud.google.com/apis/library, search for "Geocoding API"\n'
          '    in the search bar, select the top result, and finally hit "Enable".')
    sys.exit()


def main():
    parser = ArgumentParser(description='Converts conv/data/test.hdf file to raster '
                                        'format and saves under conv/data/'
                                        'ben-ralston_raster.asc. Prints the location '
                                        'of the raster in latitude/longitude as well as '
                                        'city/state/country using Google\'s Geocoding API.')
    parser.add_argument('-r', '--requirements', action='store_true',
                        help='display all required packages and exit',
                        default=False)
    parser.add_argument('-a', '--api', action='store_true',
                        help='display instructions for creating Google '
                             'API key and exit',
                        default=False)

    args = parser.parse_args()
    if args.requirements:
        requirements()
    elif args.api:
        api_help()

    hdf_path = os.path.join('data', 'test.hdf')
    raster_path = os.path.join('data', 'ben-ralston_raster.asc')

    raster_array, attribute_dict = read_hdf(hdf_path)
    write_raster(raster_array, attribute_dict, raster_path)
    print_location(attribute_dict)


if __name__ == '__main__':
    main()
