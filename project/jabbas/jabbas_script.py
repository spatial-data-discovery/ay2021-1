#! /usr/bin/env python

# Author: Jamil Abbas
# Last Updated: 2020-11-08
#
#Script Description:
#
#This script takes in the US Crisis Monitor data as a .csv file and writes 4 new .csv
#files each containing the total data points by increasing 40 day intervals.
#The first file written includes the datapoints corresponding to the first 40 days of the data,
#the next file includes datapoints corresponding to the first 80 days of the data and so on.

#####################
# REQUIRED MODULES  #
#####################
from datetime import datetime, timedelta

import pandas as pd
import argparse

#####################
# Global Variables  #
#####################


def split_write_csv(fpath):
    '''
    Name: split_write_csv
    Inputs: str, absolute filepath to the .csv dataset (fpath)
    Objective: Imports the .csv dataset as a pandas dataframe and then manipulates the data
    dataframe and timedelta object to write four new .csv files containing the total data based on
    40 day increments.
    '''
    if fpath.endswith('.csv') == True: #Error handling

        #Import the data as a pandas dataframe
        rawdata = pd.read_csv(fpath)

        #Adjust the dates in the dataframe to follow the format that datetime uses (YYYY-MM-DD)
        for i in range(len(rawdata)):
            date_arr = rawdata.loc[i , "EVENT_DATE"]
            date_arr = date_arr.split('-')
            if date_arr[1] == 'May':
                date_arr[1] = '5'
            if date_arr[1] == 'June':
                date_arr[1] = '6'
            if date_arr[1] == 'July':
                date_arr[1] = '7'
            if date_arr[1] == 'August':
                date_arr[1] = '8'
            if date_arr[1] == 'September':
                date_arr[1] = '9'
            if date_arr[1] == 'October':
                date_arr[1] = '10'

            adj_date = date_arr[2] + '-' + date_arr[1] + '-' + date_arr[0]
            rawdata["EVENT_DATE"][i] = adj_date

        #Seperate data into segments by 40 days and create a raster containing the total
        #data until that segment

        print('---------------------Processing Data---------------------')

        for k in range(1,5):
            end_date = datetime(2020,10,31) #Set datetime variable for the last date of the data
            temp_frame = rawdata.copy()
            x=0
            for i in range(len(rawdata)):
                temp_date = rawdata["EVENT_DATE"][i].split('-')
                for j in range(len(temp_date)):
                    temp_date[j] = int(temp_date[j])
                temp_date = datetime(2020 , temp_date[1], temp_date[2])
                date_diff = end_date - temp_date
                if date_diff >= timedelta(days=160-(40*k)):
                    x = x + 1
            temp_frame = temp_frame.iloc[0:x, :]
            file_name = '40_day_segment' + str(k) + '.csv'
            temp_frame.to_csv(file_name, header=True)


        print('---------------------Data Files Successfully Created---------------------')

    else:
        raise TypeError('Invalid file input. Filetype must be <.csv>')


#########
# Main  #
#########
if __name__ == '__main__':

    description = "This script takes in the US Crisis Monitor data as a .csv file and writes 4 new \n .csv files each containing the total data points by increasing 40 day intervals. The \n first file written includes the datapoints corresponding to the first 40 days of the data, \n the next file includes datapoints corresponding to the first 80 days of the data and so on."

    parser = argparse.ArgumentParser(description=description)
    args = parser.parse_args()

    filepath = input('Enter the aboslute filepath to the Armed Conflict dataset: ')
    #Example filepath:
    #C:\Repositories\sdd\ay2021-1\project\jabbas\data\USA_2020_Oct31.csv

    split_write_csv(filepath)
