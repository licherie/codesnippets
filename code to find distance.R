#need to add ID to link up points 
#getting necessary packages -- geodist we use to calculate distance between two points
#we use dplyr to manipulate tables 
install.packages("geodist")
require("geodist")
install.packages("dplyr")
require(dplyr)

#define a function with parameters risk_row and coastline_pnts
#risk_row --> one row in a table with columns Lon and Lat 
#coastline_pnts --> table of all points on our coastline also with columns lon lat 
#for QGIS we divided the coastline_pnts by UTM zone 
#so we just keep it the same here for consistency 
#this finds the min distance from one risk to any of hte coastline points

my_func_geo_dist<- function(risk_row, coastline_pnts) {
  min(geodist(risk_row, coastline_pnts), measure = "geodesic")
}


#we imported our data using the R UI but we could also have done it through code
#Coastline_UTM_19 is our coastline points
#UTM_19_20200630 is our 20200630 risks in UTM 19 
#can take subset of rows to test runtime

x<-Coastline_UTM_19 %>%select(Lon, Lat)  
y<-UTM_19_20200630%>% select(Longitude, Latitude)  %>% slice(1:1000)

#now we iterate the function we made above over all risks 
#write to csv the result of the distance matrix 

write.csv(apply(y, MARGIN = 1, FUN= my_func_geo_dist, coastline_pnts= x), 
          "C:\\Users\\LiCherie\\Desktop\\my_R_distMatrix.csv", row.names = FALSE)

