# Bear Path Prediction

A geospatial analysis project that predicts bear movement patterns, generates probability heatmaps, and simulates movement paths based on historical GPS tracking data.

## Overview

This project analyzes bear tracking data to create frequency grids and probability heatmaps showing areas where bears are likely to be found. It also simulates bear movement paths using a greedy algorithm on the probability grid. It supports multiple bear species and years of tracking data.

## Features

- **Frequency Grid Analysis**: Converts GPS coordinates into a grid-based frequency map with configurable cell sizes (default 100m)
- **Time-Adjusted Weighting**: Weights observations based on time of day to account for temporal patterns in bear behavior
- **Grid Propagation**: Fills empty grid cells using neighboring cell values to create smooth probability distributions
- **Geographic Visualization**: Overlays probability heatmaps on Google satellite imagery using Cartopy
- **Path Simulation**: Uses a greedy algorithm to simulate bear movement from high-probability areas
- **Multi-Species Support**: Analyze different bear species (Black Bear, Brown Bear) across different years

## Data

The project uses CSV datasets containing bear GPS tracking data:
- `BlackBear2012_data.csv` - Black bear tracking data from 2012
- `BlackBear2013_data.csv` - Black bear tracking data from 2013
- `BrownBear_data.csv` - Brown bear tracking data

Expected CSV columns:
- `Latitude` - GPS latitude coordinate
- `Longitude` - GPS longitude coordinate
- `Time` - Time of observation (12-hour format, e.g., "12:30 PM")

## Project Structure

- `main.py` - Entry point that generates and displays visualizations with probability heatmaps and simulated paths
- `frequency_grid.py` - Creates frequency grids from raw tracking data
- `graph_prob.py` - Handles geographic visualization and heatmap rendering
- `propagate.py` - Smooths the grid by propagating values to nearby empty cells
- `time_adjusted_grid.py` - Calculates time-based weights for observations
- `time_dist.py` - Analyzes time periods and movement speeds
- `path_find.py` - Simulates bear movement paths based on probability grid

## Usage

```bash
python main.py
```

This will generate and display probability heatmaps with simulated bear movement paths on an interactive map.

## Configuration

In `frequency_grid.py`, you can customize:
- `grid_size` - Cell size in meters (default: 100m)
- `data_file` - Which dataset to analyze (default: combines BlackBear2012 and BlackBear2013 data)
- `user_time` - Reference time for time-adjusted weighting (default: "12:00")

## Dependencies

- numpy
- pandas
- matplotlib
- cartopy
- scipy
- global-land-mask

