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
- geoBoundariesUSA-ADM1-shp.zip
    
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


# GIF_Script.py
## Packages imported:
- imageio version 2.6
- imageio-ffmpeg
- os
- sys
## How it works:
After spatially joining geoBoundariesUSA-ADM1-shp.zip and admissions_screening.csv in QGIS, I took the joined shapefile into ArcGIS Pro on the Virtual Desktop.  I created 10 maps that showcased each attribute in the shapefile.  Each of these maps are stored in the "./data/images/" directory within my project folder.  This script creates a GIF out of the 10 maps in that directory using imageio version 2.6.  I used an older version of this package because it had the functionally to change the duration that each image was shown on the screen, while the most recent update did not.  This script exports the admissions_screening.gif file to the project directory. 
