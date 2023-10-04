import math

def haversine_distance(lat1, lon1, lat2, lon2):
   
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (math.sin(dlat / 2)**2 + 
         math.cos(lat1) * 
         math.cos(lat2) * 
         math.sin(dlon / 2)**2)
    

    return 6371.0 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def example():
    lat1 = 52.5200  # Latitude of the first point (e.g., city 1)
    lon1 = 13.4050  # Longitude of the first point
    lat2 = 48.8566  # Latitude of the second point (e.g., city 2)
    lon2 = 2.3522   # Longitude of the second point
    
    distance = haversine_distance(lat1, lon1, lat2, lon2)
    print(f"Distance: {distance} kilometers")
    
    
# example()