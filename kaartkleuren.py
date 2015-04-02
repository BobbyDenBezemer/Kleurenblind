import csv
    
def penssylvania_dict_reader(filename, seperator):
    """
    import the data as a dictionary and the values as lists of ints
    """
    data = {}
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter= seperator)
        for row in reader:
            print row
            data[str(row[0])] = [e for e in row[1:] if e]
            
    # now convert items to ints
    storage = []
    for key, item in data.iteritems():
        for e in item:
            storage.append(int(e))
        data[key] = storage
        storage = []
    return data
    
    
data = penssylvania_dict_reader("Pennsylvania_counties_list.csv", ",")
    
