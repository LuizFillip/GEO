import numpy as np

re = 6371.2          # Reference radius of IGRF
eps = 1e-5             # Small number
fltnvrs = 298.257223563  # Inverse flatness of geoid

# Given desired range of geographic latitude, longitude and altitude, 
# choose an appropriate grid that can be used in subsequent calls to 
# subs apex_mka, apex_mall, apex_q2g.
glatmin = -90
glatmax = 90

glonmin = -180
glonmax = 180

altmin = 0
altmax = 400

nvert = 40 # Resolution parameter, corresponding
#  to the maximum number of vertical grid increments when altmax=infinity.
#   Points are spaced uniformly in 1/r between the Earth's surface and an
#   altitude that is at least altmax (or a very large value if altmax=infinity).  

mxlat = 3 * nvert + 1 # number of latitude grid points
mxlon = 5 * nvert + 1 # number of longitude grid points
mxalt = nvert + 1 # maximum number of height grid points

gplat = np.zeros(mxlat)
gplon = np.zeros(mxlon)
gpalt = np.zeros(mxalt)

if glatmin > glatmax:
    print(f"gggrid: glatmin = {glatmin} must be glatmax = {glatmax}")
    
if glonmin > glonmax:
    print(f"gggrid: glonmin = {glonmin} must be glonmax = {glonmax}")
    
if altmin > altmax:
    print(f"gggrid: altmin = {altmin} must be altmax = {altmax}")
    

dnv = float(nvert)

dlon = 360. / (5. * dnv)
dlat = 180. / (3. * dnv)
diht = 1.   / dnv

nlatmin = max(int((glatmin + 90.) / dlat), 0)
nlatmax = min(int((glatmax + 90.) / dlat + 1.), 3 * nvert)

print(nlatmax, nlatmin, )
nlat = nlatmax - nlatmin + 1

for j in range(1, nlat):
  gplat[j] = dlat * float(nlatmin + j - 1) - 90.

gplat[nlat - 1] = min(gplat[nlat - 1], 90.)
 
print(gplat)   

#%%

nlonmin = max(int((glonmin + 180.)/ dlon), 0)

 
glonmaxx = min(glonmax, glonmin + 360.)
nlonmax = min(int((glonmaxx + 180.) 
                  / dlon + 1.), 10 * nvert)
  
x = re / (re + altmax) / diht-eps
naltmin = max(x, 1.)
naltmin = min(naltmin, nvert - 1)
x = re / (re + altmin) / diht + eps
i = x + 1.
naltmax = min(i, nvert)
nlon = nlonmax - nlonmin + 1
nlon = min(nlon, 5 * nvert + 1)


for j in range(1, nlat):
  gplat[j] = dlat * float(nlatmin + j - 1) - 90.

gplat[nlat] = min(gplat(nlat), 90.)

for i in range(1, nlon):
  gplon[i] = dlon * float(nlonmin + i - 1) - 180.

nalt = naltmax - naltmin + 1
for k in range(1, nalt):
  kk = naltmax - k +1
  gpalt[k] = (re*(float(nvert - kk) - eps) / 
              (float(kk) + eps))

if (gplon(nlon - 1) >= glonmax): nlon = nlon-1

gpalt[1] = max(gpalt(1), 0.)