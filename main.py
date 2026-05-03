import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import freqency_grid
import propagate
from matplotlib.colors import LinearSegmentedColormap


white_to_red = LinearSegmentedColormap.from_list("wtr", ["white", "red"])

grid, min_lon, max_lon, min_lat, max_lat = freqency_grid.get_grid()
prob = propagate.propagate(grid)


plt.figure(figsize=(14, 6))
ca_map = plt.axes(projection=ccrs.PlateCarree())
#ca_map.add_feature(cfeature.LAND)
#ca_map.add_feature(cfeature.OCEAN)
#ca_map.add_feature(cfeature.COASTLINE)
#ca_map.add_feature(cfeature.BORDERS, linestyle=':')
ca_map.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())
ca_map.add_feature(cfeature.COASTLINE.with_scale("50m"), linewidth=0.9, edgecolor="#4a6070")
ca_map.add_feature(cfeature.BORDERS.with_scale("50m"),   linewidth=0.5, edgecolor="#888", linestyle="--")
ca_map.add_feature(cfeature.RIVERS.with_scale("50m"),    edgecolor="#3B8BD4", linewidth=0.5)
ca_map.add_feature(cfeature.LAKES.with_scale("50m"),     facecolor="#c8dff0")

ca_map.xaxis.set_visible(True)
ca_map.yaxis.set_visible(True)



ca_map.imshow(grid,
                    origin='lower',
                    extent=[min_lon, max_lon, min_lat, max_lat],
                    transform=ccrs.PlateCarree(),
                    cmap=white_to_red,
                    interpolation='nearest',
                    alpha=0.2
)
ca_map.set_title("Frequency Grid")
#plt.colorbar(im1, ax=plt.gca(), orientation='vertical', label='Point count')

'''
fig.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)

im2 = ax2.imshow(prob,
            cmap=white_to_red,
            interpolation='nearest')
ax2.set_title("Propagated Probability")

fig.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)
'''

plt.show()
