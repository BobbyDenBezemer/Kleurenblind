# import libraries
import os
import csv
import collections
import numpy as np
import random

# Import function that makes and colors the actual map
# import map_making
# map_making.make_map()

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


# returns the most connected countie based on a dictionary
def most_connected(edges_table):
    longest = 0
    countie_longest = 0
    for countie, borders in edges_table.items():
        #print countie, borders
        if len(borders) > longest:
            longest = len(borders)
            county_longest = countie
    return county_longest

def get_shell(edges_table, start):
    # nu willen we dus een subset counties hebben die alleen in de shell zitten
    keys = {}
    length =[]
    for borders in edges_table[start]:
        for shell_border in edges_table[borders]:
            if shell_border in edges_table[start]:
                length.append(shell_border)
        keys[borders] = length
        length = []
    return keys

def color_counties(county, is_colored, colors):
    if len(is_colored) == 0:
        colors[county] = 0
        is_colored.append(county)
    else:
        if county not in is_colored:
            is_colored.append(county)

    return colors, is_colored

def main(edges_table):
    number_counties = len(edges_table)
    colors = {}
    is_colored = []

    # get the starting point and the shell
    start = most_connected(edges_table)
    shell = get_shell(edges_table, start)
    #print start, shell

    # color the starting point
    colors, is_colored = color_counties(start, is_colored, colors)
    print colors, is_colored

    # now move on to all the counties are colored
    while len(is_colored) < number_counties:
        for key in shell.keys():
            color_counties(key, is_colored, colors)
        print is_colored
main()

    # now get the shell country where you will start coloring


i = 1
while i <= len(edges_table):
    colors.append(1)
    i += 1

# Optie 2)
colors = []
for i in range(67):
    colors.append(1)

# change color of each countie to satisfy constraints
for key in edges_table:
    # eigenlijk moeten we hier beginnen met het land met meeste grensen
    # loop over alle keys heen en check len values
    aanliggend = edges_table.get(key)

    for i in range(4):
        for countie in aanliggend:
            if colors[key] == colors[countie]:
                colors[key] += 1


# check for collissions
def collission_test():
    for key in edges_table:
        aanliggend = edges_table.get(key)
        for countie in aanliggend:
            if colors[key] == colors[countie]:
                print lookup_table[key], lookup_table[countie]
                return False
    return True

print colors
print collission_test()



# prints each countie and corresponding 'color'
def print_counties_colors():
    look_up = {}
    i = 1
    while i <= len(edges_table):
        look_up[lookup_table[i]] = colors[i] - 1
        i += 1
    return look_up

data_lookup = print_counties_colors()

colours = ["red", "blue", "green", "pink", "purple", "yellow"]

