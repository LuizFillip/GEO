import numpy as np 
import GEO as gg 
import cartopy.crs as ccrs

        
def sectors_coords(
        year = 2013, 
        radius = 10,  
        angle = -45,
        delta1 = 3
        ):
    '''
    Compute coordinates of sectors from a longitude 
    range with an inclination  
    
    '''
    df = gg.load_equator(year)

    if radius == 10:
        
        delta = delta1 #3
        longs = np.arange( -65, -30, radius)
        
    elif radius == 5:
        delta = 1.5
        longs = np.arange( -70, -35, radius)
     
    x_coords = []
    y_coords = []
               
    for slon in longs:
        
        coords = df.loc[
            (df['lon'] > slon - radius) &
            (df['lon'] < slon)].min()
        
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
        angle = 45, 
        delta1 = 3
        ):
    
    lons, lats = sectors_coords(
        year, 
        radius, 
        angle, 
        delta1 
        )
    
    coords = {}
    
    def round_up(x):
        return int(np.ceil((x - 5) / 10.0)) * 10


    for x, y in zip(lons, lats):
        
        lon_set = sorted(tuple(set(x)))
        lat_set = sorted(tuple(set(y)))
        
        lon_key = round(lon_set[0])
        
        coords[round_up(lon_key)] = (lon_set, lat_set)
    
    return coords


def middle_point(arr):
    return sum(list(set(arr))) / 2


def first_edge(year = 2013, delta1 = 3):

    '''
    First intersection of terminator and the 
    region square
    '''
    out = {}
    
    corners = set_coords(year, delta1 = delta1)

    eq_lon, eq_lat = gg.load_equator(year, values = True)

    for key in corners.keys():
        xlim, ylim = corners[key]
        
        ilon, ilat = gg.intersection(
            eq_lon, eq_lat, [xlim[1], xlim[1]], ylim
            )
        out[key] = (ilon[0], ilat[0]) 
        
    return out

def plot_rectangles_regions(
        ax,
        year = 2013,
        center_dot = False, 
        index_box = True,
        first_inter = True,
        delta1 = 3
        ):
    
    lons, lats = sectors_coords(year, delta1 = delta1)
    
    numbers = list(range(len(lons)))
    
        
    for i, (xlim, ylim) in enumerate(zip(lons, lats)):
        
        index = numbers[i] + 1 
        
        ax.plot(
            xlim, ylim,
            color = 'black', 
            linewidth = 2, 
            transform = ccrs.PlateCarree(),
            )
        
        clon = middle_point(xlim)
        clat = middle_point(ylim)
        
        if center_dot:
            ax.scatter(clon, clat, c = 'b', s = 100)
        
        if index_box:
            ax.text(
                clon, max(ylim) + 1, index, 
                transform = ax.transData,
                fontsize = 35
                )
            
    if first_inter:
        for (x, y) in first_edge(year).values():
        
            ax.scatter(x, y, c = 'k', s = 400, marker = '*')
            
    return 



