import numpy as np

def find_closest_value(target, values):
    return min(values, key=lambda x: abs(x - target))

def find_longitudes(dic, length = 6):
    
    lon = list(dic.keys())
    
    deltas = [(10 * (j + 1)) for j in range(0, length, 1)]
    index = 0
    out = []
    for i, l in enumerate(lon):
        
        x, y = dic[lon[i]]
        x0, y0 = dic[lon[index]]
        
        dis = round(
            np.sqrt(pow(x - x0, 2) + pow(y - y0, 2)), 2)
        
        value = find_closest_value(dis, deltas)
    
        if dis < value:
            index =+ 1
        else:
            out.append([dis, lon[i], value])
            
    return {i[-1]: tuple(i[:2]) for i in out[::length - 1]}