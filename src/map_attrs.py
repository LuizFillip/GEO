import shapely.geometry as sgeom
from cartopy.geodesic import Geodesic
import cartopy.crs as ccrs

def find_range(x, y, clon, clat, radius = 500):
    
    factor = radius / 111
    
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

lat_min = -12 
lat_max = -2 
lon_max = -32
lon_min = -42
