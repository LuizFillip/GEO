import numpy as np
import datetime as dt
import spacepy.coordinates as coord
from spacepy.time import Ticktock


def colatitude(latitude):
    return (np.pi / 2) - latitude

def convert_to_dip(table):
    return np.rad2deg(np.arctan(np.tan(np.deg2rad(table)) * 0.5))

def dip(inclination):
   """Latitude inlicação magnética (dip) """
   return np.degrees(np.arctan(0.5 * np.tan(
       np.radians(inclination)) / 2)
       )

def geo2mag(geo_lat, geo_lon, date):
    """
    return the magnetic coords in the 
    same units as the geographic"""
    
    Re = 6378.0 #mean Earth radius in kilometers
     
    cvals = coord.Coords([float(Re), 
                          float(geo_lat), 
                          float(geo_lon)], 
                         'GEO', 'sph', 
                         ['Re','deg','deg'])
    
    date = date.strftime("%Y-%m-%dT%H:%M")
    cvals.ticks = Ticktock([date], 'UTC')
    
    dat_coords =  cvals.convert('MAG','sph').data[0]
    
    mag_lat = dat_coords[1]
    mag_lon = dat_coords[2]
    
    return (mag_lat, mag_lon)


def mag2geo(mag_lat, mag_lon, date):
    
    """
    Convert the results from 'geo_to_mag' functions
    from numeric tuple
    
    """
    
    r = 6378.0
    
    date = date.strftime("%Y-%m-%dT%H:%M")
    
    cvals = coord.Coords([float(300 + r), 
                          float(mag_lat), #
                          float(mag_lon)], 
                         'MAG', 'sph', 
                         ['Re','deg','deg'])
    
    
    cvals.ticks = Ticktock([date], 'UTC')
    
    dat_coords = cvals.convert('GEO','sph').data[0]
    
    geo_lat = dat_coords[1]
    geo_lon = dat_coords[2]
    
    return geo_lat, geo_lon

def main():
  
    date = dt.datetime(2013, 1, 1)
    
    glat, glon  = -2.53, -44.296
    
    mlat, mlon = geo2mag(glat, glon, date)
    
    print("geografic coords: {glat}, {glon}")
    
    glat, glon = mag2geo(0, mlon, date)
    
    
            