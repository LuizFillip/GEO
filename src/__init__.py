from .core import sites, run_igrf
from .mapping import quick_map, map_attrs, mag_equator
from .meridians import limit_hemisphere, split_meridian, interpolate
from .dip import load_equator
from .conversions import year_fraction

import settings as s

s.config_labels()