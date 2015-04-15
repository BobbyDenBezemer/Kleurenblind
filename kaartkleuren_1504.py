import os
import csv
import collections
import numpy as np
import random

os.chdir("C:\Users\Bobby\Documents\Kleurenblind")
    
def penssylvania_dict_reader(filename, seperator):
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

    
    
edges_table, lookup_table = penssylvania_dict_reader("Pennsylvania_counties_list.csv", ",")


colors = {}
is_colored = []

# returns the most connected countie based on a dictionary
def most_connected(edges_table):
    longest = 0
    countie_longest = 0
    for countie, borders in edges_table.items():
        #print countie, borders
        if len(borders) > longest:
            longest = len(borders)
            county_longest = countie      
    return county_longest
    
def get_shell(edges_table, start):
    # nu willen we dus een subset counties hebben die alleen in de shell zitten
    keys = {}
    length =[]
    for borders in edges_table[start]:
        for shell_border in edges_table[borders]:
            if shell_border in edges_table[start]:
                length.append(shell_border)
        keys[borders] = length
        length = []
    return keys
    
test = get_shell(edges_table, 33)

def color_counties(county):
    if county not in is_colored:
        colors[county] = 0 # hier moet beter algoritme komen dat bepaalt welke kleur
        is_colored.append(county)
    
    
def main():
    start = most_connected(edges_table)
    shell = get_shell(edges_table, start)
    
    
        
    # now get the shell country where you will start coloring
    color_start = max(keys, key=lambda x:len(keys[x]))
    return color_start

i = 1
while i <= len(edges_table):
    colors.append(1)
    i += 1
    
# Optie 2)
colors = []
for i in range(67):
    colors.append(1)

# change color of each countie to satisfy constraints
for key in edges_table:
    # eigenlijk moeten we hier beginnen met het land met meeste grensen
    # loop over alle keys heen en check len values
    aanliggend = edges_table.get(key)

    for i in range(4):
        for countie in aanliggend:
            if colors[key] == colors[countie]:
                colors[key] += 1


# check for collissions
def collission_test():
    for key in edges_table:
        aanliggend = edges_table.get(key)
        for countie in aanliggend:
            if colors[key] == colors[countie]:
                print lookup_table[key], lookup_table[countie]
                return False
    return True

print colors
print collission_test()



# prints each countie and corresponding 'color'
def print_counties_colors():
    look_up = {}
    i = 1
    while i <= len(edges_table):
        look_up[lookup_table[i]] = colors[i] - 1
        i += 1
    return look_up

data_lookup = print_counties_colors()

colours = ["red", "blue", "green", "pink", "purple", "yellow"]

### Making the map
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
m = Basemap(projection='merc',
            resolution='h',llcrnrlat=39,
    urcrnrlat=43,
    llcrnrlon=-82,
    urcrnrlon=-74, area_thresh=10000)
    

  
m.drawcoastlines()  # draw the coastlines
m.drawstates() # draw the states
m.drawcountries() # draw countries
m.drawmapboundary(fill_color='white') # draw the boundary

# read in the shapefile and draw them
m.readshapefile('./shapefile/PA_counties_clip', 'countries_sf', drawbounds=True)

print len(m.countries_sf) #number of shapes, so 69
test = []
#for i in range(len(m.countries_sf_info)):
#    if m.countries_sf_info[i]['NAME'] not in test:
#        test.append(m.countries_sf_info[i]['NAME'])
print m.countries_sf_info[0]['NAME'] # this is how you get the state names


# look over the shapes and actual data
for shape, countie in zip(m.countries_sf, m.countries_sf_info):
    # now loop over all the keys and values in the dictionary
    for lookup in data_lookup.items():
        # compare the countie name of the data with the countie name in the lookup table
        if lookup[0] == countie['NAME']:
            # then choose a country from our list depending on the value of the key
            color = colours[lookup[1]]          
    poly = Polygon(shape, facecolor=color)
    plt.gca().add_patch(poly)
    
plt.show()
