import numpy as np 
import GEO as gg 
import pandas as pd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt



def longitude_sector(
        ds, 
        long_start, 
        long_delta = 10
        ):

    s = (ds['lon'] >= long_start)
    e = (ds['lon'] <= long_start + long_delta)
    
    return ds.loc[s & e].sort_index()

        
def corner_coords(
        year = 2013, 
        radius = 5,  
        angle = -45
        ):
    
    df = gg.load_equator(year)

    if radius == 10:
        
        delta = 3
        longs = np.arange( -65, -30, radius)
        
    elif radius == 5:
        delta = 1.5
        longs = np.arange( -70, -35, radius)
     
    x_coords = []
    y_coords = []
               
    for slon in longs:
        
        coords = df.loc[
            (df['lon'] > slon - radius) &
            (df['lon'] < slon)
            ].min()
        
        
        clon = coords['lon']
        clat = coords['lat']
                
        x_limits = []
        y_limits = []
        
        for i in range(4):
            angle_corner = np.radians(angle) + i * np.pi / 2  
            x = clon + (radius - delta) * np.cos(angle_corner)
            y = clat + 10 * np.sin(angle_corner) 
            
            x_limits.append(round(x, 4))
            y_limits.append(round(y, 4))
        
        
        x_limits.append(x_limits[0])
        y_limits.append(y_limits[0])
        
        x_coords.append(x_limits)
        y_coords.append(y_limits)
    
    
    return x_coords[::-1], y_coords[::-1]
            
    
def set_coords(
        year = 2013, 
        radius = 10, 
        angle = 45
        ):
    
    x_coords, y_coords = corner_coords(
        year, 
        radius, 
        angle 
        )
    
    coords = {}
    
    for x, y in zip(x_coords, y_coords):
        
        lon_set = sorted(tuple(set(x)))
        lat_set = sorted(tuple(set(y)))
        
        lon_key = round(lon_set[0])
        
        coords[lon_key] = (lon_set, lat_set)
    
    return coords


def middle_point(arr):
    return sum(list(set(arr))) / 2

def plot_rectangles_regions(
        ax,
        center = False, 
        label_box = False
        ):
    
    x_coords, y_coords = corner_coords(
            year = 2013, 
            radius = 10,  
            angle = -45
            )
    
    numbers = list(range(len(x_coords)))
        
    for i, (xlim, ylim) in enumerate(zip(x_coords, y_coords)):
        
        index = numbers[i] + 1 
        ax.plot(
            xlim, ylim,
            color = 'black', 
            linewidth = 2, 
            transform = ccrs.PlateCarree(),
            )
        
        clon = middle_point(xlim)
        clat = middle_point(ylim)
        
        if center:
            ax.scatter(clon, clat, c = 'k', s = 100)
        
        if label_box:
            ax.text(
                clon, 
                max(ylim) + 1, index, 
                transform = ax.transData)
            
    return 

fig, ax = plt.subplots(
    dpi = 300,
    sharex = True, 
    figsize = (10,10),
    subplot_kw = {'projection': ccrs.PlateCarree()}
)

year = 2013

gg.map_attrs(ax, year = 2013, grid = False)

plot_rectangles_regions(
    ax,
        center = True, 
        label_box = True
        )

set_coords(
        year = 2013, 
        radius = 10, 
        angle = 45
        )