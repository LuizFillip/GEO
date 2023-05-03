from GEO import quick_map#, marker_sites
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
#from GEO import get_receivers_in_range, circle_range, sites
from GEO import run_igrf, sites


    
def plot_map():
    fig, ax = plt.subplots(
        figsize = (5, 5), 
        subplot_kw = {'projection': ccrs.PlateCarree()}
        )
    
    
    
    quick_map(ax, lon_lims, lat_lims)
    
    return fig, ax 

def plot_circles_ranges(
        ax, 
        sites, 
        radius = 500
        ):
    
    for site in sites.keys():
        
        clat, clon = tuple(sites[site].values())
        
        circle_range(
            ax, 
            clon,
            clat, 
            radius = radius, 
            color = "gray"
            )


def plot_brazil_receivers(sites):
    fig, ax = plot_map(sites)
    
    path_json = "database/GNSS/json/2013/001.json"
    
    plot_circles_ranges(
            ax, 
            sites, 
            radius = 500
            )
    #get_receivers_in_range(path_json, sites, ax = ax)
    
  
lat_lims = dict(min = -30, 
                max = 0, 
                stp = 5)

lon_lims = dict(min = -60, 
                max = -30, 
                stp = 5)    

    
    
fig, ax = quick_map(lat_lims = lat_lims, 
          lon_lims = lon_lims)

for site in ["car", "cap"]:
    lat, lon = sites[site]["coords"]
    ax.scatter(lon, lat, s = 40)