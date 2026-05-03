import graph_prob as gp
import cartopy.crs as ccrs
import path_find as pf
import random as rand

#gp.plt.ion()

# Create the map visualization
ca_map = gp.graph_data(name="Initial Probability Map")

# Print the valid coordinate range for the loaded grid.
print(f"Grid latitude range: {gp.lat_matrix.min():.6f} to {gp.lat_matrix.max():.6f}")
print(f"Grid longitude range: {gp.lon_matrix.min():.6f} to {gp.lon_matrix.max():.6f}")

# Example start coordinate inside the dataset bounds.
# Replace these values with the desired starting latitude/longitude.
user_start_lat = 61.180106
user_start_lon = -149.787058

start_row, start_col = pf.nearest_grid_cell(gp.lat_matrix, gp.lon_matrix, user_start_lat, user_start_lon)
print(f"Nearest grid cell for start coordinate ({user_start_lat}, {user_start_lon}) -> row={start_row}, col={start_col}")

# Run path finding algorithm to get the bear movement path using the nearest grid cell for the given lon/lat.
path = pf.run(
    user_start_lon=user_start_lon,
    user_start_lat=user_start_lat,
)

# Convert grid indices to geographic coordinates for plotting
first = True
x_list = []
y_list = []

for x, y in path:
    x_list.append(gp.lon_matrix[x,y])
    y_list.append(gp.lat_matrix[x,y])

# Plot the path on the map
ca_map.plot(x_list, y_list,
            markersize=3,
            color='blue',
            zorder=3,
            transform=ccrs.PlateCarree(), 
            marker='o', 
            label='Start',
            linestyle='solid',
            linewidth=1)

# Add a zoomed-in view around the bear path.
gp.graph_zoomed_data(path=path, name="zoomed_bear_path")

#gp.plt.pause(0.01)

gp.plt.show()