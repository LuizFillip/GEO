import pyIGRF
import datetime as dt
import time
import pandas as pd

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


def load_equator(
        infile = "database/GEO/dip_2013.txt"
        ):
    return pd.read_csv(infile, index_col = 0).values











