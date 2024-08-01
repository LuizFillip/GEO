import os 
import json 
import numpy as np 

sites = {
 'cp': {'name': 'Cachoeira Paulista', 'coords': (-22.703, -45.00)},
 'ca': {'name': 'São João do Cariri', 'coords': (-7.38, -36.528)},
 'fza': {'name': 'Fortaleza', 'coords': (-3.73, -38.522)},
 'caz': {'name': 'Cajazeiras', 'coords': (-6.89, -38.56)},
 'saa': {'name': 'São Luis', 'coords': (-2.53, -44.296)},
 'bvj': {'name': 'Boa Vista', 'coords': (2.8, -60.7)},
 'ccb': {'name': 'Cachimbo', 'coords': (-9.5, -54.8)},
 'cgg': {'name': 'Campo Grande', 'coords': (-20.5, -54.7)},
 'jic': {'name': 'Jicamarca', 'coords': (-11.95, -76.87)},
 'rga': {'name': 'Rio Grande', 'coords': (-53.78, -67.7)},
 'sms': {'name': 'São Martinho da Serra', 'coords': (-29.53, -53.85)},
 'str': {'name': 'Santarem', 'coords': (-2.43, -54.7)},
 'tcm': {'name': 'Tucumán', 'coords': (-26.56, -64.88)},
 'sjc': {'name': 'São José Dos Campos', 'coords': (-23.19, -45.89)},
 'vss': {'name': 'Vassouras', 'coords': (-22.41, -43.66)},
 'jat': {'name': 'Jataí', 'coords': (-17.88, -51.72)},
 'cba': {'name': 'Cuiabá', 'coords': (-15.6, -56.1)},
 'ara': {'name': 'Araguatins', 'coords': (-5.65, -48.12)},
 'eus': {'name': 'Eusébio', 'coords': (-3.89, -38.45)},
 'slz': {'name': 'São Luis', 'coords': (-2.53, -44.3)},
 'pil': {'name': 'Pilar', 'coords': (-31.7, -63.89)},
 'ttb': {'name': 'Tatuoca', 'coords': (-1.205, -48.51)}, 
 'bjl': {'name': 'Bom Jesus da Lapa', 'coords': (-13.250, -43.540)}
 }

PATH_COORDS = 'database/GEO/coords/'

def load_coords(year = 2021):
    infile = os.path.join(
        PATH_COORDS, 
        f'{year}.json'
        )
    return json.load(open(infile))


def arr_coords(year = 2021):
    
    sites = load_coords(year)
    
    arr = np.array(
        list(sites.values())
        )
    
    lon = arr[:, 0]
    lat = arr[:, 1]
    sits = list(sites.keys())
    return sits, lon, lat

# sites