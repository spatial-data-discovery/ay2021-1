import os
import h5py
import numpy
import argparse

def read_hdf(file_path):
    hdf_file = h5py.File(file_path, 'r')
    data = hdf_file['data']['assignment']

    attributes = []
    for attribute in data.attrs.items():
        attributes.append(attribute)

    nrows = attributes[4][1].decode('utf-8')
    ncols = attributes[3][1].decode('utf-8')
    xll = attributes[5][1].decode('utf-8')
    yll = attributes[6][1].decode('utf-8')
    cellsize = attributes[1][1].decode('utf-8')
    nodata = attributes[0][1].decode('utf-8')
    crs = attributes[2][1].decode('utf-8')

    values=[]
    for d in data:
        values.append(d)
    values = numpy.asarray(values)

    hdf_file.close()

    raster_path = os.path.join('data', 'conv1_kelannen.asc')
    with open(raster_path, "w+") as asc:
        asc.write("nrows "+ nrows+"\n"+"ncols "+ncols+"\n"+"xllcorner "+xll+'\n'+'yllcorner '+yll+'\n'+'cellsize '+cellsize+'\n' "nodata_value "+nodata+'\n')
        count_row = 0
        count_col = 0
        for row in values:
            for col in row:
                asc.write(str(col)+' ')
                count_col += 1
            if count_col != int(ncols):
                print("Error, the number of columns in row "+str(count_row+6)+" is not the number specified in ncols.")
            asc.write('\n')
            count_col = 0
            count_row += 1
        if count_row != int(nrows):
            print("Error, the number of rows in the file is not the number specified in nrows.")
    asc.close()

    prj_path = os.path.join('data', 'conv1_kelannen.prj')
    with open(prj_path, "w+") as prj:
        prj.write(crs)
    prj.close()

    print(".asc and .prj files have been created.")
    print('This raster is located in Jasper County, Georgia at the intersection of Fullerton Phillips Road and Goolsby Road.')


if __name__ == "__main__":
    parser= argparse.ArgumentParser(description='Converts the data from the HDF5 file ./test.hdf to an ASCII raster file'
                                                'Saves this raster file as ./data/conv1_kelannen.asc along with its corresponding'
                                                '.prj file. Prints out the location of this test.hdf raster file.')
    args = parser.parse_args()

    file_path = os.path.join('data', 'test.hdf')
    if os.path.isfile(file_path):
        read_hdf(file_path)
    else:
        print("Error, the test.hdf file could not be found in the subdirectory data.")
    
