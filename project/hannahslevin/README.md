# README

- LAST UPDATED: 2020-11-24
- ORGANIZATION: spatial-data-discovery
- REPOSITORY: ay2021-1
- FOLDER: project/hannahslevin


## Files

### Scripts 
* [GIF_Script.py](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/GIF_Script.py)
* [admissions_screening_conv.py](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/admissions_screening_conv.py)




### Inputs
- [prison_healthcare.pdf](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/prison_healthcare.pdf)
- [Images](https://github.com/spatial-data-discovery/ay2021-1/tree/master/project/hannahslevin/data/images):
    - [EKG.png](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/images/EKG.png)
    - [Elevated Lipids.png](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/images/Elevated%20Lipids.png)
    - [Hepatitis A.png](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/images/Hepatitis%20A.png)
    - [Hepatitis B.png](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/images/Hepatitis%20B.png)
    - [Hepatitis C.png](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/images/Hepatitis%20C.png)
    - [High BP.png](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/images/High%20BP.png)
    - [Mental Health.png](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/images/Mental%20Health.png)
    - [Suicide Risk.png](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/images/Suicide%20Risk.png)
    - [Tuberculosis.png](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/images/Tuberculosis.png)
- [geoBoundariesUSA-ADM1-shp.zip](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/geoBoundariesUSA-ADM1-shp.zip)
    
### Outputs
- [admissions_screening.gif](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/admissions_screening.gif)
- [admissions_screening.csv](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/admissions_screening.csv)


# admissions_screening_conv.py
## Packages imported:
- [Pandas](https://pandas.pydata.org/)
- [tabula-py](https://pypi.org/project/tabula-py/)
- [numpy](https://numpy.org)
- [java](https://www.java.com/en/)

## File types:
* [csv](https://www.computerhope.com/issues/ch001356.htm)
* [pdf](https://www.computerhope.com/jargon/p/pdf.htm)

## How it works:
This script takes the first table stored in the prison_healthcare.pdf file and converts the table to a csv.  Tabula-py is a python wrapper for a java package, so java must be installed on your local before using tabula-py.  The package turns the table into a pandas dataframe.  I then use pandas to clean the table and get it ready to export to csv.  The script outputs the admissions_screening.csv file.  

This script is necessary because I use the outputed csv to perform a spatial join to the GeoBoundaries ADM 1 shapefile.  

# Spatial Join
## Software Used
- [QGIS](https://www.qgis.org/en/site/)

## File types:
* [csv](https://www.computerhope.com/issues/ch001356.htm)
* [shp](https://desktop.arcgis.com/en/arcmap/10.3/manage-data/shapefiles/what-is-a-shapefile.htm)

## Inputs
- [admissions_screening.csv](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/admissions_screening.csv)
- [geoBoundariesUSA-ADM1-shp.zip](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/geoBoundariesUSA-ADM1-shp.zip)
## Outputs
- admissions_screening.shp
## Process
I added the admissions_screening.csv and geoBoundariesUSA-ADM1-shp to an empty project in QGIS.  I clicked on the shapefile's properties and went to the join tab, I joined on admissions_screening.csv's state column and the shapefile's shapeName column.  I then went in and manually deleted all of the US territories, since my analysis focused on the contiguous United States.  

# Map Visualization 
## Software Used
- [ArcGIS Pro](hhttps://www.esri.com/en-us/arcgis/products/arcgis-pro/overview)

## File types:
* [shp](https://desktop.arcgis.com/en/arcmap/10.3/manage-data/shapefiles/what-is-a-shapefile.htm)

## Inputs
- [admissions_screening.shp](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/Admissions%20Screening%20SHP.zip)
## Outputs
- [EKG.png](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/images/EKG.png)
- [Elevated Lipids.png](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/images/Elevated%20Lipids.png)
- [Hepatitis A.png](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/images/Hepatitis%20A.png)
- [Hepatitis B.png](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/images/Hepatitis%20B.png)
- [Hepatitis C.png](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/images/Hepatitis%20C.png)
- [High BP.png](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/images/High%20BP.png)
- [Mental Health.png](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/images/Mental%20Health.png)
- [Suicide Risk.png](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/images/Suicide%20Risk.png)
- [Tuberculosis.png](https://github.com/spatial-data-discovery/ay2021-1/blob/master/project/hannahslevin/data/images/Tuberculosis.png)

## Process
For each attribute in the admissions_screening.shp, I created a map.  To create the maps, I added the admissions_screening shapefile to 10 different map tabs in Arc Pro. The QGIS join that I performed messed up some of the attribute names, so I manually re-entered them as they appeared in the original PDF.  For each attribute (EKG, Hepitatis A, etc..), I selected unique symbology and designated yes as green, no as red, and no data and other values as grey.  For each map tab, I opened a letter sized landscape layout tab.  I placed the corresponding map frame in the layout and added the title, Admissions Screenings in Prisons by State, and added the attribute as a subtitle.  I then added a legend with white bolded font and exported the layout to png.  After exporting, I cropped each png to the same extent using [Croppola](https://croppola.com).  Each of these pngs are used in the GIF_Script.py to create the admissions_screening.gif.  

# GIF_Script.py
## Packages imported:
- [imageio version 2.6](https://pypi.org/project/imageio/)
- [imageio-ffmpeg](https://github.com/imageio/imageio-ffmpeg)
- [os](https://docs.python.org/3/library/os.html)
- [sys](https://docs.python.org/3/library/sys.html)

## File types:
* [png](https://www.computerhope.com/jargon/p/png.htm)
* [gif](https://www.computerhope.com/jargon/g/gif.htm)

## How it works:
After spatially joining geoBoundariesUSA-ADM1-shp.zip and admissions_screening.csv in QGIS, I took the joined shapefile into ArcGIS Pro on the Virtual Desktop.  I created 10 maps that showcased each attribute in the shapefile.  Each of these maps are stored in the "./data/images/" directory within my project folder.  This script creates a GIF out of the 10 maps in that directory using imageio version 2.6.  I used an older version of this package because it had the functionally to change the duration that each image was shown on the screen, while the most recent update did not.  This script exports the admissions_screening.gif file to the project directory. 
