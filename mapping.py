import cartopy.feature as cf
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import setup as s


class limits(object):
    def __init__(self, **kwargs):
        self.min = kwargs['min'] 
        self.max = kwargs['max']
        self.stp = kwargs['stp']
         

def map_features(ax):
    
    states_provinces = cf.NaturalEarthFeature(
                        category='cultural',
                        name='admin_1_states_provinces_lines',
                        scale='50m',
                        facecolor='none')
    
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
    
    axs.set(ylabel = 'Latitude (°)', 
            xlabel = 'Longitude (°)') 
        
def marker_sites(axs):
    sites = {
            'Fortaleza': {'lat': -3.73, 'lon': -38.522}, 
             'Sao luis': {'lat': -2.53, 'lon': -44.296}, 
             'Cariri':   {"lat": -7.38, 'lon': -36.528}
             }
    
    for key in sites.keys():
        coords = sites[key]
        lon = coords["lon"]
        lat = coords["lat"]
        axs.plot(lon, lat, 
                 marker = "o", markersize = 8)
        
        axs.text(lon + 1, lat, key, 
                 transform = ccrs.PlateCarree())
def equator(ax, 
            infile, 
            label = True,
            **args):
    
    """Plotting geomagnetic equator"""
    
    df = pd.read_csv(infile, 
                     index_col = 0)

    pivot = pd.pivot_table(df, 
                           columns = "lon", 
                           index = "lat", 
                           values = "i")
    
    cs = ax.contour(pivot.columns, 
                    pivot.index, 
                    pivot.values, 
                    transform = ccrs.PlateCarree(), 
                    **args)
    
    cs.cmap.set_over('red')
    
    if label:
        x = -55
        manual_locations = [(x, -10), 
                            (x, -15), 
                            (x, -20), 
                            (x, -25)]
        
        ax.clabel(cs, 
                  inline = 8, 
                  fontsize = 15, 
                  manual = manual_locations)



ncols, nrows = 1, 1
heigth, width = 8, 6


fig, axs = plt.subplots(figsize = (heigth, width), 
                       ncols = ncols, 
                       nrows = nrows, 
                       subplot_kw = {'projection': 
                                     ccrs.PlateCarree()})
s.config_labels()

map_features(axs)


lat = limits(min = -40.0, max = 10, stp = 10)
lon = limits(min = -80, max = -30, stp = 10)

#lat = limits(min = -90.0, max = 90, stp = 15)
#lon = limits(min = -180, max = 180, stp = 30)

    
map_boundaries(axs, lon, lat)
marker_sites(axs)


infile = "database/dips/"

_, _, files = next(os.walk(infile))



#for filename in files:
filename = files[2]
args = dict(linewidths = 2, colors = "red",
            levels = [-30, -20, -10, 0])

year = filename.replace(".txt", "")
axs.set(title = f"Inclinação - {year}")
equator(axs, infile + filename, **args)

