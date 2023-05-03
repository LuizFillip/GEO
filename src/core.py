import pyIGRF
import datetime as dt
import time
import pandas as pd


sites = {
 'cap': {'name': 'Cachoeira Paulista', 'coords': (-22.7038, -45.0093)},
 'car': {'name': 'Cariri', 'coords': (-7.38, -36.528)},
 'for': {'name': 'Fortaleza', 'coords': (-3.73, -38.522)},
 'caj': {'name': 'Cajazeiras', 'coords': (-6.89, -38.56)},
 'saa': {'name': 'São Luis', 'coords': (-2.53, -44.296)},
 'boa': {'name': 'Boa Vista', 'coords': (2.8, -60.7)},
 'ccb': {'name': 'Cachimbo', 'coords': (-9.5, -54.8)},
 'cgg': {'name': 'Campo Grande', 'coords': (-20.5, -54.7)},
 'jic': {'name': 'Jicamarca', 'coords': (-11.95, -76.87)},
 'rga': {'name': 'Rio Grande', 'coords': (-53.78, -67.7)},
 'sms': {'name': 'São Martinho da Serra/RS', 'coords': (-29.53, -53.85)},
 'tcm': {'name': 'Tucumán', 'coords': (-26.56, -64.88)},
 'sjc': {'name': 'São José Dos Campos', 'coords': (-23.19, -45.89)},
 'vss': {'name': 'Vassouras/RJ', 'coords': (-22.41, -43.66)},
 'jat': {'name': 'Jataí', 'coords': (-17.88, -51.72)},
 'cba': {'name': 'Cuiabá', 'coords': (-15.6, -56.1)},
 'ara': {'name': 'Araguatins/TO', 'coords': (-5.65, -48.12)},
 'eus': {'name': 'Eusébio/CE', 'coords': (-3.89, -38.45)},
 'slz': {'name': 'São Luis', 'coords': (-2.53, -44.3)},
 'pil': {'name': 'Pilar', 'coords': (-31.7, -63.89)},
 'ttb': {'name': 'Tatuoca', 'coords': (-1.205, -48.51)}}




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



