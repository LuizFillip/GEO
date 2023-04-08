import pyIGRF
import datetime as dt
import time
import numpy as np
import pandas as pd

coords = {
    "car": (-7.38, -36.528),  # Cariri
    "for": (-3.73, -38.522),  # Fortaleza
    "caj": (-6.89, -38.56),   # Cajazeiras
    "saa": (-2.53, -44.296),  # Sao Luis
    "boa": ( 2.8,  -60.7),    # Boa Vista
    "ccb": (-9.5,  -54.8),    # Cachimbo
    "cgg": (-20.5, -54.7)     # Campo Grande
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
         
    lat, lon = coords[site]
    
    #lon += 360
    
    d, i, h, x, y, z, f = pyIGRF.igrf_value(
        lat, lon, 
        alt = alt, 
        year = year
        )

    return d, i 


def middle(array, m = 0):
    return array[int((len(array) - 1) /2) - m]

def intersection_in_geo_equator(eq, xx, yy):
    
    lon_cond = (eq[:, 0] > xx[0]) & (eq[:, 0] < xx[-1]) 
    lat_cond = (eq[:, 1] < yy[0]) & (eq[:, 1] > yy[-1])
    
    ds = eq[np.where(lat_cond & lon_cond), :][0]

    return tuple(middle(ds, m = 1))

def compute_meridian(
        lon = -60, 
        max_lat = 20,
        alt = 0, 
        year = 2013,
        align_to_equator = True
        ):
    
    xx = []
    yy = []
    
    delta = 1.0
    
    for lat in np.arange(-max_lat, max_lat)[::-1]:
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
        
    if align_to_equator:
    
        eq = load_equator()
    
        nx, ny = intersection_in_geo_equator(eq, xx, yy)
        xx += abs(nx - middle(xx))
        yy += abs(ny - middle(yy))
        
        return xx, yy
    
    else:
        return xx, yy


def load_equator(infile = "database/GEO/dip_2013.txt"):

    df = pd.read_csv(infile, index_col = 0)
   
    return df.values

