#PDF to CSV conversion script
#
#Hannah Slevin
#
#admissions_screening_conv.py
#
#VERSION 1.0
#
#LAST EDIT: 2020-11-24
#
#This module is a python wrapper for a java package, so make sure you have java installed
#Check to see if Java is installed on local
!java -version
#################################################
###############IMPORT MODULES####################
#################################################
!pip install -q tabula-py
import pandas as pd
import tabula
import numpy as np

#check tabula environment
tabula.environment_info()

#establish path to pdf
pdf_path = input('Input path to PDF document:')
#pdf_path = "./data/prision_health.pdf"

#read in pdfs as pandas dataframes
# read_pdf returns list of DataFrames
dfs = tabula.read_pdf(pdf_path, stream=True,pages = 'all')


##TABLE 1: Admissions Screening##
admissions_screening = dfs[0]

#Adjust Header
new_header = admissions_screening.iloc[0] #grab the first row for the header
admissions_screening = admissions_screening[1:] #take the data less the header row
admissions_screening.columns = new_header #set the header row as the df new_header
admissions_screening = admissions_screening.rename(columns = {'pressure':'High blood pressure', 'injury': 'Tramautic brain injury'})
admissions_screening = admissions_screening.iloc[0:45,:]

#Copy DF to sum Yes' and Nos
copy_admissions_screening = admissions_screening
copy_admissions_screening= copy_admissions_screening.replace('Yes', 1)
copy_admissions_screening= copy_admissions_screening.replace('No', 0)
copy_admissions_screening= copy_admissions_screening.replace("Don't Know", 0)
column_list = list(copy_admissions_screening)
copy_admissions_screening["sum"] = copy_admissions_screening[column_list].sum(axis=1)

#Add sum to DF
Sum = copy_admissions_screening["sum"].to_list()
admissions_screening['Sum'] = Sum

#Export to csv
admissions_screening.to_csv("./data/admissions_screening.csv")
