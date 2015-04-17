import csv

""" METHODS """
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

# change color of each countie to satisfy constraints
def set_colors():
    for parent in edges_table:
        colors[parent] = upgrade_parent(parent)
        # optimalisatie (AANNAME!!!)
        for child in edges_table.get(parent):
            colors[child] = upgrade_parent(child)


# recursively upgrade parent color
def upgrade_parent(parent):
    for child in edges_table.get(parent):
        while colors[parent] == colors[child]:
            colors[parent] += 1
            upgrade_parent(parent)
    return colors[parent]

# prints each countie and corresponding 'color'
def print_counties_colors():
    i = 1
    while i <= len(edges_table):
        print i, lookup_table[i], colors[i]
        i += 1


""" LOGIC """
#load csv
edges_table, lookup_table = penssylvania_dict_reader("Pennsylvania_counties_list.csv", ",")

# list of all colors, index of list corresponds with countie number - 1
colors = {}
for parent in edges_table:
    colors[parent] = 0

# change map colors
set_colors()

# print feedback
#print print_counties_colors()

# dictionary of colors for map-coloring
dictionary_colors = {}
for i in range(1, len(edges_table) + 1):
    dictionary_colors[lookup_table[i]] = colors[i]

#print dictionary_colors
