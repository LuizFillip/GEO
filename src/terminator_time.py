import astral 
from astral.sun import sun
import GEO as gg
import base as b
import datetime as dt
from datetime import datetime

def dusk_time(
        dn,  
        lat = -2.53, 
        lon = -44.296, 
        twilight = 18,
        suni = 'dusk'
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
    
    dusk = b.aware_dn(sun_phase[suni])
    
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
    
    try:
        time_dn = dusk_time(
                dn,  
                lat = lat, 
                lon = lon, 
                twilight = 18
                )
    except:
        time_dn = dn + dt.timedelta(hours = 2)
        
    if float_fmt:
        return b.dn2float(time_dn)
    else:
        return time_dn
    


def plot_sunrise_sunset(ax, dn, site = 'saa'):
    
    glat, glon = gg.sites[site]['coords']
    
    colors = ['k', 'b']
    out = []
    for i, suni in enumerate(['dusk', 'dawn']):
        
        time = dusk_time(
                dn,  
                lat = glat, 
                lon = glon, 
                twilight = 18,
                suni = suni
            )
        out.append(time)
        ax.axvline(
            time, lw = 2, 
            color = colors[i], 
            linestyle = '--')
    
    return out