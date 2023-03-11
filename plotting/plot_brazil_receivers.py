from GEO.mapping import quick_map, marker_sites
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from GEO.map_attrs import get_receivers_in_range, circle_range, sites


    
def plot_map(sites):
    fig, ax = plt.subplots(
        figsize = (8, 8), 
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
    
    path_json = "D:\\database\\json\\2013\\300.json"
    
    plot_circles_ranges(
            ax, 
            sites, 
            radius = 500
            )
    get_receivers_in_range(path_json, sites, ax = ax)


