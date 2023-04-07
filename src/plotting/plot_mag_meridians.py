from GEO.src.mapping import quick_map
from GEO.src.core import compute_meridian
import cartopy.crs as ccrs
import matplotlib.pyplot as plt


def plot_mag_meridians(lon = -50):
    fig, ax = plt.subplots(
        figsize = (10, 10), 
        dpi = 300, 
        subplot_kw = 
        {'projection': ccrs.PlateCarree()}
        )
    
    
    lat_lims = dict(min = -30, 
                    max = 20, stp = 10)
    
    
    lon_lims = dict(min = -90, 
                    max = -15, 
                    stp = 15)    
    
    quick_map(ax, lon_lims, lat_lims)
    
    xx, yy  = compute_meridian(
            lon = lon, 
            alt = 0, 
            year = 2013
            )
    
    ax.plot(xx, yy, lw = 2)
    
    return fig 


plot_mag_meridians()




