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
            "name": "São Luis"},
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




def load_equator(
        infile = "database/GEO/dip_2013.txt"
        ):
    return pd.read_csv(infile, index_col = 0).values


def find_closest(arr, val):
   idx = np.abs(arr - val).argmin()
   return idx








