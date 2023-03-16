import pyIGRF
import numpy as np
import pandas as pd
from GEO.conversions import  year_fraction
import matplotlib.pyplot as plt


def run_igrf(
        date, 
        step_lon = 5, 
        step_lat = 1, 
        alt = 250
        ):
    if isinstance(date, int):
        year = date
    else:
        year = year_fraction(date)
    out = []
    for lat in np.arange(-90, 90 + step_lat, step_lat):
        for lon in np.arange(-180, 180 + step_lon, step_lon):
            d, i, h, x, y, z, f = pyIGRF.igrf_value(lat, lon, 
                                                    alt= alt, 
                                                    year = year)
            
            out.append([lat, lon, d, i])
            
    return pd.DataFrame(out, 
                        columns = ["lat", "lon", "d", "i"])
 

def save_df(df, year):

    name_to_save = f"database/GEO/dip_{year}.txt"
    df.to_csv(name_to_save,
              sep = ",",
              index = True, 
              header = True)        

def get_dip(date = 2013, 
            step_lon = 5, 
            step_lat = 1, 
            alt = 250):   
     
    df = run_igrf(date, 
                step_lon = step_lon, 
                step_lat = step_lat, 
                alt = alt)
    
    pivot = pd.pivot_table(
        df, 
        columns = "lon", 
        index = "lat", 
        values = "i"
        )
    cs = plt.contour(
        pivot.columns, 
        pivot.index, 
        pivot.values, 
        levels = 0)
    
    p = cs.collections[1].get_paths()[0]
    v = p.vertices
    return pd.DataFrame({"lon": v[:,0], "lat": v[:,1]})

save_df(get_dip(), year = 2013)