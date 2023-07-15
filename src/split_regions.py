# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 13:01:14 2023

@author: Luiz
"""


lat_min = -10
lat_max = -2
lon_max = -32
lon_min = -40

limits = [lon_min, lon_max, lat_min, lat_max]

def slip_array(arr, *args, factor = 2):
    
    """
    
    arr = np.arange(64).reshape(8, 8)
    list_out = slip_array(arr, *limits, factor = 2)
    
    max_values = [np.nanmax(list_out[num]) for num in range(len(list_out))]
    """

    dx = int((lon_max - lon_min) / factor)
    dy = int((lat_max - lat_min) / factor)

    xsize =  int(lon_max - lon_min)
    ysize =  int(lat_max - lat_min)

    out = []

    for x in range(0, xsize, dx):
        for y in range(0, ysize, dy):
            if x == y: 
                continue
            equal = arr[x: x + dx, x: x + dx]
            out.append(equal)
            cross = arr[x: x + dx, y: y + dy]
            out.append(cross)
                        
    return out