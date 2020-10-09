
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
hdf_path = input('Enter file path to the .hdf file you wish to convert, including HDF file name: ')

#checks valid file, takes new input if invalid
while os.path.isfile(hdf_path) != True:
    print('Invalid Filepath! Try again')
    hdf_path = input('Enter file path to the .hdf file you wish to convert, including HDF file name: ')

if os.path.isfile(hdf_path):
    hdfile = h5py.File(hdf_path, 'r')
    datadic = get_object_attrs(hdfile, "data/assignment")
    datatest = hdfile['data/assignment']
#prepping .hdf attributes to be .asc headers
    noDATAstring = ('NODATA_value '+ datadic['NODATA_value'])
    print(noDATAstring)
    cellsizestring = ('CELLSIZE '+ datadic['cellsize'])
    print(cellsizestring)
    ncolsstring = ('NCOLS '+ datadic['ncols'])
    print(ncolsstring)
    nrowsstring = ('NROWS '+ datadic['nrows'])
    print(nrowsstring)
#should differentiate between hdf files that have x corner/x center coordinates
    if datadic['xllcorner']:
        xllcornerstring = ('XLLCORNER '+ datadic['xllcorner'])
        print(xllcornerstring)
        yllcornerstring = ('YLLCORNER '+ datadic['yllcorner'])
        print(yllcornerstring)
    elif datadic['xllcenter']:
        xllcornerstring = ('XLLCENTER '+ datadic['xllcenter'])
        print(xllcornerstring)
        yllcornerstring = ('YLLCENTER '+ datadic['yllcenter'])
        print(yllcornerstring)
    datarray = datatest[0:]
    asc = open("h5converted.asc", "x")
    asc.close()
    asc = open("h5converted.asc", "w")
#writes headers to .asc file, but will cause error if .asc already exists
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
    print ("This file is a raster file with a cell size of " + cellsizestring +" and where " + xllcornerstring + ' and ' + yllcornerstring)
    hdfile.close()
