import astral 
from astral.sun import sun
import pandas as pd
import numpy as np

def dn2float(arr):
    """Not sum an"""
    return (arr.hour + 
            arr.minute / 60 + 
            arr.second / 3600)


def plot_terminators(ax, ds, dusk = True):
    dates = np.unique(ds.index.date)[:-1]
    
    color = ["cyan", "k"]
    if dusk:
        dates = dates[-1]
        color = color[-1]
    for dn in dates:
        for i, d in enumerate(dawn_dusk(dn)):
        
            ax.axvline(d, linestyle = "--", 
                       color = color[i])
            
    return d


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
    return sun_phase["dawn"], sun_phase["dusk"]

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

