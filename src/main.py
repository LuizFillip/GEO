from tqdm import tqdm  
import datetime as dt
import GEO as gg


site = 'jic'
glat, glon = gg.sites[site]['coords']
    
# for year in tqdm(range(2013, 2022)):
    
year = 2022
    
date = dt.datetime(year, 1, 1)

gg.save_meridian(
        date, 
        glon, 
        glat, 
        site
        )
