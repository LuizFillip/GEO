import astral 
from astral.sun import sun
import datetime as dt
import matplotlib.pyplot as plt

def dawn_dusk(dn,  
            lat = -2.53, 
            lon = -44.296, 
            twilightAngle = 18):

    observer = astral.Observer(latitude = lat, longitude = lon)
    sun_phase = sun(observer, 
                    dn, 
                    dawn_dusk_depression = twilightAngle
                    )
    return sun_phase["dawn"], sun_phase["dusk"]

date_list = [dt.datetime(2013, 1, 1), dt.datetime(2013, 1, 2)]



def plot_lines(
        ax, date_list, 
        glat = -2.53, glon= -44.296):

    for dn in date_list:
        for regionF in dawn_dusk(dn,  
                    glat, 
                    glon, 
                    twilightAngle = 18):
        
            l2 = ax.axvline(regionF)
        
        for regionE in dawn_dusk(dn,  
                    glat, 
                    glon, 
                    twilightAngle = 12):
        
            l3 = ax.axvline(regionE, color = "blue")
            
    
    
    labels = ["300 km", "120 km"]
    
    ax.legend([l2, l3], labels, 
                     loc = "lower left", 
                     )        
    
    

