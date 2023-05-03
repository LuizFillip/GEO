from GEO import quick_map
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import shapely.geometry as sgeom
from cartopy.geodesic import Geodesic
from GEO import sites
import json 


def circle_range(
        ax, 
        longitude, 
        latitude, 
        radius = 500, 
        color = "gray"
        ):
             
    
    gd = Geodesic()

    cp = gd.circle(lon = longitude, 
                   lat = latitude, 
                   radius = radius * 1000.)
    
    geoms = [sgeom.Polygon(cp)]

    ax.add_geometries(geoms, crs=ccrs.PlateCarree(), 
                      edgecolor = 'black', color = color,
                      alpha = 0.2, label = 'radius')

def plot_brazil_receivers():
  
    lat_lims = dict(min = -30, 
                    max = 0, 
                    stp = 5)
    
    lon_lims = dict(min = -60, 
                    max = -30, 
                    stp = 5)    
    
        
        
    fig, ax = quick_map(
        lat_lims = lat_lims, 
        lon_lims = lon_lims)
    
    for site in ["car", "cap"]:
        s = sites[site]
        lat, lon = s["coords"]
        ax.scatter(lon, lat, s = 200, 
                   marker = "^", 
                   label = s["name"])
        
        circle_range(ax, lon, lat,
                radius = 500, 
                color = "gray"
                )
        
    ax.legend(loc = "lower right")
    
    dat = json.load(open("coords.json"))
    
    
    for key in dat.keys():
        lon, lat = tuple(dat[key])
        
        ax.scatter(lon, lat, 
                   marker = "o", color = "r")
        
    
    ax.set(title = "15/01/2022")
    
    fig.savefig("meteor_stations.png", dpi = 400)