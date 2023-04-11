from GEO.src.core import compute_meridian, sites
from GEO.src.mapping import quick_map
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import settings as s
from utils import save_plot
import numpy as np
from FluxTube.src.mag import Apex



def plot_all_meridians(
         ax, 
         slon = -100, 
         elon = -30, 
         step = 1, 
         max_lat = 40, 
         alt = 300, 
         year = 2013
         ):
 
     for lon in np.arange(slon, elon, step):
         
         x, y  = compute_meridian(
             lon = lon, 
             alt = alt, 
             max_lat = max_lat,
             year = year
                 )
             
         ax.plot(x, y, lw = 1, color = "tomato")
         
def plot_sites(ax):
    
    for site in ["jic", "saa", "car"]:
    
        glat, glon = sites[site]["coords"]
        name = sites[site]["name"]
        
        ax.scatter(glon, glat,
            marker = "^", 
            s = 100,
            label = name)
        
        

def plot_mag_meridians(
        alt = 300, 
        max_lat = 10, 
        year = 2013
        ):
    
    fig, ax = plt.subplots(
        figsize = (8, 8), 
        dpi = 300, 
        subplot_kw = 
        {'projection': ccrs.PlateCarree()}
        )
    
    s.config_labels(fontsize = 15)
    
    lat_lims = dict(min = -30, max = 15, stp = 5)
    lon_lims = dict(min = -100, max = -30, stp = 10)    
    
    quick_map(ax, lon_lims, lat_lims)
    
    
    #max_mlat = Apex(alt).apex_lat_base(base = 150)
    
    alt = 300
    plot_all_meridians(
             ax, 
             slon = -100, 
             elon = -30, 
             step = 0.5, 
             max_lat = 80, 
             alt = alt, 
             year = 2013
             )
    
    quick_map(ax, lon_lims, lat_lims)
        
    plot_sites(ax)
    ax.set(title = f"{alt} km - {year}")
    ax.legend(ncol = 1, loc = "upper right")
    
    return fig, ax  


#save_plot(plot_mag_meridians)

#fig, ax = plot_mag_meridians()



fig, ax = plt.subplots(
    figsize = (8, 8), 
    dpi = 300, 
    subplot_kw = 
    {'projection': ccrs.PlateCarree()}
    )


lat_lims = dict(min = -10, max = 10, stp = 5)
lon_lims = dict(min = -50, max = -40, stp = 10)    

quick_map(ax, lon_lims, lat_lims)





