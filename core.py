import pyIGRF
from GEO.conversions import year_fraction
import datetime as dt

coords = {"car": (-7.38, -36.528),  # Cariri
          "for": (-3.73, -38.522),  # Fortaleza
          "saa": (-2.53, -44.296),  # Sao Luis
          "boa": (2.8, -60.7),      # Boa Vista
          "ccb": (-9.5, -54.8),     # Cachimbo
          "cgg": (-20.5, -54.7)}     # Campo Grande

def run_igrf(
        date, 
        site = "car", 
        alt = 250, 
        ):
    
    if isinstance(date, dt.datetime):
        frac_year = year_fraction(date)
    else:
        frac_year = float(date)
        
        
    lat, lon = coords[site]
    
    #lon += 360
    
    d, i, h, x, y, z, f = pyIGRF.igrf_value(
        lat, lon, 
        alt = alt, 
        year = frac_year
        )
    
    return d, i 

def main():
    
    date = dt.datetime(2002, 10, 11)


    print(run_igrf(
            date, 
            site = "car", 
            alt = 250, 
            ))