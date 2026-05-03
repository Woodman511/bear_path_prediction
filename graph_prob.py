import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimg
import freqency_grid
import propagate
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch

# Load the raw grid and geographic bounds from the input dataset.
grid, min_lon, max_lon, min_lat, max_lat, time_values_grid, land_mask, lat_matrix, lon_matrix = freqency_grid.get_grid()
# Propagate the grid values to fill nearby empty cells, leaving water cells zero.
prob = propagate.propagate(grid, land_mask=land_mask)

def graph_data(data=prob, mask=land_mask, name="unamed"):
    """
    Graph the probability data on a map with satellite imagery background.

    Args:
        data (numpy.ndarray): The grid data to visualize
        mask (numpy.ndarray): Boolean mask indicating land cells
        name (str): Title for the plot

    Returns:
        matplotlib.axes.Axes: The map axes object
    """
    # Apply land mask to data (set water cells to 0)
    data = np.where(mask, data, 0)
    # Use a fast matplotlib style for better performance
    plt.style.use('fast')

    # Create a transparent-to-red colormap for the overlay.
    # The first color is fully transparent, and the final color is solid red.
    white_to_red = LinearSegmentedColormap.from_list("wtr", [(0, 0, 0, 0), (3, 0, 0, 1)])
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
    ca_map.add_image(google_tiles, 10, zorder=0, alpha=0.9)

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

    # For debugging purposes: Add a colorbar showing numeric values for the heatmap.
    plt.colorbar(im, ax=ca_map, orientation='vertical', pad=0.02)

    # Add legend elements
    legend_elements = [
            Patch(facecolor='red', edgecolor='red', label='High Probability'),
            Patch(facecolor='none', edgecolor='black', label='Low Probability')
        ]
    plt.legend(handles=legend_elements, loc='upper right')
    # Optional: Plot a specific point for debugging
    # plt.plot(lat_matrix[29, 20], lon_matrix[29, 20], markersize=20, color="blue", zorder=2)

    # Set the plot title
    ca_map.set_title(name)
    return ca_map
    #def add_line():

        
        

    
if __name__ == "__main__":
    # Build the map and display the result.
    graph_data(name="probability_grid")
    # Alternative: graph the original frequency grid instead
    # graph_data(grid, name="frequency_grid")
    # Debug: print time values
    # print(time_values_grid)
    plt.show()
