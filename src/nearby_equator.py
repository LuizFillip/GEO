import json
import GEO as g



def distance_from_equator(
        lon, lat, year = 2013
        ):
    eq = g.load_equator(year)
    x, y = eq[:, 0], eq[:, 1]
    min_x, min_y, min_d = g.compute_distance(
        x, y, lon, lat)
    return min_d


def stations_near_of_equator(
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
            
    return out + extra_sts


