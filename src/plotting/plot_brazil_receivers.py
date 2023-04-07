from GEO.mapping import quick_map, marker_sites
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from GEO.map_attrs import get_receivers_in_range, circle_range, sites
from GEO.src.core import run_igrf, coords


    
def plot_map(sites):
    fig, ax = plt.subplots(
        figsize = (5, 5), 
        subplot_kw = {'projection': ccrs.PlateCarree()}
        )
    
    
    lat_lims = dict(min = -10, 
                    max = 5, 
                    stp = 5)
    
    lon_lims = dict(min = -50, 
                    max = -30, 
                    stp = 5)    
    
    quick_map(ax, lon_lims, lat_lims)

    marker_sites(ax, sites)
    
    return fig, ax 

def plot_circles_ranges(
        ax, 
        sites, 
        radius = 500
        ):
    
    for site in sites.keys():
        
        clat, clon = tuple(sites[site].values())
        
        circle_range(
            ax, 
            clon,
            clat, 
            radius = radius, 
            color = "gray"
            )


def plot_brazil_receivers(sites):
    fig, ax = plot_map(sites)
    
    path_json = "database/GNSS/json/2013/001.json"
    
    plot_circles_ranges(
            ax, 
            sites, 
            radius = 500
            )
    get_receivers_in_range(path_json, sites, ax = ax)
    
    
def main():

    fig, ax = plt.subplots(
        figsize = (10, 10), 
        subplot_kw = {'projection': ccrs.PlateCarree()}
        )
    
    
    lat_lims = dict(min = -40, 
                    max = 10, 
                    stp = 5)
    
    lon_lims = dict(min = -80, 
                    max = -30, 
                    stp = 5)    
    
    quick_map(ax, lon_lims, lat_lims)
    
    path_json = "database/GNSS/json/2013/001.json"
    
    get_receivers_in_range(path_json, sites, ranged = False, ax = ax)