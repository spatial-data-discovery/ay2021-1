### NetCDF processing script
### Amy Hilla
### Spatial Data Discovery, Fall 2020

### Summary: this script automates the pre-processing of monthly netCDF rainfall data,
to create raster files of rainfall in the US on each election day

## NOTE: this script must be run within ArcGIS Pro for arcpy to import successfully

import pandas as pd
import arcpy
from arcpy.sa import *
from arcpy.ia import *
from arcpy.mp import *
import glob
import os
import traceback

# Set the workspace environment to local file geodatabase
arcpy.env.workspace = "final_project.gdb"

# set locations of input files
elexdates = pd.read_csv(r"us_elex_dates_test2.csv")
usaboundary =  r"geoboundariesSSCGS-3_0_0-USA-ADM0.shp"
files = glob.glob(r".\WFDEI_files\Rainf_daily_WFDEI_CRU*.nc")

# set location for where output files will be saved:
output_geodatabase = r"final_project.gdb"

# set up the files to be used in the loop
list_of_files = []
files.sort(reverse = True) # sorts the files in order
for f in files:
    list_of_files.append(f)

try:

    elex_index = -1
    for file in list_of_files:
        # reads in each file, and pulls the appropriate date from the elexdates file
        elex_index = elex_index + 1
        elex_year = int(elex['year'][elex_index])
        elex_day = elex['day'][elex_index]
        inNetCDFFile = file
        new_raster_layer_name = "rainfall" + str(elex_year)

        # tell the user what year is being processed:
        print('working on ' + str(elex_year) + ', filename: ' + str(file))

        # convert the netCDF to a Raster Layer:
        variable = "Rainf"
        XDimension = "lon"
        YDimension = "lat"
        outRasterLayer = new_raster_layer_name
        bandDimmension = ""
            # this line selects the correct day from the netCDF file (which contains data for the full month):
        dimensionValues = [["tstep", int(elex_day)]]
        valueSelectionMethod = ""
        cellRegistration = ""

        rainfall = arcpy.MakeNetCDFRasterLayer_md(inNetCDFFile, variable, XDimension, YDimension,
                                       outRasterLayer, bandDimmension, dimensionValues,
                                       valueSelectionMethod, cellRegistration)

        # project raster to WGS 84
        in_raster = rainfall
        out_raster_filename = new_raster_layer_name+'prj'
        out_raster = str(output_geodatabase) + '\\' + out_raster_filename
        out_coor_system = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"
        resampling_type = "NEAREST"
        cell_size = "0.5 0.5"
        geographic_transform = ""
        Registration_Point = ""
        in_coor_system = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"
        vertical = "NO_VERTICAL"

        rainfall_prj = arcpy.ProjectRaster_management(in_raster, out_raster,
                                       out_coor_system,
                                       resampling_type,
                                       cell_size,
                                       geographic_transform,
                                       Registration_Point,
                                       in_coor_system, vertical)

        # use extract by mask to limit the extent of the raster to just the USA
        rainfall_extracted = arcpy.sa.ExtractByMask(rainfall_prj, usaboundary)

        # convert raster layer to ascii file and save to local directory
        asc_filename = new_raster_layer_name + '.asc'
        arcpy.RasterToASCII_conversion(rainfall_extracted, asc_filename)

        # also save the original raster layer to the geodatabase
        extract_filename = new_raster_layer_name + 'ext'
        extract_path = str(output_geodatabase) + '\\' + extract_filename
        rainfall_extracted.save(extract_path)

        # tell the user this file has been saved:
        print("successfully created rainfall raster for " + str(elex_year) + " saved as: " + str(extract_filename) + " and " + asc_filename)

# error handling:
except Exception as e:
    print(e)
    print(traceback.print_exc())
    conn.rollback()
