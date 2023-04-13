from FluxTube.src.mag import Apex
from GEO.src.core import (find_closest_meridian, 
                          limit_hemisphere, 
                          sites)
import numpy as np
import pandas as pd


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
    
save_meridians(site = "saa")

