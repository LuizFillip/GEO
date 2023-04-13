from GEO.src.mapping import quick_map
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import settings as s
from FluxTube.src.mag import Apex
from GEO.src.core import (find_closest_meridian, 
                          limit_hemisphere, 
                          load_equator, 
                          sites)
from intersect import intersection
import numpy as np

def plot_ranges_for_each_apex(
         x, y,
         ax,
         amin = 200, 
         amax = 500, 
         step = 100, 
         base = 150,
         set_hemis = "south"
         ):
 
     heights = np.arange(amin, amax + step, step)[::-1]
          
     for alt in heights:
         
         mlat = Apex(alt).apex_lat_base(base = base)
         
         rlat = np.degrees(mlat)
         
         x1, y1 = limit_hemisphere(
                 x, y, rlat, 
                 hemisphere = set_hemis
                 )
         
         ax.plot(x1, y1, "--", 
                label = f"{alt} km", 
                lw = 2)
         
      
     

def plot_apex_range_over_meridian(
        year = 2013, 
        alt = 300, 
        site = "saa", 
        set_hemis = "south"):    
      
    fig, ax = plt.subplots(
        figsize = (8, 8), 
        dpi = 300, 
        subplot_kw = 
        {'projection': ccrs.PlateCarree()}
        )
    
    s.config_labels(fontsize = 15)
    
    lat_lims = dict(min = -15, max = 15, stp = 5)
    lon_lims = dict(min = -55, max = -35, stp = 5) 
     
    quick_map(ax, lon_lims, lat_lims)
        
    glat, glon = sites[site]["coords"]
    name = sites[site]["name"]
    
    ax.scatter(glon, glat, s = 100, 
               label = name, 
               marker = "^")
    
    x, y = find_closest_meridian(glon, glat)
    
    eq = load_equator()
    
    nx, ny = intersection(
        eq[:, 0], 
        eq[:, 1], 
        x, y
        )
    
    plot_ranges_for_each_apex(
             x, y,
             ax,
             amin = 200, 
             amax = 500, 
             step = 100, 
             base = 150,
             set_hemis = set_hemis
             )
    
    ax.scatter(nx, ny, s = 100, 
               label = "intersecção")
    
    ax.plot(x, y, lw = 1, color = "salmon", 
            label = "meridiano magnetico")
    
    ax.legend(loc = "upper right")
        
    return fig

plot_apex_range_over_meridian(
        year = 2013, 
        alt = 300, 
        site = "saa", 
        set_hemis = "south")