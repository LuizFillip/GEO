# from scipy.signal import argrelmin
# import numpy as np
# import json  
# import GEO as gg
# from scipy.interpolate import CubicSpline
# import os 


# MERIDIAN_PATH = 'WSL/meridians/'

# def load_meridian(year, site = 'saa'):
        
#     infile = os.path.join(
#         MERIDIAN_PATH, 
#         f'{site}_{year}.json'
#         )
#     dat = json.load(open(infile))

#     x = np.array(dat["mx"])
#     y = np.array(dat["my"])

#     nx = dat["nx"]
#     ny = dat["ny"]
#     return nx, ny, x, y


# def split_meridian(
#         rlat,
#         year,
#         points = None,
#         site = 'saa'
#         ):
        
#     nx, ny, x, y = load_meridian(year, site)
    
#     lon, lat = gg.limit_hemisphere(
#             x, 
#             y, 
#             nx, 
#             ny, 
#             np.degrees(rlat), 
#             hemisphere = 'both'
#             )
    
#     lon = sorted(lon)
#     lon, lat = interpolate(
#         lon, lat, points = points
#         )

#     return lon, lat

# def compute_distance(x, y, x0, y0):
    
#     dis = np.sqrt(pow(x - x0, 2) + 
#                   pow(y - y0, 2))
    
#     min_idxs = argrelmin(dis)[0]
#     min_idx = min_idxs[np.argmin(dis[min_idxs])]
    
#     min_x = x[min_idx]
#     min_y = y[min_idx]
#     min_d = dis[min_idx]
    
#     return min_x, min_y, min_d

# def find_closest(arr, val):
#     return np.abs(arr - val).argmin()

# def intersec_with_equator(x, y, year = 2013):
#      """
#      Find intersection point between equator 
#      and meridian line 
#      """
#      e_x, e_y = gg.load_equator(year, values = True)
     
#      nx, ny = gg.intersection(
#          e_x, e_y, x, y
#          )
#      return nx.item(), ny.item()

# def interpolate(x, y, points = 30):
    
#     """
#     Interpolate the same number of points for different
#     ranges of meridians
#     """
         
    
#     spl = CubicSpline(x, y)
    
#     new_lon = np.linspace(x[0], x[-1], points)    
#     new_lat = spl(new_lon)
    
#     return np.round(new_lon, 3), np.round(new_lat, 3)


from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple, Optional

import numpy as np
from scipy.interpolate import CubicSpline

import GEO as gg


MERIDIAN_PATH = Path("WSL/meridians")


def load_meridian(year: int, site: str = "saa", base_dir: Path = MERIDIAN_PATH) -> Tuple[float, float, np.ndarray, np.ndarray]:
    """
    Carrega meridiano salvo em JSON e retorna:
      nx, ny, x(mx), y(my)
    """
    infile = base_dir / f"{site}_{year}.json"
    if not infile.exists():
        raise IOError(f"Arquivo não encontrado: {infile}")

    with infile.open("r", encoding="utf-8") as f:
        dat = json.load(f)

    x = np.asarray(dat["mx"], dtype=float)
    y = np.asarray(dat["my"], dtype=float)
    nx = float(dat["nx"])
    ny = float(dat["ny"])
    return nx, ny, x, y


 
def sort_xy(x, y):
    """Ordena x e reordena y junto (não usar sorted(x)!)."""
    x = np.asarray(x)
    y = np.asarray(y)
    idx = np.argsort(x)
    return x[idx], y[idx]

def split_meridian(
    rlat_rad: float,
    year: int,
    points: Optional[int] = 30,
    site: str = "saa",
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Recorta o meridiano em torno do equador em um raio rlat (em radianos),
    e interpola para um número fixo de pontos.

    Retorna: (lon, lat)
    """
    nx, ny, x, y = load_meridian(year, site)

    lon, lat = gg.limit_hemisphere(
        x, y, nx, ny,
        np.degrees(rlat_rad),
        hemisphere="both",
    )

    lon, lat = sort_xy(lon, lat)

    if points is None:
        return np.round(lon, 3), np.round(lat, 3)

    lon_i, lat_i = interpolate(lon, lat, points=points)
    return lon_i, lat_i


def compute_distance(x: np.ndarray, y: np.ndarray, x0: float, y0: float) -> Tuple[float, float, float]:
    """
    Retorna o ponto do meridiano mais próximo do ponto (x0, y0),
    usando distância euclidiana em graus (rápido e robusto).

    (Se você quiser distância geodésica real, aí seria outro método.)
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    dis = np.hypot(x - x0, y - y0)
    idx = int(np.nanargmin(dis))

    return float(x[idx]), float(y[idx]), float(dis[idx])


def find_closest(arr: np.ndarray, val: float) -> int:
    arr = np.asarray(arr, dtype=float)
    return int(np.nanargmin(np.abs(arr - val)))


def intersec_with_equator(x: np.ndarray, y: np.ndarray, year: int = 2013) -> Tuple[float, float]:
    """
    Encontra o ponto de interseção entre o equador magnético (ou geográfico, dependendo do gg.load_equator)
    e a linha (x,y).
    """
    e_x, e_y = gg.load_equator(year, values=True)
    nx, ny = gg.intersection(e_x, e_y, x, y)
    return float(np.asarray(nx).item()), float(np.asarray(ny).item())


def interpolate(x: np.ndarray, y: np.ndarray, points: int = 30) -> Tuple[np.ndarray, np.ndarray]:
    """
    Interpola (x,y) para um número fixo de pontos usando CubicSpline.

    Importante:
      - CubicSpline exige x estritamente crescente.
      - Se houver duplicatas em x, removemos.
    """
    if points is None or points <= 1:
        return np.round(np.asarray(x, dtype=float), 3), np.round(np.asarray(y, dtype=float), 3)

    x, y = sort_xy(x, y)

    # remove duplicatas em x (CubicSpline não aceita x repetido)
    ux, idx = np.unique(x, return_index=True)
    uy = y[idx]

    if ux.size < 2:
        raise ValueError("Poucos pontos únicos para interpolar (x precisa ter pelo menos 2 valores distintos).")

    spl = CubicSpline(ux, uy, bc_type="natural")

    new_x = np.linspace(ux[0], ux[-1], int(points))
    new_y = spl(new_x)

    return np.round(new_x, 3), np.round(new_y, 3)

# -------------------------
# Helpers
# -------------------------
def limit_hemisphere(x, y, nx, ny, rlat=0.0, hemisphere="both"):
    """
    Recorta (x,y) em torno do ponto (nx, ny) (ex.: intersecção com equador),
    limitando por um raio em latitude (rlat, em graus).

    hemisphere:
      - 'north': retorna do (ny+rlat) até (ny)
      - 'south': retorna do (ny) até (ny-rlat)
      - 'both' : retorna do (ny+rlat) até (ny-rlat)
    """
    hemisphere = hemisphere.lower().strip()
    if hemisphere not in {"north", "south", "both"}:
        raise ValueError("hemisphere deve ser 'north', 'south' ou 'both'.")

    x = np.asarray(x)
    y = np.asarray(y)

    # índices próximos do ponto de referência
    ix0 = gg.find_closest(x, nx)
    iy0 = gg.find_closest(y, ny)

    # índices dos limites por latitude
    i_end = gg.find_closest(y, ny - rlat)     # mais ao sul
    i_start = gg.find_closest(y, ny + rlat)   # mais ao norte

    # garanta ordem de slice (independente se y cresce/decresce)
    lo = min(i_start, i_end)
    hi = max(i_start, i_end)

    if hemisphere == "north":
        a, b_ = sorted([i_start, iy0])
        sl = slice(a, b_ + 1)
        return x[sl], y[sl]

    if hemisphere == "south":
        a, b_ = sorted([iy0, i_end])
        sl = slice(a, b_ + 1)
        return x[sl], y[sl]

    # both
    sl = slice(lo, hi + 1)
    return x[sl], y[sl]



def interpolate_path(x, y, points=50):
    """
    Interpolação paramétrica (x(t), y(t)) usando comprimento de arco.
    Não exige x monotônico. Ideal para curvas verticais/complexas.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    # remove NaNs
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]

    if x.size < 2:
        return x, y

    # parâmetro t: distância acumulada ao longo do caminho
    ds = np.hypot(np.diff(x), np.diff(y))
    t = np.concatenate([[0.0], np.cumsum(ds)])

    # remove pontos repetidos (t repetido quebra spline)
    keep = np.concatenate([[True], np.diff(t) > 0])
    x, y, t = x[keep], y[keep], t[keep]

    if t.size < 2:
        return x, y

    # nova malha em t
    t_new = np.linspace(t[0], t[-1], int(points))

    sx = CubicSpline(t, x, bc_type="natural")
    sy = CubicSpline(t, y, bc_type="natural")

    return sx(t_new), sy(t_new)