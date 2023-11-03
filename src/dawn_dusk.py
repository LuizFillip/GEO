import astral 
from astral.sun import sun
import pandas as pd
import GEO as gg
import base as b
import datetime as dt


def dusk_from_coords(
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
    
    dusk = dusk_from_coords(
           dn,  
           lat = glat, 
           lon = glon, 
           twilight = twilight_angle
           )
   
    return dusk


def twilights(
        dn, 
        lat = -2.53, 
        lon = -44.296, 
        twilightAngle = 18
        ):
    
    
    times = sun(
        astral.Observer(
            latitude = lat, 
            longitude = lon), 
        dn, 
        dawn_dusk_depression = twilightAngle
                    
        )
    
    del times['noon']
    
    for key in times.keys():
        times[key] = b.dn2float(times[key])
    
    return pd.DataFrame(times, index = [dn])

def run_days(
        year = 2013, 
        twilightAngle = 18
        ):
    
    out = []
    dn = dt.datetime(year, 1, 1, 0)
    for day in range(365):
        
        delta = dt.timedelta(days = day)
        
        out.append(
            twilights(
                dn + delta, 
                twilightAngle = twilightAngle
                )
            )
    
    return pd.concat(out)


