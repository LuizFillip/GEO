import pyIGRF
import numpy as np
import pandas as pd
from GEO.conversions import  year_fraction



def run_magnetic_data(date, 
                      step_lon = 5, 
                      step_lat = 1, 
                      alt = 250):
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
def main():
    
    for year in [2013]:
        
        save_df(run_magnetic_data(year), year)


main()