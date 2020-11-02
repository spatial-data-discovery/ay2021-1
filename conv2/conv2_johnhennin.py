#Modules
import zipfile
import os
import sys
import datetime
from datetime import date
import numpy as np
from scipy.io import netcdf
import argparse

#Main

if __name__ == "__main__":
    parser= argparse.ArgumentParser(description="This script pulls zipfiles of ASCII raster data from the 'data' file to create a new netCDF file in classic format with 3 dimensions (time, latitude, and longitude) and 4 variables (time, latitude, longitude, and EVI).")
    args = parser.parse_args()

    #Find zip files
    files=[]
    for file in os.listdir("data"):
        if file[-4:]==".zip":
            files.append(file)
    files.sort()
    if len(files)>0:
        print("Found "+str(len(files))+" files. Now opening files and extracting data.")
    else:
        print("ERROR: Could not find zip files. Please try again")
        sys.exit()

    #Open files and extract data
    totaldata=[]
    dates=[]
    for zfile in files:
        rasterdata = []
        file=zfile[:-4]
        with zipfile.ZipFile("data/"+zfile) as zfile:
            with zfile.open(file) as rast:
                text=rast.read()
                text=text.decode('UTF-8')
                #Save heading information
                heading=text.splitlines()[0:6]
                #Separate data from heading
                text2=text.splitlines()[6:]
                for i in range(len(text2)):
                    linel=[]
                    rng=text2[i].split(" ")
                    for p in range(len(rng)):
                        pixel=rng[p]
                        #Ensures pixels fit within EVI bounds
                        if ((int(pixel)/10000)<-0.2 and (int(pixel)/10000)!=-0.3) or ((int(pixel)/10000)>1):
                            print("ERROR: Found EVI value that doesn't fit within specified bounds."+' Check file: "'+file+'" and try again.')
                            sys.exit()
                        #Appends pixel in list representing one line
                        linel.append(int(pixel)/10000)
                    #Appends list representing one line in list representing entire raster
                    rasterdata.append(linel)
                rasterdata=np.asarray(rasterdata)
                rasterdata=np.flipud(rasterdata)
                totaldata.append(rasterdata)
    totaldata=np.asarray(totaldata)

    print("Data compiled into single array. Creating netCDF file now.")

    #Days since
    days=[]
    for i in range(0,12):
        days.append((date(2006,i+1,1)-date(1900,1,1)).days)
    days=np.asarray(days)

    #Create netCDF file
    f=netcdf.netcdf_file("data/conv2_johnhennin.nc", 'w')

    #File attributes:
    f.history = "created %s" % datetime.date.today()
    f.contact = 'John H. Hennin (jhennin@email.wm.edu)'
    f.institution = 'College of William and Mary'
    f.title = 'Monthly Global Enhanced Vegetation Indexes (EVI) at 0.5-degree resolution'
    f.satellite = 'Terra'

    #Creates longitude dimension and variable
    f.createDimension('longitude',720)
    longitude=f.createVariable('longitude','f',('longitude',))
    longitude[:]=np.arange(-179.75,180,.5,float)
    longitude.units="deg_East"

    #Creates latitude dimension and variable
    f.createDimension('latitude',360)
    latitude=f.createVariable('latitude','f',('latitude',))
    latitude[:]=np.arange(-89.75,90,0.5,float)
    latitude.units="deg_North"

    #Creates time dimension and variable
    f.createDimension('time',12)
    time=f.createVariable('time','i',('time',))
    time[:]=days
    time.units="days since 1900-01-01"

    #Creates EVI variable
    EVI=f.createVariable('EVI','f4',('time','latitude','longitude'))
    EVI._FillValue = -0.3
    EVI.missing_value = -0.3
    EVI.units='unitless'
    EVI[:]=totaldata

    print("NetCDF file successfully created in 'data' folder.")

    f.close()
