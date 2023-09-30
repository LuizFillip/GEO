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
        latitude = 0
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



# def test():
dn = dt.datetime(2017, 1, 2)



# location = location_timezone(
#     longitude, 
#     latitude = 0
#     )

# delta = aware_dn(dn, tzinfo = pytz.utc)  - aware_dn(dn, tzinfo = location)

# delta
# import numpy as np 


# for lon in np.arange(-80, -30, 10):
    
#     delta = delta_timezone(
#             dn, 
#             lon 
#             )
    
#     print(lon, (dn - delta) - dn )