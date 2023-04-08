from GEO.src.core import compute_meridian, coords, run_igrf
from GEO.src.mapping import quick_map
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import settings as s
from utils import save_plot
import numpy as np
from FluxTube.src.mag import Apex
from GEO.src.conversions import dip

def apex_heights(amin = 200, amax = 400, step = 50):
    return np.arange(amin, amax + step, step)

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
    
    lat_lims = dict(min = -15, max = 15, stp = 5)
    lon_lims = dict(min = -75, max = -30, stp = 10)    
    
    quick_map(ax, lon_lims, lat_lims)
      
    max_mlat = Apex(alt).apex_lat_base(base = 150)
    
    site = "saa"
    glon, glat = coords[site][::-1]
    
    d, i = run_igrf(site = site)

    #lon_start = glon + delta_lon -43
    

    xx, yy  = compute_meridian(
        lon = lon_start, 
        alt = alt, 
        max_lat = np.degrees(max_mlat),
        year = year, 
        align_to_equator = True
            )
    
    
    ax.plot(xx, yy, lw = 2, label = f"{alt} km")
    ax.plot(glon, glat,
            marker = "^", 
            markersize = 10,
            linestyle = "none",
            color = "b",
            label = "São luis")

    ax.legend(
        ncol = 1, loc = "lower right"
        )
    
    return fig, ax  


#save_plot(plot_mag_meridians)

fig, ax = plot_mag_meridians(lon_start = -48.5)








