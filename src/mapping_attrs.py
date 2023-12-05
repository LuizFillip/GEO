import shapely.geometry as sgeom
from cartopy.geodesic import Geodesic
import cartopy.crs as ccrs
import GEO as gg 
import numpy as np
import base as b 

def find_range(x, y, clon, clat, radius = 12):
    
    factor = radius / 2 # in degrres
    
    left_x = clon - factor
    right_x = clon + factor
    
    down_y = clat - factor
    up_y = clat + factor
    
    first = (
        (y < up_y) and (y > clat) and 
        (x < right_x) and (x > clon)
        )
        
    second = (
        (y < up_y) and (y > clat) and 
        (x > left_x) and (x < clon)
        )
        
    third = (
        (y > down_y) and (y < clat) and 
        (x > left_x) and (x < clon)
        )
    
    quarter = (
        (y > down_y) and (y < clat) and 
        (x < right_x) and (x > clon)
        )
    
    return any([first, second, third, quarter])


def circle_range(
        ax, 
        longitude, 
        latitude, 
        radius = 500, 
        color = "gray"
        ):
             
    
    gd = Geodesic()

    cp = gd.circle(
        lon = longitude, 
        lat = latitude, 
        radius = radius * 1000.
        )
    
    geoms = [sgeom.Polygon(cp)]

    ax.add_geometries(
        geoms, 
        crs = ccrs.PlateCarree(), 
        edgecolor = 'black', 
        color = color,
        alpha = 0.2, 
        label = 'radius'
        )
    
def ellipse(
        center, 
        angle = 95, 
        semi_major = 10.0, 
        semi_minor = 1.0
        ):
     
    
    angle_rad = np.deg2rad(angle)
    
    t = np.linspace(0, 2 * np.pi, 100)
 
    x = (center[0] + semi_major * np.cos(t) * 
         np.cos(angle_rad) - semi_minor * np.sin(t) * 
         np.sin(angle_rad))
    
    y = (center[1] + semi_major * np.cos(t) * 
         np.sin(angle_rad) + semi_minor * 
         np.sin(t) * np.cos(angle_rad))
    
    return x, y
    
def plot_ellipse(ax, year = 2014, lon = -60):
    
   
    eq_lon, eq_lat  = gg.load_equator(
        year, values = True)
    
    i = b.find_closest(eq_lon, lon)
    
    x, y = ellipse((eq_lon[i], eq_lat[i]))
    
    ax.plot(x, y)
    
    ax.fill(x, y, color = 'gray', alpha = 0.5)
    
def marker_sites(axs, sites):
 
    for key in sites.keys():
        lat, lon = sites[key]["coords"]
        axs.scatter(
            lon, lat, 
            c = 100, 
            marker = "o")
        
        axs.text(lon, lat, key, 
                 transform = ccrs.PlateCarree())
        

def plot_square_area(
        ax, 
        lat_min = -12, 
        lon_min = -42,
        lat_max = None, 
        lon_max = None, 
        radius = 10, 
        ):
    
    
    """Plotting square area by coords limits"""
    
    if lat_max is None:
        lat_max = lat_min + radius
    
    if lon_max is None:
        lon_max = lon_min + radius
        
    x_limits = [
        lon_min, lon_max, 
        lon_max, lon_min, lon_min
        ]
    
    y_limits = [
        lat_min, lat_min, 
        lat_max, lat_max, lat_min
        ]
    
    ax.plot(
        x_limits, y_limits,
        color = 'black', 
        linewidth = 2, 
        marker = '.',
        transform=ccrs.PlateCarree() 
        )
    
    
    center_lat = (lat_max + lat_min) / 2
    center_lon = (lon_max + lon_min) / 2

    ax.scatter(center_lon, center_lat)
    
    return center_lon, center_lat


def distance_from_equator(
        lon, lat, year = 2013
        ):
    eq = gg.load_equator(year)
    x, y = eq[:, 0], eq[:, 1]
    min_x, min_y, min_d = gg.compute_distance(
        x, y, lon, lat
        )
    return min_d

def middle_point(xlim, ylim):
     clat = sum(list(set(ylim))) / 2
     clon = sum(list(set(xlim))) / 2
     
     return clon, clat