#Jamil Abbas
#Conversion Script



#NOTE: Requires creation of a blank raster file titled <test.asc> in data/test.asc

###################
#Required modules
###################
import os
import argparse
import h5py
import numpy

###################
#Functions
###################

def extract_to_raster(fpath):



    if os.path.isfile(fpath) == False: #Error Handling
        raise TypeError('Invalid File Path')


    if fpath.endswith('.hdf'):#Error Handling

        #Read in the hdf file with 'r'
        hdf_file = h5py.File(fpath, 'r')

        #Open the empty raster file
        raster_a = open('data/test.asc', 'w')

        #Get data
        d1 = hdf_file.get('data')
        d2 = d1.get('assignment')

        for k in d2.attrs.keys():
            if(k.startswith('NODATA') == False ):
                raster_a.write(k + ' ' + d2.attrs[k].decode('UTF-8'))
                raster_a.write('\n')

        d2_numpy = numpy.array(d2)


        for r in range(d2_numpy.shape[0]): #Rows
            for c in range(d2_numpy.shape[1]):#columns
                raster_a.write(str(d2_numpy[r][c]) + ' ')
            raster_a.write('\n')


        #Close files
        hdf_file.close()
        raster_a.close()


    else:
        raise TypeError('Invalid File Type')






###################
#Main
###################

par = argparse.ArgumentParser(description = 'User inputs file path to a type .hdf file and the program writes an asc raster file filled with the contents. NOTE: Requires creation of a blank raster file titled <test.asc> in data/test.asc')
args = par.parse_args()

file = input('Enter path to .hdf file: ')

extract_to_raster(file)

print('The raster is right outside Monticello, Georgia, USA, by Goolsby Road.')
