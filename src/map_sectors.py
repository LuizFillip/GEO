import numpy as np 
import GEO as gg 
import pandas as pd


def longitude_sector(
        ds, 
        long_start, 
        long_delta = 10
        ):

    s = (ds['lon'] >= long_start)
    e = (ds['lon'] <= long_start + long_delta)
    
    return ds.loc[s & e].sort_index()

def longitudes(
        start = -80, 
        end = -30, 
        step = 10
        ):
    return np.arange(start, end, step)


def equator_coords(year = 2013):

    eq = gg.load_equator(year)
    
    return pd.DataFrame(
        eq, columns = ['lon', 'lat']
        )

        
def corner_coords(
        year = 2013, 
        radius = 5,  
        angle = -45,
        ax = None
        ):
    
    df = equator_coords(year)

    x_coords = []
    y_coords = []
    
    if radius == 10:
        
        delta = 3
        longs = longitudes(
                start = -65,
                end = -30, 
                step = 10
                )
        
    elif radius == 5:
        delta = 1.5
    
        longs = longitudes(
                start = -70,
                end = -35, 
                step = 5
                )
        
        
    for slon in longs:
        
        coords = df.loc[
            (df['lon'] > slon - radius) &
            (df['lon'] < slon)
            ].min()
        
        
        clon = coords['lon']
        clat = coords['lat']
                
        x_limits = []
        y_limits = []
        
        for i in range(4):
            angle_corner = np.radians(angle) + i * np.pi / 2  
            x = clon + (radius - delta) * np.cos(angle_corner)
            y = clat + 10 * np.sin(angle_corner) 
            
            x_limits.append(round(x, 4))
            y_limits.append(round(y, 4))
        
        
        x_limits.append(x_limits[0])
        y_limits.append(y_limits[0])
        
        x_coords.append(x_limits)
        y_coords.append(y_limits)
    
    
    return x_coords, y_coords
            
    
def set_coords(
        year, 
        radius = 10, 
        angle = 45
        ):
    
    x_coords, y_coords = corner_coords(
        year, 
        radius, 
        angle 
        )
    
    coords = {}
    
    for x, y in zip(x_coords, y_coords):
        
        lon_set = sorted(tuple(set(x)))
        lat_set = sorted(tuple(set(y)))
        
        lon_key = round(lon_set[0])
        
        coords[lon_key] = (lon_set, lat_set)
    
    return coords


