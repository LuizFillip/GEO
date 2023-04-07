from GEO.src.mapping import quick_map
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from FluxTube.src.mag import Apex, u
from GEO.src.core import run_igrf, coords
import numpy as np

fig, ax = plt.subplots(
    figsize = (10, 10), 
    subplot_kw = {'projection': ccrs.PlateCarree()},
    dpi = 300
    )


lat_lims = dict(min = -45, 
                max = 45, 
                stp = 15)

lon_lims = dict(min = -100, 
                max = 0, 
                stp = 15)    

ax, df = quick_map(ax, lon_lims, lat_lims)



d, i = run_igrf(
        date = 2013, 
        site = "saa", 
        alt = 300, 
        )

lat, lon = coords["saa"]
lat, lon = -15, -60

apex  = 500 * u.km 
points = 200 
base = 150


max_lat = Apex(apex).apex_lat_base(base = base)

lats = np.linspace(-max_lat, max_lat, points).to("deg")

res = df.iloc[(df['lon'] - lon
               ).abs().argsort()[:1]]["lat"].item()

x = np.zeros(len(lats)) + lon

print(max_lat.to("deg"))

ax.plot(x, lats.value + res, color = "k", lw = 4, label = apex) 

ax.plot(lon, lat, "o", label = "São Luis")

ax.legend(loc = "lower left")
ax.grid(False)

