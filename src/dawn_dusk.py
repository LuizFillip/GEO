import astral 
from astral.sun import sun
import pandas as pd
import GEO as gg
from base import aware_dn
import datetime as dt


def dn2float(arr):
    """Not sum an"""
    return (arr.hour + 
            arr.minute / 60 + 
            arr.second / 3600)



def dawn_dusk(
        dn,  
        lat = -2.53, 
        lon = -44.296, 
        twilightAngle = 18
        ):

    observer = astral.Observer(
        latitude = lat, 
        longitude = lon
        )
    sun_phase = sun(
        observer, 
        dn, 
        dawn_dusk_depression = twilightAngle
        )
    return aware_dn(sun_phase['dusk'])




def sun_terminator(
        dn, 
        twilight_angle = 0, 
        site = 'saa'
        ):
    glat, glon = gg.sites[site]['coords']
    
    dusk = dawn_dusk(
           dn,  
           lat = glat, 
           lon = glon, 
           twilightAngle = twilight_angle
           )
    if dusk < dn:
        dusk += dt.timedelta(days = 1)
        
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
        times[key] = dn2float(times[key])
    
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


