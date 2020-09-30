import h5py
import pandas as pd
import numpy as np
import argparse

def conversion(hdf_file_path):

    # read in the file
    try:
        file = h5py.File(hdf_file_path,'r')
        print('file opened successfully')
    except:
        print('file not found')

    # access the "assignment" dataset
    df = file['data'].get('assignment')


    # convert the dataset to an array
    d2 = np.asarray(df)

    # https://stackoverflow.com/questions/31037088/discovering-keys-using-h5py-in-python3
    # create function to pull out the keys from the dataset
    def keys(f):
        return [key for key in f.keys()]

    # get the list of keys
    keyslist = keys(df.attrs)

    # get the attributes for the ascii from the list of keys
    nodataval = df.attrs[keyslist[0]].decode('utf-8')
    cellsize = df.attrs[keyslist[1]].decode('utf-8')
    crs = df.attrs[keyslist[2]].decode('utf-8')
    ncols = df.attrs[keyslist[3]].decode('utf-8')
    nrows = df.attrs[keyslist[4]].decode('utf-8')
    xllcorner = df.attrs[keyslist[5]].decode('utf-8')
    yllcorner= df.attrs[keyslist[6]].decode('utf-8')

    # function to see if the attributes in the list of keys match the data in the array
    def check_raster_info(data_as_array, ncols, nrows):
        if int(nrows) == data_as_array.shape[0]:
            if int(ncols) == data_as_array.shape[1]:
                return True
            else:
                return "Incorrect number of columns"
        else:
            return "Incorrect number of rows"

    # run the check raster function
    if check_raster_info(d2, ncols, nrows) == True:
        print('raster has correct number of rows and columns')

    # if the raster has correct rows and columsn, write to a .asc file
        with open("./data/conv1_aehilla.asc", "w+") as blah:
            blah.write("ncols " + ncols + "\n"
                "nrows " + nrows + "\n"
                "xllcorner " + xllcorner + "\n"
                "yllcorner " + yllcorner + "\n"
                "cellsize " + cellsize + "\n"
                "NODATA_value " + nodataval + "\n")

    # write the values in the dataset to the new asc file
            for value in d2:
                for item in value:
                    blah.write(str(item) + " ")
                blah.write("\n")

    # if the raster has correct rows and columns, write to .prj file
        with open("./data/conv1_aehilla.prj", "w") as blah2:
            blah2.write(crs)

    # let the user know that the conversion succeeded
        print('conversion to ASCII and PRJ successful')

    # if the raster has the incorrect number of rows or columns, show the error and exit the conversion script
    else:
        return (str(check_raster_info(d2, ncols, nrows)) + ' conversion failed')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "conversion() converts an input HDF file to ASCII format.")
    args = parser.parse_args()

#create the filepath:

hdf_file_path = './data/test.hdf'

# call the function

conversion(hdf_file_path)

# description of the ASCII

print('this raster is from Monticello, GA near Oconee National Forest, near Goolsby Rd and Bradley Rd.')
