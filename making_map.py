## Plotting Europe by countries
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.collections import LineCollection
from matplotlib.patches import Polygon
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
import shapefile

fig = plt.figure(figsize=(15.7,12.3))
ax = plt.subplot(111)
m = Basemap(projection='merc',
            resolution='c',llcrnrlat=-80,
    urcrnrlat=80,
    llcrnrlon=-180,
    urcrnrlon=180)
            
m.bluemarble()
plt.show()

map = Basemap(projection='cyl',llcrnrlat=35,urcrnrlat=72,\
            llcrnrlon=-17,urcrnrlon=42,resolution='c')

map.drawmapboundary(fill_color='white')

map.readshapefile('./shapefile/world_by_country', 'countries_sf', drawbounds=True)

#the readshapefile method allow you to call the shapefile's shapes and info.
#Both are lists, the first containing a list of tuples (coordinates), 
# and the second containig a dictionary with associated metadata

print len(map.countries_sf) #number of shapes
print map.countries_sf_info[0].keys() #metadata, so the columns


#plots the shapes as Polygons with a random facecolor (if European), or gray (if not)
for shape, country in zip(map.countries_sf, map.countries_sf_info):
    if country['REGION'] == 'Europe':
        poly = Polygon(shape, facecolor=cm.YlGn(np.random.rand()))
        plt.gca().add_patch(poly)
    else:
        poly = Polygon(shape, facecolor="gray")
        plt.gca().add_patch(poly)

#adds the colormap legend
cmleg = np.zeros((1,20))
for i in range(20):
    cmleg[0,i] = (i*5)/100.0
plt.imshow(cmleg, cmap=plt.get_cmap("YlGn"), aspect=1)
plt.colorbar()
plt.show()

