import cartopy.feature as cf
import cartopy.crs as ccrs
import numpy as np
from GEO.src.core import load_equator
import os
import settings as s
import matplotlib.pyplot as plt

class limits(object):
    def __init__(self, **kwargs):
        self.min = kwargs['min'] 
        self.max = kwargs['max']
        self.stp = kwargs['stp']
         

def map_features(ax, grid = False):
    
    states_provinces = cf.NaturalEarthFeature(
                        category = 'cultural',
                        name = 'admin_1_states_provinces_lines',
                        scale = '50m',
                        facecolor = 'none')
    
    args = dict(edgecolor = 'black', lw = 1)
    
    ax.add_feature(states_provinces, **args)
    ax.add_feature(cf.COASTLINE, **args) 
    ax.add_feature(cf.BORDERS, linestyle = '-', **args)
    
    if grid:
    
        ax.gridlines(
            color = 'grey', 
            linestyle = '--', 
            crs = ccrs.PlateCarree()
            )
    return ax
    
    
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
    
    ax.set(ylabel = 'Latitude (°)',  xlabel = 'Longitude (°)') 
    
    return ax
        
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
    
    eq = load_equator()
   
    ax.plot(
        eq[:, 0], 
        eq[:, 1], 
        color = "r", 
        lw = 1
        )
    return ax



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
    


def map_attrs(axs, lon_lims, lat_lims):

    s.config_labels()
    
    map_features(axs)
    
    lat = limits(**lat_lims)
    lon = limits(**lon_lims)    
    
    map_boundaries(axs, lon, lat)
   
    mag_equator(axs)
    
    return axs

lat_lims = dict(min = -15, max = 15, stp = 5)
lon_lims = dict(min = -55, max = -35, stp = 5) 

def quick_map(
        lat_lims = lat_lims, 
        lon_lims = lon_lims
        ):    
      
    fig, ax = plt.subplots(
        figsize = (8, 8), 
        dpi = 300,  
        subplot_kw = 
        {'projection': ccrs.PlateCarree()}
        )
    
    s.config_labels(fontsize = 15)
     
    map_attrs(ax, lon_lims, lat_lims)
            
    return fig, ax 

    