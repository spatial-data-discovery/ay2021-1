# README

* LAST UPDATED: 2020-11-02
* USERNAME: johnhennin
* ORGANIZATION: spatial-data-discovery
* REPOSITORY: ay2021-1
* FOLDER: project/johnhennin

## Files
* [hennin_processing_script.py](hennin_processing_script.py)
* [johnhennin_process_doc.txt](johnhennin_process_doc.txt)

## How hennin_processing_script.py Works and How to Run It
hennin_processing_script.py reads files in the local directory, checks which ones are GeoTIFF files, and reads the data from each GeoTIFF file. It then, in the same directory, produces an ASCII raster file and a PRJ file for every GeoTIFF file read. Additionally, once all GeoTIFF files have been converted to ASCII raster format, a single .txt document is made containing multiple lists, each one corresponding to a single GeoTIFF file. Each list describes every unique cell value in the corresponding GeoTIFF file, along with the amount of cells with each unique value. In order to properly run this script, it must be run in the command line within the same directory as the GeoTIFF files you wish to convert.

## Necessary Packages
* [rasterio](https://rasterio.readthedocs.io/en/latest/)
* [numpy](https://numpy.org/)
* [argparse](https://docs.python.org/3/library/argparse.html)
* os

## Input Files
* [GeoTIFF file(s)](https://earthdata.nasa.gov/esdis/eso/standards-and-references/geotiff)

## Output Files
* [ASCII Raster file(s)](http://resources.esri.com/help/9.3/arcgisengine/java/GP_ToolRef/spatial_analyst_tools/esri_ascii_raster_format.htm)
* [PRJ file(s)](https://fileinfo.com/extension/prj#:~:text=A%20PRJ%20file%20contains%20a,files%20used%20by%20the%20project.)
* Plain Text Document

data file(s) attribution/metadata (see DATA ATTACHMENT above)
list of data variables/attributes that you used/created
