from GEO.src.mapping import quick_map
from FluxTube.src.mag import Apex
from ..core import sites  
from ..meridians import meridians
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
    date = dt.datetime(2013, 1, 1, 1, 21)

    glat, glon = sites["saa"]["coords"]

    from GEO import quick_map

    fig, ax = quick_map()

    m = meridians(date)

    x, y = m.closest_from_site(glon, glat)

    ax.plot(x, y)


    nx, ny = intersec_with_equator(x, y)

    print(nx, ny)

    ax.scatter(nx, ny, s = 150)
    rlat = 5
    x1, y1 = limit_hemisphere(
            x, y, nx, ny, rlat)

    ax.plot(x1, y1, color = "b", lw = 2)


