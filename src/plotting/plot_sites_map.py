from GEO import quick_map,  sites
import json
import numpy as np
    
lat_lims = dict(min = -20, max = 10, stp = 5)

lon_lims = dict(min = -60, max = -30, stp = 5)    


    
fig, ax = quick_map(
    lat_lims = lat_lims, 
    lon_lims = lon_lims, 
    figsize = (10, 10)
    )

markers = ['s', '^', 'o']

instruments = ['FPI', 'Digisonde', "GNSS receiver"]

for i, site in enumerate(["car", "saa", 'caj']):
    s = sites[site]
    clat, clon = s["coords"]
    ax.scatter(clon, clat, s = 200, 
               marker = markers[i], 
               label = s["name"])


def plot_meridian(ax):
    
    infile = 'database/GEO/meridian.json'
    
    dat = json.load(open(infile))
    
    x = np.array(dat['mx'])
    y = np.array(dat['my'])
    
    ax.plot(x, y)
    
    ax.text(-47, 6, 'Magnetic\nmeridian')
    
    
plot_meridian(ax)
ax.legend(bbox_to_anchor = (.5, 1.3), 
          ncol = 2,
          loc = 'upper center')