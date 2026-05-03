"""Shared pytest fixtures and utilities for bear path prediction tests."""

import pytest
import numpy as np
import pandas as pd
from pathlib import Path
import tempfile
import os


@pytest.fixture
def sample_data_csv():
    """Create a temporary CSV file with sample bear tracking data."""
    data = {
        'Latitude': [61.180106, 61.181, 61.182, 61.183],
        'Longitude': [-149.787058, -149.788, -149.789, -149.790],
        'Time': ['9:30 AM', '10:15 AM', '11:00 AM', '2:30 PM']
    }
    df = pd.DataFrame(data)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df.to_csv(f.name, index=False)
        temp_file = f.name
    
    yield temp_file
    
    # Cleanup
    if os.path.exists(temp_file):
        os.remove(temp_file)


@pytest.fixture
def sample_grid():
    """Create a sample probability grid for testing."""
    grid = np.array([
        [0, 0, 1, 0],
        [0, 2, 3, 0],
        [1, 3, 5, 1],
        [0, 0, 1, 0]
    ], dtype=float)
    return grid


@pytest.fixture
def sample_land_mask():
    """Create a sample land mask (True = land, False = water)."""
    land_mask = np.array([
        [True, True, True, True],
        [True, True, True, True],
        [True, True, True, True],
        [True, True, True, True]
    ], dtype=bool)
    return land_mask


@pytest.fixture
def sample_grid_with_water():
    """Create a grid with water cells (masked out)."""
    grid = np.array([
        [0, 0, 1, 0],
        [0, 2, 3, 0],
        [1, 3, 5, 1],
        [0, 0, 1, 0]
    ], dtype=float)
    
    land_mask = np.array([
        [True, False, True, False],
        [True, True, True, False],
        [True, True, True, True],
        [True, False, False, True]
    ], dtype=bool)
    
    return grid, land_mask
