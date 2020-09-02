import os
from GPSPhoto import gpsphoto
from geojson import Point, Feature, FeatureCollection, dumps
from cartopy.crs import EqualEarth, Geodetic
import matplotlib.pyplot as plt


def get_properties(geo_dict, file_name):
    properties = {'image': file_name}
    for key in geo_dict:
        if key == 'Longitude' or key == 'Latitude':
            continue
        property_name = key.lower()
        properties[property_name] = geo_dict[key]
    return properties


def save_geojson(image_directory, output_file):
    image_files = os.listdir(image_directory)
    features = []
    for file_name in image_files:
        file_path = os.path.join(image_directory, file_name)
        geo_data = gpsphoto.getGPSData(file_path)

        point = Point((geo_data['Longitude'], geo_data['Latitude']))
        properties = get_properties(geo_data, file_name)
        feature = Feature(geometry=point, properties=properties)
        features.append(feature)

    feature_collection = FeatureCollection(features)
    with open(output_file, 'w+') as file:
        file.write(dumps(feature_collection))

    return features


def save_plot(feature_list, pdf_path, png_path):
    ax = plt.axes(projection=EqualEarth())
    ax.stock_img()
    for feature in feature_list:
        lon, lat = feature['geometry']['coordinates']
        plt.plot(lon, lat, 'ro', markersize=3, markeredgecolor='k',
                 markeredgewidth=.6, transform=Geodetic())

    plt.text(-86, 31, 'Images\n1 and 6',
             horizontalalignment='right',
             transform=Geodetic())
    plt.text(2.5, 52, 'All other images',
             horizontalalignment='left',
             transform=Geodetic())

    plt.savefig(pdf_path)
    plt.savefig(png_path)


def main():
    photo_directory = 'photos'
    geojson_file = 'image_location.geojson'
    output_pdf = 'image_plot.pdf'
    output_png = 'image_plot.png'

    features = save_geojson(photo_directory, geojson_file)

    save_plot(features, output_pdf, output_png)


if __name__ == '__main__':
    main()
