import csv

def print_pennsylvania_list(filename):
    
    '''
        Prints the pennsylvania counties read from a CSV file, containing 
        county in column 1 and number of adjoining counties 
        
        @param filename: the filename to read the data from.
    '''
    
    reader = csv.reader(open(filename))
    for row in reader:
        print row 

def pennsylvania_dict( filename ):
    
    '''
    	Reads the population from a CSV file, containing 
    	county in column 1 and number of ajoining counties

    	@param filename: the filename to read the data from
    	@return dictionary containing county -> number of adjoining counties
    '''
    
    reader = csv.reader(open(filename))
    pennsylvania_dict = dict()
    for row in reader:
        pennsylvania_dict[int(row[0])] = int(float(row[3])*1000)
    return pennsylvania_dict
    
print_pennsylvania_list("Pennsylvania_counties_list.csv")