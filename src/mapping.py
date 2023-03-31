import cartopy.feature as cf
import cartopy.crs as ccrs
import numpy as np
import pandas as pd
import os
import settings as s


class limits(object):
    def __init__(self, **kwargs):
        self.min = kwargs['min'] 
        self.max = kwargs['max']
        self.stp = kwargs['stp']
         

def map_features(ax):
    
    states_provinces = cf.NaturalEarthFeature(
                        category = 'cultural',
                        name = 'admin_1_states_provinces_lines',
                        scale = '50m',
                        facecolor = 'none')
    
    args = dict(edgecolor = 'black', lw = 1)
    
    ax.add_feature(states_provinces, **args)
    ax.add_feature(cf.COASTLINE, **args) 
    ax.add_feature(cf.BORDERS, linestyle='-', **args)
    
    ax.gridlines(color = 'grey', 
                 linestyle = '--', 
                 crs = ccrs.PlateCarree())
    
    
def map_boundaries(ax, lon, lat):

    
    ax.set_extent([lon.min, lon.max, 
                   lat.min, lat.max], 
                  crs = ccrs.PlateCarree())

    ax.set_xticks(np.arange(lon.min, 
                            lon.max + lon.stp, 
                            lon.stp), 
                  crs = ccrs.PlateCarree()) 

    ax.set_yticks(np.arange(lat.min, 
                            lat.max + lat.stp, 
                            lat.stp), 
                  crs = ccrs.PlateCarree())
    
    ax.set(ylabel = 'Latitude (°)', 
            xlabel = 'Longitude (°)') 
        
def marker_sites(axs, sites):
 
    for key in sites.keys():
        coords = sites[key]
        lon = coords["lon"]
        lat = coords["lat"]
        axs.plot(lon, lat, 
                 marker = "o", markersize = 8)
        
        axs.text(lon, lat, key, 
                 transform = ccrs.PlateCarree())
def mag_equator(ax):
    
    """Plotting geomagnetic equator"""
    
    infile = "database/GEO/dip_2013.txt"
    df = pd.read_csv(infile, index_col = 0)
    lons = df["lon"].values
    lats = df["lat"].values

    ax.plot(lons, lats, color = "r", lw = 2)
    

def plot_dips(axs):
    infile = "database/dips/"
    
    _, _, files = next(os.walk(infile))
    
    #for filename in files:
    filename = files[2]
    args = dict(linewidths = 2, colors = "red",
                levels = [-30, -20, -10, 0])
    
    year = filename.replace(".txt", "")
    axs.set(title = f"Inclinação - {year}")
    mag_equator(axs, infile + filename, **args)
    


def quick_map(axs, lon_lims, lat_lims):

    s.config_labels()
    
    map_features(axs)
    
    lat = limits(**lat_lims)
    lon = limits(**lon_lims)    
    
    map_boundaries(axs, lon, lat)
   
    mag_equator(axs)
    
    return axs
