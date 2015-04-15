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

# List of all colors, index of list corresponds with countie number.
# Start with each countie in the edges_list as coloured = False
def initialize_colouring():
    coloured.append('start coloured list')
    colors.append('start colors list')
    for i in range(1, len(edges_table) + 1):
        colors.append(1)
    for i in range(1, len(edges_table) + 1):
        coloured.append(False)


# Color the countie of interest according to the surround edges. 
# if no edges of interest, passes. 
def single_countie_colliss(countie, interest_edges):
    try:
        if colors[countie] == colors[interest_edges[0]]:
            colors[countie] += 1
            try:
                if colors[countie] == colors[interest_edges[1]]:
                    colors[countie] += 1
            except:
                pass
    except:
        pass

# Color the shell, defined in edges_list. Each countie increases color by 1, 
# and becomes coloured. Second step is for each countie to check for collissions
# in its surrounding counties, and change the color if this is the case. 
def color_shell(edges_list):
    for countie in edges_list:
        colors[countie] += 1
        coloured[countie] = True
    for countie in edges_list:
        aanliggend = edges_table.get(countie)
        x = [item for item in aanliggend if item in edges_list]
        single_countie_colliss(countie, x)
    


# Find countie with most adjacent countries which are not currently coloured.
# Returns the resulting countie number that is largest in the list. 
def find_max(edges_list):
    maximum = 0
    result = 0
    for key in edges_list:
        x = 0
        for item in edges_table.get(key):
            if coloured[item] == False:
                x += 1
        if x > maximum:
            maximum = x
            result = key
    return result

# Takes a countie as input and returns a list of the surrounding counties 
# that are not currently coloured. 
def get_uncoloured_list(countie):
    uncoloured_list = []
    edges = edges_table.get(countie)
    for item in edges:
        if coloured[item] == False:
            uncoloured_list.append(item)
    return uncoloured_list

# Start of colouring first shell around maximum edges-countie. Only to be used
# for the first shell. 
def color_first_shell():
    maximum = find_max(edges_table)
    coloured[maximum] = True
    next_to = edges_table.get(maximum)
    color_shell(next_to)

# Start of colouring higher level, new shell. Starts coloring process at the
# countie with the highest amount of uncoloured edges. 
def higher_level_shells(edges_shell):
    maximum = find_max(edges_shell)
    if maximum == 0:
        return 0
    maximum_edges = get_uncoloured_list(maximum)
    color_shell(maximum_edges)
    for item in edges_shell:
        uncoloured_edges = get_uncoloured_list(item)
        color_shell(uncoloured_edges)

            
# check for collissions, error checking the coloring process. Returns true
# if there are no colissions, otherwise returns the first occurring collission
# and false. 
def collission_test():
    for key in edges_table:
        aanliggend = edges_table.get(key)
        for countie in aanliggend:
            if colors[key] == colors[countie]:
                print lookup_table[key], lookup_table[countie]
                return False
    return True


# prints each countie and corresponding 'color', in random order. 
def print_counties_colors():
    look_up = {}
    i = 1
    for i in range(len(edges_table)):
        look_up[lookup_table[i]] = colors[i]
        i += 1
    return look_up

# Checks whether all counties are colored
def not_fully_coloured(boolean_list):
    for item in boolean_list:
        if item == False:
            return True
    return False


if __name__ == '__main__':

    edges_table, lookup_table = penssylvania_dict_reader("Pennsylvania_counties_list.csv", ",")
    
    colors = []
    coloured = []

    initialize_colouring()

    color_first_shell()

    next_to = edges_table.get(33)

    for item in next_to:
        edges = edges_table.get(item)
        higher_level_shells(edges)
        for countie in edges:
            new_edges = edges_table.get(countie)
            higher_level_shells(new_edges)
            for land in new_edges:
                newer_edges = edges_table.get(land)
                higher_level_shells(newer_edges)
                for another in newer_edges:
                    newest_edges = edges_table.get(another)
                    higher_level_shells(newest_edges)


    dictionary_colors = {}
    for i in range(1, len(edges_table) + 1):
        dictionary_colors[lookup_table[i]] = colors[i]
        
### Making the map
colours = [1, 'red', 'blue', 'yellow', 'green']
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
            resolution='l',llcrnrlat=39,
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
    for lookup in dictionary_colors.items():
        # compare the countie name of the data with the countie name in the lookup table
        if lookup[0] == countie['NAME']:
            # then choose a country from our list depending on the value of the key
            color = colours[lookup[1]]          
    poly = Polygon(shape, facecolor=color)
    plt.gca().add_patch(poly)
    
plt.show()


