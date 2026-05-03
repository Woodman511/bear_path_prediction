import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimg
import freqency_grid
import propagate
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch

# Load the raw grid and geographic bounds from the input dataset.
grid, min_lon, max_lon, min_lat, max_lat, time_values_grid = freqency_grid.get_grid()
# Propagate the grid values to fill nearby empty cells.
prob = propagate.propagate(grid)

def graph_data(data=prob):
    plt.style.use('fast')

    # Create a transparent-to-red colormap for the overlay.
    # The first color is fully transparent, and the final color is solid red.
    white_to_red = LinearSegmentedColormap.from_list("wtr", [(0, 0, 0, 0), (1, 0, 0, 1)])

    # Create the figure and geographic axes using Plate Carree projection.
    plt.figure(figsize=(16, 10))
    ca_map = plt.axes(projection=ccrs.PlateCarree())

    # Set the map extent to the bounds of the loaded dataset.
    ca_map.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())

    # Show map axes and tick labels.
    ca_map.xaxis.set_visible(True)
    ca_map.yaxis.set_visible(True)

    # Add Google satellite imagery as the map background.
    google_tiles = cimg.GoogleTiles(style='satellite')
    ca_map.add_image(google_tiles, 10, zorder=0, alpha=0.7)

    # Draw the propagated probability grid on top of the background.
    im = ca_map.imshow(
        data,
        origin='lower',
        extent=[min_lon, max_lon, min_lat, max_lat],
        transform=ccrs.PlateCarree(),
        cmap=white_to_red,
        interpolation='nearest',
        alpha=1,
        zorder=1, 
        #norm=LogNorm(vmin=0.011, vmax=data.max())
    )

    #For debugging purposes: Add a colorbar showing numeric values for the heatmap.
        #plt.colorbar(im, ax=ca_map, orientation='vertical', pad=0.02)

    legend_elements = [
            Patch(facecolor='red', edgecolor='red', label='High Probability'),
            Patch(facecolor='none', edgecolor='black', label='Low Probability')
        ]
    plt.legend(handles=legend_elements, loc='upper right')


    ca_map.set_title("Frequency Grid over Google Maps")

    #def add_line():

        
        

    
if __name__ == "__main__":
    # Build the map and display the result.
    graph_data()
    graph_data(grid)
    #print(time_values_grid)
    plt.show()
