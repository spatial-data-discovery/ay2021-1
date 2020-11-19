# Author: Natalie Larsen
# Last Updated: 2020-11-19
#
# This script reads in IBTrACS historic tropical cyclone data from the local directory and
# processes the dataset for visualization. It outputs a new .csv file for map visualization,
# as well as bar charts that visualize tropical cyclone counts.
#
import argparse
import warnings
import pandas as pd
from matplotlib import pyplot as plt

#Plot tropical cyclone counts by season (year) and ocean basin
def plot_all():
    plot_data_final.plot(kind='bar', stacked=True)
    plt.title("Named Tropical Cyclones By Season and Basin")
    plt.xlabel("Season")
    plt.ylabel("Number of Named Tropical Cyclones")
    plt.legend(labels = ('East Pacific', 'South Pacific', 'West Pacific',
                        'North Atlantic','North Indian', 'South Indian'
                        ),
               loc = 'center', bbox_to_anchor=(0.5, -0.3), ncol= 3
               )
    plt.savefig('cyclone_plot.png', bbox_inches='tight')

#Plot just the North Atlantic basin hurricanes
def plot_NA():
    plot_dataNA = plot_data_final['NA']
    fig = plt.figure()
    plot_dataNA.plot(kind='bar')
    plt.title("Named North Atlantic Tropical Cyclones")
    plt.xlabel("Season")
    plt.ylabel("Number of Named Tropical Cyclones")
    plt.savefig('cycloneNA_plot.png', bbox_inches='tight')

if __name__ == "__main__":
    parser= argparse.ArgumentParser(description = "This script reads in IBTrACS historic tropical cyclone data \
                                    from the local directory and processes the dataset for visualization. \
                                    It outputs a new .csv file for map visualization, \
                                    as well as bar charts that visualize tropical cyclone counts.")
    args = parser.parse_args()

    warnings.filterwarnings("ignore") #To avoid data type warning output

    print("\nReading in data...\n")
    
#Read in .csv using pandas, make dataframe, get columns of interest
    data_raw = pd.read_csv("ibtracs.since1980.list.v04r00.csv")
    data = data_raw[['SID', 'SEASON', 'NAME', 'BASIN', 'LAT', 'LON']]

    print("--------Processing--------\n")
    #Clean up the data some
    data = data.drop([0])
    data = data.fillna('NA')
    data['SEASON'] = data['SEASON'].astype('string')

    #Then, we will simplify and only look at location of formation
        #(Or, each first row with a new storm ID)
    data = data.drop_duplicates(subset='SID', keep='first')

#Next, process data for map visualization and export to new .csv file
    hurricane_form_data = data[['SID', 'SEASON', 'LAT', 'LON']]
    hurricane_form_data.to_csv('ibtracs_processed.csv', index = False)

#Next, process data for bar chart visualization
    plot_data = data[['SID', 'SEASON', 'NAME', 'BASIN']]
    #Get all named storms
    plot_data_filtered = plot_data[plot_data['NAME'] != 'NOT_NAMED']
    plot_data_filtered = plot_data_filtered[['SID', 'SEASON', 'BASIN']]
    #Get number of storms each season
    plot_data_filtered.groupby(['SEASON', 'BASIN']).count()
    plot_data_filtered = plot_data_filtered.groupby(['SEASON', 'BASIN'])['SID'].count().reset_index(name='STORM_COUNT')
    #Reformatting
    plot_data_final = plot_data_filtered.pivot_table(values='STORM_COUNT', index='SEASON', columns='BASIN', aggfunc='first')
    plot_data_final = plot_data_final.fillna(0)
    plot_data_final = plot_data_final.drop(['2021']) #Only interested in 1980-2020
    plot_data_final = plot_data_final[['EP', 'SP', 'WP', 'NA', 'NI', 'SI']]

    plot_all()

    plot_NA()

    print("Complete! New files in local directory\n")
