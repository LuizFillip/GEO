import pyIGRF
import datetime as dt
import time
import numpy as np
import pandas as pd
from scipy.signal import argrelmin
from intersect import intersection



sites = {
    "car": {"coords": (-7.38, -36.528), 
            "name": "Cariri"},  
    "for": {"coords":  (-3.73, -38.522), 
            "name": "Fortaleza"},
    "caj": {"coords": (-6.89, -38.56), 
            "name": "Cajazeiras"},
    "saa": {"coords":  (-2.53, -44.296), 
            "name": "Sao Luis"},
    "boa": {"coords": ( 2.8,  -60.7), 
            "name": "Boa Vista"},
    "ccb": {"coords": (-9.5,  -54.8), 
            "name": "Cachimbo"},
    "cgg": {"coords":(-20.5, -54.7), 
            "name": "Campo Grande"},
    "jic": {"coords":(-11.95, -76.87), 
            "name": "Jicamarca"} 
    }     




def year_fraction(date):
    
    "Return years in fraction (like julian date) "

   # returns seconds since epoch
    def sinceEpoch(date): # returns seconds since epoch
        return time.mktime(date.timetuple())
    
    s = sinceEpoch
    
    year = date.year
    start_year = dt.datetime(
        year = year, 
        month = 1, 
        day = 1
        )
    
    next_year = dt.datetime(
        year = year + 1, 
        month = 1, 
        day = 1
        )
    
    elapsed = s(date) - s(start_year)
    duration = s(next_year) - s(start_year)
    fraction = elapsed / duration
    
    return round(date.year + fraction, 2)


def run_igrf(
        year = 2013, 
        site = "car", 
        alt = 250, 
        ):
         
    lat, lon = sites[site]["coords"]
        
    d, i, h, x, y, z, f = pyIGRF.igrf_value(
        lat, 
        lon, 
        alt = alt, 
        year = year
        )

    return d, i 

def compute_distance(x, y, x0, y0):
    
    def distance(x, y, x0, y0):
        return np.sqrt(pow(x - x0, 2) + 
                       pow(y - y0, 2))
    
    # compute distance
    dis = distance(x, y, x0, y0)
    
    # find the minima
    min_idxs = argrelmin(dis)[0]
    # take the minimum
    glob_min_idx = min_idxs[
        np.argmin(dis[min_idxs])]
    
    # coordinates and distance
    min_x = x[glob_min_idx]
    min_y = y[glob_min_idx]
    min_d = dis[glob_min_idx]
    
    return min_x, min_y, min_d



def compute_meridian(
        lon = -60, 
        max_lat = 20,
        alt = 0, 
        year = 2013
        ):
    
    xx = []
    yy = []
    
    delta = 1

    range_lats = np.arange(-max_lat, max_lat, 
                           delta)[::-1]
    
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
        alt = 300
        ):
    
    arr = compute_all_meridians(
            max_lat = 40, 
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

def load_equator(
        infile = "database/GEO/dip_2013.txt"
        ):
    return pd.read_csv(infile, index_col = 0).values


def find_closest(arr, val):
   idx = np.abs(arr - val).argmin()
   return idx



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
        set_x = x[eq_x: end]
        set_y = y[eq_y: end]
    
    elif hemisphere == "north":
        start = find_closest(y, ny + rlat)
        set_x = x[start: eq_x + 1]
        set_y = y[start: eq_y + 1]
        
    else:
        end = find_closest(y, ny - rlat)
        start = find_closest(y, ny + rlat)
        set_x = x[start: end]
        set_y = y[start: end]
        
    return set_x, set_y

def test_on_map():    
  
    
    from GEO.src.mapping import quick_map
    from GEO.src.plotting.plot_mag_meridians import plot_all_meridians, plot_sites
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt
    import settings as s
    from FluxTube.src.mag import Apex
    
    fig, ax = plt.subplots(
        figsize = (8, 8), 
        dpi = 300, 
        subplot_kw = 
        {'projection': ccrs.PlateCarree()}
        )
    
    s.config_labels(fontsize = 15)
    
    lat_lims = dict(min = -30, max = 15, stp = 5)
    lon_lims = dict(min = -90, max = -30, stp = 10) 
     
    quick_map(ax, lon_lims, lat_lims)
    
    plot_sites(ax)
    ax.legend(loc = "upper right")
    
    year = 2013
    alt = 300
 
    site = "saa"
    glat, glon = sites[site]["coords"]
    
    x, y = find_closest_meridian(glon, glat)
    
    ax.plot(x, y, "--", lw = 1,
            color = "k")
    
        
    mlat = Apex(alt).apex_lat_base(base = 150)
    
 

    rlat = np.degrees(mlat)
    
    x, y = find_closest_meridian(glon, glat)

    x1, y2 = limit_hemisphere(
            x, y, rlat, 
            hemisphere = "north"
            )
    
    ax.plot(x1, y2, color = "r")

test_on_map()



