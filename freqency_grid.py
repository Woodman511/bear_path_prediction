import numpy as np
import pandas as pd

def get_grid():
    df = pd.read_csv('BrownBear_data.csv')

    relx = df['Latitude'].min()
    rely = df['Longitude'].min()

    #Convert lat/lon to meters relative to the minimum lat/lon
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

    # Determine grid dimensions
    x_min, x_max = 0, max(x_list) + GRID_SIZE
    y_min, y_max = 0, max(y_list) + GRID_SIZE

    n_cols = int(np.ceil((x_max - x_min) / GRID_SIZE))
    n_rows = int(np.ceil((y_max - y_min) / GRID_SIZE))

    # Create grid and count points in each cell
    grid = np.zeros((n_rows, n_cols), dtype=int)

    for x, y in zip(x_list, y_list):
        col = int(x // GRID_SIZE)
        row = int(y // GRID_SIZE)
        col = min(col, n_cols - 1)
        row = min(row, n_rows - 1)
        grid[row][col] += 1

    # Print grid info
    print(f"Grid shape : {n_rows} rows by {n_cols} cols  (each cell = {GRID_SIZE}m)")
    print(f"Total points: {grid.sum()}\n")
    print(grid)

    

    return grid



if __name__ == "__main__":
    get_grid()
