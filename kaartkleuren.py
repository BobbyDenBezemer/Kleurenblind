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

print edges_table

# list of all colors, index of list corresponds with countie number - 1
colors = []
colors.append('start colors list')
i = 1
while i <= len(edges_table):
    colors.append(0)
    i += 1

print colors

# change color of each countie to satisfy constraints
for key in edges_table:
    aanliggend = edges_table.get(key)

    for countie in aanliggend:
        if colors[key] == colors[countie]:
            colors[key] += 1
    for countie in aanliggend:
        if colors[key] == colors[countie]:
            colors[key] += 1

# check for collissions

" to do "

# prints each countie and corresponding 'color'
            
#print colors

#i = 1
#while i <= len(edges_table):
    #print lookup_table[i], colors[i]
    #i += 1
