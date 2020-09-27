#Modules
import argparse
import sys
import h5py
import numpy as np

if __name__ == "__main__":
    parser= argparse.ArgumentParser(description="This script pulls data from the HDF5 file 'test.hdf' to create a new ASCII raster file and prints the location of said raster file. It also creates a PRJ file.")
    args = parser.parse_args()

    #Open to read
    hdfile = h5py.File("data/test.hdf", 'r')

    #Grab data, put in array
    data=[]
    for i in hdfile["data"]["assignment"]:
        data.append(i)
    data=np.asarray(data)

    #Access attributes (NODATA_value, cellsize, ncols, nrows, xllcorner, and yllcorner for ASC and crs for prj)
    vals=[]
    keys=[]
    for i in hdfile["data"]["assignment"].attrs.keys():
        vals.append((hdfile["data"]["assignment"].attrs[i]).decode('utf-8'))
        keys.append(i)

    #Create dictionary for writing .asc file and .prj file
    dic={}
    for key in keys:
        for val in vals:
            dic[key]=val
            vals.remove(val)
            break

    #Raster column check
    for i in range(len(data)):
        if len(data[i])!=int(dic['ncols']):
            print("The actual number of columns seems to be inconsistent with the given value. Please check the file and try again!")
            print(len(data[i]))
            sys.exit()

    #Raster row check
    if len(data)!=int(dic['nrows']):
        print("The actual number of rows seems to be inconsistent with the given value. Please check the file and try again!")
        sys.exit()

    #Create ASCII file
    with open('data/conv1_johnhennin.asc', 'w+') as ascfile:
        ascfile.write("ncols "+dic['ncols']+'\n'+"nrows "+dic['nrows']+'\n'+"xllcorner "+dic['xllcorner']+'\n'+"yllcorner "+dic['yllcorner']+'\n'+"cellsize "+dic['cellsize']+'\n'+"NODATA_value "+dic["NODATA_value"]+'\n')
        for line in data:
            for pixel in line:
                ascfile.write(str(pixel)+" ")
            ascfile.write("\n")

    #Create PRJ file
    with open('data/conv1_johnhennin.prj', 'w+') as prjfile:
        prjfile.write(dic['crs'])

    #Where is it?
    print("The raster is of Cedar Creek––specifically the general area where Goolsby Road meets Jordan Road in the north and McMichael Road in the south––southeast of Monticello, Georgia, USA.")