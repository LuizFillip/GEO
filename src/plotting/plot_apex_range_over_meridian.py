from GEO.src.mapping import quick_map
from FluxTube.src.mag import Apex
from GEO.src.core import (
    find_closest_meridian, 
    limit_hemisphere, 
    load_equator, 
    sites    )
from GEO.src.meridians import get_meridian_interpol
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
         
      
def plot_site_and_closest_meridian(
        ax, 
        site = "saa"):
      
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
      
      ax.scatter(nx, ny, s = 100, c = "r",
                 label = "intersecção")
      
      ax.plot(x, y, lw = 2, 
              color = "salmon", 
              label = "meridiano magnético")
      
      return x, y


def plot_apex_over_meridian():
    fig, ax = quick_map()
    plot_site_and_closest_meridian(
            ax, 
            site = "saa")
    
    x, y = get_meridian_interpol(site = "saa")
    
    ax.plot(x, y)
