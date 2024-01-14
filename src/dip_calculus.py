import os 
import pandas as pd
import GEO as gg 
import numpy as np


def load_equator(year = 2013, values = False):
    infile = os.getcwd() + f'/database/GEO/dips/dip_{year}.txt'
    
    df = pd.read_csv(infile, index_col = 0)

    if values:
        return df['lon'].values, df['lat'].values 
    else:
        return df

def distance_from_equator(
        lon, lat, year = 2013
        ):
    x, y = load_equator(year, values = True)

    min_x, min_y, min_d = gg.compute_distance(x, y, lon, lat)
    return min_d



def term_eq_intersect(dn, twilight = 18):
    
    """
    Find the intersection between the equator and 
    the solar terminator (by date)
    """
 
    eq_lon, eq_lat = load_equator(dn.year, values = True)
    
    te_lon, te_lat = gg.terminator2(dn, twilight)
        
    in_lon, in_lat = gg.intersection(eq_lon, eq_lat, te_lon, te_lat)
    
    return in_lon, in_lat


def stations_near_of_equator(
        year = 2015,
        distance = 5, 
        extra_sts = []
        ):
    
    sites = gg.load_coords(year = 2013)

    out = {}
    
    for name, key in sites.items():
        lon, lat, alt = tuple(key)
        
        min_d = distance_from_equator(
                lon, 
                lat, 
                year = year
                )
        
        if min_d <= distance:
          
            out[name] = (lon, lat)
            
    if len(extra_sts) != 0:
        
        for sts in extra_sts:
            lon, lat, alt = sites[sts] 
            out[sts] = (lon, lat)
            
    return out 




def stations_coordinates(year = 2013, distance = 5):
    
    sites = stations_near_of_equator(
        year,  distance = distance
        )
    
    arr = np.array([[lon, lat] for (lon, lat) in sites.values()])
    
    return arr[:, 0], arr[:, 1]
