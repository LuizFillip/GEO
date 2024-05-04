import astral 
from astral.sun import sun
import GEO as gg
import base as b
import datetime as dt
from datetime import datetime
import pytz
# from timezonefinder import TimezoneFinder
from astral import LocationInfo

def dusk_time(
        dn,  
        lat = -2.53, 
        lon = -44.296, 
        twilight = 18
        ):

    observer = astral.Observer(
        latitude = lat, 
        longitude = lon
        )
    sun_phase = sun(
        observer, 
        dn, 
        dawn_dusk_depression = twilight
        )
    
    dusk = b.aware_dn(sun_phase['dusk'])
    
    if dusk < dn:
        dusk += dt.timedelta(days = 1)

    return dusk


def dusk_from_site(
        dn, 
        site,
        twilight_angle = 0
        ):
    
    glat, glon = gg.sites[site]['coords']
    
    dusk = dusk_time(
           dn,  
           lat = glat, 
           lon = glon, 
           twilight = twilight_angle
           )
   
    return dusk


def terminators_time(
        dn, 
        lons, 
        twilight = 18, 
        float_fmt = True
        ):
        
    out = {}
    lons = [int(i) for i in lons]
    for i, col in enumerate(lons):
        
        lon, lat = gg.first_edge(dn.year)[col]
        
        try:
            time_dn = gg.dusk_time(
                    dn,  
                    lat = lat, 
                    lon = lon, 
                    twilight = twilight
                    )
        except:
           
            delta = dt.timedelta(hours = i + 2)
            time_dn = dn + delta
        
        if float_fmt:
            out[col] = b.dn2float(time_dn)
        else:
            out[col] = time_dn
            
    return out 

def terminator(lon, dn, float_fmt = True):
    
    lon, lat = gg.first_edge(dn.year)[int(lon)]
    
    time_dn = dusk_time(
            dn,  
            lat = lat, 
            lon = lon, 
            twilight = 18
            )
    
    if float_fmt:
        return b.dn2float(time_dn)
    else:
        return time_dn
    
    
# def is_night(longitude, latitude, date_time):
#     '''
#     Check if is a region encounters nighttime period
#     '''
#     tf = TimezoneFinder()
    
#     timezone_str = tf.timezone_at(
#         lng = longitude, 
#         lat = latitude
#         )
#     city_tz = pytz.timezone(timezone_str)

#     city = LocationInfo(
#         "City", 
#         "Country", 
#         timezone_str, 
#         latitude, 
#         longitude
#         )
    
#     s = sun(city.observer, date=date_time, tzinfo=city_tz)

#     sunrise = s["sunrise"].astimezone(city_tz)
#     sunset = s["sunset"].astimezone(city_tz)
    
#     date_time = date_time.astimezone(city_tz)

#     if sunrise < date_time < sunset:
#         return False  # It's day
#     else:
#         return True  # It's night

# def local_midnight(longitude, latitude, date_time):
    
#     tf = TimezoneFinder()
#     timezone_str = tf.timezone_at(lng=longitude, lat=latitude)
#     city_tz = pytz.timezone(timezone_str)
    
#     # Finding the local midnight
#     current_date = date_time.date()
#     local = city_tz.localize(
#         datetime(current_date.year,
#                  current_date.month, 
#                  current_date.day, 0, 0, 0)
#         )
    
#     dusk = b.aware_dn(local.astimezone(pytz.utc))
    
#     if dusk < date_time:
#         dusk += dt.timedelta(days = 1)
        
#     return dusk


# def main():
    
#     longitude = -46.6333  # Replace with the desired longitude
#     latitude = -23.5505  # Replace with the desired latitude
#     date_time_to_check = dt.datetime(2023, 12, 1, 8, 0, 0)  #
#     night = is_night(longitude, latitude, date_time_to_check)
#     if night:
#         print("It's night.")
#     else:
#         print("It's day.")
# dn = dt.datetime(2015, 1, 6)
# dusk_from_site(
#         dn, 
#         'jic',
#         twilight_angle = 18
#         )