#Xianglu Peng & Natalie Larsen
#for more information about KNNImputer:
    #https://scikit-learn.org/stable/modules/generated/sklearn.impute.KNNImputer.html

#import modules
import numpy as np
from sklearn.impute import KNNImputer

def impute_separately():

    red = open("red.asc","r")
    blue = open("blue.asc","r")
    green = open("green.asc","r")

    red_data = red.readlines()
    blue_data = blue.readlines()
    green_data = green.readlines()

    #write attributes into new asc file
    new_file = open("xp_nal.asc","w")
    for i in range(7):
        if red_data[i] == blue_data[i] == green_data[i]:
            new_file.write(red_data[i])
        else:
            print("Error! Inconsistent attributes.")

    #load data into numpy arrays
    red_np = np.loadtxt("red.asc",skiprows=7)
    green_np = np.loadtxt("green.asc",skiprows=7)
    blue_np = np.loadtxt("blue.asc",skiprows=7)
    #transform using KNNImputer
    print("---------Filling in missing pixels---------")
    imputer = KNNImputer(missing_values = -9999, n_neighbors=2, weights="uniform")
    new_red = imputer.fit_transform(red_np)
    new_green = imputer.fit_transform(green_np)
    new_blue = imputer.fit_transform(blue_np)
    print("-----------------Complete!-----------------")

    #write data into new asc file
    for x,y,z in zip(new_red, new_green, new_blue):
        for a,b,c in zip (x,y,z):
            #average the pixel values
            new_value = (a+b+c)/3
            new_file.write(str(new_value)+"  ")
        new_file.write('\n')

    red.close()
    blue.close()
    green.close()



if __name__ == "__main__":

    impute_separately()

    print("New raster file placed in working directory.")
