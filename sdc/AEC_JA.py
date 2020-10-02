
import os
import sys
import argparse


def Raster_Null_Fill(redpath,bluepath,greenpath):

    # Check if each path is valid
    a=0
    if redpath.endswith('.asc') or redpath.endswith('txt'):
        a+=1
    else:
        print("Path to the red raster data is in incorrect format. Try '.hdf' or '.txt' ")
    
    if bluepath.endswith('.asc') or bluepath.endswith('txt'):
        a+=1
    else:
        print("Path to the blue raster data is in incorrect format. Try '.hdf' or '.txt' ")
    
    if greenpath.endswith('.asc') or greenpath.endswith('txt'):
        a+=1
    else:
        print("Path to the green raster data is in incorrect format. Try '.hdf' or '.txt' ")

    if a == 3:
        print("Processing Files...")

    # Open each raster file
    blue = open(bluepath, 'r')
    red = open(redpath, 'r')
    green = open(greenpath, 'r')

    # Iterate all of the data in the raster files into arrays
    array_b = []
    i = 0
    for line in blue:
        if i >=7:
            temp = []
            for item in line.split():
                temp.append(int(item))
        else:
            temp = line.split()
        array_b.append(temp)
        i +=1

    array_r = []
    i = 0
    for line in red:
        if i >=7:
            temp = []
            for item in line.split():
                temp.append(int(item))
        else:
            temp = line.split()
        array_r.append(temp)
        i +=1

    array_g = []
    i = 0
    for line in green:
        if i >=7:
            temp = []
            for item in line.split():
                temp.append(int(item))
        else:
            temp = line.split()
        array_g.append(temp)
        i +=1

    # Generate a main array, and only store valid values from said array.
    col_arr = [-9999]*1200
    for k in range(len(col_arr)):
        main_arr = [-9999]*1600
        for i in range(len(main_arr)):
            if array_b[k+7][i] <= 256 and array_b[k+7][i] >=0:
                main_arr[i] = array_b[k+7][i]
            elif array_r[k+7][i] <= 256 and array_r[k+7][i] >=0:
                main_arr[i] = array_r[k+7][i]
            elif array_g[k+7][i] <= 256 and array_g[k+7][i] >=0:
                main_arr[i] = array_g[k+7][i]
        col_arr[k] = main_arr


    ### First attempted linear algorithm
    # linear +/- 3 index averager
    # for k in range(len(col_arr)):
    #     for i in range(len(main_arr)):
    #         if col_arr[k][i] == -9999:
    #             averager = 0
    #             for j in range(1,3):
    #                 if col_arr[k][(i+j)%1600] != -9999:
    #                     averager +=col_arr[k][(i+j)%1600]
    #                 if col_arr[k][(i-j)%1600] != -9999:
    #                     averager += col_arr[k][(i-j)%1600]
    #             col_arr[k][i] = averager//6
    ###

    # Fill pixels based on circular-point averaging
    for k in range(len(col_arr)):
        for i in range(len(main_arr)):
            if col_arr[k][i] == -9999:
                averager = 0
                divisor = 0
                m=1
                if col_arr[k][(i+m)%1600] != -9999:
                    averager +=col_arr[k][(i+m)%1600]
                    divisor +=1
                if col_arr[k][(i-m)%1600] != -9999:
                    averager += col_arr[k][(i-m)%1600]
                    divisor +=1
                if col_arr[(k+m)%1200][i] != -9999:
                    averager += col_arr[(k+m)%1200][i]
                    divisor+=1
                if col_arr[(k-m)%1200][i] != -9999:
                    averager += col_arr[(k-m)%1200][i]
                    divisor +=1


                if divisor == 0:
                    col_arr[k][i] = averager//1
                else:
                    col_arr[k][i] = averager//divisor

    # write the complete main raster array into asc format
    with open(os.path.dirname(sys.argv[0]) + r'/AEC_JA.asc', 'w+') as f:
        f.write("nrows 1200"+"\n"+"ncols 1600"+"\n"+"xllcorner 0"+'\n'+'yllcorner 0'+'\n'+'cellsize 0.0002'+'\n' "NODATA_value -9999"+'\n'+'\n')
        for items in col_arr:
            for ele in items:
                f.write(str(ele))
                f.write(" ")
            f.write('\n')

    blue.close()
    red.close()
    green.close()
    print("Processing complete")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Provide the red raster image data file path, then blue, then green to the function Raster_Null_Fill, and an averaged image is saved to the directory.')
    args = parser.parse_args()
    red_path = os.path.dirname(sys.argv[0]) +r'/red.asc' 
    blue_path = os.path.dirname(sys.argv[0]) +r'/blue.asc' 
    green_path = os.path.dirname(sys.argv[0]) +r'/green.asc'
    Raster_Null_Fill(red_path, blue_path, green_path)

# The image is a river delta, specficially the Lena River Delta, 
# specifically it looks like the image was taken in 2019 in the summer.



### Code for exploring the pixel data (i.e checking duplicates, triplicates, etc.)
# count = 0
# l = 0
# for item in col_arr:
#     for ele in item:
#         l +=1
#         if ele > 256 or ele < 0:
#             count +=1
# print("done", count, l)
# duplicates = 0
# triplicates = 0
# for k in range(len(col_arr)):
#     for i in range(len(main_arr)):
#         checker = [0,0,0]
#         if array_b[k+7][i] <= 256 and array_b[k+7][i] >=0:
#             checker[0]=1
#         if array_r[k+7][i] <= 256 and array_r[k+7][i] >=0:
#             checker[1]=1
#         if array_g[k+7][i] <= 256 and array_g[k+7][i] >=0:
#             checker[2]=1
#         if checker[0] + checker[1] + checker[2] == 2:
#             duplicates +=1
#         if checker[0] + checker[1] + checker[2] == 3:
#             triplicates +=1
# print(" duplicates: ", duplicates)
# print('triplicates: ', triplicates)


