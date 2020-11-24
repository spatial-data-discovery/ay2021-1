#https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python

!pip install imageio==2.6
!pip install imageio-ffmpeg
import os, sys

#establish path
path = input('Name of path to directory containing images:')
#path = './data/images/'

dirs = os.listdir( path )
#test iteration through directory
for file in dirs:
    print(path+file)

#Create Movie
images = []
for file in dirs:
    images.append(imageio.imread(path+'/'+file))
imageio.mimsave('./data/admissions_screening.gif', images,fps=.75)
