from GEO import quick_map,  sites

    
lat_lims = dict(min = -15, max = 10, stp = 5)

lon_lims = dict(min = -60, max = -35, stp = 5)    


    
fig, ax = quick_map(
    lat_lims = lat_lims, 
    lon_lims = lon_lims
    )

markers = ['s', '^']
instruments = ['FPI', 'Digisonde']
for i, site in enumerate(["car", "saa"]):
    s = sites[site]
    clat, clon = s["coords"]
    ax.scatter(clon, clat, s = 200, 
               marker = markers[i], 
               label = s["name"])
    
ax.legend(loc = 'upper right')