import csv
    
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
    
def twitter():

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
    
    print data

    return data

# List of all colors, index of list corresponds with countie number.
# Start with each countie in the edges_list as coloured = False
def initialize_colouring():
    coloured.append('start coloured list')
    colors.append('start colors list')
    for i in range(1, 100):
        colors.append(1)
    for i in range(1, 100):
        coloured.append(False)

# Find countie with most adjacent countries which are not currently coloured.
# Returns the resulting countie number that is largest in the list. 
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
def color_max_edging():
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
        aanliggend = edges_table.get(key)
        for countie in aanliggend:
            if colors[key] == colors[countie]:
                x = key
                y = countie
                print lookup_table[key] + ' collides with ' + lookup_table[countie]
                return False, x, y
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

# Find the countie with most edges in 'edges'-list
def find_most_edges(edges):
    check = 0
    largest = 0
    for item in edges:
        if len(edges_table.get(item)) > check:
            check = len(edges_table.get(item))
            largest = item
    return largest

# Color specific countie, check 4 times if there are no collissions (4 colors to be used)
def color_countie(countie):
    if coloured[countie] == True:
        return
    x = get_uncoloured_list(countie)
    y = edges_table.get(countie)

    z = [item for item in y if item not in x]
    for i in range(4):
        for item in z:
            if colors[item] == colors[countie]:
                colors[countie] += 1
    coloured[countie] = True

# Part of optimilization, if there is a color = 5 in the result, try to eliminate this. 
# Function returns countie with the 'highest' color 
def find_countie_highest_color(colors):
    maximum = 0
    countie = 0
    for i, item in enumerate(colors[1:]):
        if item > maximum: 
            maximum = item
            countie = i
    return countie + 1

def optimilization_try():
    #Collission test, try to force solution
    highest_color_countie = find_countie_highest_color(colors) 
    
    results = collission_test()
    if results != True:
        countie_1 = results[1]
        countie_2 = results[2]
    
        colors[countie_1] = 0
        colors[countie_2] = 0
    
        count = 0
    
        while collission_test() != True or colors[countie_1] != 0 or colors[countie_2] != 0:
            recount = count % 2
            if recount == 0:
                if colors[countie_1] > 3:
                    colors[countie_1] = 1
                else:
                    colors[countie_1] += 1
                count += 1
            if recount == 1:
                if colors[countie_2] > 3:
                    colors[countie_2] = 1
                else:
                    colors[countie_2] += 1
                count += 1
            if colors[countie_1] != 0 and colors[countie_2] != 0:
                if collission_test() == True:
                   break


if __name__ == '__main__':

    edges_table, lookup_table = penssylvania_dict_reader("Thomasland.csv", ",")
    edges_table = twitter()
    print edges_table
    
    
    colors = []
    coloured = []

    initialize_colouring()

    # color the countie with max edges
    maximum = color_max_edging()

    # get the shell of the first countie
    next_to = edges_table.get(maximum)

    # color the shell with a different color
    for item in next_to:
        colors[item] = colors[maximum + 1] + 1

    # find the countie in shell with most edges, color that one + 1
    start_shell = find_most_edges(next_to)
    colors[start_shell] += 1
    uncoloured_list = get_uncoloured_list(start_shell)

    # Get adjacent countries, color accordingly
    adjacent_counties = [item for item in edges_table.get(start_shell) if item in next_to]
    
    for item in adjacent_counties:
        color_countie(item)
    
    # find the other adjacent countries
    for item in adjacent_counties:
        to_color = [x for x in edges_table.get(item) if x in next_to]       
        for x in to_color:
            color_countie(x)

    for item in next_to:
        color_countie(item)

    # color the shell of the first shell
    edges = []
    for item in next_to:
        edges.append(edges_table.get(item))
    
    # Color shell for shell, in this case 5 times. Repeat until all counties are coloured = True
    third_shell = [] 
    while True:
        for i in range(len(edges)):
            for item in edges[i]:
                color_countie(item)
                third_shell.append(edges_table.get(item))
        for i in range(len(third_shell)):
            for item in third_shell[i]:
               color_countie(item)
               edges.append(edges_table.get(item))
        if all(coloured):
            break

    highest_color_countie = find_countie_highest_color(colors)     
    

    #dictionary_colors = {}
    #for i in range(1, len(edges_table) + 1):
    #dictionary_colors[lookup_table[i]] = colors[i]
    print collission_test()
    print colors