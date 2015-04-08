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

# make hte matrix
matrix = np.zeros((66,66))

# fill the matrix by means of a for loop
for key in data.keys():
    for value in data.values():
        if len(value) < 1:
            print key, value
        else:
            for item in value:
                print key, item
    
