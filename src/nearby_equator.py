import json
import GEO as g



def distance_from_equator(lon, lat, year = 2013):
    x, y = g.load_equator(year, values = True)

    min_x, min_y, min_d = g.compute_distance(
        x, y, lon, lat)
    return min_d


def stations_near_of_equator(
        ax = None,
        year = 2015,
        distance = 6, 
        extra_sts = ['ceeu', 'ceft',
                     'rnna', 'pbjp']
        ):
    
    infile = f'database/GEO/coords/{year}.json'
    sites = json.load(open(infile))
    
    out = []
    
    for name, key in sites.items():
        lon, lat, alt = tuple(key)
        
        min_d = distance_from_equator(
                lon, 
                lat, 
                year = year
                )
        
        if min_d < distance:
          
            out.append(name)
            if ax is not None:
                ax.scatter(lon, lat, marker = '^', 
                           s = 100, c = 'k')
            
    return out + extra_sts


