# IMPORTS #######################################################
import os

import numpy as np
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.patches as mpatches
import argparse

# FUNCTIONS #####################################################
def get_dt(x):
    datestr = x
    format_dt = datetime.strptime(datestr, "%a, %d %b %Y %X %Z").month
    return format_dt

def get_yr(x):
    datestr = x
    yr = datetime.strptime(datestr, "%a, %d %b %Y %X %Z").year
    return yr

def make_plot(mo,yr,temp_usa,temp_mass,plot_dir):
    f, ax = plt.subplots(1,1,figsize=(10.1,6.1),dpi=100)
    col = temp_usa['grade']
    
    # Format legend patches
    # from https://matplotlib.org/tutorials/intermediate/legend_guide.html
    f_patch = mpatches.Patch(color='firebrick',label='F')
    d_patch = mpatches.Patch(color='orange',label='D-, D, D+')
    c_patch = mpatches.Patch(color='yellow',label='C-, C, C+')
    b_patch = mpatches.Patch(color='greenyellow',label='B-, B, B+')
    a_patch = mpatches.Patch(color='forestgreen',label='A-, A')
    grade_legend = ax.legend(handles=[a_patch,b_patch,c_patch,
                                   d_patch,f_patch],
                          prop={'size':10},title='Gun Control Grade',
                          loc=4,markerscale=6)
    grade_legend.get_title().set_fontsize('10')
    
    # Plot law shapefile
    colormap = plt.cm.get_cmap('RdYlGn')
    rcm = colormap.reversed()
    temp_usa.plot(col,categorical=True,ax=ax,cmap=rcm,alpha=0.9,
                 edgecolor='black')
    
    # Plot shooting occurrences
    if temp_mass.empty == False: 
        ms = temp_mass['Total_shot']*100
        temp_mass.plot(ax=ax,marker='o',color='powderblue',markersize=ms)
        # Get location for adding text
        lat = temp_mass.iloc[:,3]
        long = temp_mass.iloc[:,4]
        coords = np.column_stack((long,lat))
        total_shots = list(temp_mass['Total_shot'].values)
        # Plot "Total_shot" value over markers
        # from https://stackoverflow.com/questions/6282058/writing-numerical-values-on-the-plot-with-matplotlib
        for (x,y), val in zip(coords,total_shots):
            ax.text(x, y, val, ha='center', size=12,color='black',fontname='Arial Black')
            
    # Titles
    ax.text(-126,27,'Gun Laws vs. \nMass Shootings',
              fontweight='bold',fontsize=23, fontname='DIN Alternate') #DIN Alternate
    ax.text(-126,24.5,'Date: {}/{}'.format(mo,yr),
          fontweight='bold',fontsize=20, fontname='DIN Alternate')
    ax.text(-126,22.5,'Circle and value indicate total shot',
          fontweight='bold',fontsize=11, fontname='DIN Alternate')
    ax.axis('off')
    if mo<10:
        mo = '0'+str(mo)
    plt.savefig(plot_dir+str(mo)+'_'+str(yr)+'.png',bbox_inches='tight',dpi=100)
    plt.close(f)

# MAIN #########################################################
if __name__ == '__main__': 
    descrip = (
        'This script accepts a shapefile and two geocoded datasets with a temporal element. It\n'
        'combines them into a choropleth map for each date (month/year) with markers displaying\n'
        'the selected qualitative. All plots are generated in the specified directory.\n'
        'This original implementation was to compare gun law strictness and mass shootings from\n'
        '2009 to 2020.'
        )
    parse = argparse.ArgumentParser(description=descrip)
    args = parse.parse_args()

    # Directories: for reading in files and output map images
    file_dir = 'data' 
    plot_dir = 'plots/' 

    # Read in files 
    filenames = os.listdir(file_dir)

    # Clean shapefile - US States
    print('------ Cleaning shapefile to include only contiguous United States -------')
    usa = gpd.read_file(file_dir+'cb_2018_us_state_500k.shp')
    remove_gdf = ['United States Virgin Islands',
            'Commonwealth of the Northern Mariana Islands', 'Guam',
            'American Samoa','Puerto Rico','Alaska','Hawaii']
    usa_contig = usa[~usa.NAME.isin(remove_gdf)]

    # Clean and merge law strictness with shapefile, store in dictionary
    remove_df = ['Alaska','Hawaii']
    law_shp = {}
    print('------ Merging dataframes with shapefile -------')
    for i in filenames:
        if i.endswith('.csv'):
            # Get year from law csv, function as name for merged dataset
            name = i[-8:-4]
            # Path to law csv
            path = os.path.join(file_dir, i)
            # Read in csv, clean dataframe
            df = pd.read_csv(path)
            df = df.rename(columns={'state':'NAME'})
            df = df[~df.NAME.isin(remove_df)]
            df.grade.astype(str)
            df = df.replace('\n','', regex=True)
            # Merge law csv with shapefile, save as {year: dataframe} 
            # from https://geopandas.org/mapping.html
            law_shp[name] = usa_contig.merge(df, on='NAME')
    print('------ Shapefiles sucessfully stored in dict (key: year, value: geodataframe) -------')
            
    # Read in mass shootings geojson
    print('------ Reading in and cleaning occurrences geojson -------')
    mass = gpd.read_file(file_dir+'massshootings_g.geojson')
    # Format year and month into separate columns
    mass['month'] = mass['Date'].apply(get_dt)
    mass['year'] = mass['Date'].apply(get_yr)

    # Generate Plots 
    print('------ Generating plots for each month/year -------')
    for yr in range(2009,2021):
        for mo in range(1,13):
            # Acquire data for each year and month
            temp_mass = mass.loc[(mass['year'] == yr) & (mass['month'] == mo)]
            # Get law shapefile when applicable
            if yr in [2009,2010,2011,2012,2013,2014]: 
                temp_usa = law_shp['2014']
            elif yr == 2020:
                temp_usa = law_shp['2019']
            else:
                year = str(yr)
                temp_usa = law_shp[year]
            # Generate one plot per month/year
            make_plot(mo,yr,temp_usa,temp_mass,plot_dir)
    print('------ Plots generated and output in {} directory ------'.format(plot_dir))

