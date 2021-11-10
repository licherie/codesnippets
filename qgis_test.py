from qgis.core import *
import os
import qgis.utils
from qgis import processing
#import csv and weather shape files 
#when you import csv, you must pass parameters in this url format
#for documentation see: https://qgis.org/api/classQgsVectorLayer.html 
#ctrl + f "delimitedtext" 
uri = "file:///C:/Users/LiCherie/Desktop/SC_distances_final.csv?crs=epsg:4326&useHeader=yes&crs=EPSG:4326&xField=Longitude&yField=Latitude&encoding=System&delimiter=,";
#create layer, which requires three parameters: the url, desired name of layer 
#and lastly, the name of our provider-i.e. mssql, postgres. In this case our provider is just delimitedtext
#see QgsVectorLayer documentation for supported providers 
exposuresLayer = QgsVectorLayer(uri, "my test csv layer","delimitedtext");
iface.addVectorLayer(uri, 'Risks Layer', 'delimitedtext')
#need to add for loop to go through each shapefile 
#my_shp_paths = [os.path.join("C:/Users/LiCherie/Desktop/", x) for x in os.listdir("C:/Users/LiCherie/Desktop/day1otlk-shp") if x.endswith(".shp")]
#for now, we add an individual weather file 
uri_2 = "C:/Users/LiCherie/Desktop/day1otlk-shp/day1otlk_cat.shp"
#here our provider is "ogr", which is used for shp files 
scratchLayer2 = QgsVectorLayer(uri_2, "my_cat_otlk", "ogr")
#for some reason, QGIS adds the file name to the layer so we don't need to use another name when we add to the canvas 
iface.addVectorLayer(uri_2, "", "ogr")
#uncomment if you want to see column names 
#for field in scratchLayer2.fields(): 
#   print(field.name())
#see if DN (the field determining level of storm is 0, which means no storm)
first_feature = scratchLayer2.getFeature(0)
if first_feature['DN'] != 0: 
    #run processing algorithm 
    myIntersection = processing.run("native:intersection", {'INPUT': exposuresLayer, 'OVERLAY' : scratchLayer2, 'OUTPUT':'C:/Users/LiCherie/Desktop/day1otlk-shp/my_intersection.shp'})
    print("yes")
#uncomment for parameters of intersection algorithm
#processing.algorithmHelp("native:intersection")
