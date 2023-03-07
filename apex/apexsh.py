import numpy as np

Re = 6371.2
rtod = 5.72957795130823E1
Req = 6378.160
dtor = 1.745329251994330e-2
def fint(x1, x2, x3, y1, y2, y3, xfit):

    # ! Second degree interpolation used by FNDAPX
    # ! INPUTS:
    # ! x1   = point 1 ordinate value
    # ! x2   = point 2 ordinate value
    # ! x3   = point 3 ordinate value
    # ! y1   = point 1 abscissa value
    # ! y2   = point 2 abscissa value
    # ! y3   = point 3 abscissa value
    # ! xfit = ordinate value to fit
    # ! RETURNS:
    # ! yfit = abscissa value corresponding to xfit
    # !
    # ! MODIFICATIONS:
    # ! Apr 2004: Change from subroutine to function, rename variables and
    # ! add intermediates which are otherwise calculated twice


    #real(8), intent(in)  :: x1, x2, x3, y1, y2, y3, xfit
   # real(8)              :: x12, x13, x23, xf1, xf2, xf3

    x12 = x1 - x2
    x13 = x1 - x3
    x23 = x2 - x3
    xf1 = xfit - x1
    xf2 = xfit - x2
    xf3 = xfit - x3

    fint = (y1 * x23 * xf2 * xf3 - y2 * x13 * 
            xf1 * xf3 + y3 * x12 * xf1 * xf2) / (x12 * x13 * x23)
    return fint

def fndapx(y, yapx, alt, zmag, a, alat, alon):
    
    """
    Find apex coordinates once tracing (in subroutine ITRACE) has
    signalled that the apex has been passed.

    INPUTS:
    alt  = Altitude of starting point
    zmag = Downward component of geomagnetic field at starting point

    OUTPUT

    a    = Apex radius, defined as (Apex height + Req)/Req, where
    Req = equatorial Earth radius.
    A is analogous to the L value in invariant coordinates.
    alat = Apex Lat. (deg)
    alon = Apex Lon. (deg)

    IMPORTS:
    apxin
    dipole

    apxin has step locations determined in itrace:
    yapx  = Matrix of cartesian coordinates (loaded columnwise) of the
    three points about the apex.  Set in subroutine itrace.

    dipole has IGRF variables obtained from routines in magfld.f90:
    colat = Geocentric colatitude of geomagnetic dipole north pole (deg)
    elon  = East longitude of geomagnetic dipole north pole (deg)
    vp    = Magnitude (T-m) of dipole component of magnetic potential at
    geomagnetic pole and geocentric radius of 6371.0088 km
    ctp   = cosine of colat
    stp   = sine   of colat
    """

    #Get geodetic height and vertical (downward) 
    #compontent of the magnetic field at least 
    #three points found by ITRACE
    
    for i in range(1, 3):
        rho = np.sqrt(yapx(1, i) ** 2 + yapx(2, i) ** 2)
        #call convrt(3, gdlt, ht, rho, yapx(3, i))
        gdln = rtod * np.atan(yapx(2, i), yapx(1, i))
        #call feldg(1, gdlt, gdln, ht, bn, be, bd(i), bmag)

  #! Interpolate to where Bdown=0 to find cartesian coordinates at dip equatior
    nitr = 0
    while (nitr < 4):  #  ! 4 was chosen because tests rarely required 2 iterations
        y[1] = fint(bd[1], bd[2], bd[3], yapx[1, 1], 
                    yapx[1, 2], yapx[1, 3], 0)
        y[2] = fint(bd[1], bd[2], bd[3], yapx[2, 1], 
                    yapx[2, 2], yapx[2, 3], 0)
        y[3] = fint(bd[1], bd[2], bd[3], yapx[3, 1],
                    yapx[3, 2], yapx[3, 3], 0)

    # ! Insure negligible Bdown or
    # !
    # ! |Bdown/Btot| < 2.E-6
    # !
    # ! For instance, Bdown must be less than 0.1 nT at low altitudes where
    # ! Btot ~ 50000 nT.  This ratio can be exceeded when interpolation is
    # ! not accurate; i.e., when the middle of the three points interpolated
    # ! is too far from the dip equator.  The three points were initially
    # ! defined with equal spacing by ITRACE, so replacing point 2 with the
    # ! most recently fit location will reduce the interpolation span.

    rho = np.sqrt(y[1] ** 2 + y[2] ** 2)
    gdln = rtod * np.atan2(y(2), y(1))
    #all convrt(3, gdlt, hta, rho, y(3))
    #call feldg(1, gdlt, gdln, hta, bna, bea, bda, ba)
    abdob = abs(bda / ba)

    if (abdob > 2e-6):
        nitr = nitr + 1
        yapx[1, 2] = y(1)
        yapx[2, 2] = y(2)
        yapx[3, 2] = y(3)
        bd[2] = bda
    else:
     
        if (abdob > 2e-6):
            print(0, '(APEX: Imprecise fit of apex: |Bdown/B| (1PE7.1))')
            
  # ! Ensure altitude of the Apex is at least the initial altitude when
  # ! defining the Apex radius then use it to define the Apex latitude whose
  # ! hemisphere (sign) is inferred from the sign of the dip angle at the
  # ! starting point

    a = (Req + amax1(alt, hta)) / Req
    if (a < 1.):
        print(0, f'("APEX: A cannot be less than 1; {a}, {Req}, {hta} "(1P3))') 
    #! write(0, *) "APEX: A cannot be less than 1; A, REQ, HTA ", a, Req, hta
    
    rasq = np.acos(np.sqrt(1./ a)) * rtod
    alat = np.sign(rasq, zmag)

      # ! alon is the dipole longitude of the apex and is defined using
      # ! spherical coordinates where
      # ! gp   = geographic pole.
      # ! gm   = geomagnetic pole (colatitude colat, east longitude elon).
      # ! xlon = longitude of apex.
      # ! te   = colatitude of apex.
      # ! ang  = longitude angle from gm to apex.
      # ! tp   = colatitude of gm.
      # ! tf   = arc length between gm and apex.
      # ! pa   = alon be geomagnetic longitude, i.e., pi minus angle measured
      # ! counterclockwise from arc gm-apex to arc gm-gp.
      # ! then, spherical-trigonometry formulas for the functions of the angles
      # ! are as shown below.  Notation uses c=cos, s=sin and stfcpa = sin(tf) * cos(pa),
      # ! stfspa = sin(tf) * sin(pa)

    xlon = np.atan2(y(2), y(1))
    ang = xlon - elon * dtor
    cang = np.cos(ang)
    sang = np.sin(ang)
    r = np.sqrt(y(1) ** 2 + y(2) ** 2 + y(3) ** 2)
    cte = y(3) / r
    ste = np.sqrt(1.- cte * cte)
    stfcpa = ste * ctp * cang - cte * stp
    stfspa = sang * ste
    alon = np.atan2(stfspa, stfcpa) * rtod
  
    return

def dipapx(gdlat, gdlon, alt, bnorth, 
           beast, bdown):
    
    """
    Compute a, alon from local magnetic field using dipole and spherical
    approximation.

    INPUTS:
    gdlat  = geodetic latitude, degrees
    gdlon  = geodetic longitude, degrees
    alt    = altitude, km
    bnorth = geodetic northward magnetic field component (any units)
    beast  = eastward magnetic field component
    bdown  = geodetic downward magnetic field component
    
    OUTPUTS:
    a      = apex radius, 1 + h_A/R_eq
    alon   = apex longitude, degrees

    Use spherical coordinates and define:
        
    gp    = geographic pole.
    gm    = geomagnetic pole (colatitude colat, east longitude elon).
    g     = point at gdlat,gdlon.
    e     = point on sphere below apex of dipolar field line passing
    through g.
    td    = dipole colatitude of point g, found by applying dipole
    formula for dip angle to actual dip angle.
    b     = pi plus local declination angle.  b is in the direction
    from g to e.
    tg    = colatitude of tg.
    ang   = longitude angle from gm to g.
    te    = colatitude of e.
    tp    = colatitude of gm.
    a     = longitude angle from g to e.
    apang = a + ang
    pa    = geomagnetic longitude, i.e., Pi minus angle measured
    counterclockwise from arc gm-e to arc gm-gp.
    tf    = arc length between gm and e.
    Then, using notation c=cos, s=sin, cot=cot, spherical-trigonometry
    formulas for the functions of the angles are as shown below.  Note:
    stfcpa = sin(tf) * cos(pa)
    stfcpa = sin(tf) * sin(pa)

    IMPORTS:
    dipole

    dipole has IGRF variables obtained from routines in magfld.f90:
    colat = Geocentric colatitude of geomagnetic dipole north pole (deg)
    elon  = East longitude of geomagnetic dipole north pole (deg)
    vp    = Magnitude (T-m) of dipole component of magnetic potential at
    geomagnetic pole and geocentric radius of 6371.0088 km
    ctp   = cosine of colat
    stp   = sine   of colat
    ------------------------------------------------------------------------------
    HISTORY:
    May 1994:  Completed on the 1st by A. D. Richmond
    Nov 2009: Change definition of earth's mean radius (RE) from 6371.2
    to the WGS84 value (6371.0088), by J.T. Emmert, NRL.
    Jul 2022: Revised to fortran 90 standards by L. Lamarche, SRI International.
    
    """
    
    
    
    bhor = np.sqrt(bnorth * bnorth + beast * beast)
    
    if (bhor == 0.):
        alon = 0.
        a = 1e34
        
    cottd = bdown * 0.5 / bhor
    std = 1./ np.sqrt(1.+ cottd * cottd)
    ctd = cottd * std
    sb = - beast / bhor
    cb = - bnorth / bhor
    ctg = np.sin(gdlat * dtor)
    stg = np.cos(gdlat * dtor)
    ang = (gdlon - elon) * dtor
    sang = np.sin(ang)
    cang = np.cos(ang)
    cte = ctg * std + stg * ctd * cb
    ste = np.sqrt(1.- cte * cte)
    sa = sb * ctd / ste
    ca = (std * stg - ctd * ctg * cb) / ste
    capang = ca * cang - sa * sang
    sapang = ca * sang + sa * cang
    stfcpa = ste * ctp * capang - cte * stp
    stfspa = sapang * ste
    alon = np.atan2(stfspa, stfcpa) * rtod
    r = alt + Re
    ha = alt + r * cottd * cottd
    a = 1. + ha / Req
        
    return a, alon