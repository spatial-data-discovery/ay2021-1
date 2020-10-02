# IMPORT MODULES ##############################
import os

import numpy as np
import rasterio
from osgeo import osr, gdal
import argparse
from sklearn.impute import KNNImputer

# FUNCTIONS ####################################
def to_array(file):
    ''' 
    Adapted from hdf_write.py by Professor Davis
    Inputs:     - file: ASCII raster  
    Purpose: Converts ASCII raster into array
    '''
    rdat = np.array([], dtype="float")
    head = []
    nrows = 0
    ncols = 0
    with open(file) as f:
        head = [next(f) for x in range(7)]
        for line in f:
            nrows += 1
            tmp = line.strip().split()
            vals = [float(x) for x in tmp]
            ncols_temp = len(vals)
            ncols = ncols_temp
            rdat = np.append(rdat, vals)
    rdat.resize((nrows,ncols))
    return rdat

def nearest_neighbors(array,k,new_fp):
    '''
    Inputs:     - array: ASCII in array format
                - k: radius of neighbors
                - new_fp: name of output ASCII raster
    Purpose: Uses K Nearest Neighbors to impute missing cell values
    '''
    # Define imputer strategy
    imputer = KNNImputer(missing_values = -9999, n_neighbors = k)
    # Fit imputer to dataset and transform
    imputed_data = imputer.fit_transform(array)
    # Write new ASCII with no missing values
    with open(str(new_fp), "w") as asc:
        asc.write(
        'ncols 1600\n'+
        'nrows 1200\n'+
        'xllcenter 0\n'+
        'yllcenter 0\n'+
        'cellsize 0.0002\n'+
        'nodata_value -9999\n')
        for row in imputed_data:
            for item in row:
                asc.write((str(item))+' ')
            asc.write("\n")
    asc.close()

# MAIN ###########################################
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = "This script fills imputes the missing cell values of ASCII raster files. It converts the ASCIIs into geotiffs and stacks them into one multiband geotiff. All files output in working directory.")
    args = parser.parse_args()

    # RGB ASCII file paths
    red = 'red.asc'
    blue = 'blue.asc'
    green = 'green.asc'

    print('------- Starting imputation --------')

    # Convert to array
    blue_raster = to_array(blue)
    red_raster = to_array(red)
    green_raster = to_array(green)

    # KNN imputation
    nearest_neighbors(blue_raster,5,'blue_KNN_imputed.asc')
    nearest_neighbors(red_raster,5,'red_KNN_imputed.asc')
    nearest_neighbors(green_raster,5,'green_KNN_imputed.asc')

    filenames = ['red_KNN_imputed.asc','blue_KNN_imputed.asc','green_KNN_imputed.asc']
    print('Imputed ASCII rasters output into working directory: ', filenames)
    print('------- Imputation Complete --------')
    
    # Convert ASCIIs to geoTIFFs
    # from https://gis.stackexchange.com/questions/42584/how-to-call-gdal-translate-from-python-code
    print('\n------- Converting ASCII to geoTIFF --------')
    band_files = ['red.tif','blue.tif','green.tif']
    for i in range(len(filenames)):
        source = gdal.Open(filenames[i])
        dest = band_files[i]
        driver = gdal.GetDriverByName('GTiff')
        dst_ds = driver.CreateCopy(dest,source,0)
        source = None
        dest = None
    print('GeoTiffs output in working directory: ',band_files)
    print('------- Conversion Complete --------')
    
    # Combine geoTIFFs into one raster
    # from https://gis.stackexchange.com/questions/223910/using-rasterio-or-gdal-to-stack-multiple-bands-without-using-subprocess-commands
    print('\n------- Generating Multispectral geoTIFF --------')
    outvrt = 'multispec_raster.vrt'
    outtif = 'multispec_raster.tif'
    outds = gdal.BuildVRT(outvrt, band_files, separate=True)
    outds = gdal.Translate(outtif, outds)
    
    print('Multispectral GeoTIFF %s output in working directory\n' % outtif)
    print('------- Multispectral geoTIFF Complete --------')
    print('Raster is located on Lena Delta, Sakha Republic of Siberia, Russia')
    
