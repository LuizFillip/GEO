import pytz
from timezonefinder import TimezoneFinder
from base import aware_dn
import datetime as dt
import pandas as pd


def location_timezone(
        longitude, 
        latitude = 0
        ):
    tf = TimezoneFinder()
    
    location = tf.timezone_at(
        lng = longitude, 
        lat = latitude
        )
    
    return pytz.timezone(location)



def delta_timezone(
        dn, 
        longitude, 
        latitude
        ):
    
    if isinstance(dn, dt.date):
        dn = pd.to_datetime(dn)

    location = location_timezone(
        longitude, 
        latitude = latitude
        )
    
    utc_time = aware_dn(dn, tzinfo = pytz.utc) 
   
    local_time = aware_dn(dn, tzinfo = location)
   
    return utc_time - local_time



# dn = dt.datetime(2017, 1, 1, 5, 0)


def local_midnight(dn, lon, delta_day = None):
    
    hour = dn.hour 

    if hour != 0:
        dn -= dt.timedelta(hours = hour)
    
    delta = dt.timedelta(hours = lon / 15)
    
    target = dn - delta
    
    if delta_day is None:
        return target 
    else:
        return target + dt.timedelta(days = delta_day)



    
    
