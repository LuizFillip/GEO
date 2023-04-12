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
import pandas as pd

def save_ranges_over_meridian(
         x, y,
         ax = None,
         amin = 200, 
         amax = 700, 
         step = 5, 
         base = 150,
         save = True,
         set_hemis = "south"
         ):
 
     out = []
     heights = np.arange(amin, amax + step, step)
     
     if ax is not None: heights = heights[::-1]
     
     for alt in heights:
         
         mlat = Apex(alt).apex_lat_base(base = base)
         
         rlat = np.degrees(mlat)
         
         x1, y1 = limit_hemisphere(
                 x, y, rlat, 
                 hemisphere = set_hemis
                 )
         
         if ax is not None:
             ax.plot(x1, y1, "--", 
                     label = f"{alt} km", 
                     lw = 2)
         
         idx = np.ones(len(x1)) * alt
         mlats = np.ones(len(x1)) * rlat
         
         out.append(pd.DataFrame(
             {
                 "lon": x1, 
                 "lat": y1, 
                 "rlat": mlats
              }, 
             index = idx)
             )
     
     if save:
         df = pd.concat(out)
         df.to_csv(
             f"ranges_{set_hemis}.txt",
             index = True
             )
         return df

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
    lon_lims = dict(min = -55, max = -35, stp = 10) 
     
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
    
    ax.scatter(nx, ny, s = 100, 
               label = "intersecção")
    
    ax.plot(x, y, lw = 1, color = "salmon", 
            label = "meridiano magnetico")
    
    
    
    ax.legend(loc = "upper right")
        
    return fig

def save_meridians(site = "saa"):
    
    glat, glon = sites[site]["coords"]
    x, y = find_closest_meridian(glon, glat)
    
    for col in ["south", "north", "both"]:
    
        save_ranges_over_meridian(
                 x, 
                 y,
                 ax = None,
                 amin = 200, 
                 amax = 500, 
                 step = 5, 
                 base = 150,
                 save = True,
                 set_hemis = col,
                 )
    
