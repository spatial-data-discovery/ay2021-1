
###############################################################################
# IMPORT MODULES
###############################################################################
import os
import os.path

import numpy
import h5py


###############################################################################
# MAIN
###############################################################################


def get_object_attrs(hf, obj_path):
        """
        Name:     get_object_attrs
        Features: Returns dictionary of group/dataset attributes
        Inputs:   - open h5py file object (hf)
                  - str, object path (obj_path)
        Outputs:  dict, session attributes (attrs_dict)
        """
        attr_dict = {}
        if obj_path is not None and obj_path in hf:
            for key in hf[obj_path].attrs.keys():
                val = hf[obj_path].attrs[key]
                if isinstance(val, bytes):
                    attr_dict[key] = val.decode('UTF-8')
                else:
                    attr_dict[key] = val
        else:
            print(
                "could not get attributes for %s; object does not exist!",
                obj_path)

        return attr_dict

def list_objects(hf, parent_path):
        """
        Name:     list_objects
        Features: Returns a sorted list of HDF5 objects under a given parent
        Inputs:   - open h5py file object (hf)
                  - str, HDF5 path to parent object
        Outputs:  list, HDF5 objects
        """
        rlist = []
        if parent_path in hf:
            try:
                hf[parent_path].keys()
            except:
                # Dataset has no members
                rlist = 0
            else:
                for obj in sorted(list(hf[parent_path].keys())):
                    rlist.append(obj)
        else:
            wmgs = "'%s' does not exist!" % (parent_path)
            print(wmgs)
            print('returning empty list')

        return rlist
###############################################################################
# MAIN
###############################################################################
# I use Prof. Davis' pre-written methods, which are outlined above
#takes user input to file
hdf_folder = input('Enter folder path to the .hdf file you wish to convert: ')
hdf_filename = input('Enter filename of .hdf file you wish to convert, including the .hdf file extension:')
hdf_path = hdf_folder+ "\\"+ hdf_filename
asc_path = hdf_folder + '\\' + "h5converted.asc"

#checks valid file, takes new input if invalid
while os.path.isfile(hdf_path) != True:
    print('Invalid Filepath! Try again')
    hdf_path = input('Enter file path to the .hdf file you wish to convert, including HDF file name: ')

if os.path.isfile(hdf_path):
    hdfile = h5py.File(hdf_path, 'r')
    datadic = get_object_attrs(hdfile, "data/assignment")
    datatest = hdfile['data/assignment']
#prepping .hdf attributes to be .asc headers
    noDATAstring = ('NODATA_VALUE '+ datadic['NODATA_value'])
    cellsizestring = ('CELLSIZE '+ datadic['cellsize'])
    ncolsstring = ('NCOLS '+ datadic['ncols'])
    nrowsstring = ('NROWS '+ datadic['nrows'])
#should differentiate between hdf files that have x corner/x center coordinates
    if datadic['xllcorner']:
        coordinatestr = "lower left corner"
        xllcornerstring = ('XLLCORNER '+ datadic['xllcorner'])
        yllcornerstring = ('YLLCORNER '+ datadic['yllcorner'])
    elif datadic['xllcenter']:
        coordinatestr = "center"
        xllcornerstring = ('XLLCENTER '+ datadic['xllcenter'])
        yllcornerstring = ('YLLCENTER '+ datadic['yllcenter'])

    datarray = datatest[0:]
    asc = open(asc_path, "w+")
#writes headers to .asc file
    asc.write(ncolsstring + ' \n')
    asc.write(nrowsstring+ ' \n')
    asc.write(xllcornerstring+ ' \n')
    asc.write(yllcornerstring+ ' \n')
    asc.write(cellsizestring+ ' \n')
    asc.write(noDATAstring+ ' \n')
#writes data to .asc
    for item in datarray:
        for num in item:
            asc.write(str(num)+ ' ')
    asc.close()
#prints information about location
    print ("This file is a raster file with a cell size of " + cellsizestring +". It has a "+ coordinatestr+' located at latitude/longitude X coordinate ' + xllcornerstring  + ' and Y coordinate ' + yllcornerstring)
    hdfile.close()
