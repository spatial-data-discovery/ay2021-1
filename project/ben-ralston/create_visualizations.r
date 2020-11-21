# Author: Ben Ralston
# Date: 2020-11-20
# 
# Description: This script reads two CSV files, unemployment_by_state.csv and
# monthly_covid_cases_by_state.csv, and creates visual representations of the
# data stored in them. It saves these visualizations in nine separate TIFF files
# named map_1.tiff, map_2.tiff, ..., map_9.tiff.

# Load necessary packages:
library(ggplot2)
library(usmap)
library(stringr)
library(maptools)
library(rgdal)

# Load the datasets we made in Python:
unemployment <- read.csv(file.path("IntermediateOutput", "unemployment_by_state.csv"))
covid <- read.csv(file.path("IntermediateOutput", "monthly_covid_cases_by_state.csv"))

# Adjusts latitude/longitude for displaying on map:
covid_transformed <- usmap_transform(covid)

# Add row to covid_transformed with location way below bounds of map.
# The cases per capita value of this new row is slightly higher than the highest
# value in the actual data. This causes the scale of the circles to remain constant
# between different months. Otherwise, the scale readjusts and we don't get an
# accurate representation of covid cases. There's almost certainly a better way to
# do this, but I couldn't figure out how lol.
new_df <- data.frame(0, 0, "NA", "Base", 1500, 1500, 1500, 1500, 1500,
                     1500, 1500, 1500, 1500, 1500, 1500, -200000, -4000000)
names(new_df) <- names(covid_transformed)
new_transformed <- rbind(covid_transformed, new_df)

year <- 2020

for (month in 1:9) {
  col_name <- sprintf("X%d.%02d.01", year, month)
  sub <- sprintf("%s, %d", month.name[month], year)

  # Create smaller df with only the current months covid case numbers. Then rename
  # the data column so we can always use the same name but get different parts of
  # the data.
  rows_to_keep <- new_transformed[ ,month+4] > 0
  cols_to_keep <- c(month+4, 16, 17)
  monthly_df <- new_transformed[rows_to_keep, cols_to_keep]
  names(monthly_df)[1] <- "cases_per_capita"

  output_name <- sprintf("map_%d.tiff", month)
  output_path <- file.path("IntermediateOutput", output_name)
  
  # Saves plot to TIFF format instead of displaying it to us:
  tiff(output_path, units="in", width=8, height=5, res=400)

  print(plot_usmap(data = unemployment, values = col_name, color = "white") +

        # Set bounds so the extra point isn't shown:
        scale_y_continuous(limits = c(-2550000, 850000)) +

        # Display unemployment rate as color of each state:
        scale_fill_continuous(name = "Unemployment\nRate (%)", label = scales::comma,
                              limits=c(2,20), low = "dodgerblue4", high = "orange",
                              na.value = "orange") +

        # Display covid cases as red circles:
        geom_point(data = monthly_df, color = "red", alpha = 0.85,
                   aes(x = lon.1, y = lat.1, stroke = 0, size = cases_per_capita)) +

        # Add/format titles and such:
        labs(title = "US Unemployment During the Pandemic", subtitle = sub,
             size = "New COVID-19 Cases\nper 100K People") +
        theme(plot.title = element_text(hjust = 0.5, face = "bold"),
              plot.subtitle = element_text(hjust = 0.5), legend.position = "right"))

  dev.off()
}
