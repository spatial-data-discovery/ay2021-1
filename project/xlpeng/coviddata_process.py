#! /usr/bin/env python

# coviddata_process.py
# Author: Xianglu Peng
# Last Update: 2020-11-20
#
# Purpose: 
# This script extracts the data from the given csv file
# and save the data into separate newly created csv files.
#
#
##########################
#    REQUIRED MODULES    #
##########################

import os
import sys
import argparse
import csv
import numpy as np


##################
#    Function    #
##################

def readCSV():


    #the created files will be saved in the local directory folder 
    
    #folder = 'data_files'
    input_file = 'us-states.csv'

    #filepath = os.path.join(folder, input_file)

    #open the file and read each line
    if os.path.exists(input_file):
        file = open(input_file,"r")
        reader = csv.reader(file, delimiter=',')
        data = file.readlines()

    #Error handling
    else:
        print('File not found. Please check your file path.')
        sys.exit()

    #initialize the dates I want
    #can adjust this list to get the data of other dates if needed
    dates = ['2020-01-25','2020-02-15','2020-03-05','2020-03-25','2020-04-15',
    '2020-05-05','2020-05-25','2020-06-15','2020-07-05','2020-07-25','2020-08-15',
    '2020-09-05','2020-09-25','2020-10-15','2020-11-05','2020-11-18']

    #hardcode the arrtibutes of the csv file
    attr = ['date','state','fips','cases','deaths']

    #write data into new files
    for i in range(len(dates)):
        new = open(dates[i]+".csv","w")
        new.write(data[0])
        for line in data:
            temp = list(line.split(","))
            if temp[0] == dates[i]:
                new.write(line)

        
################## 
#      Main      #
##################           

if __name__ == "__main__":

    description = (
        'This script extracts the data from the given csv file'
        'and save the data into separate newly created csv files.\n')

    parser = argparse.ArgumentParser(description)
    args=parser.parse_args()

    readCSV()