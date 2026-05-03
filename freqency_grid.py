import numpy as np
import pandas as pd
import time_adjusted_grid as tim_ajd

#Convert lat/lon to meters relative to the minimum lat/lon
METERS_PER_LAT_DEGREE = 111320.0
def lat_lon_to_meters(lat, lon, ref_lat, ref_lon):
        lat_diff = lat - ref_lat
        lon_diff = lon - ref_lon

        x = lon_diff * (METERS_PER_LAT_DEGREE * np.cos(np.radians(ref_lat)))
        y = lat_diff * METERS_PER_LAT_DEGREE
        
        return x, y


def get_grid(grid_size = 100, data_file = 'BlackBear2013_data.csv'):
    df = pd.read_csv(data_file)

    relx = df['Latitude'].min()
    rely = df['Longitude'].min()

    # Parse datetime from the Date and Time columns so we can attach time values to each cell.
    df['DateTime'] = df['Time'].astype(str)

    #grid size in meters
    GRID_SIZE = grid_size
    x_list = []
    y_list = []
    time_list = []
    for lat, lon, timestamp in zip(df['Latitude'], df['Longitude'], df['DateTime']):
        x, y = lat_lon_to_meters(lat, lon, relx, rely)
        x_list.append(x)
        y_list.append(y)
        time_list.append(timestamp)

    # Determine grid dimensions
    x_min, x_max = 0, max(x_list) + GRID_SIZE
    y_min, y_max = 0, max(y_list) + GRID_SIZE

    n_cols = int(np.ceil((x_max - x_min) / GRID_SIZE))
    n_rows = int(np.ceil((y_max - y_min) / GRID_SIZE))

    # Create grid and count points in each cell.
    # Use float dtype so time-based weights are preserved.
    grid = np.zeros((n_rows, n_cols), dtype=float)
    time_values_grid = [[[] for _ in range(n_cols)] for _ in range(n_rows)]

    user_time = "12:00"

    for x, y, timestamp in zip(x_list, y_list, time_list):
        col = int(x // GRID_SIZE)
        row = int(y // GRID_SIZE)
        col = min(col, n_cols - 1)
        row = min(row, n_rows - 1)
        grid[row][col] += tim_ajd.time_difference(user_time, timestamp)
        #tim_ajd.time_difference(user_time, k, timestamp)

        if tim_ajd.time_difference(user_time, timestamp) > 0:
            print(tim_ajd.time_difference(user_time, timestamp))
        #print(timestamp)

        #tim_ajd.time_difference(user_time, k, timestamp)
        if pd.notna(timestamp):
            time_values_grid[row][col].append(timestamp)

    # Print grid info
    print(f"Grid shape : {n_rows} rows by {n_cols} cols  (each cell = {GRID_SIZE}m)")
    print(f"Total points: {grid.sum()}\n")
    
    #print(grid)
    #print(time_values_grid)

    min_lat = relx
    min_lon = rely

    meters_per_lon_degree = METERS_PER_LAT_DEGREE * np.cos(np.radians(relx))
    lat_step_deg = GRID_SIZE / METERS_PER_LAT_DEGREE
    lon_step_deg = GRID_SIZE / meters_per_lon_degree

    max_lat = min_lat + n_rows * lat_step_deg
    max_lon = min_lon + n_cols * lon_step_deg

    print(grid[grid > 1])

    return grid, min_lon, max_lon, min_lat, max_lat, time_values_grid



if __name__ == "__main__":
    get_grid()
