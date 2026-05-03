import numpy as np
import pandas as pd
import time_adjusted_grid as tim_ajd
from global_land_mask import globe

#Convert lat/lon to meters relative to the minimum lat/lon
METERS_PER_LAT_DEGREE = 111320.0
def lat_lon_to_meters(lat, lon, ref_lat, ref_lon):
        lat_diff = lat - ref_lat
        lon_diff = lon - ref_lon

        x = lon_diff * (METERS_PER_LAT_DEGREE * np.cos(np.radians(ref_lat)))
        y = lat_diff * METERS_PER_LAT_DEGREE
        
        return x, y

data = ["BlackBear2012_data.csv", "BlackBear2013_data.csv"]
def get_grid(index = 0 , grid_size = 100, data_file = data):
    #df = pd.DataFrame()
    df = pd.concat([pd.read_csv(f) for f in data_file], ignore_index=True)



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

    #TODO: add input to set the user time that a bear was seen
    user_time = "6:00"

    for x, y, timestamp, lat, long in zip(x_list, y_list, time_list, df['Latitude'], df['Longitude']):
        col = int(x // GRID_SIZE)
        row = int(y // GRID_SIZE)
        col = min(col, n_cols - 1)
        row = min(row, n_rows - 1)
        grid[row][col] += 1
        
        tim_ajd.time_difference(user_time, timestamp,index_time=index)

        #if tim_ajd.time_difference(user_time, timestamp) > 0:
            #print(tim_ajd.time_difference(user_time, timestamp))
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

    # Mask out water cells so they remain zero in the final grid.
    row_centers = min_lat + (np.arange(n_rows) + 0.5) * lat_step_deg
    col_centers = min_lon + (np.arange(n_cols) + 0.5) * lon_step_deg
    lat_centers = row_centers[:, None]
    lon_centers = col_centers[None, :]
    land_mask = globe.is_land(lat_centers, lon_centers)
    grid[~land_mask] = 0

    np.log1p(grid, out=grid)

    lat_matrix = lat_centers.repeat(n_cols, axis=1)
    lon_matrix = lon_centers.repeat(n_rows, axis=0)

    return grid, min_lon, max_lon, min_lat, max_lat, time_values_grid, land_mask, lat_matrix, lon_matrix


def nearest_grid_cell(lat_matrix, lon_matrix, target_lat, target_lon):
    """Find the nearest grid cell index for a latitude/longitude coordinate.

    This uses the haversine distance over the globe to account for the
    different physical scaling of latitude and longitude.
    """
    if lat_matrix.shape != lon_matrix.shape:
        raise ValueError("lat_matrix and lon_matrix must have the same shape")

    # Earth radius in meters.
    R = 6371000.0
    lat1 = np.radians(lat_matrix)
    lon1 = np.radians(lon_matrix)
    lat2 = np.radians(target_lat)
    lon2 = np.radians(target_lon)

    dlat = lat1 - lat2
    dlon = lon1 - lon2
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    dist = 2 * R * np.arcsin(np.sqrt(a))

    idx = np.unravel_index(np.argmin(dist), dist.shape)
    return idx


if __name__ == "__main__":
    get_grid()
