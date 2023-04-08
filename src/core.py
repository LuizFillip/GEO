import pyIGRF
import datetime as dt
import time
import numpy as np


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
        date = 2013, 
        site = "car", 
        alt = 250, 
        ):
    
    if isinstance(date, dt.datetime):
        frac_year = year_fraction(date)
    else:
        frac_year = float(date)
        
        
    lat, lon = coords[site]
    
    lon += 360
    
    d, i, h, x, y, z, f = pyIGRF.igrf_value(
        lat, lon, 
        alt = alt, 
        year = frac_year
        )

    return d, i 

def compute_meridian(
        lon = -60, 
        max_lat = 20,
        delta = 1.0, 
        alt = 0, 
        year = 2013
        ):
    
    xx = []
    yy = []
    
    for lat in np.arange(-max_lat, max_lat)[::-1]:
        d, i, h, x, y, z, f = pyIGRF.igrf_value(
            lat, 
            lon, 
            alt = alt, 
            year = year
            )
       
        new_point_x = lon - delta * np.tan(np.radians(d))
        new_point_y = lat - delta
        
        xx.extend([lon, new_point_x])
        yy.extend([lat, new_point_y])
                
        lon = new_point_x
        lat = new_point_y
        
    return (np.array(list(dict.fromkeys(xx))), 
            np.array(list(dict.fromkeys(yy))))