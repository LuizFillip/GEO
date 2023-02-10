import pyIGRF


coords = {"car": (-7.38, -36.528), 
          "for": (-3.73, -38.522), 
          "saa": (-2.53, -44.296)}

def run_igrf(
        frac_year, 
        site = "car", 
        alt = 250, 
        ):

    lat, lon = coords[site]
    
    lon += 360
    
    d, i, h, x, y, z, f = pyIGRF.igrf_value(lat, lon, 
                                            alt = alt, 
                                            year = frac_year)
    return d, i 

