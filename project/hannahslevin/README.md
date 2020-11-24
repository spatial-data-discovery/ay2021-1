# README

- LAST UPDATED: 2020-10-13
- ORGANIZATION: spatial-data-discovery
- REPOSITORY: ay2021-1


## Files

### Scripts 
- GIF_Script.py(https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/GIF_Script.py)
- admissions_screening_conv.py

### Inputs
- prison_healthcare.pdf
- Images:
    - EKG.png
    - Elevated Lipids.png
    - Hepatitis A.png 
    - Hepatitis B.png
    - Hepatitis C.png
    - High BP.png
    - Mental Health.png
    - Suicide Risk.png
    - Tuberculosis.png
    
### Outputs
- admissions_screening.gif
- admissions_screening.csv


# admissions_screening_conv.py
## Packages imported:
- pandas
- tabula-py
- numpy
- java

## How it works:
This script takes the first table stored in the prison_healthcare.pdf file and converts the table to a csv.  Tabula-py is a python wrapper for a java package, so java must be installed on your local before using tabula-py.  The package turns the table into a pandas dataframe.  I then use pandas to clean the table and get it ready to export to csv.  The script outputs the admissions_screening.csv file.  

This script is necessary because I use the outputed csv to perform a spatial join to the GeoBoundaries ADM 1 shapefile.  
    
