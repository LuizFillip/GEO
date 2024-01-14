import os 

def load_equator(year, values = False):
    infile = os.getcwd() + f'/database/GEO/dips/dip_{year}.txt'
    
    df = pd.read_csv(infile, index_col = 0)

    if values:
        return df['lon'].values, df['lat'].values 
    else:
        return df


def distance_from_equator(
        lon, lat, year = 2013
        ):
    x, y = load_equator(year, values = True)

    min_x, min_y, min_d = gg.compute_distance(
        x, y, lon, lat
        )
    return min_d


 
    

 
def plot_terminator_and_equator(
        ax, dn, twilight = 18):
 
    eq_lon, eq_lat  = gg.load_equator(
        dn.year, values = True)
    
    term_lon, term_lat = gg.terminator2(
        dn, twilight)
    
    ax.scatter(term_lon, term_lat, s = 10)
    
    inter_lon, inter_lat = gg.intersection(
        eq_lon, eq_lat, term_lon, term_lat)
    
    
    ax.scatter(inter_lon, inter_lat, s = 100, 
               marker = 'X', color = 'r')
    
    return eq_lon, eq_lat