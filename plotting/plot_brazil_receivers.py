import json 
from GEO.mapping import quick_map, marker_sites
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from GNSS.IPP import convert_coords
import shapely.geometry as sgeom
from cartopy.geodesic import Geodesic
import numpy as np


path_json = "database/GNSS/json/2013/001.json"


sites = {
         'Fortaleza': {'lat': -3.73, 'lon': -38.522}, 
         'Sao luis': {'lat': -2.53, 'lon': -44.296}, 
         "Cachoeira": {"lat": -22.7038, 'lon': -45.0093}, 
         "Santa Maria": {"lat": -29.6897, "lon": -53.8043}
         }

def circle_range(ax, longitude, latitude, 
                 radius = 500, color = "gray"):
             
    gd = Geodesic()

    cp = gd.circle(lon = longitude, 
                   lat = latitude, 
                   radius = radius * 1000.)
    
    geoms = [sgeom.Polygon(cp)]

    ax.add_geometries(geoms, crs=ccrs.PlateCarree(), 
                      edgecolor = 'black', color = color,
                      alpha = 0.2, label = 'radius')
    
    
def plot_map(sites):
    fig, ax = plt.subplots(
        figsize = (8, 8), 
        subplot_kw = {'projection': ccrs.PlateCarree()}
        )
    
    
    lat_lims = dict(min = -40, 
                    max = 10, 
                    stp = 5)
    
    lon_lims = dict(min = -80, 
                    max = -30, 
                    stp = 5)    
    
    quick_map(ax, lon_lims, lat_lims)

    marker_sites(ax, sites)
    
    return fig, ax 



fig, ax = plot_map(sites)


dat = json.load(open(path_json)) 




def find_range(x, y, clon, clat, radius = 500):
    
    factor = radius / 111
    
    xleft = clon - factor
    xright = clon + factor
    
    ydown = clat - factor
    yup = clat + factor
    
    first = ((y < yup) and (y > clat) and 
             (x < xright) and (x > clon))
        
    second = ((y < yup) and (y > clat) and 
              (x > xleft) and (x < clon))
        
    third = ((y > ydown) and (y < clat) and 
             (x > xleft) and (x < clon))
    
    quarter = ((y > ydown) and (y < clat) and 
               (x < xright) and (x > clon))
    
    return any([first, second, third, quarter])


for site in sites.keys():
    clat, clon = tuple(sites[site].values())
    circle_range(
        ax, 
        clon,
        clat, 
        radius = 500, 
        color = "gray"
        )
  
for site, coords in dat.items():
    try:
        positions = coords["position"]
        ox, oy, oz = tuple([float(f) for f in positions])
        lon, lat, alt = convert_coords(ox, oy, oz, 
                                       to_radians = False)
        
        for site in sites.keys():
            clat, clon = tuple(sites[site].values())
            
            if find_range(lon, lat, clon, clat):
                ax.plot(lon, lat, 
                        marker = "o", 
                        color = "k", 
                        markersize = 3)
    except:
        print(site)


