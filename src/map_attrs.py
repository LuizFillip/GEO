import shapely.geometry as sgeom
from cartopy.geodesic import Geodesic
import cartopy.crs as ccrs
from GNSS.IPP import convert_coords
import json 



def find_range(x, y, clon, clat, radius = 500):
    
    factor = radius / 111
    
    left_x = clon - factor
    right_x = clon + factor
    
    down_y = clat - factor
    up_y = clat + factor
    
    first = ((y < up_y) and (y > clat) and 
             (x < right_x) and (x > clon))
        
    second = ((y < up_y) and (y > clat) and 
              (x > left_x) and (x < clon))
        
    third = ((y > down_y) and (y < clat) and 
             (x > left_x) and (x < clon))
    
    quarter = ((y > down_y) and (y < clat) and 
               (x < right_x) and (x > clon))
    
    return any([first, second, third, quarter])

def circle_range(
        ax, 
        longitude, 
        latitude, 
        radius = 500, 
        color = "gray"
        ):
             
    
    gd = Geodesic()

    cp = gd.circle(lon = longitude, 
                   lat = latitude, 
                   radius = radius * 1000.)
    
    geoms = [sgeom.Polygon(cp)]

    ax.add_geometries(geoms, crs=ccrs.PlateCarree(), 
                      edgecolor = 'black', color = color,
                      alpha = 0.2, label = 'radius')


    
def get_receivers_in_range(
        path_json, 
        sites = sites, 
        ranged = False, 
        ax = None
        ):
    
    args = dict(marker = "o", 
                color = "k", 
                markersize = 7
                )

    dat = json.load(open(path_json)) 
    
    out = []
    
    for site, coords in dat.items():
        try:
            positions = coords["position"]
            ox, oy, oz = tuple([float(f) for f in positions])
            lon, lat, alt = convert_coords(ox, oy, oz, 
                                           to_radians = False)
            
            for site in sites.keys():
                clat, clon = tuple(sites[site].values())
                
                if ranged and find_range(lon, lat, clon, clat):
                    out.append(coords["filename"])
                    ax.plot(lon, lat, **args) 
                else:
                    ax.plot(lon, lat, **args)
        except:
            pass
    return out


