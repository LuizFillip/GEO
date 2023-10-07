import numpy as np
import GEO as gg


def filter_latitudes(
        xx, yy, 
        lat_min = -30, 
        lat_max = 20
        ):
    yy = np.where(
        (yy < lat_min) | 
        (yy > lat_max ), 
        np.nan, yy
        )
    
    mask = np.isnan(yy)
        
    return xx[~mask], yy[~mask]

def get_line_eq(x0, x1, y0, y1):
    return y0 - y1, x1 - x0, x0 * y1 - x1 * y0

def filter_between_curves(x, y, xx, yy, xx1, yy1):

    ar, br, cr = get_line_eq(
        xx[0], xx[-1], yy[0], yy[-1]
        )
    
    mask1 = (
        (x < xx[0]) | (x < xx[-1]) & 
        (ar * x + br * y + cr <= 0)
        )
   
    ar, br, cr = get_line_eq(
        xx1[0], xx1[-1], yy1[0], yy1[-1]
        )
    
    mask2  = (
        (x > xx1[-1]) | (x > xx1[0]) & 
        (ar * x + br * y + cr >= 0)
        )
    
    x = x[~(mask1 | mask2)]
    y = y[~(mask1 | mask2)]

    return x, y



def get_limit_meridians(
        dn,
        lon = -50, 
        delta = 10,
        max_lat = 30, 
        lat_min = -20
        ):
    xx, yy = gg.meridians(
        dn,
        max_lat,
        delta = delta
        ).compute(lon)
    
    
    xx1, yy1 = gg.meridians(
        dn,
        max_lat,
        delta = delta
        ).compute(lon + delta)
    
    
    xx, yy = filter_latitudes(
        xx, yy, 
        lat_min, 
        lat_max = max_lat
        )
    
    xx1, yy1 = filter_latitudes(
        xx1, yy1, 
        lat_min, 
        lat_max = max_lat
        )
    
    return xx, yy, xx1, yy1