### Election Date Web Scraper Script
### Amy Hilla
### Spatial Data Discovery, Fall 2020

### Summary: this script automates the web scraping process for US election dates from Wikipedia

from bs4 import BeautifulSoup
import requests 
import google
import re
import pandas as pd
from datetime import datetime
import dateutil.parser as dparser
from urllib import request
import wikipedia
import numpy as np
from googlesearch import search 

## read in the input file
idea_data = pd.read_csv('idea_data.csv')

## select just the rows for the US
USA = idea_data[idea_data['Country'] == 'United States']

newdf = pd.DataFrame()
newdatadict = {}

## For loop to search for the exact date of the election for each election in the data
for year in USA['Year'].unique():
    newdatadict['year'] = year
    #electiontype = list(USA[USA['Year'] == year]['Election type'])[0]

    # to search 
    newdatadict['date'] = np.nan
    try:
        query =  str(year) + ' United States Election Wikipedia'
        results = search(query, tld="co.in", num=10, stop=1, pause=1)
        results_list= []

        for j in results: 
            #print(j) 
            results_list.append(j)
            
        try:
            url = results_list[0]
            html = request.urlopen(url).read().decode('utf8')
            html[:60]
            soup = BeautifulSoup(html, 'html.parser')
            title = (soup.find('title')).string
            #title = str(title).replace('wikipedia', '')
            #title = str(title).replace('- Wikipedia', '')
            try: 
                wiki = wikipedia.page(title)
                string_cstext = wiki.content
                try:
                    m = re.search('\w{3,9}?\s\d{1,2}?,\s\d{4}?', string_cstext)
                    print(m)
                    ## take this date parser part out of the for loop 
                    date = dparser.parse(m.group(),fuzzy=True)
                    newdatadict['date'] = date
                    newdf = newdf.append(newdatadict, ignore_index = True)
                    print('USA' + ' ' + str(year) + ' election date is ' + str(date))
                except:
                    try:
                        m = re.search('\d{1,2}?\s\w{3,9}?', string_cstext)
                        ## take this date parser part out of the for loop 
                        date = dparser.parse(m.group(),fuzzy=True)

                        date = date.replace(year = year)

                        newdatadict['date'] = date
                        newdf = newdf.append(newdatadict, ignore_index = True)
                        print('USA' + ' ' + str(year) + ' election date is ' + str(date))
                    except:
                        rowerror = 'USA ' + str(year)
                        print('failed to parse data from: ' + rowerror + ', appending null')
                        newdatadict['date'] = np.nan
                        newdf = newdf.append(newdatadict, ignore_index = True)
            except:
                print('failed to get wiki content')
                newdatadict['date'] = np.nan
                newdf = newdf.append(newdatadict, ignore_index = True)
        except:
            print('failed to parse wikipedia page title from google search results ' + year)
            newdatadict['date'] = np.nan
            newdf = newdf.append(newdatadict, ignore_index = True)

    except:
        rowerror = 'USA ' + str(year)
        print('google search failed for: ' + rowerror)

## this script does not run perfectly
## fill in the following election dates manually:

newdf.iloc[6, newdf.columns.get_loc('date')] =  np.datetime64(datetime(2006,11,7))
newdf.iloc[12, newdf.columns.get_loc('date')] =  np.datetime64(datetime(1994,11,8))
newdf.iloc[14, newdf.columns.get_loc('date')] =  np.datetime64(datetime(1990,11,6))
newdf.iloc[16, newdf.columns.get_loc('date')] =  np.datetime64(datetime(1986,11,4))
newdf.iloc[22, newdf.columns.get_loc('date')] =  np.datetime64(datetime(1974,11,5))
newdf.iloc[24, newdf.columns.get_loc('date')] =  np.datetime64(datetime(1970,11,3))
newdf.iloc[25, newdf.columns.get_loc('date')] =  np.datetime64(datetime(1968,11,5))
newdf.iloc[28, newdf.columns.get_loc('date')] =  np.datetime64(datetime(1962,11,6))
newdf.iloc[36, newdf.columns.get_loc('date')] =  np.datetime64(datetime(1946,11,5))
newdf.iloc[8, newdf.columns.get_loc('date')] =  np.datetime64(datetime(2002,11,5))


## add a "day" column to make the output table easier to work with in the netCDF processing script
newdf['day'] = pd.DatetimeIndex(newdf['date']).day

## save to a new csv file
newdf.to_csv('us_elex_dates_test2.csv')