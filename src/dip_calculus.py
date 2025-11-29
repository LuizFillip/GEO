import os 
import pandas as pd
import GEO as gg 
import numpy as np

def sectors_coords(
        year = 2013, 
        radius = 10,  
        angle = -45,
        delta1 = 3, 
        lat_ext = 20
        ):
    '''
    Compute coordinates of sectors from a longitude 
    range with an inclination  
    
    '''
    df = gg.load_equator(year)

    if radius == 10:
        
        delta = delta1 #3
        longs = np.arange( -65, -30, radius)
        
    elif radius == 5:
        delta = 1.5
        longs = np.arange( -70, -35, radius)
     
    x_coords = []
    y_coords = []
               
    for slon in longs:
        
        coords = df.loc[
            (df['lon'] > slon - radius) &
            (df['lon'] < slon)].min()
        
        clon = coords['lon']
        clat = coords['lat']
                
        x_limits = []
        y_limits = []
        
        for i in range(4):
            angle_corner = np.radians(angle) + i * np.pi / 2  
            x = clon + (radius - delta) * np.cos(angle_corner)
            y = clat + lat_ext * np.sin(angle_corner) 
            
            x_limits.append(round(x, 4))
            y_limits.append(round(y, 4))
              
        x_limits.append(x_limits[0])
        y_limits.append(y_limits[0])
        
        x_coords.append(x_limits)
        y_coords.append(y_limits)
      
    return x_coords[::-1], y_coords[::-1]
            
    
def load_equator(year = 2013, values = False):
    infile = os.getcwd() + f'/database/GEO/dips/dip_{year}.txt'
    
    df = pd.read_csv(infile, index_col = 0)

    if values:
        return df['lon'].values, df['lat'].values 
    else:
        return df

def distance_from_equator(
        lon, lat, year = 2013
        ):
    x, y = load_equator(year, values = True)

    min_x, min_y, min_d = gg.compute_distance(x, y, lon, lat)
    return min_d

def set_coords(
        year = 2013, 
        radius = 10, 
        angle = 45, 
        delta1 = 3
        ):
    
    lons, lats = sectors_coords(
        year, 
        radius, 
        angle, 
        delta1 
        )
    
    coords = {}
    
    def round_up(x):
        return int(np.ceil((x - 5) / 10.0)) * 10
    
    for x, y in zip(lons, lats):
        
        lon_set = sorted(tuple(set(x)))
        lat_set = sorted(tuple(set(y)))
        
        lon_key = round(lon_set[0])
        
        coords[round_up(lon_key)] = (lon_set, lat_set)
    
    return coords



def first_edge(year = 2013, delta1 = 3):

    '''
    First intersection of terminator and the 
    region square
    '''
    out = {}
    
    corners = set_coords(year, delta1 = delta1)

    eq_lon, eq_lat = load_equator(year, values = True)

    for key in corners.keys():
        xlim, ylim = corners[key]
        
        ilon, ilat = gg.intersection(
            eq_lon, eq_lat, [xlim[1], xlim[1]], ylim
            )
        out[key] = (ilon[0], ilat[0]) 
        
    return out

def term_eq_intersect(dn, twilight = 18):
    
    """
    Find the intersection between the equator and 
    the solar terminator (by date)
    """
 
    eq_lon, eq_lat = load_equator(dn.year, values = True)
    
    te_lon, te_lat = gg.terminator2(dn, twilight)
        
    in_lon, in_lat = gg.intersection(eq_lon, eq_lat, te_lon, te_lat)
    
    return in_lon, in_lat


def stations_near_of_equator(
        year = 2015,
        distance = 5, 
        extra_sts = []
        ):
    
    sites = gg.load_coords(year = 2013)

    out = {}
    
    for name, key in sites.items():
        lon, lat, alt = tuple(key)
        
        min_d = distance_from_equator(
                lon, 
                lat, 
                year = year
                )
        
        if min_d <= distance:
          
            out[name] = (lon, lat)
            
    if len(extra_sts) != 0:
        
        for sts in extra_sts:
            lon, lat, alt = sites[sts] 
            out[sts] = (lon, lat)
            
    return out 




def stations_coordinates(year = 2013, distance = 5):
    
    sites = stations_near_of_equator(
        year,  distance = distance
        )
    
    arr = np.array([[lon, lat] for (lon, lat) in sites.values()])
    
    return arr[:, 0], arr[:, 1]

