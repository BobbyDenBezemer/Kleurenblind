# import libraries
import os
import collections
import numpy as np
import pandas as pd
import data_loading
import time

def most_connected(edges_table):
    """
    returns the most connected countie as starting point based on
    an edges table
    """
    num_connections = []
    counties = []
    
    # loop over all counties and get their number of connections
    for countie, borders in edges_table.items():
        num_connections.append(len(borders))
        counties.append(countie)
    
    # Make a pandas data frame from the data
    data = pd.DataFrame({'Num_borders': num_connections,
                      'Countie': counties})
    # order the dataframe at first by number of borders
    data = data.sort_index(by = 'Num_borders', ascending = False)
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
        
        # get the data in order of the most connected counties first
        ordered_frame = ordered_frame.ix[connections] \
        .sort_index(by = 'Num_borders', ascending = False)
        
    # in other iterations the shell is much larger than that it surrounds
    # just one countie. Then we take the entire second shell that is not
    # colored
    else:
        connections = []
        for node in start:
            for child in edges_table.get(node):
                if colors[child] == 0:
                    connections.append(child)
        connections = list(set(connections))
        ordered_frame = ordered_frame.ix[connections] \
        .sort_index(by = 'Num_borders', ascending = False)
        
    for grand_child in ordered_frame['Countie']:
        shell[grand_child] = edges_table.get(grand_child)
            
    return shell
        
def order_shell(edges_table, shell, ordered_frame): 
    """
    function that returns the order in which the shell should be coloured
    It starts with the focal node which is the most connected node of the shell
    It then moves to its neighbour and so on
    """
    shell_order = [shell.keys()[0]]
    focal_node = shell.keys()[0]
    count = 0
    first_neighbour = 0
    
    # continue until the entire shell is ordered
    while len(shell_order) != len(shell.keys()):
        # loop over all the connections of the focal node. If they are in the shell
        # not ordered yet and it's the first neighbour, order them
        for edge in edges_table.get(focal_node):
            if edge in shell.keys() and edge not in shell_order and first_neighbour == 0:
                shell_order.append(edge)
                first_neighbour += 1

            # if the focal node has not been ordered, order it now
            elif focal_node not in shell_order:
                shell_order.append(focal_node)
        # Try to get a new focal node after the first neighbour of the first
        # focal node has been selected
        try:
            if len(shell_order) == len(shell.keys()):
                break
            count += 1
            #print 'count', count
            focal_node = shell_order[count]
            #print 'focal node', focal_node
            first_neighbour = 0
            
        # If there's no new focal node to go to from a specific point in the shell
        # then return to the children of other nodes that are already ordered. 
        # If these children arent in the shell either or they are already given an order, then
        # pick the next node from the shell with most connections
        except IndexError:
            focal_node = 0
            while focal_node == 0:
                for ordered_node in shell_order:
                    #print ordered_node
                    for child in edges_table.get(ordered_node):
                        if child in shell.keys() and child not in shell_order:
                            #print 'hello'
                            focal_node = child
                            shell_order.append(focal_node)
                            #print shell_order, focal_node
                # apparently all the children of ordered nodes are already given
                # an order or they aren't in the shell
                if focal_node == 0:
                    for node, garbage in ordered_frame.iterrows():
                        if node in shell and node not in shell_order:
                            #print 'node', node
                            focal_node = node
                            first_neighbour = 0
                            break
                        
            #print 'shell_order', shell_order
            #print 'shell', shell
            
    #print shell_order
    return shell_order
    
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
    
def color_map(colours, low_lat, up_lat, low_lon, up_lon, dictionary_colors):    
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
    fig = plt.figure(figsize=(4,4))
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

    plt.tight_layout(pad = 0)
    plt.show()
                  
if __name__ == '__main__':
    # Read in the data 
    edges_table, lookup_table = data_loading.edges_table_reader("Pennsylvania_counties_list_new.csv", ",")
    edges_table = data_loading.social_graph_reader("netwerk1.csv", ",")

    trials = 0
    unique_colors = []
    runtime = []
    

    while True:
        trials += 1
        print 'finding solution: #', trials
        if trials > 1000:
            break

        start = time.clock()
        # initialize the colors
        colors = {key: 0 for key in (edges_table)}
    
        # get the starting point and the shell
        ordered_frame = most_connected(edges_table)
        start = ordered_frame.iloc[0,0]
        shell = get_shell(edges_table, start, ordered_frame, colors)
        shell = order_shell(edges_table, shell, ordered_frame)
        colors[start] += 1
        count = 1
        
        # now continue until all counties are colored
        while any ([color == 0 for color in colors.values()]):
        # while count < 7: To color shell by shell
            for parent in shell:
                colors[parent] += 1
                # keep checking for conflicts, if so upgrade
                while (is_conflict(edges_table, parent, colors)):
                    colors[parent] += 1           
            # get to the next shell
            try:
                shell = get_shell(edges_table, shell, ordered_frame, colors)
                shell = order_shell(edges_table, shell, ordered_frame)
                #print shell
            # when there is no shell anymore, algorithm is finished.
            except:
                IndexError
            count = count + 1
            
        end = time.clock()
        runtime.append(end - start)
        # now let's combine the names of the lookup table with those of
        dictionary_colors = {}
        for key, key1 in zip(lookup_table, colors):
            if key == key1:
                dictionary_colors[lookup_table[key]] = colors[key1]
      
        uniques = set(colors.values())
        unique_colors.append(len(uniques))
        
    print 'unique colors: ', unique_colors
    print 'runtime: ', runtime
        
#color_map(colours =  ['#F1F4F5','#CCCCFF', '#92A1CF', '#0000FF', '#003399', '#002366' ], \
#low_lat = 39, up_lat = 43, low_lon = -82, up_lon = -74, dictionary_colors = dictionary_colors)
 
