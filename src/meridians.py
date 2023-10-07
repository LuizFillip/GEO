import pyIGRF
import numpy as np
import GEO as gg
import datetime as dt
import json

MERIDIAN_PATH = 'WSL/meridians/'

def limit_hemisphere(
        x, 
        y, 
        nx, ny, 
        rlat = 0, 
        hemisphere = 'both'
        ):
    
    """
    Get range limits in each hemisphere by 
    radius (in degrees)
    
    """    
    # find meridian indexes (x and y) 
    # where cross the equator and upper limit
    eq_x = gg.find_closest(x, nx)  
    eq_y = gg.find_closest(y, ny)  

    # create a line above of intersection point 
    # with radius from apex latitude 
    if hemisphere == "south":
        end = gg.find_closest(y, ny - rlat)
        set_x = x[eq_x: end + 1]
        set_y = y[eq_y: end + 1]
    
    elif hemisphere == "north":
        start = gg.find_closest(y, ny + rlat)
        set_x = x[start: eq_x + 1]
        set_y = y[start: eq_y + 1]
        
    else:
        end = gg.find_closest(y, ny - rlat) + 1
        start = gg.find_closest(y, ny + rlat)
        set_x = x[start: end]
        set_y = y[start: end]
        
    return set_x, set_y



        
class meridians:
    
    def __init__(
            self, 
            dn, 
            alt_mag = 300,
            max_lat = 40, 
            delta = 1
            ):
        
        if isinstance(
                dn, 
                (dt.datetime, dt.date)):
            date = gg.year_fraction(dn)
        else:
            date = dn
        
        self.year = date
        self.alt_mag = alt_mag
        self.max_lat = max_lat
        self.delta = delta
        
    def compute(self, lon = -60):
        
        xx = []
        yy = []
        
        range_lats = np.arange(
            -self.max_lat, self.max_lat, self.delta)[::-1]
        
        for lat in range_lats:
            d, _, _, _, _, _, _ = pyIGRF.igrf_value(
                lat, 
                lon, 
                alt = self.alt_mag, 
                year = self.year
                )
           
            new_point_x = (
                lon - self.delta *
                np.tan(np.radians(d))
                )
            new_point_y = lat - self.delta
            
            lon = new_point_x
            lat = new_point_y
            
            xx.append(lon)
            yy.append(lat)
                
        return np.array(xx), np.array(yy)
    
    def range_meridians(
            self, 
            lmin = -120, 
            lmax = -30
            ):
        
        out = []

        for lon in np.arange(
                lmin, 
                lmax, 
                self.delta
                ):
            
            x, y = self.compute(lon)
                    
            out.append([x, y])
                    
        return np.array(out)
    
    def closest_from_site(
            self, 
            glon, 
            glat, 
            interpol = True
            ):
        
        arr = self.range_meridians()
        
        out = {}
        
        for num in range(arr.shape[0]):
            x, y = arr[num][0], arr[num][1]
            
            min_x, min_y, min_d = gg.compute_distance(
                x, y, glon, glat)
                
            out[num] = min_d
        
        closest = min(out, key = out.get)
        
        x, y = arr[closest][0], arr[closest][1]
      
        return x, y 
    
   
def save_meridian(
        date, 
        glon, 
        glat, 
        site = 'saa'
        ):
    
    year = date.year

    name = f'{site}_{year}.json'
    
    m = meridians(date)

    x, y = m.closest_from_site(glon, glat)

    nx, ny = gg.intersec_with_equator(x, y, year)
    
    dic = {
        "mx": x.tolist(), 
        "my": y.tolist(), 
        "nx": nx, 
        "ny": ny
        }
    
    with open(
            MERIDIAN_PATH + name, 'w'
            ) as fp:
        json.dump(dic, fp)
        
    return dic

        
def split_meridian(
        rlat,
        site = 'jic',
        year = 2013,
        hemisphere = 'both',
        points = None
        ):
    
    name = f'{site}_{year}.json'
    nx, ny, x, y = gg.load_meridian(
        MERIDIAN_PATH + name
        )
    
    lon, lat = limit_hemisphere(
            x, y, nx, ny, 
            np.degrees(rlat), 
            hemisphere = hemisphere
            )
    
    if points is not None:
        lon, lat =  gg.interpolate(
            lon, lat, points = points
            )

    return lon, lat


