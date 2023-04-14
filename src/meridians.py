from FluxTube.src.mag import Apex
from GEO.src.core import (find_closest_meridian, 
                          limit_hemisphere, 
                          sites)
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline


def save_ranges_over_meridian(
         x, y,
         amin = 200, 
         amax = 700, 
         step = 5, 
         base = 150,
         set_hemis = "south"
         ):
 
     out = []
     heights = np.arange(amin, amax + step, step)
          
     for alt in heights:
         
         mlat = Apex(alt).apex_lat_base(base = base)
         
         rlat = np.degrees(mlat)
         
         x1, y1 = limit_hemisphere(
                 x, y, rlat, 
                 hemisphere = set_hemis
                 )

         
         idx = np.ones(len(x1)) * alt
         mlats = np.ones(len(x1)) * rlat
         
         out.append(pd.DataFrame(
             {
                 "lon": x1, 
                 "lat": y1, 
                 "rlat": mlats
              }, 
             index = idx)
             )
     
     df = pd.concat(out)
     df.to_csv(
        f"ranges_{set_hemis}.txt",
        index = True
        ) 
     return df
 
    
def save_meridians(site = "saa"):
    
    glat, glon = sites[site]["coords"]
    x, y = find_closest_meridian(glon, glat)
    
    for col in ["south", "north", "both"]:
    
        save_ranges_over_meridian(
                 x, 
                 y,
                 ax = None,
                 amin = 200, 
                 amax = 500, 
                 step = 5, 
                 base = 150,
                 save = True,
                 set_hemis = col,
                 )

def get_meridian_interpol(site = "saa"):
    
    glat, glon = sites[site]["coords"]
    x, y = find_closest_meridian(glon, glat)
    
    spl = CubicSpline(x, y)
    
    new_lon = np.linspace(x[0], x[-1], len(x) * 3)    
    new_lat = spl(new_lon)
    
    return np.round(new_lon, 3), np.round(new_lat, 3)
import iri2016 as iri
import datetime as dt

def get_ionos(dn, zeq, glat, glon):
    ds = iri.IRI(dn, [zeq, zeq, 1], glat, glon)
    
    ne = ds["ne"].values[0]
    Te = ds["Te"].values[0]
    return ne, Te

dn = dt.datetime(2013, 1, 1, 21, 0)
heights = np.arange(200, 505, 5)

out = []

for h in heights:

    rlat = Apex(h).apex_lat_base(base = 150)
    
    x, y = get_meridian_interpol(site = "saa")
    
    glon, glat = limit_hemisphere(
            x, y, np.degrees(rlat), 
            hemisphere = "south")
             
    mlat_range = np.linspace(0, -rlat, len(glon))
    
    out1 = []
    out.append(sum(out1))
    
    for i, mlat in enumerate(mlat_range):
        
        zeq = Apex(h).apex_height(mlat)
        
        ne, te = get_ionos(dn, zeq, glat[i], glon[i])
        
        out1.append(ne)