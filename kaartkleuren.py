# Kleurenblind

import csv


def print_pennsylvania_list(filename):
    
    '''
        Prints the pennsylvania counties read from a CSV file, containing 
        county in column 1 and number of ajoining counties 
        
        @param filename: the filename to read the data from.
    '''
    reader = csv.reader(open(filename))
    reader.next()
    for row in reader:
        print str(row[1]) + ": " + str(int(float(row[3])*1000))
        
print_pennsylvania_list("Pennsylvania_counties_list.csv")

def pennsylvania_dict( filename ):
    
    '''
    	Reads the population from a CSV file, containing 
    	county in column 1 and number of ajoining counties

    	@param filename: the filename to read the data from
    	@return dictionary containing county -> number of ajoining counties
    '''
    reader = csv.reader(open(filename))
    reader.next()
    pennsylvania_dict = dict()
    for row in reader:
        pennsylvania_dict[int(row[2])] = int(float(row[3])*1000)
    return pennsylvania_dict