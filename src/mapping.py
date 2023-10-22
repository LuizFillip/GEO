import cartopy.feature as cf
import cartopy.crs as ccrs
import numpy as np
import GEO as g
import matplotlib.pyplot as plt

class limits(object):
    def __init__(self, **kwargs):
        self.min = kwargs['min'] 
        self.max = kwargs['max']
        self.stp = kwargs['stp']
         

def map_features(ax, grid = True):
    
    states = cf.NaturalEarthFeature(
        category = 'cultural',
        name = 'admin_1_states_provinces_lines',
        scale = '50m',
        facecolor = 'none'
        )
    
    args = dict(edgecolor = 'black', lw = 1)
    
    ax.add_feature(states, **args)
    ax.add_feature(cf.COASTLINE, **args) 
    ax.add_feature(
        cf.BORDERS, linestyle = '-', **args)
    
    if grid:
    
        ax.gridlines(
            color = 'grey', 
            linestyle = '--', 
            crs = ccrs.PlateCarree()
            )
    return ax
    
    
def map_boundaries(ax, lon, lat):
  
    ax.set_extent(
        [lon.min, lon.max, 
        lat.min, lat.max], 
        crs = ccrs.PlateCarree()
        )

    ax.set_xticks(
        np.arange(
            lon.min, 
            lon.max + lon.stp, 
            lon.stp
            ), 
            crs = ccrs.PlateCarree()
        ) 

    ax.set_yticks(
        np.arange(
            lat.min, 
            lat.max + lat.stp, 
            lat.stp
            ), 
            crs = ccrs.PlateCarree()
        )
    
    ax.set(ylabel = 'Latitude (°)',  
           xlabel = 'Longitude (°)') 
    
    return ax

def marker_sites(axs, sites):
 
    for key in sites.keys():
        lat, lon = sites[key]["coords"]
        axs.scatter(
            lon, lat, 
            c = 100, 
            marker = "o")
        
        axs.text(lon, lat, key, 
                 transform = ccrs.PlateCarree())
        

def mag_equator(
        ax, 
        year = 2013, 
        degress = None
        ):
    
    """Plotting geomagnetic equator"""
        
    eq = g.load_equator(year)
    x, y = eq[:, 0], eq[:, 1] 
    ax.plot(x, y, color = 'r', lw = 2)
    
    if degress is not None:
        ax.fill_between(
            x, 
            y + degress, 
            y - degress, 
            alpha = 0.2, 
            color = 'tomato'
            )
    return ax


lat_lims = dict(min = -45, max = 15, stp = 5)
lon_lims = dict(min = -80, max = -35, stp = 5) 

def map_attrs(
        axs, 
        lon_lims, 
        lat_lims,
        grid = False
        ):

    map_features(axs, grid)
    
    lat = limits(**lat_lims)
    lon = limits(**lon_lims)    
    
    map_boundaries(axs, lon, lat)
   
    return axs


def quick_map(
        lat_lims = lat_lims, 
        lon_lims = lon_lims,
        figsize = (8, 8),
        year = 2014,
        degress = 10,
        grid = False
        ):    
      
    fig, ax = plt.subplots(
        figsize = figsize, 
        dpi = 300,  
        subplot_kw = 
        {'projection': ccrs.PlateCarree()}
        )
         
    map_attrs(ax, lon_lims, lat_lims, grid)
    
    mag_equator(ax, 
                year = year, 
                degress = degress
                )
            
    return fig, ax 

    
