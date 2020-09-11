#This script reads in a file path to a folder of images and returns a GeoJSON file with the coordinates of where the images were taken.


from GPSPhoto import gpsphoto
import os
import exifread
from geojson import Point, Feature, FeatureCollection, dump




#Function that extracts the longitutde and latittude of the photos, input is a string path to the images
#Returns the geojson file
def extract_data(path, image_titles):


    image_features = []
    for title in image_titles:
        full_path = os.path.join(path, title)
        image_data = gpsphoto.getGPSData(full_path)
        image_data['image'] = title

        image_point = Point((image_data['Longitude'], image_data['Latitude']))
        image_feat = Feature(geometry=image_point, properties=image_data)
        image_features.append(image_feat)

    geojson_data = FeatureCollection(image_features)
    geojson_file = 'images.geojson'
    with open(geojson_file, 'w') as d:
        dump(geojson_data, d)



    return geojson_file


if __name__ == "__main__":

    path = input("Enter the abosolute filepath to the folder of images: ")
    image_titles = os.listdir(path)

    extract_data(path, image_titles)
