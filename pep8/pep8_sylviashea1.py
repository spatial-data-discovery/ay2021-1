#! /usr/bin/env python

# pep8_sylviashea1.py

# By: Sylvia Shea

# Version 1.0

# Last Edit: 2020-11-05

# Purpose: This script extracts the metadata from a
# collection of images and puts it into a geojson. 
# It plots the locations on a map as a .png and
# outputs it to the working directory.

###########################################################
# REQUIRED MODULES
###########################################################
import sys
import os

import geopandas as gpd
import descartes
import matplotlib.pyplot as plt
from GPSPhoto import gpsphoto 
from geojson import Point, Feature, FeatureCollection, dump
import argparse

###########################################################
# FUNCTIONS
###########################################################
def get_meta_json(photo_dir, file_names):
    """
    Name:     get_meta_json
    Inputs:   - str, photo directory (photo_dir)
              - str, file names (file_names)
    Outputs:  Path to single geojson (geojson_path)
    Features: Generates geojson file with metadata from photos.
    """
    features = []
    for name in file_names:
        path = os.path.join(photo_dir, name)
        # Get photo metadata dictionary 
        geo = gpsphoto.getGPSData(path)
        geo['image'] = name 
        # Extract coordinates from metadata dictionary  
        coords = Point((geo['Longitude'],geo['Latitude']))
        image_loc = Feature(geometry=coords, properties=geo)
        features.append(image_loc)
    # Create geoJSON with image names and coordinates
    feat_collection = FeatureCollection(features)
    geojson_path = 'image_locations.geojson'
    with open(geojson_path,'w') as f:
        dump(feat_collection,f)
    return geojson_path

def plot_gjson(geojson_path,output):
    '''
    Name:     plot_gjson
    Inputs:   - str, path to geojson (geojson_path)
              - str, map name (output)
    Outputs:  .png image
    Features: Generate map with photo locations in .png format.
    geojson_path: path to geojson file
    output: name of png
    '''
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    gdf = gpd.read_file(geojson_path)
    ax = world[world.continent!='Antarctica'].plot(color='lightgrey',
                                                   edgecolor='black',
                                                   figsize=(20,20))
    gdf.plot(ax=ax,color='red')
    ax.set_title('Image Locations',fontdict={'fontsize':30})
    plt.savefig(output,bbox_inches='tight')

def main():
    sys.stdout.write('Please input the path to folder with photos.')
    sys.stdout.write('Ensure folder is located in working directory.')
    sys.stdout.write('\n---------------------\n')
    photo_dir = input()
    try:
        filenames = os.listdir(photo_dir)
    except FileNotFoundError:
        print('Photo directory not found. Please check path and try again.')
        sys.exit()
    gjson_file = get_meta_json(photo_dir,filenames)
    sys.stdout.write('Input name of map.')
    sys.stdout.write('\n---------------------\n')
    map_name = str(input())
    print('----- Plotting image locations -----')
    plot_gjson(gjson_file,map_name)
    print('----- Plot generated and located in working directory -----')

###########################################################
# MAIN
###########################################################
if __name__ == '__main__':
    descrip = (
        'This script extracts the metadata from photos (located in a\n'
        'subfolder of the working directory) and plots their locations\n'
        'on a map. The map is output as a .png and located in the working\n'
        'directory.'
    )
    parse = argparse.ArgumentParser(description=descrip)
    args = parse.parse_args()
    main()