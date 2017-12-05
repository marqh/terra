# Manage Cartopy namespace to enable terra to be used
# without cartopy being available.

try:
    import cartopy
    is_true_cartopy = True
except ImportError:
    is_true_cartopy = False

if is_true_cartopy:
    Globe = cartopy.crs.Globe
    Geodetic = cartopy.crs.Geodetic
    CRS = cartopy.crs.CRS
else:
    Globe = object
    Geodetic = object
    CRS = None
