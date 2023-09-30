import astral 
from astral.sun import sun
import pandas as pd
import GEO as gg
from base import aware_dn

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
    return aware_dn(sun_phase["dusk"])




def sun_terminator(
        dn, 
        twilight_angle = 0, 
        site = 'saa'
        ):
    glat, glon = gg.sites[site]['coords']
    sun_phase = dawn_dusk(
           dn,  
           lat = glat, 
           lon = glon, 
           twilightAngle = twilight_angle
           )
    return aware_dn(sun_phase[1])


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
    for dn in pd.date_range(
            f'{year}-01-01', 
            f'{year}-12-31', 
            freq = '1D'
            ):
        out.append(twilights(
            dn, 
            twilightAngle = twilightAngle)
            )
    
    return pd.concat(out)

def run_years(angle = 0):
    
    
    out = []
    for year in [2013, 2014, 2015] :
        out.append(
            run_days(
            year = year, 
            twilightAngle = angle
            )
            )
    return pd.concat(out)
    
        
def run_angles():
    save_in = 'database/GEO/twilights/'
    for angle in [0, 12, 18]:
        df = run_years(angle = angle)
        
        df.to_csv(
            save_in + f'{angle}.txt'
            )
        
        
# run_angles()

