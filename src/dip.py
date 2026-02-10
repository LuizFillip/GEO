import pyIGRF
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm 





def run_igrf(
        year, 
        step_lon = 5, 
        step_lat = 1, 
        alt = 250,
        cols = ["lat", "lon", "d", "i"]
        ):
    
    longitudes = np.arange(
        -180, 180 + step_lon, step_lon
        )
    latitudes = np.arange(
        -90, 90 + step_lat, step_lat
        )
    
    out = []
    for lat in latitudes:
        for lon in tqdm(longitudes, str(lat)):
            
            d, i, _, _, _, _, _ = pyIGRF.igrf_value(
                lat, lon, 
                alt = alt, 
                year = year
                )
            
            out.append([lat, lon, d, i])
            
    return pd.DataFrame(out, columns = cols)
 

 

def get_dip(
        date = 2013, 
            step_lon = 0.1, 
            step_lat = 0.1, 
            alt = 300
            ):   
    
    print('[compute_dip]', date)
     
    df = run_igrf(
        date, 
        step_lon = step_lon, 
        step_lat = step_lat, 
        alt = alt
        )
    
    pivot = pd.pivot_table(
        df, 
        columns = "lon", 
        index = "lat", 
        values = "i"
        )
    cs = plt.contour(
        pivot.columns, 
        pivot.index, 
        pivot.values, 
        levels = 0)
    
    p = cs.collections[1].get_paths()[0]
    v = p.vertices
    return pd.DataFrame({"lon": v[:,0], "lat": v[:,1]})


def save_df(year = 2023):
    
    df = get_dip(
        year, 
        step_lon = 0.1, 
        step_lat = 0.1, 
        alt = 300
        )
    
    name_to_save = f"database/GEO/dips/dip_{year}.txt"
    
    df.to_csv(
        name_to_save,
        sep = ",",
        index = True, 
        header = True
        )       
    

def dip_angle_xyz(X, Y, Z, degrees=True):
    """
    Calcula o ângulo de dip magnético a partir dos componentes do campo.
    
    Parâmetros
    ----------
    X : float ou array
        Componente norte (nT)
    Y : float ou array
        Componente leste (nT)
    Z : float ou array
        Componente vertical (nT, positivo para baixo)
    degrees : bool
        Retorna em graus (True) ou radianos (False)
    
    Retorno
    -------
    I : float ou array
        Ângulo de dip magnético
    """
    H = np.sqrt(X**2 + Y**2)
    I = np.arctan2(Z, H)  # mais robusto que arctan(Z/H)

    if degrees:
        I = np.degrees(I)

    return I

    
# save_df(year = 2002)
d, i, h, x, y, z, f = pyIGRF.igrf_value(
    -2.33, -44.2, 
    alt = 350, 
    year = 2023
    
    )


# dip_angle_xyz(x, y, z, degrees=True)

i