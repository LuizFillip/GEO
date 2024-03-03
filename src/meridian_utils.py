# from intersect import intersection
from scipy.signal import argrelmin
import numpy as np
import json  
import GEO as gg
from scipy.interpolate import CubicSpline
import os 


MERIDIAN_PATH = 'WSL/meridians/'

def load_meridian(year, site = 'saa'):
        
    infile = os.path.join(
        MERIDIAN_PATH, 
        f'{site}_{year}.json'
        )
    dat = json.load(open(infile))

    x = np.array(dat["mx"])
    y = np.array(dat["my"])

    nx = dat["nx"]
    ny = dat["ny"]
    return nx, ny, x, y


def split_meridian(
        rlat,
        year,
        points = None,
        site = 'saa'
        ):
        
    nx, ny, x, y = load_meridian(year, site)
    
    lon, lat = gg.limit_hemisphere(
            x, 
            y, 
            nx, 
            ny, 
            np.degrees(rlat), 
            hemisphere = 'both'
            )
    
    lon = sorted(lon)
    lon, lat = interpolate(
        lon, lat, points = points
        )

    return lon, lat

def compute_distance(x, y, x0, y0):
    
    dis = np.sqrt(pow(x - x0, 2) + 
                  pow(y - y0, 2))
    
    min_idxs = argrelmin(dis)[0]
    min_idx = min_idxs[np.argmin(dis[min_idxs])]
    
    min_x = x[min_idx]
    min_y = y[min_idx]
    min_d = dis[min_idx]
    
    return min_x, min_y, min_d

def find_closest(arr, val):
    return np.abs(arr - val).argmin()

def intersec_with_equator(x, y, year = 2013):
     """
     Find intersection point between equator 
     and meridian line 
     """
     e_x, e_y = gg.load_equator(year, values = True)
     
     nx, ny = gg.intersection(
         e_x, e_y, x, y
         )
     return nx.item(), ny.item()

def interpolate(x, y, points = 30):
    
    """
    Interpolate the same number of points for different
    ranges of meridians
    """
         
    
    spl = CubicSpline(x, y)
    
    new_lon = np.linspace(x[0], x[-1], points)    
    new_lat = spl(new_lon)
    
    return np.round(new_lon, 3), np.round(new_lat, 3)


