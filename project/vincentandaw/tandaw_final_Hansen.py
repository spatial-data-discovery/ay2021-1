#!/usr/bin/env python3

# Author: Vincent Tandaw
# Last Updated: November 21, 2020

# Script Description:
# Creates rasters that show forest loss by year in Mesoamerica from Hansen et al dataset

import importlib
import os
import sys
import glob
import argparse

print('Checking for ArcPy installation')
check_for_arcpy = importlib.util.find_spec("arcpy") 
found = check_for_arcpy is not None 
if found == True: #ensures arcpy exists BEFORE importing, or else code breaks
    import arcpy 
    from arcpy import sa
    print('Checking for ArcPy installation. ArcPy found.')
else:
    print('ArcPy is unavailable and required for this script. Is this an activated' \
          'ArcGIS Pro environment? If not, please activate and try again.')
    sys.exit()


def hansen_mesoamerica():
    """
    Creates temporal forest cover rasters of Mesoamerica from Hansen et al dataset
    
    Hansen et al. forest cover data is a very useful dataset for conservationists as
    it provides rasters on forest cover, forest gained, forest lost, and other useful
    spatial data. This function will take gross forest cover, subtract it with forest
    lost, add forest gained, and multiplied by a binary mask showing mappable land 
    surfaces to create approximate forest loss rasters of Mesoamerican forests. 
    Rasters produced will be clumped into three-year chunks: 2001-2003, 
    2004-2006...2012-2015 to better show change/loss of forest cover, as year-on-year
    change is relatively small and indistinguishable on a larger scale.
    
    Credit, written in format as described by the authors:
    Hansen, M. C., P. V. Potapov, R. Moore, M. Hancher, S. A. Turubanova, A. Tyukavina, 
    D. Thau, S. V. Stehman, S. J. Goetz, T. R. Loveland, A. Kommareddy, A. Egorov, 
    L. Chini, C. O. Justice, and J. R. G. Townshend. 2013. 
    “High-Resolution Global Maps of 21st-Century Forest Cover Change.” 
    Science 342 (15 November): 850–53. 
    Data available online from: 
    http://earthenginepartners.appspot.com/science-2013-global-forest.
    """

    MAKE_FOLDER_ALLOWED = True
    
    try:
        print('Checking for Spatial Analyst license')
        if arcpy.CheckExtension("Spatial") == "Available": #also needs Spatial Analyst
            arcpy.CheckOutExtension("Spatial") 
        else:
            print('Checking for Spatial Analyst license. Unavailable. Exiting...')
            sys.exit()
        print('Checking for Spatial Analyst license. License found')
        print('Finding raster data sources...')

        ###SET ARCPY ENVIRONMENT PARAMETERS###
        arcpy.env.overwriteOutput = True
        arcpy.env.extent = "MAXOF"

        ###DATA SOURCES###
        file_location = os.path.join('data','*.tif') #Data folder is provided by me
        data = sorted(glob.glob(file_location)) #sorted uses timsort, a Insertion Sort-and
                                                #Merge Sort hybrid for python use. 

        mask_20N90W = arcpy.Raster(data[0])
        mask_20N100W = arcpy.Raster(data[1])
        gain_20N90W = arcpy.Raster(data[2])
        gain_20N100W = arcpy.Raster(data[3])
        lossyr_20N90W = arcpy.Raster(data[4])
        lossyr_20N100W = arcpy.Raster(data[5])
        treecov_20N90W = arcpy.Raster(data[6])
        treecov_20N100W = arcpy.Raster(data[7])

        print('Raster data found! Building rasters. This may take a while...')

        ###ANALYSIS###
        #make output folder if not exists but allowed. EAFP!
        try:
            if not os.path.exists('Output'):
                os.mkdir('Output')
        except OSERROR as e:
            if e.errno==errno.EEXIST:
                MAKE_FOLDER_ALLOWED = False
        
        #reclassify mask to only get value=1 i.e. forest (0=Nodata,2=permanent water bodies)
        remap = sa.RemapValue([[0,"NODATA"],[1,1],[2,"NODATA"]])
        mask_1 = sa.Reclassify(mask_20N90W, 'value', remap, "NODATA")
        mask_2 = sa.Reclassify(mask_20N100W,'value',remap,"NODATA")

        #reclassify forest cover: 1-70=0; 71-100=1
        remap = sa.RemapRange([[1,70,0],[71,100,1]])

        forcov_recl1 = sa.Reclassify(treecov_20N90W, 'value', remap, "NODATA")
        forcov_recl2 = sa.Reclassify(treecov_20N100W,'value',remap,"NODATA")

        #raster calculator = forcov (0-1) - forloss (0 NO LOSS, 1-14 BY YEAR)
        #range: -14<r<1; 1 no loss, and other values refers to year at which forest was lost
        rc1_20N90W = sa.RasterCalculator([forcov_recl1, lossyr_20N90W],
                                         ['rc','ly'],'rc-ly')
        rc1_20N100W = sa.RasterCalculator([forcov_recl2, lossyr_20N100W],
                                          ['rc','ly'],'rc-ly')

        #raster calculator = rc1 + forestgain
        rc2_20N90W = sa.RasterCalculator([rc1_20N90W, gain_20N90W],
                                         ['f','g'],'f+g')
        rc2_20N100W = sa.RasterCalculator([rc1_20N100W, gain_20N100W],
                                          ['f2','g2'],'f2+g2')

        #Reclassify 2s to 1s to account for raster errors
        reclass_rc2_20N90W = sa.Reclassify(rc2_20N90W,'value',
                                           sa.RemapValue([[2,1]]))
        reclass_rc2_20N100W = sa.Reclassify(rc2_20N100W,'value',
                                            sa.RemapValue([[2,1]]))

        #raster calculator: masking for only mapped surface area
        rc3_20N90W = sa.RasterCalculator([reclass_rc2_20N90W,mask_1],
                                         ['rc2','mask'],'rc2*mask')
        rc3_20N100W = sa.RasterCalculator([reclass_rc2_20N100W,mask_2],
                                          ['rc2','mask'],'rc2*mask')

        #reclass values from raster calculator output to add meaning
        remap = sa.RemapValue([[1,0],[0,2001],[-1,2002],[-2,2003],[-3,2004],[-4,2005],
                               [-5,2006],[-6,2007],[-7,2008],[-8,2009],[-9,2010],
                               [-10,2011],[-11,2012],[-12,2013],[-13,2014],[-14,2015]])

        recl_rc3_20N90W = sa.Reclassify(rc3_20N90W, 'value',remap,"NODATA")
        recl_rc3_20N100W = sa.Reclassify(rc3_20N100W,'value',remap,"NODATA")

        if MAKE_FOLDER_ALLOWED == True:
            recl_rc3_20N90W.save(r'./Output/TreeLoss_20N90W.tif')
            recl_rc3_20N100W.save(r'./Output/TreeLoss_20N100W.tif')
        else:
            recl_rc3_20N90W.save(r'./TreeLoss_20N90W.tif')
            recl_rc3_20N100W.save(r'./TreeLoss_20N100W.tif')

        return 'done!'
    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))
    finally:
        arcpy.CheckInExtension("Spatial")
    

if __name__=='__main__':
    parser = argparse.ArgumentParser(description=
                'Creates approximate tree cover rasters from Hansen dataset of 20N90W' \
                ' and 20N100W swaths from 2000-2015')
    args = parser.parse_args()

    user_warning = input(
        'This may take a substantial amount: some 30min and 280mb. ' \
        'Proceed? y/n \n')
    if user_warning.lower() in ['yes','y']:
        hansen_mesoamerica()
        print('Done. Check output in generated Output folder if allowed. ' \
              'Output raster is in tif format')
    else:
        sys.exit()
