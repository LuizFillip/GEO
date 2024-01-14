import shapely.geometry as sgeom
from cartopy.geodesic import Geodesic
import cartopy.crs as ccrs
import GEO as gg 
import base as b 
import matplotlib.colors as mcolors
from shapely.geometry import Polygon
import matplotlib.pyplot as plt

markers = [
    "o", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "P",
    "*", "h", "H", "+", "x", "X", "D", "d", "|", "_"
]
    

def plot_circle(
        ax, 
        center_lon, 
        center_lat, 
        radius = 500, 
        color = "gray"
        ):
             
    cp = Geodesic().circle(
        lon = center_lon, 
        lat = center_lat, 
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
    
def plot_rectangle(ax, longitudes, latitudes):
    
    square = Polygon(zip(longitudes, latitudes))
    
    x, y = square.exterior.xy
    
    ax.add_patch(plt.Polygon(
        list(zip(x, y)),
        transform = ccrs.PlateCarree(), 
        color = 'red', 
        alpha = 0.5)
        )
    

def plot_ellipse(ax, year = 2014, lon = -60):
    
   
    eq_lon, eq_lat  = gg.load_equator(
        year, values = True)
    
    i = b.find_closest(eq_lon, lon)
    
    x, y = b.ellipse((eq_lon[i], eq_lat[i]))
    
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
                 transform = ccrs.PlateCarree()
                 )
        
    
def plot_sites_markers(ax, sites, names):
    
    colors = ['g', 'b', 'red']
    for i, site in enumerate(sites):
    
        glat, glon = gg.sites[site]['coords']
        name =  names[i]
        marker = markers[i]
    
        ax.scatter(
            glon, glat,
            s = 200, 
            c = colors[i],
            label = name, 
            marker = marker
            )
        
    return ax
        
        
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

colors = list(mcolors.CSS4_COLORS.keys())


