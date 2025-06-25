import shapely.geometry as sgeom
from cartopy.geodesic import Geodesic
import cartopy.crs as ccrs
import GEO as gg 
import matplotlib.colors as mcolors
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
from matplotlib.patches import Circle

markers = [
    "o", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "P",
    "*", "h", "H", "+", "x", "X", "D", "d", "|", "_"
]
    

def plot_circle(
        ax, 
        center_lon, 
        center_lat, 
        radius = 500, 
        edgecolor = "gray",
        lw = 3
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
        edgecolor = edgecolor, 
        lw = lw,
        # alpha = 0.5,
        facecolor='none',
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


def connection_areas(
        ax1, 
        ax2, 
        xy, 
        color = 'b', 
        radius = 0.1
        ):
    
  
     # Radius of the circle
    circle = Circle(
        xy, 
        radius, 
        fill = False, 
        edgecolor=color)
    
    
    ax1.add_patch(circle)
    
    x_center, y_center = xy
    
    con1 = ConnectionPatch(
        xyA = (x_center + radius, y_center), 
        xyB = (0, 0),       
        coordsA="data", 
        coordsB="axes fraction",
        arrowstyle='->', 
        axesA=ax1, 
        axesB=ax2, color=color, zorder=10)
    
    con2 = ConnectionPatch(
        xyA=(x_center + radius, y_center), xyB=(0, 1),         
        coordsA="data", 
        coordsB="axes fraction",
        axesA=ax1, axesB=ax2, 
        color=color, zorder=10)
    
    ax2.add_artist(con1)
    ax2.add_artist(con2)

def plot_areas(ax, ax1, ax2, site):

    lat, lon = gg.sites['car']['coords']
    xy = (lon, lat)
    connection_areas(
        ax, ax1, xy, color = 'k', 
                     radius = 5)
    
    gg.plot_circle(
            ax, 
            lon, 
            lat, 
            radius = 500, 
            
            edgecolor = "k"
            )
    
    
    if site[0] == 'S':
        lat, lon = gg.sites['saa']['coords']
    else:
        lat, lon = gg.sites['fza']['coords']
        
    gg.plot_circle(
            ax, 
            lon, 
            lat, 
            radius = 230, 
            edgecolor = "r"
            )
    
        
    xy = (lon, lat)
    connection_areas(ax, ax2, xy, color = 'w')



    
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
        color = 'black',
        center_dot = False
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
        color = color, 
        linewidth = 4, 
        # marker = '.',
        transform=ccrs.PlateCarree() 
        )
    
    
    center_lat = (lat_max + lat_min) / 2
    center_lon = (lon_max + lon_min) / 2
    
    if center_dot:
        ax.scatter(center_lon, center_lat)
    
    return center_lon, center_lat

colors = list(mcolors.CSS4_COLORS.keys())


