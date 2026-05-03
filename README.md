# Bear Path Prediction

A geospatial analysis project for predicting bear movement patterns, generating probability heatmaps, and simulating movement paths from historical GPS tracking data.

## Overview

This repository processes GPS tracking records for bears and converts them into a land-based probability grid. The workflow includes:
- building a frequency grid from location points,
- optionally weighting observations by time of day,
- propagating values into nearby cells,
- visualizing results on satellite imagery,
- and simulating a greedy bear movement path.

## Features

- **Grid-based probability model**: Converts latitude/longitude points into a cell grid for spatial analysis.
- **Time-adjusted weighting**: Supports temporal weighting of observations.
- **Propagation smoothing**: Spreads probability values into adjacent cells for smoother maps.
- **Satellite visualization**: Renders heatmaps over Google satellite tiles using Cartopy.
- **Greedy path simulation**: Walks through the highest-probability neighbors from a start point.
- **Multiple datasets**: Includes historical bear tracking data for Bears.

## Data

The project loads the following CSV data files:
- `BlackBear2012_data.csv`
- `BlackBear2013_data.csv`

Required columns in each CSV:
- `Latitude`
- `Longitude`
- `Time` (e.g. `12:30 PM`) (Not yet implemented fully)

## Project Structure

- `main.py` - Main entry point that renders the probability heatmap and simulated bear path.
- `freqency_grid.py` - Builds the raw grid from CSV coordinates and applies time-based analysis.
- `graph_prob.py` - Visualizes the probability grid and zoomed path map using Cartopy.
- `propagate.py` - Smooths empty grid cells by propagating values from nearby land cells.
- `time_adjusted_grid.py` - Computes time differences and supports time-weighting logic.
- `time_dist.py` - Analyzes time distributions and movement speed patterns.
- `path_find.py` - Simulates a sequential path through the grid using greedy adjacent-cell selection.

## Installation

1. Create and activate a Python environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the main analysis script from the repository root:

```bash
python main.py
```

This will:
- build the probability grid from the included CSV files,
- display the complete probability heatmap,
- simulate a bear movement path,
- and open a zoomed-in map of the path.

## Notes

- `main.py` Change the variable to change the bear start location.
- The `graph_prob.py` visualization loads Google satellite tiles and requires internet access.
- The project file is named `freqency_grid.py`, so use that exact name when reading or importing.

## Dependencies

- numpy
- pandas
- matplotlib
- cartopy
- scipy
- global-land-mask

