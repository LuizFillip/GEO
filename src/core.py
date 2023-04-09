import pyIGRF
import datetime as dt
import time
import numpy as np
import pandas as pd
from scipy.signal import argrelmin

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
    name = sites[site]["name"]
        
    d, i, h, x, y, z, f = pyIGRF.igrf_value(
        lat, lon, 
        alt = alt, 
        year = year
        )

    return d, i 


def middle(array, m = 0):
    return array[int((len(array) - 1) /2) - m]




def compute_distance(x, y, x0, y0):
    
    def distance(x, y, x0, y0):
        d_x = x - x0
        d_y = y - y0
        dis = np.sqrt( d_x**2 + d_y**2 )
        return dis
    
    # compute distance
    dis = distance(x, y, x0, y0)
    
    # find the minima
    min_idxs = argrelmin(dis)[0]
    # take the minimum
    glob_min_idx = min_idxs[np.argmin(dis[min_idxs])]
    
    # coordinates and distance
    min_x = x[glob_min_idx]
    min_y = y[glob_min_idx]
    min_d = dis[glob_min_idx]
    
    return min_x, min_y, min_d

def find_closest(arr, val):
   idx = np.abs(arr - val).argmin()
   return idx

def intersection_in_equator(eq, xx, yy):
    
    lon_cond = (eq[:, 0] > xx[0]) & (eq[:, 0] < xx[-1]) 
    lat_cond = (eq[:, 1] < yy[0]) & (eq[:, 1] > yy[-1])
    
    ds = eq[np.where(lat_cond & lon_cond), :][0]

    return tuple(middle(ds, m = 0))


def align_to_site(x, y, glon):
    mx, my = middle(x), middle(y)
    eq = load_equator()
    
    idx = find_closest(eq[:, 0], glon)
    nx, ny = tuple(eq[idx, :])
    
    x -= abs(nx - mx)
    y -= abs(ny - my)
    
    return x, y

def align_to_equator(x, y, glon, glat):
    
    eq = load_equator()
    
    min_x, min_y, min_d = compute_distance(
        eq[:, 0], eq[:, 1], glon, glat)
    
    delta_lon = abs(min_x - glon)
    delta_lat = abs(min_y - glat)

    x -= delta_lon
    y += delta_lat
    return x, y

def compute_meridian(
        lon = -60, 
        max_lat = 20,
        alt = 0, 
        year = 2013
        ):
    
    xx = []
    yy = []
    
    delta = 1

    range_lats = np.arange(-max_lat, max_lat, delta)[::-1]
    
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


def load_equator(infile = "database/GEO/dip_2013.txt"):

    df = pd.read_csv(infile, index_col = 0)
   
    return df.values

def test_on_map():    
    year = 2013
    
    from GEO.src.mapping import quick_map
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
    lon_lims = dict(min = -100, max = -30, stp = 10) 
    
    quick_map(ax, lon_lims, lat_lims)
    
    site = "car"
    
    glat, glon = sites[site]["coords"]
    name = sites[site]["name"]
    
    ax.scatter(glon, glat,
        marker = "^", 
        s = 100,
        color = "r",
        label = name)
    
    alt = 300        
    max_mlat = Apex(alt).apex_lat_base(base = 150)
    
    d, i = run_igrf(site = site)
        
    x, y  = compute_meridian(
        lon = glon, 
        alt = alt, 
        max_lat = np.degrees(max_mlat),
        year = year
            )
    
    x, y = align_to_site(x, y, glon)
    
    x, y = align_to_equator(x, y, glon, glat)
    
    ax.plot(x, y, lw = 2, label = f"{alt} km")

    ax.legend(loc = "upper right")
    
    
test_on_map()
