import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimg
import freqency_grid
import path_find
import propagate
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
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
    fig = plt.figure(figsize=(16, 10))
    fig.subplots_adjust(left=0.08, right=0.98, top=0.96, bottom=0.04)
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
        zorder=1
    )
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    # For debugging purposes: Add a colorbar showing numeric values for the heatmap.
    #plt.colorbar(im, ax=ca_map, orientation='vertical', pad=0.02)

    # Add legend elements
    legend_elements = [
            Patch(facecolor='red', edgecolor='black', label='High Probability'),
            Patch(facecolor=(1,0,0,0.2), edgecolor='black', label='Low Probability')
        ]
    plt.legend(handles=legend_elements, loc='upper right')
    # Optional: Plot a specific point for debugging
    # plt.plot(lat_matrix[29, 20], lon_matrix[29, 20], markersize=20, color="blue", zorder=2)

    # Set the plot title
    ca_map.set_title(name)
    return ca_map


def graph_zoomed_data(data=prob, mask=land_mask, path=None, name="zoomed_probability_grid", pad_degrees=0.015):
    """
    Graph a zoomed-in region around the bear path with updated Google imagery.

    Args:
        data (numpy.ndarray): The grid data to visualize
        mask (numpy.ndarray): Boolean mask indicating land cells
        path (list[tuple[int, int]]|None): Sequence of (row, col) path indices
        name (str): Title for the plot
        pad_degrees (float): Padding around the path in degrees

    Returns:
        matplotlib.axes.Axes: The map axes object
    """
    data = np.where(mask, data, 0)
    plt.style.use('fast')

    # Determine the zoomed bounding box from the path
    if path is not None and len(path) > 0:
        path_lats = np.array([lat_matrix[r, c] for r, c in path])
        path_lons = np.array([lon_matrix[r, c] for r, c in path])
        row_indices = np.array([r for r, c in path])
        col_indices = np.array([c for r, c in path])
        min_lat_path = max(min_lat, float(path_lats.min() - pad_degrees))
        max_lat_path = min(max_lat, float(path_lats.max() + pad_degrees))
        min_lon_path = max(min_lon, float(path_lons.min() - pad_degrees))
        max_lon_path = min(max_lon, float(path_lons.max() + pad_degrees))

        row_min, row_max = row_indices.min(), row_indices.max()
        col_min, col_max = col_indices.min(), col_indices.max()
        data = data[row_min:row_max + 1, col_min:col_max + 1]
        mask = mask[row_min:row_max + 1, col_min:col_max + 1]
    else:
        min_lon_path, max_lon_path, min_lat_path, max_lat_path = min_lon, max_lon, min_lat, max_lat

    fig = plt.figure(figsize=(16, 10))
    fig.subplots_adjust(left=0.04, right=0.98, top=0.96, bottom=0.08)
    ca_zoom = plt.axes(projection=ccrs.PlateCarree())
    ca_zoom.set_extent([min_lon_path, max_lon_path, min_lat_path, max_lat_path], crs=ccrs.PlateCarree())

    # Show map axes and tick labels.
    ca_zoom.xaxis.set_visible(True)
    ca_zoom.yaxis.set_visible(True)

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    # Updated Google satellite imagery for the zoomed graph
    google_tiles = cimg.GoogleTiles(style='satellite')
    ca_zoom.add_image(google_tiles, 12, zorder=0, alpha=0.9)

    white_to_red = LinearSegmentedColormap.from_list("wtr", [(0, 0, 0, 0), (3, 0, 0, 0.5)])

    im = ca_zoom.imshow(
        data,
        origin='lower',
        extent=[min_lon_path, max_lon_path, min_lat_path, max_lat_path],
        transform=ccrs.PlateCarree(),
        cmap=white_to_red,
        interpolation='nearest',
        alpha=1,
        zorder=1,
    )

    if path is not None and len(path) > 0:
        path_lats = np.array([lat_matrix[r, c] for r, c in path])
        path_lons = np.array([lon_matrix[r, c] for r, c in path])
        ca_zoom.plot(
            path_lons,
            path_lats,
            marker='o',
            color='blue',
            linewidth=2,
            markersize=4,
            transform=ccrs.PlateCarree(),
            zorder=2,
            label='Bear Path'
        )

    #plt.colorbar(im, ax=ca_zoom, orientation='vertical', pad=0.02)

    legend_elements = [
        Patch(facecolor='red', edgecolor='black', label='High Probability'),
        Patch(facecolor=(1,0,0,0.2), edgecolor='black', label='Low Probability')
    ]
    if path is not None and len(path) > 0:
        legend_elements.append(Line2D([0], [0], color='blue', lw=2, label='Bear Path'))

    plt.legend(handles=legend_elements, loc='upper right')
    ca_zoom.set_title(name)
    return ca_zoom


if __name__ == "__main__":
    # Build the full map and zoomed bear path map.
    graph_data(name="probability_grid")
    bear_path = path_find.run()
    graph_zoomed_data(path=bear_path, name="zoomed_bear_path")
    plt.show()
