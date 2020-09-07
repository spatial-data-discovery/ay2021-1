from GPSPhoto import gpsphoto 
from geojson import Point, Feature, FeatureCollection, dump
import os
import geopandas as gpd
import descartes
import matplotlib.pyplot as plt

def get_meta_json(photo_dir, filenames):
    '''
    Purpose: generates geojson file with metadata from photos
    photo_dir: path to photos
    filenames: names of photos 
    returns: path to geojson
    '''
    features = []
    for name in filenames:
        path = os.path.join(photo_dir, name)
        geo = gpsphoto.getGPSData(path)
        geo['image'] = name   
        lalong = Point((geo['Longitude'],geo['Latitude']))
        feat = Feature(geometry=lalong, properties=geo)
        features.append(feat)
    feat_col = FeatureCollection(features)
    geojson_path = 'image_locations.geojson'
    with open(geojson_path,'w') as f:
        dump(feat_col,f)
    return geojson_path

def plot_gjson(geojson_path,output):
    '''
    Purpose: generate map in .png format
    geojson_path: path to geojson file
    output: name of png
    '''
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    gdf = gpd.read_file(geojson_path)
    ax = world[world.continent!='Antarctica'].plot(color='lightgrey',edgecolor='black',figsize=(20,20))
    gdf.plot(ax=ax,color='red')
    ax.set_title('Image Locations',fontdict={'fontsize':30})
    plt.savefig(output,bbox_inches='tight')
    
def main():
    photo_dir = 'photos'
    filenames = os.listdir(photo_dir)
    gjson_file = get_meta_json(photo_dir,filenames)
    print('----- Plotting image locations -----')
    plot_gjson(gjson_file,'image_map.png')
    print('----- Plot generated! -----')

if __name__ == '__main__':
    main()