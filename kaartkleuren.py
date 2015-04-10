import csv
import collections
import numpy as np
    
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


# list of all colors, index of list corresponds with countie number - 1
colors = []
colors.append('start colors list')
i = 1
while i <= len(edges_table):
    colors.append(1)
    i += 1

# change color of each countie to satisfy constraints
for key in edges_table:
    aanliggend = edges_table.get(key)

    i = 0
    while i < 4:
        for countie in aanliggend:
            if colors[key] == colors[countie]:
                colors[key] += 1
        i += 1


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

data = print_counties_colors()

colours = ["red", "blue", "green", "pink", "purple", "yellow"]

### Making the map
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.collections import LineCollection
from matplotlib.patches import Polygon
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
print m.countries_sf_info[0]#metadata, so the columns
#print m.countries_sf_info

#plots the shapes as Polygons with so far a random color
for shape, country in zip(m.countries_sf, m.countries_sf_info):
    poly = Polygon(shape, facecolor=cm.YlGn(np.random.rand()))
    plt.gca().add_patch(poly)
    
plt.show()
