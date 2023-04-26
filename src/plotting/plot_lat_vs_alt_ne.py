import pandas as pd
import matplotlib.pyplot as plt

infile = "199410010000.txt"

df = pd.read_csv(infile, index_col = 0)

df = pd.pivot_table(df, values = "Ne", columns = "lat", index = "alt")


plt.contourf(df.columns + 13.7, 
             df.index, 
             df.values, 20, 
             cmap = "rainbow")

plt.xlim([-20, 20])