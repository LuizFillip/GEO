import numpy as np 
import GEO as gg 
import cartopy.crs as ccrs
import matplotlib.patches as patches

        


def middle_point(arr):
    return sum(list(set(arr))) / 2




def plot_rectangles_regions(
        ax,
        year = 2013,
        center_dot = False, 
        index_box = True,
        first_inter = True,
        delta1 = 3,
        color = 'black', 
        stop_index = 4, 
        lat_ext = 10
        ):
    
    lons, lats = sectors_coords(year, delta1 = delta1, 
    lat_ext = lat_ext)
    
    numbers = list(range(len(lons)))
    
    # colors = ['k', '#0C5DA5', '#00B945', '#FF9500']
        
    for i, (xlim, ylim) in enumerate(zip(lons, lats)):
        
        
        index = numbers[i] + 1 
        
        if index == stop_index:
            break
        
        ax.plot(
            xlim, ylim,
            color = color, 
            linewidth = 2, 
            transform = ccrs.PlateCarree(),
            )
   
        # polygon = patches.Polygon(
        #     list(zip(xlim, ylim)), closed=True, 
        #     linewidth=2, edgecolor='k',
        #     alpha = 0.6, 
        #     facecolor= colors[i])

        # ax.add_patch(polygon)
        
        clon = middle_point(xlim)
        clat = middle_point(ylim)
        
        if center_dot:
            ax.scatter(clon, clat, c = 'b', s = 100)
        
        if index_box:
            ax.text(
                clon, max(ylim) + 1, index, 
                transform = ax.transData,
                fontsize = 35, 
                color = color
                )
            
    if first_inter:
        for (x, y) in first_edge(year).values():
        
            ax.scatter(x, y, c = 'k', s = 400, marker = '*')
            
    return 



