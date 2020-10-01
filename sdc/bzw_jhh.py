#Modules
from itertools import islice
import sys
#Main

#Finds vals of neighboring pixels, returns list of pixels with data values (try and excepts are to account for pixels on edges or in corners)
def neighborpixels(layer,i,p):
    neighbors=[]
    try:
        if layer[i + 1][p] != "-9999":
            neighbors.append(int(layer[i + 1][p]))
    except: IndexError
    try:
        if layer[i - 1][p] != "-9999":
            neighbors.append(int(layer[i - 1][p]))
    except: IndexError
    try:
        if layer[i + 1][p - 1] != "-9999":
            neighbors.append(int(layer[i + 1][p - 1]))
    except: IndexError
    try:
        if layer[i + 1][p + 1] != "-9999":
            neighbors.append(int(layer[i + 1][p + 1]))
    except: IndexError
    try:
        if layer[i - 1][p + 1] != "-9999":
            neighbors.append(int(layer[i - 1][p + 1]))
    except: IndexError
    try:
        if layer[i - 1][p - 1] != "-9999":
            neighbors.append(int(layer[i - 1][p - 1]))
    except: IndexError
    try:
        if layer[i][p + 1] != "-9999":
            neighbors.append(int(layer[i][p + 1]))
    except:IndexError
    try:
        if layer[i][p - 1] != "-9999":
            neighbors.append(int(layer[i][p - 1]))
    except: IndexError
    return neighbors

#Read in files
with open('blue.asc','r') as baselayer:
    basetext = baselayer.read()

with open('green.asc','r') as seclayer:
    sectext = seclayer.read()

with open('red.asc','r') as toplayer:
    toptext = toplayer.read()

#Split by line
basetext=basetext.splitlines()

sectext=sectext.splitlines()

toptext=toptext.splitlines()

#Save solely the pixels
baselines=basetext[7:1207]
seclines=sectext[7:1207]
toplines=toptext[7:1207]

#Split by pixel
baselines2=[]
seclines2=[]
toplines2=[]
for i in range(1200):
    baselines2.append(baselines[i].split(" "))
    seclines2.append(seclines[i].split(" "))
    toplines2.append(toplines[i].split(" "))

#List of rows (ex: baselines2)
#List of pixels/a list representing first row (ex: baselines2[0])
#First pixel in first row (ex: baselines2[0][0] = 49)

#Finds NODATA_values and appends location for top layer (red layer, to become master/final layer)
c=0
#While loop allows for 2 loops of lines 83-98 and one loop of lines 99-103. In our testing, this technique got rid of all NODATA_values in the layer.
while c!=2:

    for i in range(len(toplines2)):
        for p in range(len(toplines2[i])):
            if toplines2[i][p]=="-9999":
                if seclines2[i][p]!="-9999":
                    toplines2[i][p]=seclines2[i][p]
                elif baselines2[i][p]!="-9999":
                    toplines2[i][p]=baselines2[i][p]
                else:
                    #Replace NODATA_val with average of neighboring list from neighborpixels(). Check to see if list length/neighboring pixel count is greatest of every layer. If not, don't use.
                    if len(neighborpixels(toplines2,i,p))>len(neighborpixels(seclines2,i,p)) and len(neighborpixels(toplines2,i,p))>len(neighborpixels(baselines2,i,p)):
                        toplines2[i][p] = str(round(sum(neighborpixels(toplines2,i,p))/len(neighborpixels(toplines2,i,p))))
                    elif len(neighborpixels(seclines2,i,p))>len(neighborpixels(toplines2,i,p)) and len(neighborpixels(seclines2,i,p))>len(neighborpixels(baselines2,i,p)):
                        toplines2[i][p] = str(round(sum(neighborpixels(seclines2, i, p))/len(neighborpixels(seclines2, i, p))))
                    elif len(neighborpixels(baselines2,i,p))>len(neighborpixels(seclines2,i,p)) and len(neighborpixels(baselines2,i,p))>len(neighborpixels(toplines2,i,p)):
                        toplines2[i][p] = str(round(sum(neighborpixels(baselines2, i, p))/len(neighborpixels(baselines2, i, p))))
                    if c==1:
                        #Checking if the neighborpixel() lists are equal (just in case there was no greatest list of neighboring pixels
                        if len(neighborpixels(seclines2,i,p))==len(neighborpixels(toplines2,i,p)):
                            toplines2[i][p] = str(round(sum(neighborpixels(seclines2, i, p))/len(neighborpixels(seclines2, i, p))))
                        elif len(neighborpixels(baselines2,i,p))==len(neighborpixels(toplines2,i,p)):
                            toplines2[i][p] = str(round(sum(neighborpixels(baselines2, i, p))/len(neighborpixels(baselines2, i, p))))
    c=c+1

#Checks if there are any NODATA_vals left (if there are, the location is listed in the list count. If count is empty, there are no more NODATA_vals left).
count=[]
for i in range(len(toplines2)):
    for p in range(len(toplines2[i])):
        if toplines2[i][p]=="-9999":
            count.append([i,p])
if len(count)!=0:
    print("Something went wrong. Please try again.")
    sys.exit()

#Grabs headers
with open('red.asc', 'r') as getting:
    head = list(islice(getting, 6))

#Add headers to final raster file
with open("Brian_John.asc", 'w') as ascii:
    for line in head:
        ascii.write(line)
    ascii.write('\n')

#Create string for raster data from toplines2 (the master layer)
toplines3=[]
for i in range(len(toplines2)):
    toplines3.append(" ".join(toplines2[i]))
finalstring="\n".join(toplines3)

#Add pixel data
with open("Brian_John.asc", 'a') as ascii:
    ascii.write(finalstring)












