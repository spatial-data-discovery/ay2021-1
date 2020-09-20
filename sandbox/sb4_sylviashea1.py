import sys
import os
from itertools import chain
import zipfile

def is_number(s):
    # from https://stackoverflow.com/questions/37472361/how-do-i-check-if-a-string-is-a-negative-number-before-passing-it-through-int
    '''
    Checks values to determine if numerical.
    Works for negatives and floats 
    '''
    try:
        float(s)
        return True
    except ValueError:
        return False


def pass_fail(param,names):
    '''
    Checks if header in raster is named properly
    and if accompanying value is numerical
    '''
    is_float = is_number(param[1])
    if (param[0] in names and is_float is True):
        return 'pass'
    else:
        return 'fail' 

def check_headers(content): 
    '''
    Checks header names and if values are numerical
    '''
    col_names = ['ncols', 'NCOLS']
    row_names = ['nrows', 'NROWS']
    x = ['xllcorner', 'XLLCORNER', 'xllcenter', 'XLLCENTER']
    y = ['yllcorner', 'YLLCORNER', 'yllcenter', 'YLLCENTER']
    cell_names = ['cellsize','CELLSIZE']
    nodata_names = ['nodata_value','NODATA_VALUE','NODATA_value']
    checks = []
    for i in range(len(content)):
        if i>5:
            break
        elif i == 0:
            column = content[0].strip().split()
            col_num = column[1]
            check = pass_fail(column,col_names) 
            checks.append(check)
        elif i == 1:
            row = content[1].strip().split()
            row_num = row[1]
            check = pass_fail(row,row_names)
            checks.append(check)
        elif i == 2:
            x_coordinate = content[2].strip().split()
            check = pass_fail(x_coordinate,x)
            checks.append(check)
        elif i == 3:
            y_coordinate = content[3].strip().split()
            check = pass_fail(y_coordinate,y)
            checks.append(check)
        elif i == 4:
            cellsize = content[4].strip().split()
            check = pass_fail(cellsize,cell_names)
            checks.append(check)
        else:
            nodata_value = content[5].strip().split()
            check = pass_fail(nodata_value,nodata_names)
            checks.append(check)
    return checks, int(col_num), int(row_num) 


def numeric_check(content):
    '''
    Checks if raster values are all numeric
    '''
    nums_only = content[6:]
    for i in range(len(nums_only)):
        line = nums_only[i].strip().split()
        for x in line:
            is_float = is_number(x)
            if is_float is False:
                return 'fail'
    return 'pass'

def col_check(content,col_num):
    '''
    Determines if column value in header matches raster columns
    '''
    nums_only = content[6:]
    for i in range(len(nums_only)):
        line = nums_only[i].strip().split()
        cols = len(line)
        if cols!=col_num:
            return 'fail'
    return 'pass'
            
def row_check(content,row_num):
    '''
    Determines if row value in header matches raster rows
    '''
    nums_only = content[6:]
    rows = len(nums_only)
    if rows!=row_num:
        return 'fail'
    else:
        return 'pass'

def check_prj(path,file):
    '''
    Checks .prj for proper entries
    '''
    with open(path) as f:
        content = f.readlines()
    content = [lines.strip() for lines in content]
    checks = []
    items = content[0].split(',')
    for i in range(len(items)):
        if i==0:
            geo = items[i].split('[')[0]
            if geo=='GEOGCS':
                checks.append('pass')
            else:
                checks.append('fail')
        if i==1:
            datum = items[i].split('[')[0]
            if datum=='DATUM':
                checks.append('pass')
            else:
                checks.append('fail')
        if i==2:
            spher = items[i].split('[')[0]
            if spher=='SPHEROID':
                checks.append('pass')
            else:
                checks.append('fail')
        if i==5:
            prim = items[i].split('[')[0]
            if prim=='PRIMEM':
                checks.append('pass')
            else:
                checks.append('fail')
        if i==7:
            unit = items[i].split('[')[0]
            if unit=='UNIT':
                checks.append('pass')
            else:
                checks.append('fail')
    if 'fail' in checks:
        print('ERROR: %s is not a valid raster' % file)
    else:
        print('PASS: %s is a valid raster' % file)

def check_txt(path,file):
    with open(path) as f:
        content = f.readlines()
        content = [lines.strip() for lines in content]
        # Checking header names and values. Extracting col and row values.
        header_checks, col_num, row_num = check_headers(content)
        if 'fail' in header_checks:
            print('%s has an invalid header' % file)
        # Determine if raster values are all numerical
        num_check = numeric_check(content)
        if num_check == 'fail':
            print('%s contains a non-numerical value' % file)
        # Determines if col value in header matches raster columns
        cols_valid = col_check(content,col_num)
        if cols_valid=='fail':
            print('%s columns do not match column header value' % file)
        # Determines if row value in header matches raster rows
        rows_valid = row_check(content,row_num)
        if rows_valid=='fail':
            print('%s rows do not match row header value' % file)
        # Message if raster is correct
        if 'fail' in chain(header_checks,[num_check],[cols_valid],[rows_valid]):
            print('ERROR: %s is not a valid raster' % file)
        else:
            print('PASS: %s is a valid raster' % file)

def main():
    folder = 'data'
    abs_path = os.path.abspath(folder)
    raster_files = os.listdir(abs_path)
    print('----- Validating rasters -----')
    for file in raster_files:
        print('Checking %s' % file)
        if (file.endswith('.txt') or file.endswith('.asc')):
            path = os.path.join(folder,file)
            check_txt(path,file)
        # elif file.endswith('.zip'): *Could not get this working for some reason
        #     zf = zipfile.ZipFile(file,'r')
        #     zip_names = zf.namelist()
        #     for filename in zip_names:
        #         if (filename.endswith('.txt') or filename.endswith('.asc')):
        #             zf.extract(filename)
        #             path = os.path.join(folder,filename)
        #             check_txt(path,filename)
        elif file.endswith('.prj'):
            path = os.path.join(folder,file)
            check_prj(path,file)
        else: 
            print('%s is incorrect file type' % file)
        print('--------------------')
    print('----- Check complete -----')
            
                
        

if __name__ == "__main__":
    main()

