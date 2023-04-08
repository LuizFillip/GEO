from GEO.src.mapping import quick_map
from GEO.src.core import compute_meridian, coords
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import settings as s
from utils import save_plot
import numpy as np
from FluxTube.src.mag import Apex

def apex_heights(amin = 200, amax = 400, step = 50):
    return np.arange(amin, amax + step, step)

def plot_mag_meridians(
        lon_start = -48.5, 
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
    
    lat_lims = dict(min = -20, max = 10, stp = 5)
    lon_lims = dict(min = -75, max = -30, stp = 10)    
    
    _, df = quick_map(ax, lon_lims, lat_lims)
      
    max_mlat = Apex(alt).apex_lat_base(base = 150)

    xx, yy  = compute_meridian(
        lon = lon_start, 
        alt = alt, 
        max_lat = np.degrees(max_mlat),
        year = year
            )
    
    def middle(array):
        return array[int((len(array) - 1) /2)]

    
   
    
    ds = df.loc[(df["lon"] > xx[0]) & (df["lon"] < xx[-1]) & 
                (df["lat"] < yy[0]) & (df["lat"] > yy[-1])]
    
  
    xd, yd = tuple(ds.iloc[int((len(ds) -  1) /2) - 1, :].values)
     
    ax.plot(xd, yd,"o", label = "dip")
    
    
    nx = middle(xx) + abs(xd - middle(xx))
    ny = middle(yy) + abs(yd - middle(yy))
    ax.plot(nx, ny, "o", label = "centro", 
            markersize = 10)
    
    ax.plot(xx + abs(xd - middle(xx)), 
            yy + abs(yd - middle(yy)), lw = 2, 
            label = f"{alt} km")
    
    
    
    glon, glat = coords["saa"][::-1]
    
    ax.plot(glon, glat,
            marker = "^", 
            markersize = 15,
            linestyle = "none",
            color = "b",
            label = "São luis")
    
    
    ax.legend(
       # bbox_to_anchor=[0.5, 1.1], 
        ncol = 1, loc = "upper right"
        )
    
    return fig 


#save_plot(plot_mag_meridians)





fig = plot_mag_meridians()


