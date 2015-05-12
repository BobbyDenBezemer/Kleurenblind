import csv
import random
import matplotlib.pyplot as plt
import time
    
def dict_reader(filename, seperator):
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
    
def import_data():

    data = dict()
    
    filename = "netwerk1.csv"
    seperator = ","
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter= seperator)
        next(csvfile)
        for row in reader:
            if int(row[0]) in data:
                data[int(row[0])].append(row[1])
            else:
                data[int(row[0])] = [row[1]]
            if int(row[1]) in data:
                data[int(row[1])].append(row[0])
            else:
                data[int(row[1])] = [row[0]]
    
    storage = []
    for key, item in data.iteritems():
        for e in item:
            storage.append(int(e))
        data[key] = storage
        storage = []
    
    return data

# List of all colors, index of list corresponds with county number.
# Start with each county in the edges_list as coloured = False
def initialize_colouring(coloured, colors):
    coloured.append('start coloured list')
    colors.append('start colors list')
    for i in range(1, len(edges_table) + 1):
        colors.append(1)
    for i in range(1, len(edges_table) + 1):
        coloured.append(False)
    
    #if netwerk1:
    coloured[76] = True
    
    #if netwerk2:
    #coloured[81] = True
    
    #if netwerk3:
    #len edges_table NIET + 1


# check for collissions, error checking the coloring process. Returns true
# if there are no colissions, otherwise returns the first occurring collission
# and false. 
def collission_test(colors):
    x = 0
    y = 0
    for key in edges_table:
        adjacent = edges_table.get(key)
        for county in adjacent:
            if colors[key] == colors[county]:
                x = key
                y = county
                #print lookup_table[key] + ' collides with ' + lookup_table[county]
                return False, x, y
    return True
    
# Get a random node from the edges_table list. Returns this node. 
def random_node_selector(edges_table):
    random_range = len(edges_table)
    selected_node = random.randint(1, random_range)
    return selected_node

# Colors a single node
def color_node(node, coloured, colors):
    edges = edges_table.get(node)
    while collission_edges(edges, node, colors):
        for item in edges:
            if colors[item] == colors[node]:
                colors[node] += 1
    coloured[node] = True

# Checks for color collissions around single node
def collission_edges(edges, node, colors):
    if edges == None:
        return False
    else: 
        for item in edges:
            if colors[item] == colors[node]:
                return True
    return False

# Color all nodes
def color_all(edges_table, coloured, colors):
    while True:
        node = random_node_selector(edges_table)
        color_node(node, coloured, colors)
        if all(coloured) and collission_test(colors) == True:
            break

def showPlot(max_colors, trials):
    """
    """
    x_axis = []

    for i in range(0, trials):
        x_axis.append(i)
    
  
    plt.plot(x_axis, max_colors, 'ro')
    plt.ylabel('Number of colors')
    plt.xlabel('Trial')
    plt.axis([0, trials, 0,10])
    plt.grid(True)
    plt.title('Random colouring of nodes: how many different colors needed')
    plt.show()

def main(trials):
    max_colors = []
    runtime = [] 
    
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
        
        if maximum_color == 4: 
            print colors

    return max_colors, runtime

if __name__ == '__main__':

    #edges_table, lookup_table = dict_reader("pennsylvania_counties_list.csv", ",")     
    
    edges_table = import_data()
    
    trials = 10
    
    max_colors, runtime = main(trials)
    
    showPlot(max_colors, trials)
    
