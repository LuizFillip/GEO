import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import pyIGRF

out_dir = "database/GEO/dips"

def run_igrf(year, step_lon=5.0, step_lat=1.0, alt=250.0, cols=("lat", "lon", "d", "i")):
    """
    Calcula declinação (d) e inclinação/dip (i) em uma grade lat/lon.
    Retorna DataFrame com colunas [lat, lon, d, i].
    """
    lons = np.arange(-180.0, 180.0 + step_lon, step_lon, dtype=float)
    lats = np.arange(-90.0, 90.0 + step_lat, step_lat, dtype=float)

    n = len(lats) * len(lons)
    out = np.empty((n, 4), dtype=float)

    k = 0
    for lat in tqdm(lats, desc=f"Computing IGRF (dip/decl): {year}"):
        for lon in lons:
            d, i, *_ = pyIGRF.igrf_value(lat, lon, alt=alt, year=year)
            out[k, :] = (lat, lon, d, i)
            k += 1

    return pd.DataFrame(out, columns=list(cols))


def _largest_contour_segment(contour_set) -> np.ndarray:
    """
    Retorna os vértices do maior segmento (maior número de pontos)
    do contorno gerado pelo matplotlib.
    """
    # contour_set.allsegs é uma lista por nível; como usamos 1 nível, pega [0]
    segs = contour_set.allsegs[0]
    if not segs:
        return np.empty((0, 2), dtype=float)
    # escolhe o segmento com mais vértices
    return max(segs, key=lambda a: a.shape[0])


def get_dip_equator(year=2013, step_lon=0.5, step_lat=0.5, alt=300.0):
    """
    Calcula a linha dip=0° (equador magnético) numericamente,
    detectando mudança de sinal da inclinação para cada longitude.
    """

    df = run_igrf(year, step_lon=step_lon, step_lat=step_lat, alt=alt)

    # grade organizada
    pivot = df.pivot(index="lat", columns="lon", values="i").sort_index()

    lats = pivot.index.to_numpy()
    lons = pivot.columns.to_numpy()

    eq_lon = []
    eq_lat = []

    for lon in lons:
        dip = pivot[lon].to_numpy()

        # detectar mudança de sinal
        sign_change = np.where(np.diff(np.sign(dip)) != 0)[0]

        if len(sign_change) == 0:
            continue

        idx = sign_change[0]  # pega o primeiro cruzamento

        # interpolação linear
        lat1, lat2 = lats[idx], lats[idx + 1]
        dip1, dip2 = dip[idx], dip[idx + 1]

        if dip2 != dip1:
            lat_zero = lat1 - dip1 * (lat2 - lat1) / (dip2 - dip1)
        else:
            lat_zero = lat1

        eq_lon.append(lon)
        eq_lat.append(lat_zero)

    return pd.DataFrame({"lon": eq_lon, "lat": eq_lat})


def save_df(
        year=2023, 
        step_lon=0.5, 
        step_lat=0.5, alt=300.0):
    """
    Salva a linha dip=0 (equador magnético) em CSV.
    """
    os.makedirs(out_dir, exist_ok=True)

    df = get_dip_equator(year, step_lon=step_lon, step_lat=step_lat, alt=alt)

    fn = os.path.join(out_dir, f"dip_{year}.txt")
    df.to_csv(fn, sep=",", index=False, header=True)

    return fn



import numpy as np
from scipy.interpolate import UnivariateSpline


def interpolate_lon_lat(
    df,
    step=0.1,
    method="linear",
    spline_order=3,
    smoothing=0
):
    """
    Interpola curva lon → lat para nova resolução.

    Parameters
    ----------
    df : DataFrame
        Pode estar:
        - com índice = lon e coluna 'lat'
        - ou colunas ['lon','lat']
    step : float
        Novo passo em longitude.
    method : str
        'linear' ou 'spline'
    spline_order : int
        Ordem da spline (se method='spline')
    smoothing : float
        Fator de suavização da spline

    Returns
    -------
    DataFrame com colunas ['lon','lat']
    """

    # Detecta formato
    if "lon" in df.columns:
        lon = df["lon"].values
        lat = df["lat"].values
    else:
        lon = df.index.values
        lat = df.iloc[:, 0].values

    # Ordena
    order = np.argsort(lon)
    lon = lon[order]
    lat = lat[order]

    # Remove duplicatas
    lon_unique, idx = np.unique(lon, return_index=True)
    lat_unique = lat[idx]

    # Novo grid
    new_lon = np.arange(lon_unique.min(), lon_unique.max() + step, step)

    # Interpolação
    if method == "linear":
        new_lat = np.interp(new_lon, lon_unique, lat_unique)

    elif method == "spline":
        spline = UnivariateSpline(
            lon_unique,
            lat_unique,
            k=spline_order,
            s=smoothing
        )
        new_lat = spline(new_lon)

    else:
        raise ValueError("method deve ser 'linear' ou 'spline'")

    return pd.DataFrame({"lon": new_lon, "lat": new_lat})

def load_equator(year = 2013, values = False):
    infile = os.getcwd() + f'/{out_dir}/dip_{year}.txt'
    
    df = pd.read_csv(infile, index_col = 0)

    if values:
        return df['lon'].values, df['lat'].values 
    else:
        return df

def interpolated():
    for year in range(2010, 2026):
        
        infile = os.getcwd() + f'/{out_dir}/dip_{year}.txt'
        
        df = load_equator(year = 2013, values = False)
        
        df_interp = interpolate_lon_lat(df, step=0.1)
        
        df_interp.to_csv(infile)
    

