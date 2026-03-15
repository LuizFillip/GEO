# # import pyIGRF
# # import numpy as np
# # import GEO as gg
# # import datetime as dt
# # import json
# # from tqdm import tqdm 

# # MERIDIAN_PATH = 'WSL/meridians/'

# # def limit_hemisphere(
# #         x, 
# #         y, 
# #         nx, ny, 
# #         rlat = 0, 
# #         hemisphere = 'both'
# #         ):
    
# #     """
# #     Get range limits in each hemisphere by 
# #     radius (in degrees)
    
# #     """    
# #     # find meridian indexes (x and y) 
# #     # where cross the equator and upper limit
# #     eq_x = gg.find_closest(x, nx)  
# #     eq_y = gg.find_closest(y, ny)  

# #     # create a line above of intersection point 
# #     # with radius from apex latitude 
# #     if hemisphere == "south":
# #         end = gg.find_closest(y, ny - rlat)
# #         set_x = x[eq_x: end + 1]
# #         set_y = y[eq_y: end + 1]
    
# #     elif hemisphere == "north":
# #         start = gg.find_closest(y, ny + rlat)
# #         set_x = x[start: eq_x + 1]
# #         set_y = y[start: eq_y + 1]
        
# #     else:
# #         end = gg.find_closest(y, ny - rlat) #+ 1
# #         start = gg.find_closest(y, ny + rlat)
# #         set_x = x[start: end]
# #         set_y = y[start: end]
        
# #     return set_x, set_y



        
# # class meridians:
    
# #     def __init__(
# #             self, 
# #             dn, 
# #             alt_mag = 300,
# #             max_lat = 40, 
# #             delta = 1
# #             ):
        
# #         if isinstance(dn, (dt.datetime, dt.date)):
# #             date = gg.year_fraction(dn)
# #         else:
# #             date = dn
        
# #         self.year = date
# #         self.alt_mag = alt_mag
# #         self.max_lat = max_lat
# #         self.delta = delta
        
# #     def compute(self, lon = -60):
        
# #         xx = []
# #         yy = []
        
# #         range_lats = np.arange(
# #             -self.max_lat, self.max_lat, self.delta)[::-1]
        
# #         for lat in range_lats:
# #             d, _, _, _, _, _, _ = pyIGRF.igrf_value(
# #                 lat, 
# #                 lon, 
# #                 alt = self.alt_mag, 
# #                 year = self.year
# #                 )
           
# #             new_point_x = (
# #                 lon - self.delta *
# #                 np.tan(np.radians(d))
# #                 )
# #             new_point_y = lat - self.delta
            
# #             lon = new_point_x
# #             lat = new_point_y
            
# #             xx.append(lon)
# #             yy.append(lat)
                
# #         return np.array(xx), np.array(yy)
    
# #     def range_meridians(
# #             self, 
# #             lmin = -120, 
# #             lmax = -30
# #             ):
        
# #         out = []

# #         for lon in tqdm(np.arange(
# #                 lmin, 
# #                 lmax, 
# #                 self.delta
# #                 )):
            
# #             x, y = self.compute(lon)
                    
# #             out.append([x, y])
                    
# #         return np.array(out)
    
# #     def closest_from_site(
# #             self, 
# #             glon, 
# #             glat, 
# #             interpol = True
# #             ):
        
# #         arr = self.range_meridians()
        
# #         out = {}
        
# #         for num in range(arr.shape[0]):
# #             x, y = arr[num][0], arr[num][1]
            
# #             min_x, min_y, min_d = gg.compute_distance(
# #                 x, y, glon, glat)
                
# #             out[num] = min_d
        
# #         closest = min(out, key = out.get)
        
# #         x, y = arr[closest][0], arr[closest][1]
      
# #         return x, y 
    
   
# # def save_meridian(
# #         date, 
# #         glon, 
# #         glat, 
# #         site = 'saa'
# #         ):
    
# #     year = date.year

# #     name = f'{site}_{year}.json'
    
# #     m = meridians(date)

# #     x, y = m.closest_from_site(glon, glat)

# #     nx, ny = gg.intersec_with_equator(x, y, year)
    
# #     dic = {
# #         "mx": x.tolist(), 
# #         "my": y.tolist(), 
# #         "nx": nx, 
# #         "ny": ny
# #         }
    
# #     with open(MERIDIAN_PATH + name, 'w') as fp:
# #         json.dump(dic, fp)
        
# #     return dic


# # def main(year):
# #     date = dt.datetime(year, 1, 1)
# #     glat, glon = gg.sites['saa']['coords']
            
# #     save_meridian(
# #             date, 
# #             glon, 
# #             glat, 
# #             site = 'saa'
# #             )
    
# # main(2024)

from __future__ import annotations

import json
import datetime as dt
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple, Optional

import numpy as np
import pyIGRF
from tqdm import tqdm

import GEO as gg


MERIDIAN_PATH = Path("WSL/meridians")


def limit_hemisphere(
    x: np.ndarray,
    y: np.ndarray,
    nx: float,
    ny: float,
    rlat: float = 0.0,
    hemisphere: str = "both",
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Recorta o meridiano ao redor do equador (ponto nx, ny), limitando por rlat (graus).

    hemisphere:
      - "south": do equador até (ny - rlat)
      - "north": de (ny + rlat) até o equador
      - "both" : de (ny + rlat) até (ny - rlat)
    """
    hemisphere = hemisphere.lower().strip()
    if hemisphere not in {"south", "north", "both"}:
        raise ValueError("hemisphere deve ser 'south', 'north' ou 'both'.")

    # índices onde o meridiano cruza o equador (ou ponto de referência)
    eq_x = gg.find_closest(x, nx)
    eq_y = gg.find_closest(y, ny)

    # índices dos limites
    end = gg.find_closest(y, ny - rlat)
    start = gg.find_closest(y, ny + rlat)

    if hemisphere == "south":
        sl = slice(eq_x, end + 1)
        sl_y = slice(eq_y, end + 1)
    elif hemisphere == "north":
        sl = slice(start, eq_x + 1)
        sl_y = slice(start, eq_y + 1)
    else:
        sl = slice(start, end)
        sl_y = slice(start, end)

    return x[sl], y[sl_y]


@dataclass
class Meridians:
    """
    Gera linhas de meridiano magnético aproximadas integrando a inclinação magnética (declination).
    """
    dn: dt.date | dt.datetime | float
    alt_mag: float = 300.0
    max_lat: float = 40.0
    delta: float = 1.0

    def __post_init__(self):
        # ano fracionário
        if isinstance(self.dn, (dt.datetime, dt.date)):
            self.year = float(gg.year_fraction(self.dn))
        else:
            self.year = float(self.dn)

        if self.delta <= 0:
            raise ValueError("delta deve ser > 0.")
        if self.max_lat <= 0:
            raise ValueError("max_lat deve ser > 0.")

        self._cache_range: Optional[np.ndarray] = None  # cache opcional

    def compute_single(self, lon0: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Computa um meridiano iniciando em lon0, integrando latitude de +max_lat para -max_lat
        (ou vice-versa, conforme seu range_lats).

        Retorna (x, y) arrays.
        """
        # latitudes decrescentes (igual seu [::-1])
        lats = np.arange(-self.max_lat, self.max_lat, self.delta)[::-1]

        x = np.empty_like(lats, dtype=float)
        y = np.empty_like(lats, dtype=float)

        lon = float(lon0)
        lat = float(lats[0])

        for i, lat in enumerate(lats):
            d, *_ = pyIGRF.igrf_value(lat, lon, alt=self.alt_mag, year=self.year)

            # # passo "para baixo" em latitude
            # new_lon = lon - self.delta * np.tan(np.radians(d))
            # new_lat = lat - self.delta
            
            d = np.clip(d, -80, 80)

            # NOVA EQUAÇÃO (estável)
            new_lon = lon - self.delta * np.sin(np.radians(d))
            new_lat = lat - self.delta
            
            x[i] = new_lon
            y[i] = new_lat

            lon = new_lon

        return x, y

    def range_meridians(
        self,
        lmin: float = -120.0,
        lmax: float = -30.0,
        *,
        use_cache: bool = True,
        show_progress: bool = True,
    ) -> np.ndarray:
        """
        Gera um conjunto de meridianos variando lon inicial de lmin..lmax com passo delta.

        Retorna um array shape (N, 2) onde arr[i,0]=x e arr[i,1]=y (cada um é um vetor).
        """
        if use_cache and self._cache_range is not None:
            return self._cache_range

        lons0 = np.arange(lmin, lmax, self.delta)
        iterator = tqdm(lons0, disable=not show_progress)

        out = []
        for lon0 in iterator:
            x, y = self.compute_single(float(lon0))
            out.append([x, y])

        arr = np.array(out, dtype=object)

        if use_cache:
            self._cache_range = arr

        return arr

    def closest_from_site(
        self,
        glon: float,
        glat: float,
        *,
        lmin: float = -120.0,
        lmax: float = -30.0,
        use_cache: bool = True,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Encontra o meridiano (entre lmin..lmax) que passa mais perto do ponto (glon, glat).
        Retorna (x, y) do meridiano escolhido.

        A aceleração aqui é:
          - calcula min distância de cada meridiano e pega argmin
        """
        arr = self.range_meridians(lmin=lmin, lmax=lmax, use_cache=use_cache, show_progress=False)

        # calcula distância mínima por meridiano
        dmins = np.empty(arr.shape[0], dtype=float)

        for i in range(arr.shape[0]):
            x = np.asarray(arr[i][0], dtype=float)
            y = np.asarray(arr[i][1], dtype=float)
            _, _, dmin = gg.compute_distance(x, y, glon, glat)
            dmins[i] = dmin

        idx = int(np.nanargmin(dmins))
        x_best = np.asarray(arr[idx][0], dtype=float)
        y_best = np.asarray(arr[idx][1], dtype=float)

        return x_best, y_best


def save_meridian(
    date: dt.date | dt.datetime,
    glon: float,
    glat: float,
    *,
    site: str = "saa",
    out_dir: Path = MERIDIAN_PATH,
    lmin: float = -120.0,
    lmax: float = -30.0,
) -> Dict:
    """
    Computa e salva em JSON o meridiano mais próximo do site.

    JSON:
      mx, my: listas
      nx, ny: interseção com equador (ou ponto retornado por gg.intersec_with_equator)
    """
    out_dir.mkdir(parents=True, exist_ok=True)

    year = date.year if isinstance(date, (dt.date, dt.datetime)) else int(date)
    name = f"{site}_{year}.json"
    path = out_dir / name

    m = Meridians(date)

    x, y = m.closest_from_site(glon, glat, lmin=lmin, lmax=lmax)
    nx, ny = gg.intersec_with_equator(x, y, int(m.year))

    payload = {
        "mx": x.tolist(),
        "my": y.tolist(),
        "nx": float(nx),
        "ny": float(ny),
        "year": float(m.year),
        "alt_mag": float(m.alt_mag),
        "max_lat": float(m.max_lat),
        "delta": float(m.delta),
        "site": site,
    }

    with path.open("w", encoding="utf-8") as fp:
        json.dump(payload, fp, ensure_ascii=False, indent=2)

    return payload


def main(year: int = 2024, site: str = 'saa'):
    date = dt.datetime(year, 1, 1)
    glat, glon = gg.sites[site]["coords"]
    save_meridian(date, glon, glat, site = site)


# # # if __name__ == "__main__":
# main(2024, site = 'jic')
 