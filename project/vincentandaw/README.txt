# README

* LAST UPDATED: 2020-11-13
* USERNAME: vincentandaw
* ORGANIZATION: spatial-data-discovery
* REPOSITORY: ay2021-1
* FOLDER: project/vincentandaw

#RUNNING THE SCRIPT#
The script can be run from the command line. This script will import the following modules: importlib, os, sys, glob and arcpy.
The last item on this list requires an ESRI ArcGIS Pro license, as well as the Spatial Analyst license. These two requirements will 
be checked by the script. 

#INPUT DATA#
Due to how large the original dataset is, I have included a folder called "Data" with all the inputs
necessary for the script to work. The data comes from http://earthenginepartners.appspot.com/science-2013-global-forest/download_v1.7.html

#OUTPUT DATA#
Script will output two adjacent rasters that make up Mesoamerica, each raster is a 10x10 degree swath/granule, one with the top left point at
20N 90W and the other at 20N 100W, at five different three-year time intervals. This creates a total of 10 rasters: 20N 90W raster at years 
2000-2003, 2004-2006, 2007-2009, 2010-2012, 2013-2015; and 20N 100W raster with similar time intervals. The output will also create ArcGIS Pro
helper files such as OVR files that help with pyramid generation for use within ArcGIS Pro

#CREATED VARIABLES#

*mask_20N90W = Hansen datamask for 20N90W read into arcpy as a raster
*mask_20N100W = Hansen datamask for 20N100W read into arcpy as a raster
*gain_20N90W = Hansen data on forest gained in 20N90W read into arcpy as a raster
*gain_20N100W = Hansen data on forest gained in 20N100W read into arcpy as a raster
*lossyr_20N90W = Hansen data on forest lost by year in 20N90W read into arcpy as a raster
*lossyr_20N100W = Hansen data on forest lost by year in 20N100W read into arcpy as a raster
*treecov_20N90W = Hansen gross tree cover in year 2000 in 20N90W read into arcpy as a raster
*treecov_20N100W = Hansen gross tree cover in year 2000 in 20N100W read into arcpy as a raster

*mask_1 = reclassify mask to only get value=1 i.e. forest (0=Nodata,2=permanent water bodies) in 20N90W
*mask_2 = reclassify mask to only get value=1 i.e. forest (0=Nodata,2=permanent water bodies) in 20N100W

*forcov_recl1 = reclassify forest cover: 1-70=0; 71-100=1. For 20N90W
*forcov_recl2 = reclassify forest cover: 1-70=0; 71-100=1. For 20N100W

*rc1_20N90W = raster calculator = forcov (0-1) - forloss (0 NO LOSS, 1-14 BY YEAR)
				range of raster: -14<r<1; 1 no loss, and other values refers to year at which forest was lost
*rc1_20N100W = raster calculator = forcov (0-1) - forloss (0 NO LOSS, 1-14 BY YEAR)
				range of raster: -14<r<1; 1 no loss, and other values refers to year at which forest was lost

*rc2_20N90W = raster calculator = rc1 + forestgain
*rc2_20N100W = raster calculator = rc1 + forestgain

*reclass_rc2_20N90W = Reclassify 2s to 1s to account for raster errors from Hansen dataset (Value of two can only be achieved by forest cover raster
						having value of 1 and forest gained also having a value of 1. Forest gain cannot be one if a forest is already there, by
						definition specified by Hansen et al.)
*reclass_rc2_20N100W = Reclassify 2s to 1s to account for raster errors from Hansen dataset

*rc3_20N90W = raster calculator: masking for only mapped surface area
*rc3_20N100W = raster calculator: masking for only mapped surface area


#CREDIT#
(written in format as described by the authors)

Hansen, M. C., P. V. Potapov, R. Moore, M. Hancher, S. A. Turubanova, A. Tyukavina, D. Thau, S. V. Stehman, S. J. Goetz, T. R. Loveland,
A. Kommareddy, A. Egorov, L. Chini, C. O. Justice, and J. R. G. Townshend. 2013. “High-Resolution Global Maps of 21st-Century Forest Cover Change.” 
Science 342 (15 November): 850–53. Data available online from: http://earthenginepartners.appspot.com/science-2013-global-forest.