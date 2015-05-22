import random
import matplotlib.pyplot as plt
import time
import data_loading

def initialize_colouring(coloured, colors):
    """
    List of all colors, index of list corresponds with county number.
    Start with each county in the edges_list as coloured = False
    Takes two empty arrays, and adds above. 
    """
    coloured.append('start coloured list')
    colors.append('start colors list')
    for i in range(1, len(edges_table) + 1):
        colors.append(1)
    for i in range(1, len(edges_table) + 1):
        coloured.append(False)
    
    #if netwerk1:
    #coloured[76] = True
    
    #if netwerk2:
    #coloured[81] = True
    
    #if netwerk3:
    #len edges_table NIET + 1

def collission_test(colors):
    """
    Check for collissions, error checking the coloring process. Returns true
    if there are no colissions, otherwise returns false. 
    """
    for key in edges_table:
        adjacent = edges_table.get(key)
        for county in adjacent:
            if colors[key] == colors[county]:
                return False
    return True
    
def random_node_selector(edges_table):
    """
    Get a random node from the edges_table list. Returns this node. 
    """
    random_range = len(edges_table)
    selected_node = random.randint(1, random_range)
    return selected_node

def color_node(node, coloured, colors, edges_table):
    """
    Colors a single node, and adjusts coloured and colors array accordingly. 
    """
    edges = edges_table.get(node)
    colors[node] = random.randint(1, len(edges_table))
    while collission_edges(edges, node, colors):
        for item in edges:
            if colors[item] == colors[node]:
                colors[node] += 1
    coloured[node] = True

def collission_edges(edges, node, colors):
    """
    Checks for color collissions around single node, returns true if there 
    is at least 1 collission. If the node has no edges and/or no collissions, 
    returns false. 
    """
    if edges == None:
        return False
    else: 
        for item in edges:
            if colors[item] == colors[node]:
                return True
    return False

def color_all(edges_table, coloured, colors):
    """    
    Color all nodes by random selecting nodes and coloring this node.
    Keeps coloring until there are no collissions and every node has been
    coloured. 
    """
    while True:
        node = random_node_selector(edges_table)
        color_node(node, coloured, colors, edges_table)
        if all(coloured) and collission_test(colors) == True:
            break

def showPlot(max_colors, trials):
    """
    Plots the max_colors vs. trials as red dots. 
    """
    x_axis = []

    for i in range(0, trials):
        x_axis.append(i)
    
  
    plt.plot(x_axis, max_colors, 'ro')
    plt.ylabel('Number of colors')
    plt.xlabel('Trial')
    plt.axis([0, trials, 0,100])
    plt.grid(True)
    plt.title('Random colouring of nodes (Netwerk #1)')
    plt.show()

def main(trials):
    """
    Runs the coloring algorithm XXX trials times, and returns the highest
    absolute color, the runtime for each trial, and the amount of unique colors
    that have been used. 
    """
    max_colors = []
    runtime = [] 
    performance = []
    
    for i in range(trials):
        colors = []
        coloured = []
        start = time.clock()
        
        initialize_colouring(coloured, colors)
        
        color_all(edges_table, coloured, colors)
        
        end = time.clock()
        runtime.append(end - start)
        
        maximum_color = 0
        for item in range(1, len(colors) - 1):
            if colors[item] > maximum_color:
                maximum_color = colors[item]
        max_colors.append(maximum_color)
        
        unique_colors = set(colors)
        performance.append(len(unique_colors))

    return max_colors, runtime, performance

if __name__ == '__main__':

    #edges_table, lookup_table = data_loading.edges_table_reader("Pennsylvania_counties_list.csv", ",")
    edges_table = data_loading.social_graph_reader("netwerk1.csv", ",")
    
    trials = 1000
    
    max_colors, runtime, performance = main(trials)
    
    showPlot(performance, trials)
    
