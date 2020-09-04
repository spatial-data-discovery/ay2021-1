from geojson import Point, Feature, FeatureCollection, dump
from GPSPhoto import gpsphoto
import exifread


# Extract EXIF data from each image
image_names = ['000','001','002','003','004','005','006','007','008','009','010','011','012','013','014']
image_data=[]
for name in image_names:
    photo = gpsphoto.getGPSData(r"C:\Users\andre\OneDrive\Desktop\photos\image"+name+".jpg")
    photo_name = "image"+name
    foto = open(r"C:\Users\andre\OneDrive\Desktop\photos\image"+name+".jpg", 'rb')
    pdata = exifread.process_file(foto) # Need to use EXIF read here to access the Timestamp of the photo
    image_data.append([photo_name,photo['Latitude'],photo['Longitude'],photo['Altitude'],str(pdata['Image DateTime'])])



# Iterate through the extracted EXIF data and write it into a geojson format
data = []
for i in range(len(image_data)):
    data.append(Feature(geometry=Point((image_data[i][2],image_data[i][1])),properties={'image':image_data[i][0],'altitude':image_data[i][3], 'time_taken':image_data[i][4]}))

# Save our Image GPS data into a GeoJson file
geojson_output = FeatureCollection(data)
with open(r"C:\Users\andre\OneDrive\Desktop\photos\geojson_images.geojson",'w') as a:
    dump(geojson_output, a)








