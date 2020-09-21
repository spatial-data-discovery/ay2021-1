import pandas as pd

def CheckRasterFormat(file):

    data = pd.read_csv(file, sep=" ", header=None, index_col =False, skiprows = 6)

    def logic(index):
        if index not in [0,1,2,3,4,5]:
            return True
        return False

    specs = pd.read_csv('aehillaraster.txt', sep=" ", header=None, index_col =False, skiprows= lambda x: logic(x) )
    # https://thispointer.com/pandas-skip-rows-while-reading-csv-file-to-a-dataframe-using-read_csv-in-python/

    #check ncols:
    def checkncols(data, specs):
        if (specs[specs[0] == 'ncols'][1][0]) == (data.shape[1]):
            return True
        else:
            return False

    #check nrows
    def checknrows(data, specs):
        if (specs[specs[0] == 'nrows'][1][0]) == (data.shape[0]):
            return True
        else:
            return False

    if (checkncols(data, specs) == True) and (checknrows(data,specs) == True):
        return 'Raster is in correct format'
    else:
        return 'Raster is in incorrect format'
