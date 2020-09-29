import h5py, argparse, numpy as np

def hdf2rastertxt(file_name):
    try:
        source_hdf = h5py.File(file_name,'r') #read the hdf file
    except:
        return 'file not found'
    
    data = source_hdf['data'] #navigate to data group
    
    ###create array from hdf to write into txt file
    raster_data = []
    for num in data['assignment']: 
        raster_data.append(num)
    raster_array = np.asarray(raster_data)
    
    ###take metadata: if not exist, throw error
    try:
        metadata = []
        for md in data['assignment'].attrs.items(): #https://docs.h5py.org/en/stable/high/attr.html
            metadata.append(md)
    except:
        return 'no metadata found. file may not be a raster, or it was improperly formatted'
    
    #trial and error. for some reason they were printed not in order?
    ncols = metadata[3][1].decode('UTF-8')
    nrows = metadata[4][1].decode('UTF-8')
    xllcorner = metadata[5][1].decode('UTF-8')
    yllcorner = metadata[6][1].decode('UTF-8')
    cellsize = metadata[1][1].decode('UTF-8')
    ncols = metadata[4][1].decode('UTF-8')
    nodat = metadata[0][1].decode('UTF-8')
    crs = metadata[2][1].decode('UTF-8')
    
    ###write data
    with open(r'data/vincentandaw_raster.txt','w') as txt:
        txt.write("nrows "+ nrows+"\n"+
                  "ncols "+ncols+"\n"+
                  "xllcorner_or_center "+xllcorner_or_center+'\n'+
                  'yllcorner_or_center '+yllcorner_or_center+'\n'+
                  'cellsize '+cellsize+'\n'+
                  "NODATA_value "+nodat+'\n')
        for i in raster_array:
            for j in i:
                txt.write(str(j)+' ')
            txt.write('\n')
    with open(r'data/vincentandaw_metadata.prj','w') as prj:
        prj.write(crs)
    
    return 'done! please check your output folder'

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='extracts out a raster file from within an hdf5')
    parser.add_argument('file_name',type=str,help='Input directory of hdf5 file')
    args = parser.parse_args()
    
    hdf2rastertxt(args.file_name)
    print('location: a portion of Cedar Creek with Goolsby Road within it, near Monticello, GA.') 
