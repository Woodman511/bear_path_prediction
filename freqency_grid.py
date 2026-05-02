import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

df = pd.read_csv('BrownBear_data.csv')
#df['Latitude'] = df['Latitude']

relx = df['Latitude'].min()
rely = df['Longitude'].min()

def lat_lon_to_meters(lat, lon, ref_lat, ref_lon):
    METERS_PER_LAT_DEGREE = 111320.0

    lat_diff = lat - ref_lat
    lon_diff = lon - ref_lon

    x = lon_diff * (METERS_PER_LAT_DEGREE * np.cos(np.radians(ref_lat)))
    y = lat_diff * METERS_PER_LAT_DEGREE
    
    return x, y

#grid size in meters
GRID_SIZE = 500 
x_list = []
y_list = []
for lat, lon in zip(df['Latitude'], df['Longitude']):
    x, y = lat_lon_to_meters(lat, lon, relx, rely)
    x_list.append(x)
    y_list.append(y)

arr = np.column_stack((x_list, y_list))

x_min, x_max = 0, max(x_list) + GRID_SIZE
y_min, y_max = 0, max(y_list) + GRID_SIZE

n_cols = int(np.ceil((x_max - x_min) / GRID_SIZE))
n_rows = int(np.ceil((y_max - y_min) / GRID_SIZE))

grid = np.zeros((n_rows, n_cols), dtype=int)

for x, y in zip(x_list, y_list):
    col = int(x // GRID_SIZE)
    row = int(y // GRID_SIZE)
    col = min(col, n_cols - 1)   # clamp to grid bounds
    row = min(row, n_rows - 1)
    grid[row][col] += 1

print(f"Grid shape : {n_rows} rows by {n_cols} cols  (each cell = {GRID_SIZE}m)")
print(f"Total points: {grid.sum()}\n")
print(grid)

white_to_red = LinearSegmentedColormap.from_list("wtr", ["white", "red"])

plt.imshow(grid,
           cmap=white_to_red,
           interpolation='nearest')
plt.colorbar()
plt.show()
