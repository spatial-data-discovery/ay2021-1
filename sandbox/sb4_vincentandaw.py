#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#https://stackoverflow.com/questions/30117567/how-to-read-extract-climate-model-data-in-asc-file-format-by-using-python
#https://stackoverflow.com/questions/26825729/extract-number-from-string-in-python/26825781#:~:text=use%20list%20comprehension%2Bisdigit()&text=*Find%20list%20of%20all%20integer,then%20find%20max%20of%20it.
from itertools import islice
import numpy as np, argparse


def open_asc(file):
    #actual shape of array
    try:
        raw_grid = np.loadtxt(file,skiprows=6) #skips first 6 formatting rows
        grid = raw_grid.astype(int) #checks numeric status here.
    except ValueError:
        return 'Array contains non-numeric value. Please fix'
    actual_cols = grid.shape[1]
    actual_rows = grid.shape[0]
    
    #claimed shape of array
    with open(asc_file) as f:
        lines = f.readlines()
        ncols_line = lines[0]
        nrows_line = lines[1]
    ncols = int(''.join(filter(str.isdigit, ncols_line)))
    nrows = int(''.join(filter(str.isdigit, nrows_line)))
    
    #return actual_cols, actual_rows, ncols, nrows
    if ncols!=actual_cols or nrows!=actual_rows:
        return f'dimensions of array do not match specified size. ncols declared: {ncols}; actual: {actual_cols}. nrows declared: {nrows}; actual: {actual_rows}'
    elif ncols==actual_cols and nrows==actual_rows:
        return 'dimensions match!'
    
if __name__ = '__main__':
    parser = argparse.ArgumentParser(description='Use this to check ASC or ASC/TXT-like files for ncol/nrow validity')
    parser.add_argument('file',type=str, metavar='',help='Put directory of file here')
    args = parser.parse_args()

