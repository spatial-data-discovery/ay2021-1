# Amy Hilla and Caroline Freshcorn

# you have to have arcpy installed for this code to work
# the easiest way to run this is in an ArcPro notebook
# see: https://pro.arcgis.com/en/pro-app/arcpy/get-started/pro-notebooks.htm
# for info on how to use ArcPro notebooks

# import modules
import arcpy
import pandas as pd
from arcpy.sa import *

# set up your arcpy workspace
arcpy.env.workspace = r"C:\PrjWorkspace"

# set the filepaths to where your input files are located
red_asc_filepath = "../red.asc"
green_asc_filepath = "../green.asc"
blue_asc_filepath = "../blue.asc"

# set the filepath to your geodatabase (where your output will end up)
geodatabase_filepath = './sdc.gdb'

### Step 1: project the .asc files into rasters

# set the coordinate system to GCS_WGS_1984
coordinate_system = arcpy.SpatialReference(4326)

# project red.asc, green.asc, and blue.asc into GCS_WGS_1984
arcpy.ProjectRaster_management(red_asc_filepath , "red_raster_prj", out_coor_system = coordinate_system,\
                               resampling_type = "NEAREST", in_coor_system = coordinate_system)

arcpy.ProjectRaster_management(green_asc_filepath, "green_raster_prj", out_coor_system = coordinate_system,\
                              resampling_type = "NEAREST", in_coor_system = coordinate_system)

arcpy.ProjectRaster_management(blue_asc_filepath, "blue_raster_prj", out_coor_system = coordinate_system,\
                              resampling_type = "NEAREST", in_coor_system = coordinate_system)

### Step 2: combine the three projected rasters into a single raster layer

# make sure to save to your geodatabase
arcpy.MosaicToNewRaster_management("red_raster_prj; green_raster_prj; blue_raster_prj", geodatabase_filepath, 'mosaic2', coordinate_system_for_the_raster=coordinate_system, number_of_bands = 1)

### Step 3: fill in holes using Low Pass filter

output = Filter('mosaic2', filter_type = "LOW", ignore_nodata = "DATA")

# save to your geodatabase
output.save(geodatabase_filepath + '/mosaic_filtered')


# We think the output raster is an image of the Lena River Delta:
# we think this image is from:
# https://www.rawpixel.com/search/lena%20delta?sort=new&premium=free&freecc0=1&page=1
