from GEO.src.mapping import quick_map
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import pyIGRF

fig, ax = plt.subplots(
    figsize = (10, 10), 
    dpi = 300,
    subplot_kw = {'projection': ccrs.PlateCarree()}
    )


lat_lims = dict(min = -30, 
                max = 30, 
                stp = 10)

lon_lims = dict(min = -90, 
                max = -15, 
                stp = 15)    

quick_map(ax, lon_lims, lat_lims)

import numpy as np

def plot_meridians(ax):
    
    for xstart  in np.arange(-60, -40, 5)[::-1]:
        delta = 1.0
        
        for ystart in np.arange(-20, 20)[::-1]:
            d, i, h, x, y, z, f = pyIGRF.igrf_value(
                ystart,  xstart, alt = 0, year = 2013
                )
           
            new_point_x = xstart - delta * np.tan(np.radians(d))
            new_point_y = ystart - delta
        
          
            ax.plot([xstart, new_point_x], 
                    [ystart, new_point_y], color = "k")
                    
            xstart = new_point_x
            ystart = new_point_y
            
        

plot_meridians(ax)




   

