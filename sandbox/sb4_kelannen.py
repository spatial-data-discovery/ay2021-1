import os

def isFloat(number):
    try:
        float(number)
        return True
    except ValueError:
        return False

def checkRaster(file_path, name):
    col = 0
    row = 0
    nodata = -9999
    totalrows = 0
    has_nd_header = False
    f = open(file_path, "r")
    for line in f:
        if totalrows == 0 or totalrows == 1:
            if line[:5].lower() == "ncols":
                if line[5:].strip().isdigit():
                    if  int(line[5:].strip()) == 0:
                        print(name + " - Error, ncols is 0.")
                        return
                    else:
                        col = int(line[5:].strip())
                        totalrows += 1
                else:
                    print(name + " - Error, ncols does not have a positive integer.")
                    return
            elif line[:5].lower() == "nrows":
                if line[5:].strip().isdigit():
                    if  int(line[5:].strip()) == 0:
                        print(name - "Error, nrows is 0.")
                        return
                    else:
                        row = int(line[5:].strip())
                        totalrows += 1
                else:
                    print(name + " - Error, nrows does not have a positive integer.")
                    return
            else:
                if col == 0:
                    print(name + " - Error, does not contain ncols in the header.")
                    return
                else:
                    print(name + " - Error, does not contain nrows in the header.")
                    return
        elif totalrows == 2:
            if line[:9].lower() == "xllcorner" or line[:9].lower() == "xllcenter":
                if not isFloat(line[9:].strip()):
                    print(name + " - Error, xllcorner/xllcenter does not have a numeric value.")
                    return
                else:
                    totalrows += 1
            else:
                print(name + " - Error, does not contain xllcorner or xllcenter in the header.")
                return
        elif totalrows == 3:
            if line[:9].lower() == "yllcorner" or line[:9].lower() == "yllcenter":
                if not isFloat(line[9:].strip()):
                    print(name + " - Error, yllcorner/yllcenter does not have a numeric value.")
                    return
                else:
                    totalrows += 1
            else:
                print(name + " - Error, does not contain yllcorner or yllcenter in the header.")
                return
        elif totalrows == 4:
            if line[:8].lower() == "cellsize":
                if isFloat(line[8:].strip()):
                    if  float(line[8:].strip()) <= 0:
                        print(name + " - Error, cellsize does not have a numerice greater than 0.")
                        return
                    else:
                        totalrows += 1
                else:
                    print(name + " - Error, cellsize does not have a numeric value.")
                    return
            else:
                print(name + " - Error, does not contain cellsize in the header.")
                return
        elif totalrows == 5 and line[:12].lower() == "nodata_value":
            totalrows += 1
            has_nd_header = True
            if line[:12].lower() == "nodata_value":
                nodata = line[12:].strip()
        elif (totalrows == 5 and line.strip() == "") or (totalrows == 6 and line.strip() == ""):
            totalrows += 1
        else:
            row_values = line.split()
            if len(row_values) != col:
                print(name + " - Error, line "+str(totalrows)+" does not contain the number of cols defined in the header.")
                return
            for i in range(len(row_values)):
                if not isFloat(row_values[i]) and row_values[i] != nodata:
                    print(name + " - Error on line "+str(totalrows)+", item number "+str(i)+" is not a numeric.")
                    return
            totalrows += 1
    f.close()
    if (has_nd_header and (totalrows - 6 - row) == 0) or (has_nd_header == False and (totalrows - 5 - row) == 0):
        print(name + " - Valid raster file.")
        return
    else:
        print(name + " - Error, the number of rows does not match the nrows in the header.")
        return


if __name__ == "__main__":
    path = os.getcwd()
    if '/' in path:
        path = path + '/data'
    else:
        path = path + r'\data'

    if os.path.exists(path):
        if os.path.isdir(path):
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                if os.path.isfile(file_path):
                    extension = os.path.splitext(file_path)[1]
                    if extension == ".txt" or extension == ".asc":
                        name = file
                        checkRaster(file_path, name)

        else:
            print("Path is not a directory")
    else:
        print("Path is not valid")
        
