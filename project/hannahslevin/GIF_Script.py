#Images to GIF conversion script
#
#Hannah Slevin
#
#GIF_Script.py
#
#VERSION 1.0
#
#LAST EDIT: 2020-11-24
#
#Code was derived from:
#https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python
#
#################################################
###############IMPORT MODULES####################
#################################################
!pip install imageio==2.6
!pip install imageio-ffmpeg
import os, sys
import imageio

#Establish path
path = input('Name of path to directory containing images:')
#path = './data/images/'
dirs = os.listdir( path )

# #Uncomment for testing:
# #test iteration through directory
# for file in dirs:
#     print(path+file)

#Create Movie
images = []
for file in dirs:
    images.append(imageio.imread(path+'/'+file))
imageio.mimsave('./admissions_screening.gif', images,fps=.75)
