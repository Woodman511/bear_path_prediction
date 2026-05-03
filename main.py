import graph_prob as gp
import cartopy.crs as ccrs
import path_find as pf

# Create the map visualization
ca_map = gp.graph_data()
# Print latitude and longitude matrices for debugging
# print(gp.lat_matrix)
# print(gp.lon_matrix)

# Run path finding algorithm to get the bear movement path
path = pf.run()

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

gp.plt.show()