# Author: Vincent Tandaw
# Last Updated: November 20, 2020

# Script Description:
# Creates temporal forest cover rasters of Mesoamerica from Hansen et al dataset

import importlib
import os
import sys
import glob
import argparse

def hansen_mesoamerica():
    """
    Creates temporal forest cover rasters of Mesoamerica from Hansen et al dataset
    
    Hansen et al. forest cover data is a very useful dataset for conservationists as
    it provides rasters on forest cover, forest gained, forest lost, and other useful
    spatial data. This function will take gross forest cover, subtract it with forest
    lost, add forest gained, and multiplied by a binary mask showing mappable land 
    surfaces to create approximate forest cover rasters of Mesoamerican forests. 
    Rasters produced will be clumped into three-year chunks: 2001-2003, 
    2004-2006...2012-2015 to better show change of forest cover, as year-on-year change
    is relatively small and indistinguishable on a larger scale.
    
    Credit, written in format as described by the authors:
    Hansen, M. C., P. V. Potapov, R. Moore, M. Hancher, S. A. Turubanova, A. Tyukavina, 
    D. Thau, S. V. Stehman, S. J. Goetz, T. R. Loveland, A. Kommareddy, A. Egorov, 
    L. Chini, C. O. Justice, and J. R. G. Townshend. 2013. 
    “High-Resolution Global Maps of 21st-Century Forest Cover Change.” 
    Science 342 (15 November): 850–53. 
    Data available online from: 
    http://earthenginepartners.appspot.com/science-2013-global-forest.
    """

    check_for_arcpy = importlib.util.find_spec("arcpy") 
    found = check_for_arcpy is not None 
    if found == True: #ensures arcpy exists BEFORE importing, or else code breaks
        import arcpy 
        from arcpy import sa
    else:
        return 'ArcPy is unavailable and required for this script. Exiting script.'
    
    try:
        if arcpy.CheckExtension("Spatial") == "Available": #also needs Spatial Analyst
            arcpy.CheckOutExtension("Spatial") 
        else:
            return 'The Spatial Analyst license is unavailable. Exiting script.'

        print('finding data sources...')

        ###SET ARCPY ENVIRONMENT PARAMETERS###
        arcpy.env.overwriteOutput = True
        arcpy.env.extent = "MAXOF"

        ###DATA SOURCES###
        file_location = os.path.join('data','*.tif') #Data folder is provided by me
        data = glob.glob(file_location)

        mask_20N90W = arcpy.Raster(data[0])
        mask_20N100W = arcpy.Raster(data[1])
        gain_20N90W = arcpy.Raster(data[2])
        gain_20N100W = arcpy.Raster(data[3])
        lossyr_20N90W = arcpy.Raster(data[4])
        lossyr_20N100W = arcpy.Raster(data[5])
        treecov_20N90W = arcpy.Raster(data[6])
        treecov_20N100W = arcpy.Raster(data[7])

        print('building rasters. this will take a while...')

        ###ANALYSIS###
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

        #Extract by Attrs by three years + no loss aka starting point
        #-2 to 0, -5 to -3, -8 to -6... is 2001-2003, 2004-2006, 2007-2009...

        raster_list = [(rc3_20N90W, data[0][-12:]), (rc3_20N100W, data[1][-12:-4])]
        expression = [("VALUE>=-2 AND VALUE<=0","01-03"),("VALUE>=-5 AND VALUE<=-3", "04-06"),
                      ("VALUE>=-8 AND VALUE<=-6","07-09"),("VALUE>=-11 AND VALUE<=-9","10-12"),
                      ("VALUE>=-14 AND VALUE<=-11","13-15")]
        for ras in raster_list:
            for exp in expression:
                attExtract = sa.ExtractByAttributes(ras[0], exp[0])
                RasAsASCII =  arcpy.RasterToASCII_conversion(attExtract, f'.//{ras[1]}_{exp[1]}.asc')
        return 'done!'
    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))
    finally:
        arcpy.CheckInExtension("Spatial")
    

if __name__=='__main__':
    parser = argparse.ArgumentParser(description=
                'Creates approximate tree cover rasters from Hansen dataset of 20N90W and 20N100W' \
                'swaths from 2000-2015')
    args = parser.parse_args()

    print('please change python environment to ArcGIS Pro environment')

    user_warning = input(
        'This will take a substantial amount (up to an hour) of time and space (about 90-93GB). ' \
        'Type yes to confirm and continue')
    if user_warning.lower() == 'yes':
        hansen_mesoamerica()
        print('Done. Check the directory in which this script is located')
    else:
        sys.exit()
