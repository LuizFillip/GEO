from .core import sites
from .mapping import quick_map, map_attrs, mag_equator
from .meridians import (
    limit_hemisphere, 
    split_meridian, 
    interpolate, 
    load_meridian)
from .dip import load_equator
from .conversions import year_fraction
from .dawn_dusk import dawn_dusk
import settings as s

s.config_labels()