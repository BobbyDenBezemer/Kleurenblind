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

# Colors a single node
def random_color_node(node, coloured, colors):
    colors[node] = random.randint(1, 4)
    coloured[node] = True

# Checks for color collissions around single node
def most_collissions_node(edges_table, colors):
    collission_count = 0    
    for node in edges_table:
        edges = edges_table.get(node)
        count = 0
        for item in edges: 
            if colors[node] == colors[item]:
                count += 1
        if count > collission_count:
            collission_count = count
            most_collission_node = node
    
    return most_collission_node


# Color all nodes
def color_all(edges_table, coloured, colors):
    while True:
        node = random_node_selector(edges_table)
        random_color_node(node, coloured, colors)
        if all(coloured):
            break

def change_color(node, colors):
    colors[node] += 1
    
def showPlot(max_colors, trials):
    """
    """
    x_axis = []

    # Calculating the mean time to clean coverage of room for each number
    # of robots for num_trials, up until max_num_robots for specified.
    # robot_type. 
    for i in range(0, trials):
        x_axis.append(i)
        
    #num_bins  = 100
    #plt.hist(max_colors, num_bins)
  
    plt.plot(x_axis, max_colors, 'ro')
    plt.ylabel('number of different colors')
    plt.xlabel('trials')
    plt.axis([0, trials - 1, 0, 10])
    plt.grid(True)
    plt.title('Iterative colouring of nodes: how many different colors needed')
    plt.title('Iterative colouring of nodes. Start: color 1 to 4')
    plt.show()
    
def count_collissions(edges_table, colors):
    count = 0
    for item in edges_table:
        edges = edges_table.get(item)
        for node in edges:
            if colors[item] == colors[node]:
                count += 1
    return count

def main(trials):
    max_colors = []
    runtime = []  
    
    for i in range(trials):
        print 'Finding solution #' + str(i + 1) + '...'
        start = time.clock()
        colors = []
        coloured = []
        
        initialize_colouring(coloured, colors)
        
        color_all(edges_table, coloured, colors)
        
        swaps = 0
        time_out = 0
        
        while collission_test(colors) != True:
            #Hillclimbing for XX swaps
            if swaps > 20000:
                break
            before = count_collissions(edges_table, colors)
            node_swap1 = random_node_selector(edges_table)
            node_swap2 = random_node_selector(edges_table)
            if colors[node_swap1] != colors[node_swap2]:
                swaps += 1
                temp = colors[node_swap2]
                colors[node_swap2] = colors[node_swap1]
                colors[node_swap1] = temp
                after = count_collissions(edges_table, colors)
                if after > before:
                    time_out += 1
                    temp = colors[node_swap2]
                    colors[node_swap2] = colors[node_swap1]
                    colors[node_swap1] = temp
                else: 
                    time_out = 0
        
        while collission_test(colors) != True:
            node = most_collissions_node(edges_table, colors)
            change_color(node, colors)
        
        end = time.clock()
        
        
        maximum_color = 0
        for item in range(1, len(colors) - 1):
            if colors[item] > maximum_color:
                maximum_color = colors[item]
                
        if maximum_color == 3:
            print colors
        
        # for different colors needed
        max_colors.append(maximum_color)    

        # for histogram
        #max_colors.append(most_collissions_node(edges_table, colors))

        # algorithm timing
        runtime.append(end - start)

    return max_colors, runtime

if __name__ == '__main__':

    edges_table, lookup_table = data_loading.edges_table_reader("Pennsylvania_counties_list.csv", ",")
    #edges_table = data_loading.social_graph_reader("netwerk1.csv", ",")
    
    trials = 10
    
    max_colors, runtime = main(trials)
    
    print 'Runtimes: ' + str(runtime)
    
    showPlot(max_colors, trials)
    
