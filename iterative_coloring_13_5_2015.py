import random
import matplotlib.pyplot as plt
import time
import data_loading
import heapq

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

def iterative_optimization(edges_table, coloured, colors, available_colors):
    """
    Takes edges_table, coloured list, and colors list which already has a 
    solution through random colouring. 
    Function picks two random nodes, and checks if the colors are non-identical. 
    If they are, the first node's color becomes the same color as the second 
    node, if this is possible without collissions. Keeps repeating this process
    until constraint 'available_colors' is reached. 
    """
    iterations = 0
    changes = 0
    unique_colors = set(colors[1:])
    while len(unique_colors) > available_colors:
        if iterations > 25000:
            break
        iterations += 1
        
        node = random_node_selector(edges_table)
        node_color = colors[node]
        
        highest_colors = heapq.nlargest(10, set(colors[1:]))
        
        for i in range(2, len(unique_colors)):
            if colors[node] == highest_colors[1]:
                index = random.randint(2, len(highest_colors) - 1)
                colors[node] = highest_colors[index]
                if collission_test(colors) == True:
                    changes += 1
                    break
                else:
                    colors[node] = node_color
            
        unique_colors = set(colors[1:])


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
    plt.axis([0, trials, 0,max(performance) + 1])
    plt.grid(True)
    plt.title('Random colouring of nodes: how many different colors needed')
    plt.show()

def main(trials, available_colors):
    """
    Runs the coloring algorithm XXX trials times, iterating until the coloring
    is achieved with the number of unique colors is equal to available colors. 
    Returns the amount of unique colors for each trial, and the runtime for
    each trial. 
    """
    performance = []
    runtime = [] 
    
    
    for i in range(trials):
        print 'Finding solution #' + str(i + 1) + '...'
        colors = []
        coloured = []
        start = time.clock()
        
        
        initialize_colouring(coloured, colors)
        
        color_all(edges_table, coloured, colors)
        
        iterative_optimization(edges_table, coloured, colors, available_colors)
        
        end = time.clock()
        runtime.append(end - start)
        
        unique_colors = set(colors[1:])
        performance.append(len(unique_colors))

    return runtime, performance

if __name__ == '__main__':

    edges_table, lookup_table = data_loading.edges_table_reader("Pennsylvania_counties_list.csv", ",")
    #edges_table = data_loading.social_graph_reader("netwerk1.csv", ",")
    
    trials = 1000
    available_colors = 4
    
    runtime, performance = main(trials, available_colors)
    
    showPlot(performance, trials)
    
