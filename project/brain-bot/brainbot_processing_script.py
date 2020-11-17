# By: Brian Wu
# Last Updated: 2020-11-17

# About the Script:
# This script reads a CSV file taken from MoveBank.org and
# writes data into another CSV file. This is done to
# simplify the visualization and the used data.

import csv

# The list below helps keep track of the number of
# individual ducks that data is accounted for.
list_of_individuals = []
with open('Sea_Duck_Migration.csv', 'w', newline='') as csvfile_to:
    writer = csv.writer(csvfile_to)
    writer.writerow([ "timestamp", "location-long", "location-lat", "tag-local-identifier"])
    # Variable definitions:
    #
    # timestamp: The date in which the duck's movement was tracked
    # location-long: longitude location of the duck
    # location-lat: latitude location of the duck
    # tag-local-identifier: The tag number that helps identify individual ducks
    with open('Migration Patterns of Pacific Sea Ducks.csv', newline='') as csvfile_from:
        reader = csv.DictReader(csvfile_from)
        for row in reader:
            # We'll only use the first 5 individual ducks found in the read CSV file.
            # That way, the visualization won't be too messy.
            if(len(list_of_individuals) > 5):
                print("Time to stop")
                break;
            if(row['tag-local-identifier'] not in list_of_individuals):
                list_of_individuals.append(row['tag-local-identifier'])
            # We'll only use data for May 2014.
            # We'll also only display certain columns of data in our new CSV file.
            # Only some data aspects are useful for visualization and understanding the project.
            if(row['timestamp'][0:7] == '2014-05' ):
                writer.writerow([ row['timestamp'], row['location-long'], row['location-lat'], row['tag-local-identifier'] ])

print(list_of_individuals)
print('Information successfully transferred')
