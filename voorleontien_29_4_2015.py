import csv
    
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
    
    filename = "netwerk3.csv"
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
def initialize_colouring():
    coloured.append('start coloured list')
    colors.append('start colors list')
    for i in range(1, len(edges_table)):
        colors.append(1)
    for i in range(1, len(edges_table)):
        coloured.append(False)
    
    #if netwerk1:
    #coloured[76] = True
    
    #if netwerk2:
    #coloured[81] = True
    
    #if netwer3:
    #len edges_table NIET + 1

# Find county with most adjacent countries which are not currently coloured.
# Returns the resulting county number that is largest in the list. 
def find_max(edges_list):
    maximum = 0
    result = 0
    for key in edges_list:
        x = 0
        for item in edges_table.get(key):
            if coloured[int(item)] == False:
                x += 1
        if x > maximum:
            maximum = x
            result = key
    return result

# Takes a county as input and returns a list of the surrounding countys 
# that are not currently coloured. 
def get_uncoloured_list(county):
    uncoloured_list = []
    edges = edges_table.get(county)
    for item in edges:
        if coloured[item] == False:
            uncoloured_list.append(item)
    return uncoloured_list

# Start of colouring first shell around maximum edges-county. Only to be used
# for the first shell. 
def color_max_edges():
    maximum = find_max(edges_table)
    coloured[int(maximum)] = True
    return maximum
            
# check for collissions, error checking the coloring process. Returns true
# if there are no colissions, otherwise returns the first occurring collission
# and false. 
def collission_test():
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


# prints each county and corresponding 'color', in random order. 
def print_counties_colors():
    look_up = {}
    i = 1
    for i in range(len(edges_table)):
        look_up[lookup_table[i]] = colors[i]
        i += 1
    return look_up

# Color specific county, check 4 times if there are no collissions (4 colors to be used)
# Replace hard-coded 4 with package which finds the clustercoefficient. 
def color_county(county):
    if coloured[county] == True:
        return
    x = get_uncoloured_list(county)
    y = edges_table.get(county)

    z = [item for item in y if item not in x]
    for i in range(4):
        for item in z:
            if colors[item] == colors[county]:
                colors[county] += 1
    coloured[county] = True

# Part of optimization, if there is a color = 5 in the result, try to eliminate this. 
# Function returns county with the 'highest' color 
def find_county_highest_color(colors):
    maximum = 0
    county = 0
    for i, item in enumerate(colors[1:]):
        if item > maximum: 
            maximum = item
            county = i
    return county + 1

def optimization_try():
    #Collission test, try to force solution
    highest_color_county = find_county_highest_color(colors) 
    
    results = collission_test()
    if results != True:
        county_1 = results[1]
        county_2 = results[2]
    
        colors[county_1] = 0
        colors[county_2] = 0
    
        count = 0
    
        while collission_test() != True or colors[county_1] != 0 or colors[county_2] != 0:
            recount = count % 2
            if recount == 0:
                if colors[county_1] > 3:
                    colors[county_1] = 1
                else:
                    colors[county_1] += 1
                count += 1
            if recount == 1:
                if colors[county_2] > 3:
                    colors[county_2] = 1
                else:
                    colors[county_2] += 1
                count += 1
            if colors[county_1] != 0 and colors[county_2] != 0:
                if collission_test() == True:
                   break


if __name__ == '__main__':

    edges_table, lookup_table = dict_reader("Thomasland.csv", ",")    

    edges_table = import_data()    
    
    colors = []
    coloured = []

    initialize_colouring()

    # color the county with max edges
    maximum = color_max_edges()

    # get the shell of the first county
    next_to = edges_table.get(maximum)

    # color the shell with a different color
    for item in next_to:
        colors[item] = colors[maximum + 1] + 1

    # find the county in shell with most edges, color that one + 1
    start_shell = find_max(next_to)
    colors[start_shell] += 1
    uncoloured_list = get_uncoloured_list(start_shell)

    # Get adjacent counties, color accordingly
    adjacent_countys = [item for item in edges_table.get(start_shell) if item in next_to]
    
    for item in adjacent_countys:
        color_county(item)
    
    # find the other adjacent counties
    for item in adjacent_countys:
        to_color = [x for x in edges_table.get(item) if x in next_to]       
        for x in to_color:
            color_county(x)

    for item in next_to:
        color_county(item)

    # color the shell of the first shell
    edges = []
    for item in next_to:
        edges.append(edges_table.get(item))
    
    # Color shell for shell. Repeat until all counties are coloured = True
    third_shell = [] 
    while True:
        for i in range(len(edges)):
            for item in edges[i]:
                color_county(item)
                third_shell.append(edges_table.get(item))
        for i in range(len(third_shell)):
            for item in third_shell[i]:
               color_county(item)
               edges.append(edges_table.get(item))
        if all(coloured):
            break  
    
    print collission_test()
    print colors
