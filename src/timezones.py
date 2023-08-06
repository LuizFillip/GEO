import pytz
from timezonefinder import TimezoneFinder
from base import aware_dn

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

    location = location_timezone(
        longitude, 
        latitude = latitude
        )
    utc_time = dn.astimezone(pytz.utc)
    local = dn.astimezone(location)
    
    
    return aware_dn(utc_time) - aware_dn(local)