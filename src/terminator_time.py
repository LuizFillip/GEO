import astral 
from astral.sun import sun
import GEO as gg
import base as b
import datetime as dt


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




