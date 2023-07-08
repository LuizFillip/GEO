import astral 
from astral.sun import sun
import pandas as pd
from utils import dn2float

def plot_lines(
        ax, date_list, 
        glat = -2.53, glon= -44.296):

    for dn in date_list:
        for regionF in dawn_dusk(dn,  
                    glat, 
                    glon, 
                    twilightAngle = 18
                    ):
        
            l2 = ax.axvline(regionF)
        
        for regionE in dawn_dusk(dn,  
                    glat, 
                    glon, 
                    twilightAngle = 12):
        
            l3 = ax.axvline(regionE, color = "blue")
            
    
    
    labels = ["300 km", "120 km"]
    
    ax.legend([l2, l3], labels, 
                     loc = "lower left", 
                     )        
    
    return None

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
        twilightAngle = 18):
    
    
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


def run_years(
        year = 2013, 
        twilightAngle = 18
        ):
    
    out = []
    for dn in pd.date_range(
            f'{year}-01-01', 
            f'{year}-12-31', 
            freq = '1D'
            ):
        out.append(twilights(dn, twilightAngle = twilightAngle))
    
    return pd.concat(out)

def run_angles():
    save_in = 'database/GEO/twilights/'
    year = 2013
    
    for angle in [12, 18]:
        df = run_years(
            year = year, 
            twilightAngle = angle
            )
        df.to_csv(
            save_in + f'{2013}_{angle}.txt')
        
        

# run_angles()