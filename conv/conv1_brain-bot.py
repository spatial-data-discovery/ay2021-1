import h5py
import numpy
import os
import argparse

def conversion(file_path):
    if not os.path.isfile(file_path):   #Checks to see if file path is invalid
        print('Path not valid')
        return
    hdf = h5py.File(file_path, 'r') #Reads hdf file
    ascii = open('data/test.asc', 'w') #creates ascii raster file
    data_group = hdf.get('data') #gets data from the data group 'data' from hdf
    data_set = data_group.get('assignment') #gets assignment data set from data group
#The key that starts with 'NODATA' is not liked by QGIS. Therefore, we skip it.
#We do take the other keys and their values of the data set 
    for key in data_set.attrs.keys():
        if(key.startswith('NODATA')):
            continue
        ascii.write(key + ' ' + data_set.attrs[key].decode('UTF-8'))
        ascii.write('\n')
    data_array = numpy.array(data_set)
    m, n = data_array.shape
#Writes integers for cell sizes from hdf5 file into the ascii raster file
    for row in range(m):
        for col in range(n):
            ascii.write(str(data_array[row][col]) + ' ')
        ascii.write('\n')

    hdf.close()
    ascii.close()




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'The user provides a path to a file, and the code takes the content of that file and puts it in a .asc file')
    args = parser.parse_args()
    parser.add_argument('file_path', type=str, help="The path to a file")
    name_of_file = input('Enter the path to a file: ')
    conversion(name_of_file)
    #tested with conversion('data/test.hdf')
    print('This raster is on southeast of Monticello, Georgia, at the intersection of Goolsby Road and Fullerton Phillips Road')
