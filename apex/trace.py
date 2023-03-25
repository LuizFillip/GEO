import numpy as np

# Define the magnetic field equation as a function
# of latitude and height:
    

def B(lat, h): 
    return 1 + 0.1 * h * np.sin(lat)

# Define the magnetic field line equation as a system
# of first-order differential equations:

def f(s, y):
    lat, h = y
    B_lat = B(lat, h)
    B_h = 0.1 * np.sin(lat)
    return np.array([B_h / B_lat, 1])

# Choose an initial point on the desired magnetic 
# field line (e.g., magnetic equator) and the desired apex height:

lat0 = 0  # Initial latitude
h0 = 100  # Initial height
h_apex = 1000  # Desired apex height

y0 = np.array([lat0, h0])

#Define the range of latitudes to trace the magnetic field line:
    
lat_range = np.linspace(-20 * np.pi / 180, 0, 100)


#Trace the magnetic field line using the fourth-order Runge-Kutta method:
    
    
y = np.zeros((len(lat_range), 2))

y[0] = y0

for i in range(len(lat_range) - 1):
    
    k1 = f(lat_range[i], y[i])
    
    k2 = f(lat_range[i] + 0.5 * 
           (lat_range[i + 1] - lat_range[i]), 
           y[i] + 0.5 * (lat_range[i + 1] - lat_range[i]) * k1)
    k3 = f(lat_range[i] + 0.5 * 
           (lat_range[i + 1] - lat_range[i]), 
           y[i] + 0.5 * (lat_range[i + 1] - lat_range[i]) * k2)
    k4 = f(lat_range[i + 1], y[i] + 
           (lat_range[i + 1] - lat_range[i]) * k3)

    y[i + 1] = (y[i] + (lat_range[i + 1] - lat_range[i]) / 6 * 
                (k1 + 2 * k2 + 2 * k3 + k4))


# Extract the heights corresponding to the desired apex height
# and the latitudes of interest:
    
h_desired = y[:, 1] - h_apex
lat_range_of_interest = np.linspace(0, -20 * np.pi / 180, 100)
h_lat = np.interp(lat_range_of_interest, lat_range, h_desired)

import matplotlib.pyplot as plt

plt.plot(y)
