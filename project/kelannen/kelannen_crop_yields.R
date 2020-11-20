rm(list = ls(all = TRUE))

# Katherine Lannen

# Date Updated: 11/19/2020

# Summary: This script takes in the various source files (africa_adm0.geojson, 
# Data_Extract_FromWorld Development Indicators.xlsx, and Production_Crops_E_Africa.csv) which
# contains the geometry of Africa with the names of the countries and the crop types, yields, and years for those 
# countries and finally the avg. precipitation mm/year respectively. After reading in the files to their 
# respective dataframes it then formats the data so that the correct information is kept and in the correct format. 
# It also then merges the dataframes together and then creates the different graphs. Finally it animates those graphs 
# by creating a folder containing the still images of each year and then a html file that goes through those images 
# one by one. I screen recorded this html file to get the final video. 
# QUICK NOTE: Even though it creates separate html files, it will still show the same thing as the last version of 
# saveHTML you ran so if you want to switch back and forth either look at the videos I have created or rerun that 
# section of code.

###################################################################################################################

# Below, commented out, is the way to install any packages that you need if you don't have them installed already
# If they are already installed you only need to run the library commands

#install.packages("rstudioapi", dependencies = TRUE)
#install.packages("rgdal", dependencies = TRUE)
#install.packages("rgeos", dependencies = TRUE)
#install.packages("ggmap", dependencies = TRUE)
#install.packages("sp", dependencies = TRUE)
#install.packages("maptools", dependencies = TRUE)
#install.packages("dplyr", dependencies = TRUE)
#install.packages("gridExtra", dependencies = TRUE)
#install.packages("geojsonio", dependencies = TRUE)
#install.packages("animation", dependencies = TRUE)
#install.packages("readxl", dependencies = TRUE)

# If the packages are already installed, you can just load them using the library command below.
library(rstudioapi)
library(rgdal)
library(rgeos)
library(ggmap)
library(sp)
library(maptools)
library(dplyr)
library(gridExtra)
library(sf)
library(tidyr)
library(geojsonio)
library(animation)
library(readxl)

# Set working directory to source file location
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

# Load the geometry data for Africa
data_sf <- geojson_sf("./africa_adm0.geojson")

# Read in the crop information for the different countries in Africa
# Selecting only the relevant data (the correct metric without additional flags)
data_crops2 <- read.csv("./Production_Crops_E_Africa.csv")
data_crops2[is.na(data_crops2)] = 0
crops2 <- data_crops2[data_crops2$Element == "Yield",]
crops2 <- crops2[,c(2,4,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,100,102,104,106,108,110,112,114,116,118,120,122)]

# Create two different aggregations of the crop yield information. One representing the sum of the yields of all crops
# and the other representing the sum of the yields for select crops. Those crops being: groundnuts, wheat, cereals,
# cassava, millet, and maize.
crops_selection <- crops2[crops2$Item %in% c("Groundnuts, with shell", "Wheat", "Cereals, Total", "Cassava", "Millet", "Maize"),]
crops_selection_total <- crops_selection[,c(1,3:60)]
crops_selection_total <- aggregate(. ~ Area, data=crops_selection_total, FUN=sum)
crops2 <- crops2[,c(1,3:60)]
crop2_yield_sum <- aggregate(. ~ Area, data=crops2, FUN=sum)

# Change names of the countries in the different dataframes so that it will match up.
# This is important as the next step is using this as a key for merging the crop yield information to the geometric 
# information about those African countries. 
data_sf$name[46] <- "Eswatini"
data_sf$name[38] <- "Central African Republic"
data_sf$name[52] <- "Western Sahara"
data_sf$name[5] <- "South Sudan"
data_sf$name[41] <- "Sao Tome and Principe"
crop2_yield_sum$Area[14] <- "Dem. Rep. Congo"
crop2_yield_sum$Area[17] <- "Eq. Guinea"
crop2_yield_sum$Area[7] <- "Cape Verde"
crop2_yield_sum$Area[55] <- "Tanzania"
crops_selection_total$Area[14] <- "Dem. Rep. Congo"
crops_selection_total$Area[17] <- "Eq. Guinea"
crops_selection_total$Area[7] <- "Cape Verde"
crops_selection_total$Area[55] <- "Tanzania"

# Further cleaning of the data. The former Sudan split to become South Sudan and Sudan in 2011, as such 
# needed to add the values for 1961-2011 in crop2_yield_sum and crop_selection_total for SOuth Sudan and Sudan
crops_selection_total[49,2:52] <- crops_selection_total[51,2:52]
crops_selection_total[50,2:52] <- crops_selection_total[51,2:52]
crop2_yield_sum[49,2:52] <- crop2_yield_sum[51,2:52]
crop2_yield_sum[50,2:52] <- crop2_yield_sum[51,2:52]

# Similar to above, Ethiopia PDR became Ethiopia in 1993. Gave Ethiopia those values for 1961-1992
# in crop2_yield_sum and crop_selection_total for Ethiopia PDR.
crops_selection_total[20,2:33] <- crops_selection_total[21,2:33]
crop2_yield_sum[20,2:33] <- crop2_yield_sum[21,2:33]

# Combine spatial geometry data of Africa and the crop yield information using the names of the countries as a key.
africa_crops2 <- merge(data_sf,crop2_yield_sum,by.x = "name", by.y="Area")
africa_crop_selection_total <- merge(data_sf,crops_selection_total,by.x = "name", by.y="Area")

# Read in the rainfall information for the different countries in Africa and clean up the data some 
# Note: Did some cleaning manually after downloading the dataset and automated other parts of it
rainfall_data = readxl::read_excel("./Data_Extract_FromWorld Development Indicators.xlsx")
rainfall_data <- rainfall_data[c(1:15,17:40,42:52,54:57),c(1,3,8,13,19,24,29,34,39,44,49)]
rainfall_data$...1[7] <- "Cape Verde"
rainfall_data$...1[13] <- "Congo"
rainfall_data$...1[12] <- "Dem. Rep. Congo"
rainfall_data$...1[16] <- "Egypt"
rainfall_data$...1[17] <- "Eq. Guinea"
rainfall_data$...1[22] <- "Gambia"

# Merging the existing dataframes with the rainfall dataframe
africa_crops2 <- merge(africa_crops2, rainfall_data,by.x="name",by.y="...1",all.x=TRUE)
africa_crop_selection_total <- merge(africa_crop_selection_total, rainfall_data,by.x="name",by.y="...1",all.x=TRUE)

## CREATING THE DIFFERENT GRAPHS ACROSS THE YEARS FOR TOTAL CROP YIELDS IN AFRICA
# Standardized the scaling across the years so that the changes make more sense
# The range goes from 0 hg/ha to 15,000,000. The midpoint is 2,250,000 hg/ha and was determined by looking at the 
# values in africa_crops2 over the years. There are labels for the name of the country as well as what their 
# Average precipitation in depth (mm per year)
africa_1961 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1961)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1961", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1962'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1962 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1962)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1962", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1962'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1963 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1963)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1963", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1962'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1964 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1964)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1964", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1962'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1965 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1965)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1965", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1962'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1966 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1966)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1966", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1962'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1967 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1967)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1967", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1967'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1968 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1968)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1968", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1967'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1969 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1969)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1969", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1967'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1970 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1970)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1970", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1967'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1971 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1971)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1971", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1967'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1972 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1972)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1972", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1972'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1973 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1973)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1973", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1972'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1974 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1974)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1974", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1972'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1975 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1975)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1975", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1972'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1976 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1976)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1976", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1972'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1977 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1977)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1977", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1977'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1978 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1978)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1978", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1977'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1979 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1979)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1979", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1977'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1980 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1980)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1980", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1977'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1981 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1981)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1981", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1977'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1982 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1982)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1982", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1982'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1983 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1983)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1983", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1982'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1984 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1984)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1984", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1982'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1985 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1985)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1985", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1982'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1986 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1986)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1986", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1982'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1987 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1987)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1987", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1987'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1988 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1988)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1988", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1987'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1989 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1989)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1989", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1987'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1990 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1990)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1990", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1987'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1991 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1991)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1991", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1987'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1992 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1992)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1992", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1992'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1993 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1993)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1993", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1992'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1994 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1994)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1994", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1992'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1995 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1995)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1995", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1992'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1996 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1996)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1996", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1992'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1997 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1997)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1997", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1997'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1998 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1998)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1998", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1997'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_1999 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y1999)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 1999", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1997'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_2000 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y2000)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 2000", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1997'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_2001 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y2001)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 2001", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'1997'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_2002 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y2002)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 2002", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'2002'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_2003 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y2003)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 2003", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'2002'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_2004 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y2004)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 2004", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'2002'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_2005 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y2005)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 2005", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'2002'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_2006 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y2006)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 2006", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'2002'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_2007 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y2007)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 2007", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_2008 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y2008)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 2008", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_2009 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y2009)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 2009", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_2010 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y2010)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 2010", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_2011 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y2011)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 2011", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_2012 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y2012)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 2012", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_2013 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y2013)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 2013", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_2014 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y2014)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 2014", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_2015 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y2015)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 2015", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_2016 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y2016)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 2016", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_2017 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y2017)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 2017", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa_2018 <- ggplot(africa_crops2) +
  geom_sf(aes(fill = Y2018)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,15000000), midpoint = 2250000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Total Crop Yields in Africa - 2018", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crops2$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

# Animate the Total crop yields in Africa from 1961-2018
# This will create a folder containing the different images of the graphs that were defined above and an html file
# that will allow you to see the animation. 
saveHTML({
  oopt <- ani.options(interval = .8, nmax = 1)
  for (i in 1:ani.options("nmax")) {
    print(africa_1961)
    print(africa_1962)
    print(africa_1963)
    print(africa_1964)
    print(africa_1965)
    print(africa_1966)
    print(africa_1967)
    print(africa_1968)
    print(africa_1969)
    print(africa_1970)
    print(africa_1971)
    print(africa_1972)
    print(africa_1973)
    print(africa_1974)
    print(africa_1975)
    print(africa_1976)
    print(africa_1977)
    print(africa_1978)
    print(africa_1979)
    print(africa_1980)
    print(africa_1981)
    print(africa_1982)
    print(africa_1983)
    print(africa_1984)
    print(africa_1985)
    print(africa_1986)
    print(africa_1987)
    print(africa_1988)
    print(africa_1989)
    print(africa_1990)
    print(africa_1991)
    print(africa_1992)
    print(africa_1993)
    print(africa_1994)
    print(africa_1995)
    print(africa_1996)
    print(africa_1997)
    print(africa_1998)
    print(africa_1999)
    print(africa_2000)
    print(africa_2001)
    print(africa_2002)
    print(africa_2003)
    print(africa_2004)
    print(africa_2005)
    print(africa_2006)
    print(africa_2007)
    print(africa_2008)
    print(africa_2009)
    print(africa_2010)
    print(africa_2011)
    print(africa_2012)
    print(africa_2013)
    print(africa_2014)
    print(africa_2015)
    print(africa_2016)
    print(africa_2017)
    print(africa_2018)
  }}, img.name = "name_images",
  imgdir = "name_dir",
  htmlfile = "total_crop_yields_africa.html",
  title = "Total Crop Yields in Africa 1961-2018",
  ani.height = 800,
  ani.width = 900
)

## CREATING THE DIFFERENT GRAPHS ACROSS THE YEARS FOR SPECIFIED CROP YIELDS IN AFRICA
# Standardized the scaling across the years so that the changes make more sense
# The range goes from 0 hg/ha to 315,000 hg/ha. The midpoint is 115,000 hg/ha and was determined by looking at the 
# values in africa_crop_selection_total over the years. There are labels for the name of the country as well as what their 
# Average precipitation in depth (mm per year)
africa2_1961 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1961)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1961", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1962'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1962 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1962)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1962", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1962'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1963 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1963)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1963", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1962'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1964 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1964)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1964", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1962'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1965 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1965)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1965", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1962'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1966 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1966)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1966", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1962'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1967 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1967)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1967", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1967'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1968 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1968)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1968", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1967'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1969 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1969)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1969", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1967'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1970 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1970)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1970", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1967'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1971 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1971)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1971", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1967'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1972 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1972)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1972", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1972'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1973 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1973)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1973", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1972'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1974 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1974)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1974", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1972'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1975 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1975)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1975", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1972'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1976 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1976)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1976", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1972'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1977 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1977)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1977", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1977'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1978 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1978)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1978", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1977'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1979 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1979)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1979", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1977'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1980 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1980)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1980", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1977'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1981 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1981)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1981", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1977'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1982 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1982)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1982", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1982'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1983 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1983)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1983", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1982'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1984 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1984)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1984", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1982'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1985 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1985)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1985", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1982'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1986 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1986)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1986", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1982'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1987 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1987)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1987", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1987'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1988 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1988)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1988", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1987'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1989 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1989)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1989", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1987'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1990 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1990)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1990", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1987'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1991 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1991)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1991", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1987'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1992 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1992)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1992", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1992'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1993 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1993)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1993", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1992'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1994 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1994)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1994", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1992'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1995 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1995)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1995", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1992'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1996 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1996)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1996", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1992'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1997 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1997)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1997", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1997'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1998 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1998)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1998", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1997'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_1999 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y1999)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 1999", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1997'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_2000 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y2000)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 2000", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1997'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_2001 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y2001)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 2001", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'1997'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_2002 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y2002)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 2002", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'2002'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_2003 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y2003)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 2003", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'2002'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_2004 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y2004)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 2004", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'2002'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_2005 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y2005)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 2005", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'2002'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_2006 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y2006)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 2006", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'2002'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_2007 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y2007)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 2007", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_2008 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y2008)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 2008", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_2009 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y2009)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 2009", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_2010 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y2010)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 2010", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_2011 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y2011)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 2011", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_2012 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y2012)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 2012", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) +xlab("Longitude") + ylab("Latitude")

africa2_2013 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y2013)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 2013", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_2014 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y2014)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 2014", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_2015 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y2015)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 2015", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_2016 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y2016)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 2016", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_2017 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y2017)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 2017", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

africa2_2018 <- ggplot(africa_crop_selection_total) +
  geom_sf(aes(fill = Y2018)) +
  scale_fill_gradient2(low = "purple", mid = "yellow", high="red", limits=c(0,315000), midpoint = 115000) +
  geom_sf_text(aes(label = name), size = 2.25) + ggtitle(expression(atop("Specified Crop Yields in Africa - 2018", atop(italic("Avg. precipitation (mm) under Country names"), "")))) +
  geom_sf_text(aes(label = africa_crop_selection_total$'2007'), size = 3, nudge_y = -1.25) +
  theme(plot.title = element_text(hjust = 0.5)) + xlab("Longitude") + ylab("Latitude")

# Animate the Specified crop yields in Africa from 1961-2018
# This will create a folder containing the different images of the graphs that were defined above
# it will also create an html file that will allow you to see the animation
saveHTML({
  oopt <- ani.options(interval = .8, nmax = 1)
  for (i in 1:ani.options("nmax")) {
    print(africa2_1961)
    print(africa2_1962)
    print(africa2_1963)
    print(africa2_1964)
    print(africa2_1965)
    print(africa2_1966)
    print(africa2_1967)
    print(africa2_1968)
    print(africa2_1969)
    print(africa2_1970)
    print(africa2_1971)
    print(africa2_1972)
    print(africa2_1973)
    print(africa2_1974)
    print(africa2_1975)
    print(africa2_1976)
    print(africa2_1977)
    print(africa2_1978)
    print(africa2_1979)
    print(africa2_1980)
    print(africa2_1981)
    print(africa2_1982)
    print(africa2_1983)
    print(africa2_1984)
    print(africa2_1985)
    print(africa2_1986)
    print(africa2_1987)
    print(africa2_1988)
    print(africa2_1989)
    print(africa2_1990)
    print(africa2_1991)
    print(africa2_1992)
    print(africa2_1993)
    print(africa2_1994)
    print(africa2_1995)
    print(africa2_1996)
    print(africa2_1997)
    print(africa2_1998)
    print(africa2_1999)
    print(africa2_2000)
    print(africa2_2001)
    print(africa2_2002)
    print(africa2_2003)
    print(africa2_2004)
    print(africa2_2005)
    print(africa2_2006)
    print(africa2_2007)
    print(africa2_2008)
    print(africa2_2009)
    print(africa2_2010)
    print(africa2_2011)
    print(africa2_2012)
    print(africa2_2013)
    print(africa2_2014)
    print(africa2_2015)
    print(africa2_2016)
    print(africa2_2017)
    print(africa2_2018)
  }}, img.name = "name_images",
  imgdir = "name_dir2",
  htmlfile = "specified_crop_yields_africa.html",
  title = "Specified Crop Yields in Africa 1961-2018",
  ani.height = 800,
  ani.width = 900
)

