from GEO.src.core import compute_meridian, coords, run_igrf
from GEO.src.mapping import quick_map
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import settings as s
from utils import save_plot
import numpy as np
from FluxTube.src.mag import Apex
from GEO.src.conversions import dip

def plot_mag_meridians(
        lon_start = -48, 
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
      
    max_mlat = Apex(alt).apex_lat_base(base = 150)
    

    x, y  = compute_meridian(
        lon = lon_start, 
        alt = alt, 
        max_lat = np.degrees(max_mlat),
        year = year, 
        align_to_equator = True
            )
    
    
    ax.plot(x, y, lw = 2, label = f"{alt} km")
    
    glon, glat = coords["saa"][::-1]
    
    d, i = run_igrf(site = "saa")
    print(d, i)
    
    ax.scatter(
        glon, glat,
        marker = "^", 
        s = 50,
        color = "b",
        label = "São luis")
    
    
    glon, glat = coords["jic"][::-1]
    
    ax.scatter(
        glon, glat,
        marker = "^", 
        s = 50,
        label = "Jicamarca")
    
    d, i = run_igrf(site = "jic")
    
    x, y  = compute_meridian(
        lon = glon + d, 
        alt = alt, 
        max_lat = np.degrees(max_mlat),
        year = year, 
        align_to_equator = False
            )
    
    
    ax.plot(x, y, lw = 2, label = f"{alt} km")
    

    ax.legend(
        ncol = 1, loc = "best"
        )
    
    return fig, ax  


#save_plot(plot_mag_meridians)

fig, ax = plot_mag_meridians(lon_start = -48.5)








