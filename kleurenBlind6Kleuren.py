# import libraries
import os
import csv
import collections
import numpy as np
import pandas as pd
from supplementary_functions import *

def edges_table_reader(filename, seperator):
    """
    import the dataas an edges table with nodes and edges
    Also returns a lookup table by which edges could be combined with their
    country names
    """
    edges_table = {}
    lookup_table = {}
    # open a file to read it in
    with open(filename, 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter= seperator)

        # enumerate gives you both the value and the indice
        for i, row in enumerate(reader):
            # because the computer starts counting from 0, do i + 1
            edges_table[i + 1] = [e for e in row[1:] if e]
            lookup_table[i + 1] = str(row[0])

    # now convert items to ints
    storage = []
    for key, item in edges_table.iteritems():
        for e in item:
            storage.append(int(e))
        edges_table[key] = storage
        storage = []
        
    # returns the edges and lookup tables
    return edges_table, lookup_table

def most_connected(edges_table):
    """
    returns the most connected countie as starting point based on
    an edgestable
    """
    num_connections = []
    counties = []
    
    # loop over all counties and get their number of connections
    for countie, borders in edges_table.items():
        num_connections.append(len(borders))
        counties.append(countie)
    
    # Make a pandas data frame from the data
    data = pd.DataFrame({'Length': num_connections,
                      'Countie': counties})
    # order the dataframe at first by number of borders
    data = data.sort_index(by = 'Length', ascending = False)
    data.index = data.Countie                
    return data
    

def get_shell(edges_table, start, ordered_frame, colors):
    """
    function returns the first shell around the starting point
    """
    shell = collections.OrderedDict()
    
    # for the first iteration there's only 1 start point to get shell from
    if isinstance(start, np.integer):
        connections = edges_table[start]  
        ordered_frame = ordered_frame.ix[connections] \
        .sort_index(by = 'Length', ascending = False)
        
    # in other iterations the shell is much larger than that it surrounds
    # just one countie. Then we take the entire second shell that is not
    # colored
    else:
        connections = []
        for countie in start:
            for child in edges_table.get(countie):
                if colors[child] == 0:
                    connections.append(child)
        ordered_frame = ordered_frame.ix[connections] 
        
    # loop over their grand_children
    for grand_child in ordered_frame['Countie']:
        shell[grand_child] = edges_table.get(grand_child)
            
    return shell
    
def is_conflict(edges_table, parent, colors):
    """
    function checks whether 2 counties next to each other have the same colour
    if so, there is a conflict
    """
    for child in edges_table.get(parent):
        if colors[child] != 0:
            if colors[parent] == colors[child]:
                return True
    return False
                  
def main():
    # Read in the data 
    edges_table, lookup_table = edges_table_reader("Pennsylvania_counties_list_new.csv", ",")

    # initialize the colors
    colors = {key: 0 for key in (edges_table)}

    # get the starting point and the shell
    ordered_frame = most_connected(edges_table)
    start = ordered_frame.iloc[0,0]
    shell = get_shell(edges_table, start, ordered_frame, colors)
    colors[start] += 1
    count = 1
    
    # now continue until all counties are colored
    while any ([color == 0 for color in colors.values()]):
    #while count < 4:
        for parent in shell:
            colors[parent] += 1
            # keep checking for conflicts, if so upgrade
            while (is_conflict(edges_table, parent, colors)):
                colors[parent] += 1           
        # get to the next shell
        shell = get_shell(edges_table, shell, ordered_frame, colors)
        count = count + 1
        
    # now let's combine the names of the lookup table with those of
    dictionary_colors = {}
    for key, key1 in zip(lookup_table, colors):
        if key == key1:
            dictionary_colors[lookup_table[key]] = colors[key1]
    return dictionary_colors
        
dictionary_colors = main()
color_map(colours =  ['purple','pink', 'red', 'blue', 'yellow', 'green'], \
low_lat = 39, up_lat = 43, low_lon = -82, up_lon = -74)
 
def color_map(colours, low_lat, up_lat, low_lon, up_lon):    
    """
    This function colors the map. It takes a list of colors to use
    4 map coordinates to use 
    For Pensylvania: low_lat = 39, up_lat = 43, low_lon = -82, up_lon = -74
    For Rajachstan:
    For Spain: 
    A link to a shapefile
    A boolean country 
    """
    # Import libraries
    from matplotlib import pyplot as plt
    from matplotlib import cm
    from matplotlib.collections import LineCollection
    from matplotlib.patches import Polygon
    from mpl_toolkits.basemap import Basemap
    import shapefile
    
    # Create a figure and a subplot
    fig = plt.figure(figsize=(15.7,12.3))
    ax = plt.subplot(111)
    
    # make the map projection. Choose mercator projection
    m = Basemap(projection='merc', resolution='l',llcrnrlat = low_lat, \
    urcrnrlat = up_lat, llcrnrlon = low_lon, urcrnrlon = up_lon, \
    area_thresh=10000)
      
    m.drawcoastlines()  # draw the coastlines
    m.drawstates() # draw the states
    m.drawcountries() # draw countries
    m.drawmapboundary(fill_color='white') # draw the boundary

    # read in the shapefile and draw them
    m.readshapefile('./shapefile/PA_counties_clip', 'countries_sf', drawbounds=True)

    #print m.countries_sf_info[0]['NAME'] # this is how you get the state names


    # look over the shapes and actual data
    for shape, countie in zip(m.countries_sf, m.countries_sf_info):
        # now loop over all the keys and values in the dictionary
        for lookup in dictionary_colors.items():
            # compare the countie name of the data with the countie name in the lookup table
            if lookup[0] == countie['NAME']:
                # then choose a country from our list depending on the value of the key
                color = colours[lookup[1]]          
        poly = Polygon(shape, facecolor=color)
        plt.gca().add_patch(poly)
    
    plt.show()
        

