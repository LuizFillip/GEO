import pyIGRF
from GEO import load_equator, sites, year_fraction
import numpy as np
from scipy.interpolate import CubicSpline
from intersect import intersection
from scipy.signal import argrelmin
import datetime as dt


def compute_distance(x, y, x0, y0):
    
    def distance(x, y, x0, y0):
        return np.sqrt(pow(x - x0, 2) + 
                       pow(y - y0, 2))
    
    # compute distance
    dis = distance(x, y, x0, y0)
    
    # find the minima
    min_idxs = argrelmin(dis)[0]
    # take the minimum
    glob_min_idx = min_idxs[np.argmin(dis[min_idxs])]
    
    # coordinates and distance
    min_x = x[glob_min_idx]
    min_y = y[glob_min_idx]
    min_d = dis[glob_min_idx]
    
    return min_x, min_y, min_d

def find_closest(arr, val):
   idx = np.abs(arr - val).argmin()
   return idx

def limit_hemisphere(
        x, y, rlat, 
        hemisphere = "south"
        ):
    
    eq = load_equator()
    # Find intersection point between
    # equator and meridian
    nx, ny = intersection(eq[:, 0], eq[:, 1], x, y)
    
    # find meridian indexes (x and y) 
    # where cross the equator and upper limit
    eq_x = find_closest(x, nx)  
    eq_y = find_closest(y, ny)  

    # create a line above of intersection point 
    # with radius from apex latitude 
    if hemisphere == "south":
        end = find_closest(y, ny - rlat)
        set_x = x[eq_x: end + 1]
        set_y = y[eq_y: end + 1]
    
    elif hemisphere == "north":
        start = find_closest(y, ny + rlat)
        set_x = x[start: eq_x + 1]
        set_y = y[start: eq_y + 1]
        
    else:
        end = find_closest(y, ny - rlat) + 1
        start = find_closest(y, ny + rlat)
        set_x = x[start: end]
        set_y = y[start: end]
        
    return set_x, set_y



        
class meridians:
    
    
    def __init__(
            self, 
            date, 
            alt_mag = 300,
            max_lat = 40, 
            delta = 1):
        
        if isinstance(date, (dt.datetime, dt.date)):
            yy = year_fraction(date)
        else:
            yy = date 
        
        self.year = yy
        self.alt_mag = alt_mag
        self.max_lat = max_lat
        self.delta = delta
        
    def compute(self, lon = -60):
        
        xx = []
        yy = []
        
        range_lats = np.arange(
            -self.max_lat, self.max_lat, self.delta)[::-1]
        
        for lat in range_lats:
            d, i, h, x, y, z, f = pyIGRF.igrf_value(
                lat, 
                lon, 
                alt = self.alt_mag, 
                year = self.year
                )
           
            new_point_x = lon - self.delta * np.tan(np.radians(d))
            new_point_y = lat - self.delta
            
            lon = new_point_x
            lat = new_point_y
            
            xx.append(lon)
            yy.append(lat)
                
        return xx, yy
    
    def range_meridians(
            self, 
            lmin = -120, 
            lmax = -30):
        out = []

        for lon in np.arange(lmin, lmax, self.delta):
            
            x, y = self.compute(lon)
                    
            out.append([x, y])
                    
        return np.array(out)
    
    def closest_from_site(
            self, glon, glat, interpol = True
            ):
        
        arr = self.range_meridians()
        
        out = {}
        
        for num in range(arr.shape[0]):
            x, y = arr[num][0], arr[num][1]
            
            min_x, min_y, min_d = compute_distance(
                x, y, glon, glat)
                
            out[num] = min_d
        
        closest = min(out, key = out.get)
        
        x, y = arr[closest][0], arr[closest][1]
        
        if interpol:
            x, y = self.interpolate(x, y)
        
        return x, y 
    
    @staticmethod
    def interpolate(x, y, factor = 3):
             
        spl = CubicSpline(x, y)
        
        new_lon = np.linspace(x[0], x[-1], len(x) * factor)    
        new_lat = spl(new_lon)
        
        return np.round(new_lon, 3), np.round(new_lat, 3)
        
        
        
def main():
    date = dt.datetime(2013, 1, 1, 1, 21)
    
    glat, glon = sites["saa"]["coords"]
    
    from GEO import quick_map
    
    fig, ax = quick_map()
    
    m = meridians(date)
    
    x, y = m.closest_from_site(glon, glat)
    
    ax.plot(x, y)

