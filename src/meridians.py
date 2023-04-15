from FluxTube.src.mag import Apex
import pyIGRF
from GEO.src.core import (
    load_equator, 
    find_closest, 
    compute_distance, 
    sites)
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
from intersect import intersection

def limit_hemisphere(
        x, y, rlat, 
        hemisphere = "south"
        ):
    
    eq = load_equator()
    # Find intersection point between
    # equator and merian
    nx, ny = intersection( eq[:, 0], eq[:, 1], x, y)
    
    # find meridian indexes (x and y) 
    # where cross the equator and upper limit
    eq_x = find_closest(x, nx)  
    eq_y = find_closest(y, ny)  

    # create a line above of intersection point 
    # with radius from apex latitude 
    if hemisphere == "south":
        end = find_closest(y, ny - rlat)
        set_x = x[eq_x: end+ 1]
        set_y = y[eq_y: end + 1]
    
    elif hemisphere == "north":
        start = find_closest(y, ny + rlat)
        set_x = x[start: eq_x + 1]
        set_y = y[start: eq_y + 1]
        
    else:
        end = find_closest(y, ny - rlat) + 1
        start = find_closest(y, ny + rlat)
        set_x = x[start: end]
        set_y = y[start: end]
        
    return set_x, set_y

def save_ranges_over_meridian(
         x, y,
         amin = 200, 
         amax = 700, 
         step = 5, 
         base = 150,
         set_hemis = "south"
         ):
 
     out = []
     heights = np.arange(amin, amax + step, step)
          
     for alt in heights:
         
         mlat = Apex(alt).apex_lat_base(base = base)
         
         rlat = np.degrees(mlat)
         
         x1, y1 = limit_hemisphere(
                 x, y, rlat, 
                 hemisphere = set_hemis
                 )

         
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
     
     df = pd.concat(out)
     df.to_csv(
        f"ranges_{set_hemis}.txt",
        index = True
        ) 
     return df
 

def compute_meridian(
        lon = -60, 
        max_lat = 20,
        alt = 0, 
        year = 2013,
        delta = 1
        ):
    
    xx = []
    yy = []
    
    range_lats = np.arange(
        -max_lat, max_lat, delta
        )[::-1]
    
    for lat in range_lats:
        d, i, h, x, y, z, f = pyIGRF.igrf_value(
            lat, 
            lon, 
            alt = alt, 
            year = year
            )
       
        new_point_x = lon - delta * np.tan(np.radians(d))
        new_point_y = lat - delta
        
        lon = new_point_x
        lat = new_point_y
        
        xx.append(lon)
        yy.append(lat)
            
    return xx, yy


def compute_all_meridians(
        max_lat = 40, 
        year = 2013, 
        alt = 300
        ):
    out = []

    for lon in np.arange(-120, -30, 1):
        
        x, y = compute_meridian(
            lon = lon, 
            alt = alt, 
            max_lat = max_lat,
            year = year
                )   
        out.append([x, y])
                
    return np.array(out)


def find_closest_meridian(
        glon, 
        glat, 
        year = 2013, 
        alt = 300,
        max_lat = 40
        ):
    
    arr = compute_all_meridians(
            max_lat = max_lat, 
            year = year, 
            alt = alt
            )
    
    out = {}
    
    for num in range(arr.shape[0]):
        x, y = arr[num][0], arr[num][1]
        
        min_x, min_y, min_d = compute_distance(
            x, y, glon, glat)
            
        out[num] = min_d
    
    closest = min(out, key = out.get)
    
    return arr[closest][0], arr[closest][1]
 
    
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

def get_meridian_interpol(site = "saa", factor = 3):
    
    glat, glon = sites[site]["coords"]
    x, y = find_closest_meridian(glon, glat)
    
    spl = CubicSpline(x, y)
    
    new_lon = np.linspace(x[0], x[-1], len(x) * factor)    
    new_lat = spl(new_lon)
    
    return np.round(new_lon, 3), np.round(new_lat, 3)


        


