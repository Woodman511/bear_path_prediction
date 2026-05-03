import graph_prob as gp
import cartopy.crs as ccrs
import path_find as pf

ca_map = gp.graph_data()
#print(gp.lat_matrix)
#print(gp.lon_matrix)

path = pf.run()

first = True
x_list = []
y_list = []
for x, y in path:
    if first:
        color = "green"
        first = False
    else:
        color = "blue"
    x_list.append(gp.lon_matrix[x,y])
    y_list.append(gp.lat_matrix[x,y])

ca_map.plot(x_list, y_list,
            markersize=3,
            color=color,
            zorder=3,
            transform=ccrs.PlateCarree(), 
            marker='o', 
            label='Start',
            linestyle='solid',
            linewidth=1)

gp.plt.show()