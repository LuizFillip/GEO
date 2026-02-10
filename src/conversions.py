import numpy as np
import datetime as dt
# import spacepy.coordinates as coord
# from spacepy.time import Ticktock
import time

def year_fraction(date, rd = 4):
    
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
    
    return round(date.year + fraction, rd)

def colatitude(latitude):
    return (np.pi / 2) - latitude

def dip(inclination):
   """Latitude inlicação magnética (dip) """
   return np.degrees(np.arctan(0.5 * np.tan(
       np.radians(inclination)) / 2)
       )

            