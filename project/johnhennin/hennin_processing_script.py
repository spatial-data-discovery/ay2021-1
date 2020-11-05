# Author: John Hennin
# Last Updated: 2020-11-05

# Script Description:
# This script reads all GeoTIFF files in the local directory and produces new ASCII raster files with the same data, as well as complementary PRJ files

import rasterio
import os


for file in os.listdir("."):
    # Check for tif files in local directory
    if file[-3:] == "tif":
        with rasterio.open(file) as tif:

            # Save ASCII raster header and PRJ file features
            arraydata = tif.read(tif.indexes[0])
            ncols = tif.width
            nrows = tif.height
            crs = tif.crs
            xllcorner, yllcorner = tif.transform * (0,tif.height)
            cellsize = ((tif.transform[0]))*(-(tif.transform[4]))
            prjinfo = crs.wkt

        # Write header information and data in new ASCII raster file of same name as original GeoTIFF
        with open(file[:-4]+".asc","w+") as ascfile:
            ascfile.write("ncols " + str(ncols) + '\n' + "nrows " + str(nrows) + '\n' + "xllcorner " + str(xllcorner) + '\n' + "yllcorner " + str(yllcorner) + '\n' + "cellsize " + str(cellsize) + '\n')
            for line in arraydata:
                for pixel in line:
                    ascfile.write(str(pixel) + " ")
                ascfile.write("\n")

        # Write PRJ information in new PRJ file of same name as original GeoTIFF
        with open(file[:-4]+".prj","w+") as prjfile:
            prjfile.write(prjinfo)
