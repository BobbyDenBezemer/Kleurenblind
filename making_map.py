def making_map(lat_down, lon_down, lat_up, lon_up, shapefile):
    ### Making the map
    colours = ['purple','pink', 'red', 'blue', 'yellow', 'green']
    from matplotlib import pyplot as plt
    from matplotlib import cm
    from matplotlib.collections import LineCollection
    from matplotlib.patches import Polygon
    from mpl_toolkits.basemap import Basemap
    import shapefile
    
    # just some standard matplob lib syntax to add a figure and then make a subplot
    fig = plt.figure(figsize=(15.7,12.3))
    ax = plt.subplot(111)
    
    # make the map projection. Choose mercator and define upper and lower boundaries
    # urcrnrlat = upper right corner lattitude, urcrnrlon = upper right corner longitude
    # llcrnlat = lower left corner lattitude, llcrnrlon = lower left corner longitude
    # For Pensylvania, use following values:
    # lat_down = 39, lon_down = -82, lat_up = 43, lon = -74 
    
    # For Spain
    # lat_up = 4, lon_up = 44, lat_down = 9, lon_down = 36
    
    # For Rajistan
    # 
    m = Basemap(projection='merc',
                resolution='l',llcrnrlat= lat_down,
                llcrnrlon = lon_down, urcrnrlat = lat_up,
                urcrnrlon = -74, area_thresh=10000)
        
 
    m.drawcoastlines()  # draw the coastlines
    m.drawstates() # draw the states
    m.drawcountries() # draw countries
    m.drawmapboundary(fill_color='white') # draw the boundary
    
    # read in the shapefile and draw them
    m.readshapefile(shapefile, 'countries_sf', drawbounds=True)
    
    print len(m.countries_sf) #number of shapes, so 69
    test = []
    #for i in range(len(m.countries_sf_info)):
    #    if m.countries_sf_info[i]['NAME'] not in test:
    #        test.append(m.countries_sf_info[i]['NAME'])
    print m.countries_sf_info[0]['NAME'] # this is how you get the state names
    
    
    # look over the shapes and actual data
    for shape, countie in zip(m.countries_sf, m.countries_sf_info):
        # now loop over all the keys and values in the dictionary
        for lookup in dictionary_colors.items():
            # compare the countie name of the data with the countie name in the lookup table
            if lookup[0] == countie['NAME']:
                # then choose a country from our list depending on the value of the key
                color = colours[lookup[1]]          
        poly = Polygon(shape, facecolor=color)
        plt.gca().add_patch(poly)
        
    plt.show() 
    
