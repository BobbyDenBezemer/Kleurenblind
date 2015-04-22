# import libraries
import os
import csv
import collections
import numpy as np
import pandas as pd
from making_map import *

# Import function that makes and colors the actual map
# import map_making
# map_making.make_map()

def penssylvania_dict_reader(filename, seperator):
    #TODO change name of the function
    """
    import the data as a dictionary and the values as lists of ints
    """
    edges_table = {}
    lookup_table = {}

    # open a file to read it in
    with open(filename, 'r') as csvfile:
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
    return edges_table, lookup_table



edges_table, lookup_table = penssylvania_dict_reader("rathjastan_districts_list_comma.csv", ",")

def most_connected(edges_table):
    # returns the most connected countie based on a dictionary
    longest = [] # TODO rename to something more suitable
    countie_longest = []
    
    # loop over all counties and their borders
    for countie, borders in edges_table.items():
        longest.append(len(borders))
        countie_longest.append(countie)
    data = pd.DataFrame({'Countie': countie_longest,
                         'Length': longest})
    data = data.sort_index(by = 'Length', ascending = False)
    data.index = data.Countie
    return data
    
test1 = most_connected(edges_table)  

def get_shell(edges_table, start, ordered_frame, is_colored = None):
    # function returns the first shell around the starting point
    # in the order of counties with most borders within the shell
    shell = collections.OrderedDict()
    
    #TODO turn start into a list even for the first iteration.
    
    # for the first iteration there's only 1 start point to get shell from
    if isinstance(start, np.integer):
        connections = edges_table[start]  
        most_connected = ordered_frame.ix[connections] \
        .sort_index(by = 'Length', ascending = False)
        
    # in other iterations the shell is much larger than that it surrounds
    # just one countie. Then we take the entire second shell that is not
    # colored
    else:
        total_colored = 0
        connections = []
        for countie in start:
            for child in edges_table.get(countie):
                print countie, child
                if child not in is_colored:
                    connections.append(child)
                else:
                    total_colored = total_colored + 1
                    print 'child is colored'
            ordered_frame.ix[countie].Length - total_colored
            print total_colored
            total_colored = 0
        most_connected = ordered_frame.ix[connections] \
        .sort_index(by = 'Length', ascending = False)
        
    # loop over their grand_children
    for grand_child in most_connected['Countie']:
        shell[grand_child] = edges_table.get(grand_child)
            
    return shell
  
#test = get_shell(edges_table, 33, ordered_frame)  
#test, test2 = get_shell(edges_table, start = [33,45,26,40,48,25,42,43,32,44], \
#ordered_frame = ordered_frame, is_colored = [33,45,26,40,48,25,42,43,32,44] )
    
def is_conflict(parent, colors, is_colored):
    # function checks whether 2 countie next to each other have the same colour
    # TODO replace countie for child    
    # loop over 
    for countie in edges_table.get(parent):
        if countie in is_colored:
            print is_colored
            if colors[parent] == colors[countie]:
                print "conflict", parent, countie
                return True
    return False 
 
#parent = 33   
#for countie in edges_table.get(parent):
#    if countie in is_colored:
#        print "Hello"
                      
def main(edges_table):
    # length of counties
    number_counties = len(edges_table)
    # initialize the colors
    colors = {key: 0 for key in (edges_table)}
    # TODO remove is_colored. 0 will mean that a countie is colored
    is_colored = []

    # get the starting point and the shell and set starting as colored
    ordered_frame = most_connected(edges_table)
    # TODO turn start into a list
    start = ordered_frame.iloc[0,0]
    shell = get_shell(edges_table, start, ordered_frame)
    colors[start] += 1
    is_colored.append(start)
    count = 1

    # now continue until all counties are colored
    # TODO:  all (i != 0 for i in range(1,67)).
    #while len(is_colored) < number_counties:
    while count < 8:
        for parent in shell:
            colors[parent] += 1
            # keep checking for conflicts, if so upgrade
            while (is_conflict(parent, colors, is_colored)):
                colors[parent] += 1
            if parent not in is_colored:
                is_colored.append(parent)
        # get to the next shell
        shell = get_shell(edges_table, shell, ordered_frame, is_colored)
        count = count + 1
    
    return colors
        
colors = main(edges_table)
 
# now let's combine the names of the lookup table with those of
dictionary_colors = {}
for key, key1 in zip(lookup_table, colors):
    if key == key1:
        dictionary_colors[lookup_table[key]] = colors[key1]
        
### Making the map
colours = ['purple','pink', 'red', 'blue', 'yellow', 'green']
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.collections import LineCollection
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
import shapefile
    
# just some standard matplob lib syntax to add a figure and then make a subplot
fig = plt.figure(figsize=(15.7,12.3))
ax = plt.subplot(111)
    
# make the map projection. Choose mercator and define upper and lower boundaries
# urcrnrlat = upper right corner lattitude, urcrnrlon = upper right corner longitude
# llcrnlat = lower left corner lattitude, llcrnrlon = lower left corner longitude
# For Pensylvania, use following values:
# lat_down = 39, lon_down = -82, lat_up = 43, lon = -74 
    
# For Spain
# lat_up = 4, lon_up = 44, lat_down = 9, lon_down = 36
    
# For Rajistan
lat_up = 31
lon_up = 79
lat_down = 23
lon_down = 69
    
# For India
#lat_up = 30
#lon_up = 92
#lat_down = 8 
#lon_down = 66
m = Basemap(projection='merc',
            resolution='l',llcrnrlat= lat_down,
            llcrnrlon = lon_down, urcrnrlat = lat_up,
            urcrnrlon = lon_up, area_thresh=10000)
        
m.drawcoastlines()  # draw the coastlines
#m.drawstates() # draw the states
#m.drawcountries() # draw countries
m.drawmapboundary(fill_color='white') # draw the boundary
    
# read in the shapefile and draw them
m.readshapefile('./shapefile/India/IND_adm2', 
                'countries_sf', drawbounds=True)
    
print len(m.countries_sf) #number of shapes, so 69
for countie in m.countries_sf_info:
    if countie['NAME_1'] == 'Rajasthan':
        print countie
 
#print m.countries_sf_info

# look over the shapes and actual data
for shape, countie in zip(m.countries_sf, m.countries_sf_info):
    if countie['NAME_1'] == 'Rajasthan':
# now loop over all the keys and values in the dictionary
        for lookup in dictionary_colors.items():
            print lookup[0], countie['NAME_2']
            # compare the countie name of the data with the countie name in the lookup table
            if lookup[0] == countie['NAME_2']:
                # then choose a country from our list depending on the value of the key
                color = colours[lookup[1]] 
                break
            else:
                color = "gray"
        poly = Polygon(shape, facecolor=color)
        plt.gca().add_patch(poly)
        
plt.show() 
        

