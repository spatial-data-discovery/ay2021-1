The purpose of this project is for you to showcase spatial data on a public website (https://spatial-data-discovery.github.io). The task is to find (or create) spatial data that interests you; explain why it is interesting; describe what it is, where it came from, and any processes you used to create/modify it; and produce a visualization of the data that expresses your interest to others.

- must include at least one graphic (still or animated); (e.g., a PNG or MP4)
    - *Specifications:* max width = 910 pixels
- must include data (or link to data)
    - Please include a readme file that explains each part of your deliverables (e.g., what they are, what they do, where they came from)
- must include code used to create or process the dataset
    - *Specifications:* I should be able to reproduce your data given an input file or link to a (publicly accessible) dataset (or datasets) and your process document
- must include a summary for a general audience that explains the graphic, why it is important, how it was created, and what you learned along the way
    - Please keep a *process document*, similar to your *weekly report* that includes links to all datasets, sources, code examples, procedures, processes, analyses, etc. that you have tried and/or completed; you can use this to help you summarize your data section on your website page.
    - Please use the project_GITHUB-USERNAME.Rmd as a template for your final submission.

***

The project is worth 22 points and is broken down into categories as described below.

* font-end (45%)
    - summary, visuals, methods, and attribution
* back-end (30%)
    - data files, scripts, reproducible process
* web site design and creativity (25%)

A Graphical Representation of Deliverables
------------------------------------------
Point allocations are shown in the margin.

```
EMAIL
-----------------------------------------------------------------------------
    | TO: DAVIS
    | SUBJECT: DATA 431 - PROJECT FILES
    | - PROJECT TITLE: submit a meaningful / catchy title for your project
3.6 | - MEDIA ATTACHMENT: (.png, .jpg, .mp4, other)
1.6 | - DATA ATTACHMENT OR DATA SOURCE LINK
    |   | - Make certain your data files include the following:
    |   |   | - data origin or provider
    |   |   | - variable definitions
    |   |   | - units
    |   |   | - appropriate nodata/missing value/fillvalue
    |   |   | - contact info
    |   |   | - institution name
    |   |   | - date created
    |   | - While variables and attributes should be included with your data  
    |   |   files (.nc and .hdf), please also include them in your README file.


AY2021-1/PROJECT/USERNAME (create this subfolder with your username)
-----------------------------------------------------------------------------
1.0 | - *.py, *.R, or *.* (process script, name doesn't matter)
    |   | - please include your name and date updated in comments at the top
    |   | - please include a short summary of what your script does
    |   | - please do not include hard-coded paths; you may assume files are
    |   |   in the local directory or request a directory from the user
1.0 | - README
    |   | - include a list of files in your folder
    |   | - a how-to for running your script
    |   | - list of any necessary packages imported by your script
    |   | - list/sources of any input/output files used/created by your script
    |   | - data file(s) attribution/metadata (see DATA ATTACHMENT above)
    |   | - list of data variables/attributes that you used/created
3.0 | - process.txt (plain text file; e.g. Jupyter .ipynb also acceptable)
    |   | - should look similar to your weekly reports
    |   | - should include what you did, where you looked, what you found, what
    |   |   you used, and any other relevant information
    |   | - this will help you when you write up your data summary
    |   | - see `example-process-doc.txt`


SPATIAL-DATA-DISCOVERY.GITHUB.IO
-----------------------------------------------------------------------------
6.3 | - project-username.Rmd (create this file; use all lowercase letters)
    |   | - include a link to your media (get URL from your professor)
    |   | - include summary/overview statement of importance (see examples)
    |   | - include a data summary
    |   |   | - a general description of where data came from
    |   |   | - any processes/changes you made on it
    |   |   | - how you converted it to a visualization
    |   |  - any appropriate attributions
    |   |  - follow all Markdown writing guidelines
    |   |    (e.g., new lines for sentences in the same paragraph)

```

The remaining points that are not allocated will be awarded based on the qualitative nature of the project and website.
These points may be applied to interesting visualizations (such as video), unique processing techniques (in your python script), or stylized web layout.

Please note that our website supports CSS, if you are interested in adding any special elements or stylistic touches.
*Please contact your professor before implementing these.*

Make certain the page looks the way you want it to after it is rendered to HTML.
You can render individual pages on your end if you have R, rmarkdown, and pandoc installed (see resources on our class website).
Feel free to email your professor to pull the repository and render the website for you.
**Please refrain from running the build.R script on your end and staging, committing, and pushing the rendered outputs to our repository.**
