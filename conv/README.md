# README
* LAST UPDATED: 2020-09-21
* ORGANIZATION: spatial-data-discovery
* REPOSITORY: ay2021-1/conv

This directory is for the conversion script assignments.

## Conversion Script 1 - HDF5 to ASC
**5 points**

For this assignment, you have been given an HDF5 data file containing a raster dataset (/data/assignment) and a colleague has asked for it in ASCII raster format.
Your mission—should you choose to accept it—is to:

* extract the data from the HDF5 file along with any and all relevant attributes;
* save the data in a valid ASCII raster format; and
* create a visualization that shows where in the world the raster is located.

Upload your Python script (conv1_GITHUBNAME.py), a PNG file of your data (conv1_GITHUBNAME.png), and the answer to the question: "Where in the world is this raster data from?"

**Requirements**

1. Your Python script should execute in this folder and:
    * produce an ASC raster file in the local `data` directory
    * read the HDF5 file found in the local `data` directory; it is your choice whether to hardcode the path, take a directory path or file path as an argument or input
    * print your answer to "Where in the world is this raster from?" to the console (i.e., use the `print` function); please be as specific as possible to where in the world it is located
    * use the `h5py` Python package for reading the HDF file
    * have any and all package import statements at the top of your script
1. Your ascii file should:
    * have all the correct headings in the correct order (*remember Sandbox Challenge \#4*)
    * have the correct data organized in the correct number of rows and columns in integer format
1. You may use any tools to create your visualization, but it should be in PNG file format and be less than 1 MB file size (_it does not need to be automated by your script_)
1. Name your two files correctly

**Grading**

| Score | Description |
| :--: | :--- |
| 0 | Did not submit |
| 2.5 | Does not meet the requirements of the assignment (code crashes, ascii file is invalid, visualization missing, question unanswered) |
| 3.5 | Almost everything works; maybe a typo or an error that's easily fixed or only partial answer given |
| 4.5 | Meets all requirements |
| 5 | Meets and exceeds requirements (e.g., includes error handling, user feedback, the '-h' help message, advanced format checking, PRJ file creation) |

Any scores less than full marks may be resubmitted using the within one week of grading tagging your commit message to the "Regrade" issue on GitHub.
