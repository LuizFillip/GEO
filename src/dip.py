import pyIGRF
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import GEO as gg
import os
from tqdm import tqdm 


def dec_dip(
        year = 2013, 
        site = "car", 
        alt = 250, 
        ):
         
    lat, lon = gg.sites[site]["coords"]
        
    d, i, h, x, y, z, f = pyIGRF.igrf_value(
        lat, 
        lon, 
        alt = alt, 
        year = year
        )

    return d, i 


def run_igrf(
        year, 
        step_lon = 5, 
        step_lat = 1, 
        alt = 250,
        cols = ["lat", "lon", "d", "i"]
        ):
    
    longitudes = np.arange(
        -180, 180 + step_lon, step_lon
        )
    latitudes = np.arange(
        -90, 90 + step_lat, step_lat
        )
    
    out = []
    for lat in latitudes:
        for lon in tqdm(longitudes, str(lat)):
            
            d, i, _, _, _, _, _ = pyIGRF.igrf_value(
                lat, lon, 
                alt = alt, 
                year = year
                )
            
            out.append([lat, lon, d, i])
            
    return pd.DataFrame(out, columns = cols)
 

 

def get_dip(date = 2013, 
            step_lon = 0.1, 
            step_lat = 0.1, 
            alt = 300
            ):   
    
    print('[compute_dip]', date)
     
    df = run_igrf(
        date, 
        step_lon = step_lon, 
        step_lat = step_lat, 
        alt = alt
        )
    
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


def load_equator(year, values = False):
    infile = os.getcwd() + f'/database/GEO/dips/dip_{year}.txt'
    
    eq = pd.read_csv(infile, index_col = 0).values
    
    if values:
        return eq[:, 0], eq[:, 1] 
    else:
        return pd.DataFrame(
            eq, columns = ['lon', 'lat']
            )

def build_dataframe():
    out = {}
    for site in ['car', 'caj', 'saa']:
        out[gg.sites[site]["name"]] = dec_dip(2013, site, 300)
        
    return pd.DataFrame(out, index = ['Declinação', 'Inclinação'])

def save_df(df, year):

    name_to_save = f"database/GEO/dips/dip_{year}.txt"
    df.to_csv(name_to_save,
              sep = ",",
              index = True, 
              header = True)       
    
def main():
  
    year = 2023
    df = get_dip(year, 
                step_lon = 0.1, 
                step_lat = 0.1, 
                alt = 300)
    
    save_df(df, year)
            
