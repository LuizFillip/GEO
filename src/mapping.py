import cartopy.feature as cf
import cartopy.crs as ccrs
import numpy as np
import GEO as g
import matplotlib.pyplot as plt

lat_lims = dict(min = -30, max = 15, stp = 10)
lon_lims = dict(min = -90, max = -30, stp = 10) 

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
    
    """Plotting extensions and ticks"""
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
    
    ax.set(
        ylabel = 'Latitude (°)',  
        xlabel = 'Longitude (°)'
        ) 
    
    return ax


def mag_equator(
        ax, 
        year = 2013, 
        degress = None
        ):
    
    """Plotting geomagnetic equator"""
        
    x, y = g.load_equator(year, values = True)
  
    ax.plot(x, y, color = 'r', lw = 2)
    
    if degress is not None:
        ax.fill_between(
            x, 
            y + degress, 
            y - degress, 
            alpha = 0.2, 
            color = 'tomato'
            )
    return x, y

def map_attrs(
        ax, 
        year = None,
        lon_lims = lon_lims, 
        lat_lims = lat_lims,
        grid = True
        ):

    map_features(ax, grid)
    
    lat = limits(**lat_lims)
    lon = limits(**lon_lims)    
    
    map_boundaries(ax, lon, lat)
    
    if year is not None:
        x, y = mag_equator(
            ax,
            year,
            degress = None
            )
        
        return x, y


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

    
