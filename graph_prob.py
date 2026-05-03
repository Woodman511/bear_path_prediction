import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimg
import freqency_grid
import propagate
from matplotlib.colors import LinearSegmentedColormap


white_to_red = LinearSegmentedColormap.from_list("wtr", [(0, 0, 0, 0), (256, 0, 0, 1)])

grid, min_lon, max_lon, min_lat, max_lat = freqency_grid.get_grid()
prob = propagate.propagate(grid)


plt.figure(figsize=(16, 10))
ca_map = plt.axes(projection=ccrs.PlateCarree())
ca_map.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())

ca_map.xaxis.set_visible(True)
ca_map.yaxis.set_visible(True)

# Add Google Maps background tiles
google_tiles = cimg.GoogleTiles(style='satellite')
ca_map.add_image(google_tiles, 10, zorder=0)

ca_map.imshow(prob,
                    origin='lower',
                    extent=[min_lon, max_lon, min_lat, max_lat],
                    transform=ccrs.PlateCarree(),
                    cmap=white_to_red,
                    interpolation='nearest',
                    alpha=1,
                    zorder=1
)
ca_map.set_title("Frequency Grid over Google Maps")
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
