from .sites_infos import *
from .conversions import year_fraction

import os
os.environ['PROJ_LIB'] = 'C:\\Users\\Luiz\\anaconda3\\\anaconda3\\envs\\sai\\Library\\share\\proj'
os.environ['GDAL_DATA'] = 'C:\\Users\\Luiz\\anaconda3\\envs\sai\\Library\\share'

# import gdal


from .map_sectors import * 
from .mapping import (
    limits,
    quick_map, 
    map_attrs, 
    mag_equator, 
    map_features,
    map_boundaries
    )
from .meridians import (
    limit_hemisphere, 
    meridians
    )
from .meridian_utils import (
    interpolate, 
    compute_distance,
    intersec_with_equator,
    load_meridian, 
    find_closest,
    split_meridian
    )
from .dip_calculus import *
from .mapping_attrs import *
from .intersect import intersection
from .timezones import local_midnight
from .terminator import terminator2
from .terminator_time import *
from .haversine_distance import haversine_distance, distance_circle
