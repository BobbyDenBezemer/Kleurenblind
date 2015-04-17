### Making the map

def make_map():
    import numpy as np
    from matplotlib import pyplot as plt
    from matplotlib import cm
    from matplotlib.collections import LineCollection
    from matplotlib.patches import Polygon
    from matplotlib.patches import Polygon
    from mpl_toolkits.basemap import Basemap
    import shapefile

    # just some standard matplot lib syntax to add a figure and then make a subplot
    fig = plt.figure(figsize=(15.7,12.3))
    ax = plt.subplot(111)

    # make the map projection. Choose mercator and define upper and lower boundaries
    # urcrnrlat = upper right corner lattitude, urcrnrlon = upper right corner longitude
    # llcrnlat = lower left corner lattitude, llcrnrlon = lower left corner longitude
    m = Basemap(projection='merc',
                resolution='h',llcrnrlat=39,
        urcrnrlat=43,
        llcrnrlon=-82,
        urcrnrlon=-74, area_thresh=10000)

    m.drawcoastlines()  # draw the coastlines
    m.drawstates() # draw the states
    m.drawcountries() # draw countries
    m.drawmapboundary(fill_color='white') # draw the boundary

    # read in the shapefile and draw them
    m.readshapefile('./shapefile/PA_counties_clip', 'countries_sf', drawbounds=True)

    print len(m.countries_sf) #number of shapes, so 69
    print m.countries_sf_info[0]#metadata, so the columns
    #print m.countries_sf_info

    #plots the shapes as Polygons with so far a random color
    for shape, country in zip(m.countries_sf, m.countries_sf_info):
        poly = Polygon(shape, facecolor=cm.YlGn(np.random.rand()))
        plt.gca().add_patch(poly)

    plt.show()