import astral 
from astral.sun import sun
import GEO as gg
import base as b
import datetime as dt
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
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


def is_night(longitude, latitude, date_time):
    '''
    Check if is a region encounters nighttime period
    '''
    tf = TimezoneFinder()
    
    timezone_str = tf.timezone_at(
        lng = longitude, 
        lat = latitude
        )
    city_tz = pytz.timezone(timezone_str)

    city = LocationInfo(
        "City", 
        "Country", 
        timezone_str, 
        latitude, 
        longitude
        )
    
    s = sun(city.observer, date=date_time, tzinfo=city_tz)

    sunrise = s["sunrise"].astimezone(city_tz)
    sunset = s["sunset"].astimezone(city_tz)
    
    date_time = date_time.astimezone(city_tz)

    if sunrise < date_time < sunset:
        return False  # It's day
    else:
        return True  # It's night

# Example usage

# def main():
    
#     longitude = -46.6333  # Replace with the desired longitude
#     latitude = -23.5505  # Replace with the desired latitude
#     date_time_to_check = datetime(2023, 12, 1, 8, 0, 0)  # Replace with your desired date and time
    
#     night = is_night(longitude, latitude, date_time_to_check)
#     if night:
#         print("It's night.")
#     else:
#         print("It's day.")

# main()