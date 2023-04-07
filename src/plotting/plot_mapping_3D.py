from matplotlib.collections import LineCollection
from cartopy.mpl.patch import geos_to_path
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import itertools
import matplotlib.pyplot as plt
import numpy as np
import settings as s
from GEO.src.mapping import mag_equator
from GEO.src.plotting.plot_mag_meridians import plot_meridians
from FluxTube.src.mag import Apex, u
from GEO.src.core import run_igrf, coords

def mapping_3D():
    fig = plt.figure(
        figsize = (12, 10),
        dpi = 300, 
        )
    
    ax = fig.add_subplot(111, projection='3d')
    
    
    ax.xaxis.set_pane_color((1.0, 0.0, 1.0, .0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, .0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    
    ax.grid(False)
    
    tmp_planes = ax.zaxis._PLANES 
    ax.zaxis._PLANES = ( tmp_planes[2], tmp_planes[3], 
                     tmp_planes[0], tmp_planes[1], 
                     tmp_planes[4], tmp_planes[5])
    
    ax.set(xlim = [-180, 180], 
           ylim = [-90, 90],
           zlim = [0, 500]
           )
   
    ax.view_init(azim = -20, elev = 40)
    
    target_projection = ccrs.PlateCarree()
    
    feature = cfeature.NaturalEarthFeature(
        'physical', 'coastline', '110m')
    
    
    geoms = [target_projection.project_geometry(
        geom, feature.crs) for geom in feature.geometries()]
    
    paths = list(itertools.chain.from_iterable(
        geos_to_path(geom) for geom in geoms))
    
    segments = []
    
    for path in paths:
        vertices = [vertex for vertex, _ in 
                    path.iter_segments()]
        vertices = np.asarray(vertices)
          
        segments.append(vertices)
    

    lc = LineCollection(segments, lw = 0.5, color='black')
    
    s.config_labels()
    ax.add_collection3d(lc)
    
    return fig, ax


fig, ax = mapping_3D()

mag_equator(ax)

    
def plot_apex_heights(
        ax, 
        hmin = 200, 
        hmax = 500, 
        points = 200, 
        dz = 100, 
        base = 150
        ):
    
    heights = np.arange(hmin, hmax + dz, dz) * u.km 
    
    d, i = run_igrf(
            date = 2013, 
            site = "saa", 
            alt = 300, 
            )
    
    lat, lon = coords["saa"]
    
    print(lon, lat)
    
    
    for h in heights:
        apx = Apex(h)
        lats =  apx.latitude_range(
            points = points, 
            base = base
            )
        apex = apx.apex_range(
            points = points, 
            base = base
            )
        
        x = np.zeros(len(lats)) - lon - 3
        
        mag_lats = lats.to(u.deg).value
        
        
        ax.plot(x, 
                mag_lats - 15, 
                apex.value, color = "k") 
      

line = np.arange(-180, 180, 1)

ax.plot(line, 
        np.zeros(len(line)),
        np.zeros(len(line))
        )

plot_apex_heights(
        ax, 
        hmin = 200, 
        hmax = 500, 
        points = 200, 
        dz = 100, 
        base = 150
        )

plot_meridians(ax)


#ax.plot(lon, lat, "o", label = "São Luis")

# ax.legend(bbox_to_anchor=[0.8, 0.6], 
#           loc = "center")


ax.set(ylabel = "Latitude (°)", 
       xlabel = "Longitude (°)", 
       zlabel = "Altura de apex (km)")




plt.show()
    