"""
This file contains functions to read in country data and to read in the 
social network data
"""

import csv

def edges_table_reader(filename, seperator):
    """
    import the data an edges table with nodes and edges
    Also returns a lookup table by which edges could be combined with their
    country names
    """
    edges_table = {}
    lookup_table = {}
    # open a file to read it in
    with open(filename, 'rU') as csvfile:
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
        
    # returns the edges and lookup tables
    return edges_table, lookup_table
    
def social_graph_reader(filename, seperator):
    """
    import the social network data as a dictionary and the 
    values as lists of ints
    """
    edges_table = {}

    # open a file to read it in
    with open(filename, 'r') as csvfile:
        next(csvfile)
        reader = csv.reader(csvfile, delimiter= seperator)

        # enumerate gives you both the value and the indice
        for row in reader:
            # check whether the row[0] in a key in edges_table
            if int(row[0]) in edges_table:
                edges_table[int(row[0])].append(int(row[1]))
            else:
                edges_table[int(row[0])] = [int(row[1])]
            # check whether the row[1] is a key in edges_table
            if int(row[1]) in edges_table:
                edges_table[int(row[1])].append(int(row[0]))
            else:
                edges_table[int(row[1])] = [int(row[0])]
                
    return edges_table